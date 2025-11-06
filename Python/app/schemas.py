from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from decimal import Decimal
import datetime

# --- Autenticação (Bloco 2) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    organization_id: Optional[int] = None

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    organization_id: int
    
class User(UserBase):
    id: int
    organization_id: int

    # Configuração para Pydantic v2 (substitui orm_mode=True)
    model_config = ConfigDict(from_attributes=True)


# --- Produtos (CRUD da ONG - Bloco 3) ---

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal # Usa Decimal para precisão monetária
    category: str
    image_url: Optional[str] = None
    stock_qty: int
    weight_grams: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    organization_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Pedidos (Portal Público - Bloco 4) ---

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal
    organization_id: int
    
    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    id: int
    created_at: datetime.datetime
    items: List[OrderItem] = []

    model_config = ConfigDict(from_attributes=True)


# --- Portal Público / Busca AI (Bloco 4) ---

class AISearchQuery(BaseModel):
    query: str

class AISearchResult(BaseModel):
    """ Resposta da Busca AI, informando ao front-end o que foi entendido. """
    interpretation: str       # Ex: "Resultados para: Categoria=Doces; Preço ≤ 50"
    applied_filters: Dict[str, Any] # Os filtros que o front deve aplicar
    is_fallback: bool         # Indica se a AI falhou e o fallback foi usado