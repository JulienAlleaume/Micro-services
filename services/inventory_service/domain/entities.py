from pydantic import BaseModel, Field


class Inventory(BaseModel):
    """Entite du domaine Inventory -- stock d'un produit dans un entrepot."""
    id: int = Field(default=0, description="Identifiant unique de la ligne d'inventaire")
    product_id: int = Field(..., description="ID du produit")
    product_name: str = Field(..., max_length=100, description="Nom du produit (copie locale)")
    warehouse_id: int = Field(default=1, description="ID de l'entrepot")
    quantity: int = Field(default=0, ge=0, description="Quantite en stock")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "product_id": 1337,
                "product_name": "Renes d'Invincible",
                "warehouse_id": 1,
                "quantity": 10
            }
        }
