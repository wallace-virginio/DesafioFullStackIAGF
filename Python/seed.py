import requests
import logging
from sqlalchemy.orm import sessionmaker
from app.database import engine, Base, SessionLocal
from app.models import Organization, User, Product
from app.security import get_password_hash
from decimal import Decimal
import time
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Cria todas as tabelas se não existirem"""
    try:
        logger.info("Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        return False

def seed_data():
    db = SessionLocal()
    try:
        logger.info("Verificando se os dados já existem...")

        # Primeiro, verifica se as tabelas existem
        try:
            org1_exists = db.query(Organization).filter(Organization.name == "ONG Artesãos do Bem").first()
            org2_exists = db.query(Organization).filter(Organization.name == "ONG Sabor & Causa").first()
        except Exception as e:
            logger.warning(f"Tabelas não existem ainda: {e}")
            org1_exists = None
            org2_exists = None

        if org1_exists and org2_exists:
            logger.info("Ambas as ONGs já existem. Seed não será executado.")
            return

        # --- ONG 1: Artesãos do Bem ---
        if not org1_exists:
            org1 = Organization(name="ONG Artesãos do Bem")
            db.add(org1)
            db.flush()
            logger.info(f"Criada ONG: {org1.name}")
            
            # Usuário da ONG 1
            user1 = User(
                email="admin@artesaosdobem.org",
                hashed_password=get_password_hash("senha123"),
                organization_id=org1.id
            )
            db.add(user1)
            logger.info(f"Criado Usuário: {user1.email}")

            # Produtos da ONG 1
            products_org1 = [
                Product(name="Vaso de Cerâmica", description="Feito à mão por artesãos locais.", price=Decimal("45.50"), category="Decoração", image_url="https://placehold.co/600x400/D9A879/FFF?text=Vaso", stock_qty=15, weight_grams=800, organization_id=org1.id),
                Product(name="Bolsa de Palha", description="Ideal para praia e dia a dia.", price=Decimal("75.00"), category="Acessórios", image_url="https://placehold.co/600x400/B8D979/FFF?text=Bolsa", stock_qty=10, weight_grams=450, organization_id=org1.id),
                Product(name="Colar de Sementes", description="Biojóia da Amazônia.", price=Decimal("30.00"), category="Acessórios", image_url="https://placehold.co/600x400/D97979/FFF?text=Colar", stock_qty=30, weight_grams=100, organization_id=org1.id),
            ]
            db.add_all(products_org1)
            logger.info("Adicionados produtos para ONG 1")

        # --- ONG 2: Sabor & Causa ---
        if not org2_exists:
            org2 = Organization(name="ONG Sabor & Causa")
            db.add(org2)
            db.flush()
            logger.info(f"Criada ONG: {org2.name}")

            # Usuário da ONG 2
            user2 = User(
                email="admin@saborcausa.org",
                hashed_password=get_password_hash("senha456"),
                organization_id=org2.id
            )
            db.add(user2)
            logger.info(f"Criado Usuário: {user2.email}")

            # Produtos da ONG 2
            products_org2 = [
                Product(name="Geleia de Morango Orgânica", description="Doces sem conservantes.", price=Decimal("25.00"), category="Alimentos", image_url="https://placehold.co/600x400/D979B8/FFF?text=Geleia", stock_qty=50, weight_grams=300, organization_id=org2.id),
                Product(name="Café Especial 500g", description="Grãos selecionados de pequenos produtores.", price=Decimal("55.00"), category="Alimentos", image_url="https://placehold.co/600x400/8C5D3D/FFF?text=Café", stock_qty=25, weight_grams=500, organization_id=org2.id),
                Product(name="Camiseta 'Apoie essa Causa'", description="100% Algodão.", price=Decimal("60.00"), category="Vestuário", image_url="https://placehold.co/600x400/79D9D0/FFF?text=Camiseta", stock_qty=40, weight_grams=250, organization_id=org2.id),
            ]
            db.add_all(products_org2)
            logger.info("Adicionados produtos para ONG 2")

        db.commit()
        logger.info("Seed concluído com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao popular o banco: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Aguardando banco de dados...")
    time.sleep(10)  # Aumenta o tempo de espera
    
    # Primeiro cria as tabelas
    if create_tables():
        # Depois popula os dados
        seed_data()
    else:
        logger.error("Falha ao criar tabelas. Saindo.")
        sys.exit(1)