from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi import APIRouter
from dotenv import dotenv_values
from app.models import Product
from fastapi import status
from pathlib import Path
import os

root_dir = Path(__file__).resolve().parent.parent.parent
env_file = os.path.join(root_dir, ".env")
credentials = dotenv_values(env_file)


router = APIRouter()


conf = ConnectionConfig(
    MAIL_USERNAME=credentials.get("EMAIL", "REPLACE_ME"),
    MAIL_PASSWORD=credentials.get("PASSWORD", "REPLACE_ME"),
    MAIL_FROM=credentials.get("EMAIL", "REPLACE_ME"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp-relay.sendinblue.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class EmailContent(BaseModel):
    message: str
    subject: str


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
