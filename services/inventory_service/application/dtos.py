from typing import Optional
from pydantic import BaseModel, Field


# DTO pour la reponse (GET)
class InventoryResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    warehouse_id: int
    quantity: int

    class Config:
        from_attributes = True


# DTO pour la creation (POST) -- utilise surtout en interne via sub_product_created
class InventoryCreateRequest(BaseModel):
    product_id: int = Field(..., description="ID du produit")
    product_name: str = Field(..., max_length=100, description="Nom du produit")
    warehouse_id: int = Field(default=1, description="ID de l'entrepot")
    quantity: int = Field(default=0, ge=0, description="Quantite initiale")


# DTO pour la modification (PATCH /inventory/{warehouse_pk}/{product_pk})
class InventoryUpdateRequest(BaseModel):
    quantity: int = Field(..., ge=0, description="Nouvelle quantite en stock")
