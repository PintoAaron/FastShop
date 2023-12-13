from fastapi import FastAPI
from models.shop_models import *
from core.db import Base, engine
from api.v1 import products, collections, auth

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(products.router)
app.include_router(collections.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "FastShop"}