from typing import Optional
from pydantic import BaseModel, Field


class Price(BaseModel):
    """Entité du domaine Pricing — associe un prix à un produit."""
    id: int = Field(default=0, description="Identifiant unique du prix")
    product_id: int = Field(..., description="ID du produit associé")
    product_name: str = Field(..., max_length=100, description="Nom du produit (copie locale)")
    amount: float = Field(..., gt=0, description="Prix en pièces d'or")
    currency: str = Field(default="gold", description="Devise (gold, EUR, USD)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "product_id": 1337,
                "product_name": "Rênes d'Invincible",
                "amount": 25000.0,
                "currency": "gold"
            }
        }
