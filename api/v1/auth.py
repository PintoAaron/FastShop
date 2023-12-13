from typing import Dict
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from models.shop_models import Customer
from schemas.shop_schemas import CustomerIn,CustomerOut,CustomerLogin
from core.db import get_db
from core.auth_services import login_keycloak_user,register_keycloak_user
from core.config import get_password_hash,verify_password 

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)



@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerIn, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(customer.password)
    customer.password = hashed_password
    try:
        new_user = Customer(**customer.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    if register_keycloak_user(new_user) != 201:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Keycloak registration failed")
    token = login_keycloak_user(customer.email, customer.password)
    return {"token":token}
    
    
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_customer(customer: CustomerLogin, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")
    if not verify_password(customer.password, db_customer.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    token = login_keycloak_user(customer.email, customer.password)
    return {"token":token}
    