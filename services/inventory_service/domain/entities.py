from pydantic import BaseModel, Field


class Warehouse(BaseModel):
    """Entite du domaine Warehouse -- un entrepot dans le monde de WoW."""
    id: int = Field(default=0, description="Identifiant unique de l'entrepot")
    name: str = Field(..., max_length=100, description="Nom de l'entrepot")
    location: str = Field(default="", max_length=100, description="Zone dans le monde de WoW")


class Inventory(BaseModel):
    """Entite du domaine Inventory -- stock d'un produit dans un entrepot."""
    id: int = Field(default=0, description="Identifiant unique de la ligne d'inventaire")
    product_id: int = Field(..., description="ID du produit")
    product_name: str = Field(..., max_length=100, description="Nom du produit (copie locale)")
    warehouse_id: int = Field(default=1, description="ID de l'entrepot")
    quantity: int = Field(default=0, ge=0, description="Quantite en stock")
