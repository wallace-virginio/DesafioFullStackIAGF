from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import schemas, crud, models, security
from .database import get_db
import logging

# Logger para debug de autenticação
logger = logging.getLogger("marketplace_api")

# Define que a URL /auth/login é a que fornece o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_data(token: str = Depends(oauth2_scheme)) -> schemas.TokenData:
    """
    Decodifica o token JWT e retorna os dados brutos (TokenData).
    Levanta exceção se o token for inválido.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        
        user_id: int = payload.get("user_id")
        organization_id: int = payload.get("org_id") # <-- CRÍTICO

        if user_id is None or organization_id is None:
            logger.warning("Token inválido: 'user_id' ou 'org_id' faltando no payload.")
            raise credentials_exception
        
        token_data = schemas.TokenData(user_id=user_id, organization_id=organization_id)
        
    except JWTError as e:
        logger.warning(f"Erro de JWT: {e}")
        raise credentials_exception
    
    return token_data

# --- Dependência CRÍTICA para Multi-Tenancy ---

async def set_request_context(
    request: Request, 
    token_data: schemas.TokenData = Depends(get_current_user_data)
):
    """
    Esta dependência injeta os IDs do token no estado da requisição.
    Isso é usado pelo middleware de log e pelas rotas restritas.
    """
    request.state.user_id = token_data.user_id
    request.state.organization_id = token_data.organization_id

async def get_current_org_id(
    request: Request,
    # Esta dependência garante que o request.state seja preenchido
    _ = Depends(set_request_context) 
) -> int:
    """
    Dependência principal para rotas restritas.
    
    Garante que o usuário está autenticado e retorna o 'organization_id'
    armazenado de forma segura no token JWT (via request.state).
    
    Qualquer endpoint que injetar esta dependência estará automaticamente
    protegido e ciente da ONG do usuário.
    """
    
    # O valor foi definido por set_request_context
    org_id = getattr(request.state, "organization_id", None)
    
    if org_id is None:
        # Isso não deve acontecer se 'set_request_context' rodou,
        # mas é uma garantia extra.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contexto da organização não encontrado na requisição.",
        )
        
    return org_id