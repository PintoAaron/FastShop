from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List,Dict
from models.shop_models import Product
from schemas.shop_schemas import ProductOut,ProductIn
from core.db import get_db

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@router.get("/",response_model=Dict[str,List[ProductOut]],status_code=status.HTTP_200_OK)
async def get_all_products(db:Session=Depends(get_db)):
    products = db.query(Product).all()
    return {"data":products}


@router.get("/{product_id}",response_model=Dict[str,ProductOut],status_code=status.HTTP_200_OK)
async def get_product(product_id:int,db:Session=Depends(get_db)):
    product = db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")
    return {"data":product}


@router.post("/",response_model=Dict[str,ProductOut],status_code=status.HTTP_201_CREATED)
async def create_product(product:ProductIn,db:Session=Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"data":db_product}