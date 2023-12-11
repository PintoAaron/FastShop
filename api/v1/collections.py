from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from models.shop_models import Collection
from schemas.shop_schemas import CollectionIn
from core.db import get_db


router = APIRouter(
    prefix="/api/v1/collections",
    tags=["collections"],
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_collections(db: Session = Depends(get_db)):
    collections = db.query(Collection).all()
    return {"data": collections}


@router.get("/{collection_id}", status_code=status.HTTP_200_OK)
async def get_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="collection not found")
    return {"data": collection}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_collection(collection: CollectionIn, db: Session = Depends(get_db)):
    db_collection = Collection(**collection.dict())
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return {"data": db_collection}