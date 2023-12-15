from pydantic import BaseModel, EmailStr


class CustomerIn(BaseModel):
    first_name: str
    last_name: str
    password: str 
    email: EmailStr
    phone: str = None

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str

class CustomerOut(BaseModel):
    id: int
    email: EmailStr


class ProductIn(BaseModel):
    name: str
    collection_id: int
    unit_price: float
    description: str = None
    inventory: int


class ProductOut(BaseModel):
    id: int
    name: str
    unit_price: float
    inventory: int
    

class CollectionIn(BaseModel):
    title: str



class OrderIn(BaseModel):
    customer_id: int



class OrderOut(BaseModel):
    id: int
    customer_id: int
    placed_at: str
    payment_status: str