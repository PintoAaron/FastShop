from sqlalchemy import Integer, String, Column, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
import sqlalchemy
from core.db import Base


class Collection(Base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False,unique=True)
    phone = Column(String)
    membership = Column(Enum('Gold', 'Silver', 'Bronze',name= 'membership_type'),default='Bronze')


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    collection_id = Column(Integer, ForeignKey(
        "collections.id"), nullable=False)
    collection = relationship("Collection", backref="products")
    unit_price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    inventory = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", backref="orders")
    placed_at = Column(sqlalchemy.DateTime,
                       server_default=sqlalchemy.func.now(), nullable=False)
    payment_status = Column(
        Enum('Pending', 'Success', 'Failed',name= 'payment_status_type'),default='Pending')


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(sqlalchemy.DateTime,
                        server_default=sqlalchemy.func.now(), nullable=False)


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
