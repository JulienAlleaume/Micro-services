from typing import Optional
from pydantic import BaseModel, Field

# DTO pour la réponse (GET) - Ce que l'API renvoie au client
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: str  # On renvoie une string simple au lieu de l'Enum
    image_url: Optional[str] = None

    class Config:
        from_attributes = True # Permet de créer ce DTO directement depuis un objet Domain/DB

# DTO pour la création (POST) - Ce que le client envoie pour créer
class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nom de l'objet")
    description: Optional[str] = Field(None, description="Description")
    category: str = Field(..., description="Catégorie (mount, pet, etc.)")
    image_url: Optional[str] = Field(None, description="URL de l'image")

# DTO pour la modification (PUT) - Ce que le client envoie pour modifier
class ProductUpdateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: str
    image_url: Optional[str] = None
