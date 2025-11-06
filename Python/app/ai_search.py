import os
import json
import logging
import google.generativeai as genai
from google.api_core.exceptions import DeadlineExceeded
from pydantic import ValidationError

# Configura o logger
logger = logging.getLogger("marketplace_api")

# Configura a API do Gemini
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY não definida. A Busca Inteligente (AI) será desativada.")
        genai = None
    else:
        genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    logger.warning("Pacote 'google-generativeai' não instalado. A Busca Inteligente (AI) será desativada.")
    genai = None

AI_SEARCH_TIMEOUT_SECONDS = float(os.getenv("AI_SEARCH_TIMEOUT_SECONDS", 3.0))

# Define o schema JSON que queremos que a AI retorne
AI_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "category": {"type": "STRING", "description": "A categoria do produto (ex: Alimentos, Vestuário, Decoração, Acessórios)"},
        "price_min": {"type": "NUMBER", "description": "O preço mínimo"},
        "price_max": {"type": "NUMBER", "description": "O preço máximo"},
        "keywords": {"type": "STRING", "description": "Termos de busca para o nome ou descrição (ex: 'orgânico', 'cerâmica')"}
    },
    "required": [] # Nenhum campo é estritamente obrigatório
}

# O prompt do sistema que instrui a AI
AI_SYSTEM_PROMPT = f"""
Você é um assistente de e-commerce para um marketplace de ONGs.
Sua tarefa é analisar a consulta de busca do usuário e extraí-la em um formato JSON.
O JSON deve seguir este schema: {json.dumps(AI_RESPONSE_SCHEMA)}

- Se o usuário mencionar um tipo de produto, preencha 'category'.
- Se o usuário mencionar valores (ex: 'até 50 reais', 'acima de 10', 'entre 10 e 30'), preencha 'price_min' e/ou 'price_max'.
- Se o usuário usar termos descritivos, preencha 'keywords'.
- Se a consulta for simples (ex: 'bolsas'), apenas preencha 'keywords'.
- Retorne apenas o objeto JSON, sem nenhum texto adicional.
"""

def parse_search_query(text: str) -> dict:
    """
    Usa o LLM para converter texto em filtros JSON.
    Retorna um dicionário com os filtros ou um dicionário de erro com fallback.
    """
    if not genai:
        logger.warning("AI Search pulada: genai não configurado.")
        return {"error": "AI not configured", "fallback_term": text}

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # gemini-2.5-flash-preview-09-2025
            system_instruction=AI_SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"Analise a seguinte consulta: '{text}'"
        
        # Faz a chamada com timeout
        response = model.generate_content(
            prompt,
            request_options={'timeout': AI_SEARCH_TIMEOUT_SECONDS}
        )
        
        # Limpa e carrega o JSON
        parsed_json = json.loads(response.text)
        
        # Filtra chaves vazias ou nulas
        filters = {k: v for k, v in parsed_json.items() if v is not None and v != ""}
        
        return filters

    except (DeadlineExceeded, TimeoutError):
        logger.warning(f"AI Search timeout ({AI_SEARCH_TIMEOUT_SECONDS}s) para a consulta: '{text}'")
        return {"error": "timeout", "fallback_term": text}
    except Exception as e:
        logger.error(f"AI Search erro: {e} | Consulta: '{text}'")
        return {"error": str(e), "fallback_term": text}