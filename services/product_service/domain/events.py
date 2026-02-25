from datetime import datetime
from pydantic import BaseModel, Field
from domain.entities import ProductCategory

class ProductCreatedEvent(BaseModel):
    """Cet événement est publié quand un produit est créé avec succès."""
    product_id: int
    name: str
    category: ProductCategory
    created_at: datetime = Field(default_factory=datetime.now)
    