from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

class ListingBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, examples=["MacBook Pro 16 M3 Max"])
    description: Optional[str] = Field(None, examples=["Holati a'lo, 36GB RAM, 1TB SSD, Space Black"])
    price: float = Field(default=0.0, ge=0.0, examples=[2899.00])
    category: str = Field(default="electronics", examples=["electronics"])
    status: str = Field(default="active", examples=["active"])
    image_url: Optional[str] = Field(None, examples=["/files/macbook-pro.jpg"])
    is_featured: bool = Field(default=False)

class ListingCreate(ListingBase):
    slug: Optional[str] = Field(
        None,
        description="Ixtiyoriy. Agar berilmasa, title dan avtomatik unikal slug generatsiya qilinadi.",
        examples=["macbook-pro-16-m3-max"]
    )

class ListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0.0)
    category: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: Optional[bool] = None

class ListingResponse(ListingBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ListingListResponse(BaseModel):
    total: int
    items: List[ListingResponse]
    skip: int
    limit: int
