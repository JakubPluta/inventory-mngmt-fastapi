from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import Supplier

SupplierPydantic = pydantic_model_creator(Supplier, name="Supplier")
SupplierPydanticIn = pydantic_model_creator(
    Supplier,
    name="SupplierIn",
    exclude_readonly=True,
)
