from typing import List
from pydantic import BaseModel, Field


class OrderLineRequest(BaseModel):
    product_id: int
    product_name: str = ""
    quantity: int = Field(default=1, ge=1)
    unit_price: float = Field(default=0.0, ge=0)


class OrderCreateRequest(BaseModel):
    customer_id: int
    lines: List[OrderLineRequest] = Field(default_factory=list)


class OrderUpdateStatusRequest(BaseModel):
    status: str


class OrderLineResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    total: float
    lines: List[OrderLineResponse] = []
