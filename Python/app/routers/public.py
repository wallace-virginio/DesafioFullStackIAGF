from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
import logging

from .. import crud, schemas, models
from ..database import get_db
from .. import ai_search

router = APIRouter(
    tags=["Portal Público"]
)

# Logger específico para este módulo
logger = logging.getLogger("marketplace_api")

@router.get("/products", response_model=List[schemas.Product])
def read_public_products(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    price_min: Optional[Decimal] = None,
    price_max: Optional[Decimal] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal do catálogo público.
    - Lista produtos de todas as ONGs.
    - Suporta filtros manuais (categoria, preço).
    - Suporta busca simples por texto (usado pelo fallback da AI).
    """
    products = crud.get_public_products(
        db, skip, limit, category, price_min, price_max, search
    )
    return products

@router.get("/categories", response_model=List[str])
def read_categories(db: Session = Depends(get_db)):
    """ Retorna uma lista de categorias únicas para o front-end usar nos filtros. """
    return crud.get_all_categories(db)

@router.post("/search-ai", response_model=schemas.AISearchResult)
def search_with_ai(
    query: schemas.AISearchQuery,
    request: Request
):
    """
    Endpoint da "Busca Inteligente".
    Recebe uma string em linguagem natural e retorna filtros JSON estruturados.
    """
    
    # Log de entrada (conforme requisito)
    log_extra = {"input_text": query.query}
    
    # 1. Tenta parsear com a AI
    ai_result = ai_search.parse_search_query(query.query)
    
    interpretation = ""
    applied_filters = {}
    is_fallback = False

    if "error" in ai_result:
        # 2. CENÁRIO DE FALLBACK
        is_fallback = True
        fallback_term = ai_result["fallback_term"]
        applied_filters = {"search": fallback_term} # Filtro de busca simples
        interpretation = f"Não foi possível usar a busca inteligente. Mostrando resultados para: '{fallback_term}'"
        
        # Log de fallback (conforme requisito)
        log_extra["ai_success"] = False
        log_extra["fallback_applied"] = True
        log_extra["error_detail"] = ai_result["error"]
        logger.warning(f"AI Search Fallback: {fallback_term}", extra={"extra_data": log_extra})
        
    else:
        # 3. CENÁRIO DE SUCESSO DA AI
        applied_filters = ai_result
        is_fallback = False
        
        # Constrói a interpretação para o usuário
        parts = []
        if "category" in applied_filters:
            parts.append(f"Categoria: {applied_filters['category']}")
        if "price_min" in applied_filters:
            parts.append(f"Preço > {applied_filters['price_min']}")
        if "price_max" in applied_filters:
            parts.append(f"Preço < {applied_filters['price_max']}")
        if "keywords" in applied_filters:
            parts.append(f"Termos: '{applied_filters['keywords']}'")
            # Renomeia 'keywords' para 'search' para o endpoint /products
            applied_filters["search"] = applied_filters.pop("keywords")
            
        interpretation = "Resultados para: " + "; ".join(parts)
        
        # Log de sucesso (conforme requisito)
        log_extra["ai_success"] = True
        log_extra["fallback_applied"] = False
        log_extra["output_filters"] = applied_filters
        logger.info(f"AI Search Success: {interpretation}", extra={"extra_data": log_extra})

    return schemas.AISearchResult(
        interpretation=interpretation,
        applied_filters=applied_filters,
        is_fallback=is_fallback
    )

@router.post("/orders", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Recebe um carrinho (lista de produtos e quantidades) e cria um Pedido.
    (Etapa 1: Sem validação de estoque ou pagamento)
    """
    try:
        created_order = crud.create_order(db=db, order_data=order)
        return created_order
    except HTTPException as e:
        # Repassa a exceção do CRUD (ex: Produto não encontrado)
        raise e
    except Exception as e:
        logger.error(f"Erro inesperado ao criar pedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao processar o pedido."
        )