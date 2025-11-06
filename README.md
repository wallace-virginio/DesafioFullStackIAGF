# 🚀 ImpactoPlace - Desafio Full Stack

Bem-vindo ao **ImpactoPlace**, um **marketplace Multi-ONG** completo, construído com **Python (FastAPI)** e **Angular**.  
O objetivo desta plataforma é conectar consumidores a produtos de impacto de diversas ONGs, fornecendo um **portal público para compras** e uma **área de gestão restrita e segura** para cada organização.

## 📁 Estrutura do Repositório

- `/Python` → Código-fonte completo do **Backend (FastAPI)**
- `/Angular` → Código-fonte completo do **Frontend (Angular)**
- `/Python/seed.py` → Script de **seed do banco de dados**
- `.env.example` → Template para configuração de variáveis de ambiente
- `README.md` → Este documento

## 🛠️ Tech Stack

| Camada             | Tecnologia                 |
| ------------------ | -------------------------- |
| **Backend**        | Python 3.11 + FastAPI      |
| **Frontend**       | Angular                    |
| **Banco de Dados** | PostgreSQL 15              |
| **ORM**            | SQLAlchemy                 |
| **Busca AI**       | Google Gemini (API de LLM) |
| **Ambiente**       | Docker & Docker Compose    |

## 🧩 1. Passo a Passo para Rodar Localmente (Docker Compose)

### 🔧 Pré-requisitos

- Docker Desktop (ou Docker Engine no Linux)
- Docker Compose instalado

### 🪄 Passo 1: Configurar o Ficheiro de Ambiente

Na raiz do projeto, duplique o arquivo `.env.example` e renomeie-o para `.env`.

```bash
# Windows (PowerShell)
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave:

```
GEMINI_API_KEY=coloque_sua_chave_aqui
```

### 🚀 Passo 2: Iniciar o Ambiente

Na raiz do projeto, execute:

```bash
docker-compose up --build
```

> O parâmetro `--build` é essencial na primeira execução.

O Docker irá:

1. Iniciar o banco **PostgreSQL (db-1)**
2. Aguardar o **healthcheck**
3. Executar o **seed (seed-1)** com dados de exemplo
4. Iniciar o **backend (FastAPI)** → `http://localhost:8000`
5. Iniciar o **frontend (Angular)** → `http://localhost:4200`

### 🌐 Passo 3: Aceder à Aplicação

- **Frontend (ImpactoPlace)** → [http://localhost:4200](http://localhost:4200)
- **Backend (Documentação da API)** → [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger)

#### 🔑 Contas de Teste

| ONG             | Email                   | Senha    |
| --------------- | ----------------------- | -------- |
| Artesãos do Bem | admin@artesaosdobem.org | senha123 |
| Sabor & Causa   | admin@saborcausa.org    | senha456 |

## 🗃️ 2. Esquema do Banco de Dados (Descrição Textual)

### 🏢 organizations

- `id` (PK)
- `name`

### 👤 users

- `id` (PK)
- `email` (Unique)
- `hashed_password`
- `organization_id` (FK → organizations)

### 📦 products

- `id` (PK)
- `name`, `description`, `price`, `category`, `image_url`, `stock_qty`, `weight_grams`
- `organization_id` (FK → organizations)

### 🧾 orders

- `id` (PK)
- `created_at`

### 🧺 order_items

- `id` (PK)
- `order_id` (FK → orders)
- `product_id` (FK → products)
- `quantity`, `price_at_purchase`, `organization_id`

## 🔌 3. Principais Rotas da API

### 🔐 Autenticação (/auth)

| Método | Rota          | Descrição                                 |
| ------ | ------------- | ----------------------------------------- |
| POST   | `/auth/login` | Recebe `email` e `password`. Retorna JWT. |

### 🏬 Área da ONG (/products) _(Requer Token)_

| Método | Rota             | Descrição                         |
| ------ | ---------------- | --------------------------------- |
| GET    | `/products/`     | Lista produtos da ONG autenticada |
| POST   | `/products/`     | Cria um novo produto              |
| GET    | `/products/{id}` | Obtém um produto específico       |
| PUT    | `/products/{id}` | Atualiza um produto               |
| DELETE | `/products/{id}` | Remove um produto                 |

### 🌎 Portal Público (/public)

| Método | Rota                 | Descrição                            |
| ------ | -------------------- | ------------------------------------ |
| GET    | `/public/products`   | Lista produtos de todas as ONGs      |
| GET    | `/public/categories` | Retorna categorias únicas            |
| POST   | `/public/search-ai`  | Faz busca em linguagem natural (LLM) |
| POST   | `/public/orders`     | Cria um novo pedido                  |

## 🤖 4. Detalhes Técnicos

### 🧠 4.1. Busca AI

- Google Gemini 1.5 Flash
- Chave no `.env`: `GEMINI_API_KEY`
- Timeout: `AI_SEARCH_TIMEOUT_SECONDS` (default 3s)
- Fallback: busca textual simples se falha

Exemplo de retorno fallback:

```json
{ "search": "doces até 50 reais", "is_fallback": true }
```

### 📜 4.2. Logs e Observabilidade

Logs estruturados (JSON) enviados para stdout do container `backend-1`.

**Exemplo Log HTTP**

```json
{
  "timestamp": "2025-11-06 01:25:21,526",
  "level": "INFO",
  "message": "HTTP Request: GET /public/products",
  "http_method": "GET",
  "http_status_code": 200,
  "http_latency_ms": 102.06,
  "user_id": "anonymous",
  "organization_id": "none"
}
```

**Exemplo Log AI**

```json
{
  "input_text": "produtos sustentáveis até 100 reais",
  "ai_success": true,
  "fallback_applied": false,
  "output_filters": { "max_price": 100 }
}
```

### ⚙️ 5.1. Consistência de Estoque e Concorrência ✅

- Atomicidade total: todas as operações numa única transação.
- Bloqueio pessimista (`SELECT ... FOR UPDATE`) evita overselling.
- Rollback automático em caso de erro.
- HTTP 409 Conflict se estoque insuficiente.

### 🧵 5.2. Processamento Assíncrono e Resiliência _(A implementar)_

## 🧩 6. Decisões de Design e Trade-offs

- Arquitetura Limpa (MVC/MVVM)
- Segurança Multi-Tenancy: ONG do token, nunca do cliente
- Fallback IA prioriza UX
- SSR Angular melhora SEO
- Concorrência: bloqueio pessimista para estoque consistente

## 👨‍💻 Autor

**Wallace Virginio – Desafio Full Stack (Python + Angular)**  
LinkedIn: [linkedin.com/in/wallace-virginio](https://linkedin.com/in/wallace-virginio)
