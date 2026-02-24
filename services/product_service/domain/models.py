from enum import StrEnum
from typing import Optional
from pydantic import BaseModel, Field

class ProductCategory(StrEnum):
    MOUNT = "mount"
    PET = "pet"
    SUBSCRIPTION = "subscription"
    SERVICE = "service"
    COSMETIC = "cosmetic"

class Product(BaseModel):
    id: int = Field(description="Identifiant unique du produit")
    name: str = Field(min_length=1, max_length=100, description="Nom de l'objet (ex: Rênes d'Invincible)")
    description: Optional[str] = Field(None, description="Description ou Lore de l'objet")
    # price: float = Field(..., gt=0, description="Prix en euros ou pièces d'or")
    category: ProductCategory = Field(..., description="Catégorie de l'objet")
    # stock: int = Field(default=0, ge=0, description="Quantité disponible")
    image_url: Optional[str] = Field(None, description="URL de l'icône")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1337,
                "name": "Rênes d'Invincible",
                "description": "Le destrier du Roi Liche.",
                "price": 25.00,
                "category": "mount",
                "stock": 5,
                "image_url": "item_image.jpg"
            }
        }
        