import os
import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    ListingCreate,
    ListingUpdate,
    ListingResponse,
    ListingListResponse,
    ListingImageResponse
)
from app.models import ListingImage
from app import crud

router = APIRouter(prefix="/api/v1/listings", tags=["Listings"])

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "files")

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

@router.get("", response_model=ListingListResponse, summary="Listinglar ro'yxatini olish")
def list_listings(
    skip: int = Query(0, ge=0, description="O'tkazib yuborish soni"),
    limit: int = Query(20, ge=1, le=100, description="Sahifadagi listinglar soni"),
    search: Optional[str] = Query(None, description="Qidiruv matni (title, short_description, description)"),
    status: Optional[str] = Query(None, description="Holat bo'yicha filter (active, inactive, sold)"),
    is_featured: Optional[bool] = Query(None, description="Tanlangan mahsulotlar bo'yicha filter"),
    min_price: Optional[float] = Query(None, ge=0.0, description="Minimal narx"),
    max_price: Optional[float] = Query(None, ge=0.0, description="Maksimal narx"),
    category_slug: Optional[str] = Query(None, description="Ota kategoriya slugi"),
    subcategory_slug: Optional[str] = Query(None, description="Sub-kategoriya slugi"),
    db: Session = Depends(get_db)
):
    """
    Barcha listinglarni qidiruv, kategoriya, narx va boshqa filtrlar bilan qaytaradi.
    """
    items, total = crud.get_listings(
        db,
        skip=skip,
        limit=limit,
        search=search,
        status=status,
        is_featured=is_featured,
        min_price=min_price,
        max_price=max_price,
        category_slug=category_slug,
        subcategory_slug=subcategory_slug
    )
    return ListingListResponse(total=total, items=items, skip=skip, limit=limit)


@router.post("", response_model=ListingResponse, status_code=status.HTTP_201_CREATED, summary="Yangi mahsulot yaratish")
def create_listing(
    listing_in: ListingCreate,
    db: Session = Depends(get_db)
):
    """
    Yangi mahsulot qo'shadi.
    `category_id` va agar kiritilgan bo'lsa `subcategory_id` tekshiriladi.
    `slug` avtomatik unikal tarzda yaratiladi.
    """
    category = crud.get_category_by_id(db, listing_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID {listing_in.category_id} ga ega bo'lgan ota kategoriya topilmadi."
        )

    if listing_in.subcategory_id:
        subcategory = crud.get_category_by_id(db, listing_in.subcategory_id)
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ID {listing_in.subcategory_id} ga ega bo'lgan sub-kategoriya topilmadi."
            )
        if subcategory.parent_id != category.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tanlangan sub-kategoriya ('{subcategory.name}') '{category.name}' ota kategoriyasiga tegishli emas."
            )

    return crud.create_listing(db, listing_in)


@router.get("/{slug}", response_model=ListingResponse, summary="Mahsulot Detail sahifasi")
def get_listing(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Unikal `slug` orqali bitta mahsulotning to'liq ma'lumotlarini qaytaradi.
    Har ochilganda `views_count` ni 1 taga oshiradi.
    """
    listing = crud.get_listing_by_slug(db, slug, increment_views=True)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha mahsulot topilmadi"
        )
    return listing


@router.patch("/{slug}", response_model=ListingResponse, summary="Mahsulotni yangilash")
def update_listing(
    slug: str,
    listing_in: ListingUpdate,
    db: Session = Depends(get_db)
):
    """
    Mahsulot ma'lumotlarini qisman yangilaydi.
    Agar `title` o'zgartirilsa, yangi unikal `slug` avtomatik generatsiya qilinadi.
    """
    if listing_in.category_id is not None:
        cat = crud.get_category_by_id(db, listing_in.category_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kategoriya topilmadi")

    if listing_in.subcategory_id is not None:
        sub = crud.get_category_by_id(db, listing_in.subcategory_id)
        if not sub:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sub-kategoriya topilmadi")

    listing = crud.update_listing_by_slug(db, slug, listing_in)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha mahsulot topilmadi"
        )
    return listing


@router.delete("/{slug}", summary="Mahsulotni o'chirish")
def delete_listing(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Mahsulotni bazadan o'chiradi (barcha bog'langan rasmlari bilan birga).
    """
    success = crud.delete_listing_by_slug(db, slug)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha mahsulot topilmadi"
        )
    return {
        "status": "success",
        "message": f"'{slug}' mahsuloti muvaffaqiyatli o'chirildi"
    }


@router.post("/{slug}/images", response_model=List[ListingImageResponse], status_code=status.HTTP_201_CREATED, summary="Mahsulotga rasmlar biriktirish")
async def upload_listing_images(
    slug: str,
    files: List[UploadFile] = File(..., description="Bir yoki bir nechta rasm fayllari"),
    db: Session = Depends(get_db)
):
    """
    Mavjud mahsulotga bir yoki bir nechta rasm yuklab, `ListingImage` jadvaliga biriktiradi.
    """
    listing = crud.get_listing_by_slug(db, slug)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha mahsulot topilmadi"
        )

    os.makedirs(FILES_DIR, exist_ok=True)
    created_images = []
    current_order = len(listing.images)

    for file in files:
        ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Fayl '{file.filename}' formati qo'llab-quvvatlanmaydi. Ruxsat berilgan: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            )

        unique_filename = f"{uuid.uuid4().hex}{ext}"
        destination = os.path.join(FILES_DIR, unique_filename)

        content = await file.read()
        with open(destination, "wb") as f:
            f.write(content)

        image_url = f"/files/{unique_filename}"
        is_main = False
        if not listing.image_url:
            listing.image_url = image_url
            is_main = True

        new_img = ListingImage(
            listing_id=listing.id,
            image_url=image_url,
            is_main=is_main,
            order=current_order
        )
        db.add(new_img)
        db.commit()
        db.refresh(new_img)
        created_images.append(new_img)
        current_order += 1

    db.refresh(listing)
    return created_images
