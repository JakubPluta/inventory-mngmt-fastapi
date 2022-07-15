from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import Product

ProductPydantic = pydantic_model_creator(Product, name="Product")
ProductPydanticIn = pydantic_model_creator(
    Product,
    name="ProductIn",
    exclude_readonly=True,
)
