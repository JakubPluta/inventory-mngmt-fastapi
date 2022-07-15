from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.schemas import EmailContent, EmailSchema
from fastapi import APIRouter
from app.models import Product
from fastapi import status
from app.core.config import settings

router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_ADDRESS,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_ADDRESS,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)


@router.post("/{product_id}")
async def send_email(product_id: int, content: EmailContent):
    product = await Product.get(id=product_id)
    supplier = await product.supplied_by
    supplier_email = supplier.email

    html_content = f"""
    <h5>John Doe Business LTD</h5>
    <br>
    <p>{content.subject}</p>
    <br>
    <p>{content.message}</p>
    <br>
    <h6>Regards!</h6>
    <h6>John Doe</h6>
    """
    msg = MessageSchema(
        subject=content.subject,
        recipients=[supplier_email],
        subtype="html",
        body=html_content,
    )
    fm = FastMail(conf)
    await fm.send_message(msg)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "email has been sent"},
    )
