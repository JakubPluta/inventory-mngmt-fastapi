from __future__ import annotations

from app import models
from app.routes.supplier import router as supplier_router
from app.routes.product import router as product_router
from app.routes.mail import router as mail_router
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware


origins = ["http://localhost:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=supplier_router, prefix="/suppliers", tags=["supplier"])
app.include_router(router=product_router, prefix="/products", tags=["products"])
app.include_router(router=mail_router, prefix="/email", tags=["email"])


@app.get("/")
def index():
    return {"msg": "hello world"}


DB_URI = "sqlite://db.sqlite3"

register_tortoise(
    app,
    db_url=DB_URI,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
