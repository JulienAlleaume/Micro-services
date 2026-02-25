from pydantic import BaseModel, Field


class CustomerResponse(BaseModel):
    id: int
    username: str
    email: str
    gold_balance: float
    is_active: bool


class CustomerCreateRequest(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    gold_balance: float = Field(default=0.0)


class CustomerUpdateRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    gold_balance: float | None = None
    is_active: bool | None = None
