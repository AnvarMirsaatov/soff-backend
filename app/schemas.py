from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

# ==========================================
# Category Schemas
# ==========================================

class CategorySimple(BaseModel):
    id: int
    name: str
    slug: str
    icon: Optional[str] = None
    level: int = 1
    parent_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CategoryTreeResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    level: int = 1
    parent_id: Optional[int] = None
    listings_count: int = 0
    children: List["CategoryTreeResponse"] = []
    subcategories: List["CategoryTreeResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Backwards compatibility aliases
CategoryResponse = CategoryTreeResponse
SubcategoryResponse = CategoryTreeResponse


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, examples=["Web dasturlash"])
    slug: Optional[str] = Field(None, examples=["web-dasturlash"])
    description: Optional[str] = Field(None, examples=["Veb-saytlar, internet-do'konlar va tizimlar"])
    icon: Optional[str] = Field(None, examples=["code"])
    parent_id: Optional[int] = Field(None, examples=[None])


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    slug: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None


# ==========================================
# ListingImage Schemas
# ==========================================

class ListingImageBase(BaseModel):
    image_url: str = Field(..., examples=["/files/preview-1.jpg"])
    is_main: bool = Field(default=False)
    order: int = Field(default=0)


class ListingImageCreate(ListingImageBase):
    pass


class ListingImageResponse(ListingImageBase):
    id: int
    listing_id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Listing Schemas
# ==========================================

class ListingBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, examples=["Professional E-commerce Veb-sayt"])
    short_description: Optional[str] = Field(None, max_length=500, examples=["Next.js va FastAPI da yozilgan tayyor onlayn do'kon"])
    description: Optional[str] = Field(None, examples=["To'liq funksional internet do'kon kodi. Stripe va Payme to'lovlari sozlangan."])
    price: float = Field(default=0.0, ge=0.0, examples=[150.00])
    file_format: Optional[str] = Field(None, examples=["ZIP, React, FastAPI"])
    image_url: Optional[str] = Field(None, examples=["/files/ecommerce-main.jpg"])
    is_featured: bool = Field(default=False)
    status: str = Field(default="active", examples=["active"])


class ListingCreate(ListingBase):
    slug: Optional[str] = Field(None, description="Ixtiyoriy. Berilmasa, title dan avtomatik unikal slug yasaladi.")
    category_id: int = Field(..., description="Ota kategoriya ID si", examples=[1])
    inner_category_id: Optional[int] = Field(None, description="2-darajali Ichki kategoriya ID si", examples=[2])
    subcategory_id: Optional[int] = Field(None, description="3-darajali Sub-kategoriya ID si", examples=[3])


class ListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=255)
    short_description: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0.0)
    file_format: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: Optional[bool] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    inner_category_id: Optional[int] = None
    subcategory_id: Optional[int] = None


class ListingResponse(ListingBase):
    id: int
    slug: str
    category_id: int
    inner_category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    category: Optional[CategorySimple] = None
    inner_category: Optional[CategorySimple] = None
    subcategory: Optional[CategorySimple] = None
    images: List[ListingImageResponse] = []
    views_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ListingListResponse(BaseModel):
    total: int
    items: List[ListingResponse]
    skip: int
    limit: int


# ==========================================
# Upload Schemas
# ==========================================

class ImageUploadResponse(BaseModel):
    url: str
    filename: str
