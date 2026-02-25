from typing import Optional
from pydantic import BaseModel, Field


# DTO pour la réponse (GET)
class PriceResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    amount: float
    currency: str

    class Config:
        from_attributes = True


# DTO pour la création (POST)
class PriceCreateRequest(BaseModel):
    product_id: int = Field(..., description="ID du produit")
    product_name: str = Field(..., max_length=100, description="Nom du produit")
    amount: float = Field(..., gt=0, description="Prix")
    currency: str = Field(default="gold", description="Devise (gold, EUR, USD)")


# DTO pour la modification (PUT)
class PriceUpdateRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Nouveau prix")
    currency: Optional[str] = Field(None, description="Nouvelle devise")
