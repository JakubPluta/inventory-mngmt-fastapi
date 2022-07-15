from typing import List
from app.models import Supplier
from app.schemas import SupplierPydantic
from app.schemas import SupplierPydanticIn
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status


router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=SupplierPydantic)
async def create_supplier(supplier_info: SupplierPydanticIn) -> SupplierPydantic:
    supplier = await Supplier.create(
        **supplier_info.dict(exclude_unset=True),
    )
    resp = await SupplierPydantic.from_tortoise_orm(supplier)
    return resp


@router.get("/")
async def get_all_suppliers() -> List[SupplierPydantic]:
    return await SupplierPydantic.from_queryset(Supplier.all())


@router.get(
    "/{supplier_id}",
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


@router.get(
    "/{supplier_name}/name",
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


@router.put("/{supplier_id}")
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


@router.delete("/{supplier_id}", status_code=status.HTTP_200_OK)
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


@router.get("/{supplier_id}/products")
async def get_all_supplier_products(supplier_id: int):
    try:
        supplier = await Supplier.get(id=supplier_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {supplier_id} was not found.",
        )

    return await supplier.products
