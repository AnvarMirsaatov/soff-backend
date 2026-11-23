from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CategoryTreeResponse, ListingListResponse
from app import crud

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])

@router.get("", response_model=List[CategoryTreeResponse], summary="Barcha ota kategoriyalar ro'yxatini olish")
def list_categories(
    include_children: bool = Query(False, description="True bo'lsa, ichidagi 10 ta ichki va ularning sub-kategoriyalari bilan to'liq daraxt ko'rinishida qaytaradi"),
    db: Session = Depends(get_db)
):
    """
    Barcha 6 ta 1-darajali (ota) kategoriyalarni qaytaradi.
    `include_children=true` berilganda, har birining ichki va sub-kategoriyalari
    rekursiv daraxt (tree) ko'rinishida yuklanadi.
    """
    return crud.get_parent_categories(db, include_children=include_children)


@router.get("/{slug}", response_model=CategoryTreeResponse, summary="Kategoriya ma'lumotlarini slug bo'yicha olish")
def get_category(slug: str, db: Session = Depends(get_db)):
    """
    Tanlangan kategoriyaning (ota, ichki yoki sub) ma'lumotlarini va
    uning bevosita ichidagi bolalarini (children) qaytaradi.
    """
    category = crud.get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha kategoriya topilmadi"
        )
    return category


@router.get("/{slug}/subcategories", response_model=List[CategoryTreeResponse], summary="Kategoriyaga tegishli bolalar (sub-kategoriyalar)")
def get_subcategories(slug: str, db: Session = Depends(get_db)):
    """
    Berilgan kategoriyaga tegishli bo'lgan barcha quyi kategoriyalarni (children) qaytaradi.
    """
    subcategories = crud.get_subcategories_by_parent_slug(db, slug)
    if subcategories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha kategoriya topilmadi"
        )
    return subcategories


@router.get("/{slug}/listings", response_model=ListingListResponse, summary="Kategoriyaga tegishli barcha cardlarni olish")
def get_category_listings(
    slug: str,
    skip: int = Query(0, ge=0, description="O'tkazib yuborish soni"),
    limit: int = Query(20, ge=1, le=100, description="Sahifadagi listinglar soni"),
    search: Optional[str] = Query(None, description="Qidiruv matni"),
    status: Optional[str] = Query(None, description="Holat bo'yicha filter"),
    is_featured: Optional[bool] = Query(None, description="Tanlangan mahsulotlar bo'yicha filter"),
    min_price: Optional[float] = Query(None, ge=0.0, description="Minimal narx"),
    max_price: Optional[float] = Query(None, ge=0.0, description="Maksimal narx"),
    db: Session = Depends(get_db)
):
    """
    Kategoriya slugi bo'yicha unga va uning barcha quyi kategoriyalariga tegishli
    barcha mahsulotlarni (cardlarni) rekursiv ravishda yig'ib qaytaradi.
    """
    category = crud.get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha kategoriya topilmadi"
        )

    items, total = crud.get_listings(
        db,
        skip=skip,
        limit=limit,
        search=search,
        status=status,
        is_featured=is_featured,
        min_price=min_price,
        max_price=max_price,
        category_slug=slug
    )
    return ListingListResponse(total=total, items=items, skip=skip, limit=limit)
