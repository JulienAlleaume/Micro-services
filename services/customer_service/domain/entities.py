from pydantic import BaseModel, Field


class Customer(BaseModel):
    """Entite du domaine Customer."""
    id: int = Field(default=0, description="Identifiant unique du client")
    username: str = Field(..., max_length=50, description="Nom d'utilisateur")
    email: str = Field(..., max_length=100, description="Adresse email")
    gold_balance: float = Field(default=0.0, description="Solde en pieces d'or")
    is_active: bool = Field(default=True, description="Compte actif ou non")
