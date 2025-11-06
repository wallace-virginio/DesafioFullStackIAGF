from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, distinct
from . import models, security
from .schemas import UserCreate, ProductCreate, OrderCreate, OrderItemCreate
from typing import Optional, List
from decimal import Decimal
from fastapi import HTTPException, status

# --- Funções de Usuário e Autenticação (Bloco 2) ---

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """ Busca um usuário pelo email. """
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """ 
    Verifica o usuário e a senha.
    Retorna o objeto User se for válido, senão None.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None # Usuário não encontrado
    if not security.verify_password(password, user.hashed_password):
        return None # Senha incorreta
    return user

def create_user(db: Session, user: UserCreate) -> models.User:
    """ Cria um novo usuário (para popular o banco). """
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        organization_id=user.organization_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Funções de Produto (CRUD da ONG - Bloco 3) ---

def get_product(db: Session, product_id: int, organization_id: int) -> Optional[models.Product]:
    """ 
    Busca um produto específico PELO ID e ID DA ONG.
    Garante que a ONG só possa ver/editar seu próprio produto.
    """
    return db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.organization_id == organization_id
    ).first()

def get_products_by_org(db: Session, organization_id: int, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """ Lista todos os produtos de UMA ONG específica. """
    return db.query(models.Product).filter(
        models.Product.organization_id == organization_id
    ).offset(skip).limit(limit).all()

def create_org_product(db: Session, product: ProductCreate, organization_id: int) -> models.Product:
    """ 
    Cria um novo produto. O 'organization_id' é injetado pelo backend,
    não confiado do 'product_data'.
    """
    db_product = models.Product(
        **product.model_dump(), # Pydantic v2
        organization_id=organization_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(
    db: Session, 
    db_product: models.Product, # O produto já buscado (e verificado)
    product_update: ProductCreate
) -> models.Product:
    """ Atualiza os dados de um produto existente. """
    update_data = product_update.model_dump(exclude_unset=True) # Pydantic v2
    
    for key, value in update_data.items():
        setattr(db_product, key, value)
        
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: models.Product):
    """ Deleta um produto. """
    db.delete(db_product)
    db.commit()
    return {"ok": True}

# --- Funções do Portal Público (Bloco 4) ---

def get_public_products(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    price_min: Optional[Decimal] = None,
    price_max: Optional[Decimal] = None,
    search: Optional[str] = None # Para o fallback
) -> List[models.Product]:
    """
    Busca produtos publicamente com filtros e paginação.
    """
    query = db.query(models.Product)
    
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if price_min is not None:
        query = query.filter(models.Product.price >= price_min)
    if price_max is not None:
        query = query.filter(models.Product.price <= price_max)
    if search:
        # Busca simples por texto no nome e descrição (fallback da AI)
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Product.name.ilike(search_term),
                models.Product.description.ilike(search_term)
            )
        )
        
    products = query.offset(skip).limit(limit).all()
    return products

def get_all_categories(db: Session) -> List[str]:
    """ Retorna uma lista de categorias únicas para os filtros. """
    categories = db.query(models.Product.category).distinct().all()
    # O resultado é uma lista de tuplas, ex: [('Alimentos',), ('Decoração',)]
    return [category[0] for category in categories if category[0]]


def create_order(db: Session, order_data: OrderCreate) -> models.Order:
    """
    Cria um registro de Pedido e seus Itens.
    ETAPA 1: Não se preocupa com concorrência ou baixa de estoque.
    """
    
    # 1. Busca os produtos e seus preços atuais
    product_ids = [item.product_id for item in order_data.items]
    products_query = db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()
    product_map = {p.id: p for p in products_query}

    # 2. Valida se todos os produtos existem
    for item in order_data.items:
        if item.product_id not in product_map:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {item.product_id} não encontrado."
            )

    # 3. Cria o Pedido (Order)
    db_order = models.Order()
    db.add(db_order)
    db.commit()
    db.refresh(db_order) # Pega o ID do pedido recém-criado

    # 4. Cria os Itens do Pedido (OrderItems)
    items_to_add = []
    for item in order_data.items:
        product = product_map[item.product_id]
        
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price,
            organization_id=product.organization_id 
        )
        items_to_add.append(db_item)

    db.bulk_save_objects(items_to_add)
    db.commit()
    
    # Recarrega o pedido com os itens associados
    db_order = db.query(models.Order).options(
        joinedload(models.Order.items) # Garante que os 'items' venham na resposta
    ).filter(models.Order.id == db_order.id).first()
    
    return db_order