# 🚀 ImpactoPlace - Desafio Vaga Desenvolvedor FullStack IA da Gerando Falcões

Bem-vindo ao **ImpactoPlace**, um marketplace Multi-ONG completo, construído com Python (FastAPI) e Angular. O objetivo desta plataforma é conectar consumidores a produtos de impacto de diversas ONGs, fornecendo um portal público para compras e uma área de gestão restrita e segura para cada organização.

Este repositório contém:

1.  O código-fonte completo do **Backend** (pasta `/Python`) e **Frontend** (pasta `/Angular`).
2.  O script de **seed** do banco de dados (em `/Python/seed.py`).
3.  Um ficheiro **.env.example** com placeholders para as variáveis de ambiente.
4.  Este **README.md** detalhado.

## 🛠️ Tech Stack

- **Backend:** **Python 3.11** com **FastAPI**
- **Frontend:** **Angular**
- **Banco de Dados:** **PostgreSQL 15**
- **ORM:** **SQLAlchemy**
- **Busca AI:** **Google Gemini** (API de LLM)
- **Ambiente:** **Docker** & **Docker Compose**

---

## 1. Passo a Passo para Rodar Localmente (Docker Compose)

Siga estes passos para executar o ambiente completo na sua máquina.

### Pré-requisitos

- **Docker Desktop** (ou Docker Engine no Linux) a correr.
- **Docker Compose**

### Passo 1: Configurar o Ficheiro de Ambiente

Na raiz deste projeto, encontrará um ficheiro chamado `.env.example`. Crie uma cópia dele e renomeie-a para `.env`.
(Porém é necessário que você altere o código para utilizar uma Chave de API real)

```bash
# No Windows (PowerShell)
copy .env.example .env

# No Mac/Linux
cp .env.example .env
```
