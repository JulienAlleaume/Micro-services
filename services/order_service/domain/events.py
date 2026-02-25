from datetime import datetime
from pydantic import BaseModel, Field


class OrderCreatedEvent(BaseModel):
    order_id: int
    customer_id: int
    total: float
    created_at: datetime = Field(default_factory=datetime.now)


class OrderLineCreatedEvent(BaseModel):
    """Publie via ZMQ PUB quand une ligne de commande est creee.
    L'inventory_service ecoute cet evenement pour decrementer le stock."""
    order_id: int
    product_id: int
    warehouse_id: int = 1  # Entrepot par defaut
    quantity: int
    created_at: datetime = Field(default_factory=datetime.now)
