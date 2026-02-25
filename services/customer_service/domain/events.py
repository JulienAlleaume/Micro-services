from datetime import datetime
from pydantic import BaseModel, Field


class CustomerCreatedEvent(BaseModel):
    """Evenement publie quand un client est cree."""
    customer_id: int
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
