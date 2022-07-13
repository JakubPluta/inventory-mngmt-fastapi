from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app import models
from app.models import SupplierPydantic, SupplierPydanticIn, ProductPydanticIn, ProductPydantic, Supplier, Product
from fastapi import status, HTTPException
from tortoise.exceptions import DoesNotExist

app = FastAPI()


@app.get('/')
def index():
    return {'msg':'hello world'}


@app.post('/supplier', status_code=status.HTTP_200_OK, response_model=SupplierPydantic)
async def add_supplier(supplier_info: SupplierPydanticIn) -> SupplierPydantic:
    supplier = await Supplier.create(
        **supplier_info.dict(exclude_unset=True)
    )
    resp = await SupplierPydantic.from_tortoise_orm(supplier)
    return resp


@app.get('/supplier')
async def get_all_suppliers():
    return await SupplierPydantic.from_queryset(Supplier.all())


@app.get('/supplier/{supplier_id}', response_model=SupplierPydantic, status_code=status.HTTP_200_OK)
async def get_supplier_by_id(supplier_id: int):
    try:
        supplier = await SupplierPydantic.from_queryset_single(Supplier.get(id=supplier_id))
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplier with id {supplier_id} was not found.")
    return supplier


@app.get('/supplier/{supplier_name}/name', response_model=SupplierPydantic, status_code=status.HTTP_200_OK)
async def get_supplier_by_name(supplier_name: str):
    try:
        supplier = await SupplierPydantic.from_queryset_single(Supplier.get(name=supplier_name))
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplier with name {supplier_name} was not found.")
    return supplier



DB_URI = 'sqlite://db.sqlite3'

register_tortoise(
    app,
    db_url=DB_URI,
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)