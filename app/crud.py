from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Listing
from app.schemas import ListingCreate, ListingUpdate
from app.utils import generate_unique_slug

def get_listing_by_slug(db: Session, slug: str) -> Optional[Listing]:
    return db.query(Listing).filter(Listing.slug == slug).first()

def get_listing_by_id(db: Session, listing_id: int) -> Optional[Listing]:
    return db.query(Listing).filter(Listing.id == listing_id).first()

def get_listings(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> Tuple[List[Listing], int]:
    query = db.query(Listing)

    if category:
        query = query.filter(Listing.category == category)
    if status:
        query = query.filter(Listing.status == status)
    if search:
        search_filter = or_(
            Listing.title.ilike(f"%{search}%"),
            Listing.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    total = query.count()
    items = (
        query.order_by(Listing.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return items, total

def create_listing(db: Session, listing_in: ListingCreate) -> Listing:
    # Agar slug foydalanuvchi tomonidan berilgan bo'lsa uni tekshirib unikal qilamiz,
    # aks holda title dan unikal slug yasaymiz.
    raw_slug_source = listing_in.slug if listing_in.slug else listing_in.title
    slug = generate_unique_slug(db, raw_slug_source)

    data = listing_in.model_dump(exclude={"slug"})
    listing = Listing(**data, slug=slug)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

def update_listing_by_slug(db: Session, slug: str, listing_in: ListingUpdate) -> Optional[Listing]:
    listing = get_listing_by_slug(db, slug)
    if not listing:
        return None

    update_data = listing_in.model_dump(exclude_unset=True)

    # Agar title o'zgartirilsa, slugni ham avtomatik yangilash
    if "title" in update_data and update_data["title"] and update_data["title"] != listing.title:
        listing.slug = generate_unique_slug(db, update_data["title"], current_id=listing.id)

    for field, value in update_data.items():
        setattr(listing, field, value)

    db.commit()
    db.refresh(listing)
    return listing
