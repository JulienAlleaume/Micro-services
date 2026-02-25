from enum import StrEnum
from typing import List
from pydantic import BaseModel, Field


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderLine(BaseModel):
    """Ligne de commande — un produit + quantite dans une commande."""
    id: int = Field(default=0)
    order_id: int = Field(default=0)
    product_id: int = Field(...)
    product_name: str = Field(default="", max_length=100)
    quantity: int = Field(default=1, ge=1)
    unit_price: float = Field(default=0.0, ge=0)


class Order(BaseModel):
    """Entite du domaine Order."""
    id: int = Field(default=0)
    customer_id: int = Field(...)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    total: float = Field(default=0.0, ge=0)
    lines: List[OrderLine] = Field(default_factory=list)
