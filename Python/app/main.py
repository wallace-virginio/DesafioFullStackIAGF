from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
import sys
import json
from .database import engine, Base
from .models import * # Importa os modelos para que o create_all os veja

# Importa os routers de todos os blocos
from .routers import auth, products, public



# Remove o handler padrão do FastAPI/Uvicorn
logging.getLogger("uvicorn.access").handlers = []

# Cria nosso logger estruturado
class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
        }
        # Adiciona dados extras do middleware
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonLogFormatter())

logger = logging.getLogger("marketplace_api")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
# ---------------------------------------------------------


# Cria as tabelas no DB (para desenvolvimento simples)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marketplace Multi-ONG")

# Configuração de CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # Origem do Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# iddleware de Logging
@app.middleware("http")
async def structured_log_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    latency = time.time() - start_time
    
    # Tenta extrair IDs do contexto (preenchido pela dependência de auth)
    user_id = getattr(request.state, "user_id", "anonymous")
    organization_id = getattr(request.state, "organization_id", "none")

    log_data = {
        "extra_data": {
            "http_method": request.method,
            "http_path": request.url.path,
            "http_status_code": response.status_code,
            "http_latency_ms": round(latency * 1000, 2),
            "user_id": user_id,
            "organization_id": organization_id
        }
    }
    
    logger.info(f"HTTP Request: {request.method} {request.url.path}", extra=log_data)
    
    return response


@app.get("/", summary="Health Check")
def read_root():
    return {"status": "Marketplace API is running"}

# --- Registra os Routers de todos os blocos ---
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(products.router, prefix="/products", tags=["Produtos (Área da ONG)"])
app.include_router(public.router, prefix="/public", tags=["Portal Público"])