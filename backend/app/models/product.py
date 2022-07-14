from __future__ import annotations

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, nullable=False)
    quantity_in_stock = fields.IntField(default=0)
    quantity_sold = fields.IntField(default=0)
    unit_price = fields.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
    )
    revenue = fields.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00,
    )

    supplied_by = fields.ForeignKeyField(
        "models.Supplier",
        related_name="products",
    )


ProductPydantic = pydantic_model_creator(Product, name="Product")
ProductPydanticIn = pydantic_model_creator(
    Product,
    name="ProductIn",
    exclude_readonly=True,
)
