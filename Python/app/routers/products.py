from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_org_id, set_request_context

router = APIRouter(
    tags=["Produtos (Área da ONG)"],
    # Esta linha aplica a dependência de autenticação a TODAS as rotas
    # neste router. Isso também preenche o request.state para os logs.
    dependencies=[Depends(set_request_context)] 
)

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    # Aqui está a segurança multi-tenancy:
    # Pegamos o org_id do token, não do body!
    org_id: int = Depends(get_current_org_id) 
):
    """
    Cria um novo produto para a ONG autenticada.
    O organization_id é extraído do token do usuário.
    """
    return crud.create_org_product(db=db, product=product, organization_id=org_id)

@router.get("/", response_model=List[schemas.Product])
def read_org_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """
    Lista todos os produtos da ONG autenticada.
    """
    products = crud.get_products_by_org(db, organization_id=org_id, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """
    Busca um produto específico da ONG autenticada.
    """
    db_product = crud.get_product(db, product_id=product_id, organization_id=org_id)
    if db_product is None:
        # Se não encontrar, é porque o produto não existe OU
        # pertence a outra ONG. Retornamos 404 por segurança.
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_org_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """
    Atualiza um produto específico da ONG autenticada.
    """
    db_product = crud.get_product(db, product_id=product_id, organization_id=org_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return crud.update_product(db=db, db_product=db_product, product_update=product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_org_product(
    product_id: int,
    db: Session = Depends(get_db),
    org_id: int = Depends(get_current_org_id)
):
    """
    Deleta um produto específico da ONG autenticada.
    """
    db_product = crud.get_product(db, product_id=product_id, organization_id=org_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    crud.delete_product(db=db, db_product=db_product)
    # Retorna 204 No Content, que não envia corpo
    return