from fastapi import FastAPI
from infrastructure.rest.routes import router

app = FastAPI(
    title="WoW Shop Gateway",
    description="Point d'entrée unique pour les microservices WoW Shop",
    version="1.0.0"
)

app.include_router(router)
