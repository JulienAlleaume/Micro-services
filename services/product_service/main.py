import uvicorn
from fastapi import FastAPI

# Imports
from infrastructure.db.models import Base
from infrastructure.db.database import engine

# Import du router après la config DB pour éviter les soucis d'import circulaire
from infrastructure.rest.routes import router as product_router

# Création automatique des tables au démarrage (pour le dev)
Base.metadata.create_all(bind=engine)

# --- Initialisation de l'application FastAPI ---
app = FastAPI(
    title="WoW Shop API",
    description="API de gestion de boutique World of Warcraft (Microservice Produit)",
    version="1.0.0"
)

# Inclusion des routes
app.include_router(product_router)

# Permet de lancer le serveur directement avec `python main.py`
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
