from datetime import datetime

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price: float = Field(default=0, ge=0)


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    image_url: str
    created_at: datetime

    model_config = {"from_attributes": True}
