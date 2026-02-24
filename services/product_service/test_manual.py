import sys
import os

# Astuce pour que Python trouve vos dossiers (domain, infrastructure, etc.)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Imports de vos modules
from infrastructure.db.models import Base
from infrastructure.db.repositories import ProductRepository
from application.services import ProductService
from domain.models import Product, ProductCategory

# 1. Configuration d'une base de données en mémoire (RAM) pour le test
# "sqlite:///:memory:" signifie que la BDD est détruite à la fin du script
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Création des tables dans la base de données virtuelle
Base.metadata.create_all(bind=engine)

def run_test():
    print("--- ⚔️  Démarrage du test World of Warcraft ⚔️  ---")
    
    # 3. Initialisation de la session, du repo et du service
    db = SessionLocal()
    repo = ProductRepository(db)
    service = ProductService(repo)

    try:
        # 4. Création d'un produit (Données de test)
        # Note: L'ID est mis à 0 ici, mais c'est la BDD qui va générer le vrai ID (1)
        new_item = Product(
            id=0, 
            name="Rênes d'Invincible", 
            description="Le destrier du Roi Liche, on ne le voit jamais car il est invincible.", 
            category=ProductCategory.MOUNT,
            image_url="invincible.jpg"
        )

        print(f"\n1. Tentative de création de l'item : {new_item.name}")
        created_product = service.create_product(new_item)
        print(f"✅ SUCCÈS ! Item créé en base. ID généré : {created_product.id}")

        # 5. Récupération du produit
        print(f"\n2. Tentative de lecture de l'ID {created_product.id} depuis la base...")
        fetched_product = service.get_product(created_product.id)
        print(f"✅ SUCCÈS ! Item récupéré : {fetched_product.name}")
        print(f"   Description : {fetched_product.description}")

    except Exception as e:
        print(f"❌ ERREUR : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_test()
    