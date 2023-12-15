from fastapi import APIRouter,Depends,HTTPException,status,Header
from sqlalchemy.orm import Session
from typing import List,Dict
from models.shop_models import Order
from schemas.shop_schemas import OrderIn,OrderOut
from core.db import get_db
from core.auth_services import verify_token


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["orders"],
)


@router.get("/",response_model=Dict[str,List[OrderOut]],status_code=status.HTTP_200_OK)
async def get_all_orders(db:Session=Depends(get_db),token=Header(...)):
    payload = verify_token(token)
    if payload.get("resource_access").get("realm-management").get("roles")[4] != "realm-admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access")
    orders = db.query(Order).all()
    return {"data":orders}



@router.get("/{order_id}",response_model=Dict[str,OrderOut],status_code=status.HTTP_200_OK)
async def get_order(order_id:int,db:Session=Depends(get_db),token=Header(...)):
    payload = verify_token(token)
    if payload.get("resource_access").get("realm-management").get("roles")[4] != "realm-admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access")
    order = db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
    return {"data":order}