from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ListingCreate, ListingUpdate, ListingResponse, ListingListResponse
from app import crud

router = APIRouter(prefix="/api/v1/listings", tags=["Listings"])

@router.get("", response_model=ListingListResponse, summary="Listinglar ro'yxatini olish")
def list_listings(
    skip: int = Query(0, ge=0, description="O'tkazib yuborish soni"),
    limit: int = Query(20, ge=1, le=100, description="Sahifadagi listinglar soni"),
    category: Optional[str] = Query(None, description="Kategoriya bo'yicha filter"),
    status: Optional[str] = Query(None, description="Status bo'yicha filter (active, sold, inactive)"),
    search: Optional[str] = Query(None, description="Qidiruv matni (title va description ichidan)"),
    db: Session = Depends(get_db)
):
    """
    Barcha listinglarni pagination va filterlar bilan qaytaradi.
    """
    items, total = crud.get_listings(
        db,
        skip=skip,
        limit=limit,
        category=category,
        status=status,
        search=search
    )
    return ListingListResponse(total=total, items=items, skip=skip, limit=limit)

@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED, summary="Yangi listing yaratish")
def create_listing(
    listing_in: ListingCreate,
    db: Session = Depends(get_db)
):
    """
    Yangi listing qo'shadi. Agar `slug` ko'rsatilmagan bo'lsa, `title` asosida avtomatik unikal slug generatsiya qilinadi.
    """
    return crud.create_listing(db, listing_in)

@router.get("/{slug}", response_model=ListingResponse, summary="Slug bo'yicha listingni ko'rish")
def get_listing(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Unikal `slug` orqali bitta listing ma'lumotlarini qaytaradi.
    """
    listing = crud.get_listing_by_slug(db, slug)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha listing topilmadi"
        )
    return listing

@router.patch("/{slug}", response_model=ListingResponse, summary="Slug bo'yicha listingni yangilash")
def update_listing(
    slug: str,
    listing_in: ListingUpdate,
    db: Session = Depends(get_db)
):
    """
    Listingni yangilaydi. Agar `title` o'zgartirilsa, uning `slug`i ham avtomatik qayta generatsiya qilinadi.
    """
    listing = crud.update_listing_by_slug(db, slug, listing_in)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha listing topilmadi"
        )
    return listing
