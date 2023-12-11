from fastapi import FastAPI
from models.shop_models import *
from core.db import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI()



@app.get("/")
async def root():
    return {"message": "FastShop"}