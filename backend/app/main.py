from __future__ import annotations

from typing import List
from typing import Optional

from app import models
from app.models import Product
from app.models import ProductPydantic
from app.models import ProductPydanticIn
from app.models import Supplier
from app.models import SupplierPydantic
from app.models import SupplierPydanticIn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist


app = FastAPI()


@app.get("/")
def index():
    return {"msg": "hello world"}


@app.post("/supplier", status_code=status.HTTP_200_OK, response_model=SupplierPydantic)
async def add_supplier(supplier_info: SupplierPydanticIn) -> SupplierPydantic:
    supplier = await Supplier.create(
        **supplier_info.dict(exclude_unset=True),
    )
    resp = await SupplierPydantic.from_tortoise_orm(supplier)
    return resp


@app.get("/supplier")
async def get_all_suppliers() -> List[SupplierPydantic]:
    return await SupplierPydantic.from_queryset(Supplier.all())


@app.get(
    "/supplier/{supplier_id}",
    response_model=SupplierPydantic,
    status_code=status.HTTP_200_OK,
)
async def get_supplier_by_id(supplier_id: int) -> SupplierPydantic:
    try:
        supplier = await SupplierPydantic.from_queryset_single(
            Supplier.get(id=supplier_id),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {supplier_id} was not found.",
        )
    return supplier


@app.get(
    "/supplier/{supplier_name}/name",
    response_model=SupplierPydantic,
    status_code=status.HTTP_200_OK,
)
async def get_supplier_by_name(supplier_name: str) -> SupplierPydantic:
    try:
        supplier = await SupplierPydantic.from_queryset_single(
            Supplier.get(name=supplier_name),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with name {supplier_name} was not found.",
        )
    return supplier


@app.put("/supplier/{supplier_id}")
async def update_supplier(
    supplier_id: int,
    supplier_update: SupplierPydanticIn,
) -> SupplierPydantic:
    try:
        supplier = await Supplier.get(id=supplier_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {supplier_id} was not found.",
        )

    update_info = supplier_update.dict(exclude_unset=True)
    for k, v in update_info.items():
        setattr(supplier, k, v)
    await supplier.save()
    return await SupplierPydantic.from_tortoise_orm(supplier)


@app.delete("/supplier/{supplier_id}", status_code=status.HTTP_200_OK)
async def delete_supplier(supplier_id: int) -> dict:
    try:
        supplier = await Supplier.get(id=supplier_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {supplier_id} was not found.",
        )
    await supplier.delete()
    return {"message": f"Supplier with id {supplier_id} was successfully deleted"}


@app.get("/products")
async def get_all_products():
    return await ProductPydantic.from_queryset(Product.all())


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    try:
        product = await Product.get(id=product_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} was not found.",
        )
    return await ProductPydantic.from_queryset_single(product)


@app.post("/products", status_code=status.HTTP_200_OK, response_model=ProductPydantic)
async def create_product(supplier_id: int, product_in: ProductPydanticIn):
    try:
        supplier = await Supplier.get(id=supplier_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {supplier_id} was not found.",
        )

    product_info = product_in.dict(exclude_unset=True)
    product = Product.create(**product_info, supplied_by=supplier)
    return await ProductPydantic.from_queryset(product)


DB_URI = "sqlite://db.sqlite3"

register_tortoise(
    app,
    db_url=DB_URI,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
