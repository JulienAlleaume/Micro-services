from fastapi import FastAPI
from infrastructure.rest.routes import (
    product_router,
    pricing_router,
    inventory_router,
    warehouse_router,
    customer_router,
    order_router,
)

app = FastAPI(
    title="WoW Shop Gateway",
    description="Point d'entree unique pour les microservices WoW Shop",
    version="1.0.0",
)

app.include_router(product_router)
app.include_router(pricing_router)
app.include_router(inventory_router)
app.include_router(warehouse_router)
app.include_router(customer_router)
app.include_router(order_router)
