from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CategoryResponse, SubcategoryResponse
from app import crud

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])

@router.get("", response_model=List[CategoryResponse], summary="Barcha ota kategoriyalar ro'yxatini olish")
def list_categories(db: Session = Depends(get_db)):
    """
    Barcha 6 ta ota kategoriyani ularning sub-kategoriyalari va har birining listinglar soni bilan birga qaytaradi.
    """
    return crud.get_parent_categories(db)

@router.get("/{slug}", response_model=CategoryResponse, summary="Kategoriya ma'lumotlarini slug bo'yicha olish")
def get_category(slug: str, db: Session = Depends(get_db)):
    """
    Tanlangan kategoriya haqida to'liq ma'lumot va unga tegishli barcha sub-kategoriyalar ro'yxatini qaytaradi.
    """
    category = crud.get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha kategoriya topilmadi"
        )
    return category

@router.get("/{slug}/subcategories", response_model=List[SubcategoryResponse], summary="Ota kategoriyaga tegishli sub-kategoriyalar")
def get_subcategories(slug: str, db: Session = Depends(get_db)):
    """
    Faqat berilgan ota kategoriyaga tegishli bo'lgan barcha sub-kategoriyalarni qaytaradi.
    """
    subcategories = crud.get_subcategories_by_parent_slug(db, slug)
    if subcategories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slug '{slug}' bo'yicha ota kategoriya topilmadi"
        )
    return subcategories
