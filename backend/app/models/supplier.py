from __future__ import annotations

from tortoise import fields
from tortoise.models import Model
from .product import Product


class Supplier(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    company = fields.CharField(max_length=20)
    email = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=15)

    products: fields.ReverseRelation["Product"]
