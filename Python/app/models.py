from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Organization(Base):
    """ Define a ONG """
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    users = relationship("User", back_populates="organization")
    products = relationship("Product", back_populates="organization")
    order_items = relationship("OrderItem", back_populates="organization")

class User(Base):
    """ Usuário administrador de uma ONG """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    
    organization = relationship("Organization", back_populates="users")

class Product(Base):
    """ Produtos das ONGs """
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String, index=True)
    image_url = Column(String)
    stock_qty = Column(Integer, nullable=False)
    weight_grams = Column(Integer, nullable=False)
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="products")

class Order(Base):
    """ Estrutura do Pedido (Dados Gerais) """
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    """ Itens do Pedido """
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_purchase = Column(Numeric(10, 2)) 
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    organization = relationship("Organization", back_populates="order_items")