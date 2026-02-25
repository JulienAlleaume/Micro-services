from datetime import datetime
from pydantic import BaseModel, Field


class InventoryCreatedEvent(BaseModel):
    """Evenement emis quand une ligne d'inventaire est creee."""
    inventory_id: int
    product_id: int
    warehouse_id: int
    quantity: int
    created_at: datetime = Field(default_factory=datetime.now)


class InventoryUpdatedEvent(BaseModel):
    """Evenement emis quand le stock est modifie."""
    inventory_id: int
    product_id: int
    warehouse_id: int
    old_quantity: int
    new_quantity: int
    updated_at: datetime = Field(default_factory=datetime.now)
