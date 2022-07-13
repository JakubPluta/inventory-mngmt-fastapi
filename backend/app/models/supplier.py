from __future__ import annotations

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from .product import Product


class Supplier(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    company = fields.CharField(max_length=20)
    email = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=15)

    product: fields.ReverseRelation["Product"]


SupplierPydantic = pydantic_model_creator(Supplier, name="Supplier")
SupplierPydanticIn = pydantic_model_creator(
    Supplier,
    name="SupplierIn",
    exclude_readonly=True,
)
