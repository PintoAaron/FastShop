from pydantic import BaseModel, EmailStr


class CustomerIn(BaseModel):
    full_name: str
    password: str
    email: EmailStr
    phone: str


class CustomerOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr


class ProductIn(BaseModel):
    name: str
    collection_id: int
    unit_price: float
    description: str = None
    inventory: int


class ProductOut(BaseModel):
    name: str
    unit_price: float
    inventory: int
    

class CollectionIn(BaseModel):
    title: str


