from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=100)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=255)
    customer_phone: str = Field(min_length=3, max_length=64)
    items: list[OrderItemCreate] = Field(min_length=1)
    idempotency_key: str | None = Field(default=None, max_length=64)


class OrderItemRead(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class OrderRead(BaseModel):
    id: str
    customer_name: str
    customer_phone: str
    items: list[OrderItemRead]
    total: float
    created_at: datetime

    model_config = {"from_attributes": True}
