from __future__ import annotations
from app.models import Product
from app.schemas import ProductPydantic
from app.schemas import ProductPydanticIn
from app.models import Supplier
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status


router = APIRouter()


@router.get("/")
async def get_all_products():
    return await ProductPydantic.from_queryset(Product.all())


@router.get("/{product_id}")
async def get_product(product_id: int):
    try:
        product = await Product.get(id=product_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} was not found.",
        )
    return await ProductPydantic.from_queryset_single(product)


@router.post("/", status_code=status.HTTP_200_OK, response_model=ProductPydantic)
async def create_product(supplier_id: int, product_in: ProductPydanticIn):
    try:
        supplier = await Supplier.get(id=supplier_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {supplier_id} was not found.",
        )

    product_info = product_in.dict(exclude_unset=True)
    product_info["revenue"] += (
        product_info["quantity_sold"] * product_info["unit_price"]
    )
    product = await Product.create(**product_info, supplied_by=supplier)
    return await ProductPydantic.from_tortoise_orm(product)


@router.put(
    "/{product_id}",
    response_model=ProductPydantic,
    status_code=status.HTTP_200_OK,
)
async def update_product(product_id: int, update_info: ProductPydanticIn):
    try:
        product = await Product.get(id=product_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} was not found.",
        )

    update_dict = update_info.dict(exclude_unset=True)
    product.name = update_dict["name"]
    product.quantity_in_stock = update_dict["quantity_in_stock"]
    product.revenue += update_dict["quantity_sold"] * update_dict["unit_price"]
    product.quantity_sold += update_dict["quantity_sold"]
    product.unit_price = update_dict["unit_price"]
    await product.save()
    return await ProductPydantic.from_queryset(product)


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    try:
        product = await Product.get(id=product_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} was not found",
        )

    await product.delete()
    return {"message": f"Product with id {product_id} was successfully deleted"}
