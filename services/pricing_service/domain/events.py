from datetime import datetime
from pydantic import BaseModel, Field


class PriceCreatedEvent(BaseModel):
    """Événement émis quand un prix est créé."""
    price_id: int
    product_id: int
    amount: float
    currency: str
    created_at: datetime = Field(default_factory=datetime.now)


class PriceUpdatedEvent(BaseModel):
    """Événement émis quand un prix est mis à jour."""
    price_id: int
    product_id: int
    old_amount: float
    new_amount: float
    currency: str
    updated_at: datetime = Field(default_factory=datetime.now)
