from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.shop_models import *
from core.db import Base, engine
from api.v1 import products, collections, auth, orders

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(products.router)
app.include_router(collections.router)
app.include_router(auth.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"message": "FastShop"}