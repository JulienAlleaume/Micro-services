from fastapi import FastAPI

from infrastructure.db.schema import Base
from infrastructure.db.database import engine
from infrastructure.rest.routes import router as product_router

# Création automatique des tables au démarrage (pour le dev)
Base.metadata.create_all(bind=engine)

# --- Initialisation de l'application FastAPI ---
app = FastAPI(
    title="WoW Shop API - Product Service",
    description="Microservice de gestion des produits WoW Shop (port 8001)",
    version="1.0.0"
)

app.include_router(product_router)
