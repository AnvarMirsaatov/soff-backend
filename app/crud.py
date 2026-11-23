from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Category, Listing, ListingImage
from app.schemas import ListingCreate, ListingUpdate, CategoryCreate, CategoryUpdate
from app.utils import generate_unique_slug, generate_unique_category_slug

# ==========================================
# Category CRUD
# ==========================================

def get_parent_categories(db: Session) -> List[dict]:
    """
    Barcha ota kategoriyalarni sub-kategoriyalari va har birining listinglar soni bilan qaytaradi.
    """
    parents = (
        db.query(Category)
        .filter(Category.parent_id == None)
        .order_by(Category.id.asc())
        .all()
    )

    result = []
    for parent in parents:
        sub_list = []
        for sub in parent.subcategories:
            sub_count = db.query(Listing).filter(Listing.subcategory_id == sub.id).count()
            sub_list.append({
                "id": sub.id,
                "name": sub.name,
                "slug": sub.slug,
                "description": sub.description,
                "icon": sub.icon,
                "parent_id": sub.parent_id,
                "listings_count": sub_count
            })

        parent_count = db.query(Listing).filter(Listing.category_id == parent.id).count()
        result.append({
            "id": parent.id,
            "name": parent.name,
            "slug": parent.slug,
            "description": parent.description,
            "icon": parent.icon,
            "parent_id": None,
            "subcategories": sub_list,
            "listings_count": parent_count
        })

    return result

def get_category_by_slug(db: Session, slug: str) -> Optional[dict]:
    """
    Slug bo'yicha kategoriyani qidiradi.
    Agar ota kategoriya bo'lsa, sub-kategoriyalar va listinglar soni bilan qaytaradi.
    """
    category = db.query(Category).filter(Category.slug == slug).first()
    if not category:
        return None

    sub_list = []
    for sub in category.subcategories:
        sub_count = db.query(Listing).filter(Listing.subcategory_id == sub.id).count()
        sub_list.append({
            "id": sub.id,
            "name": sub.name,
            "slug": sub.slug,
            "description": sub.description,
            "icon": sub.icon,
            "parent_id": sub.parent_id,
            "listings_count": sub_count
        })

    listings_count = (
        db.query(Listing).filter(Listing.category_id == category.id).count()
        if category.parent_id is None
        else db.query(Listing).filter(Listing.subcategory_id == category.id).count()
    )

    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "icon": category.icon,
        "parent_id": category.parent_id,
        "subcategories": sub_list,
        "listings_count": listings_count
    }

def get_subcategories_by_parent_slug(db: Session, parent_slug: str) -> Optional[List[dict]]:
    """
    Ota kategoriya slugiga asosan faqat uning sub-kategoriyalarini qaytaradi.
    """
    parent = db.query(Category).filter(Category.slug == parent_slug, Category.parent_id == None).first()
    if not parent:
        return None

    sub_list = []
    for sub in parent.subcategories:
        sub_count = db.query(Listing).filter(Listing.subcategory_id == sub.id).count()
        sub_list.append({
            "id": sub.id,
            "name": sub.name,
            "slug": sub.slug,
            "description": sub.description,
            "icon": sub.icon,
            "parent_id": sub.parent_id,
            "listings_count": sub_count
        })
    return sub_list

def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


# ==========================================
# Listing CRUD
# ==========================================

def get_listing_by_slug(db: Session, slug: str, increment_views: bool = False) -> Optional[Listing]:
    listing = db.query(Listing).filter(Listing.slug == slug).first()
    if listing and increment_views:
        listing.views_count += 1
        db.commit()
        db.refresh(listing)
    return listing

def get_listing_by_id(db: Session, listing_id: int) -> Optional[Listing]:
    return db.query(Listing).filter(Listing.id == listing_id).first()

def get_listings(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    status: Optional[str] = None,
    is_featured: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    category_slug: Optional[str] = None,
    subcategory_slug: Optional[str] = None
) -> Tuple[List[Listing], int]:
    query = db.query(Listing)

    if category_slug:
        cat = db.query(Category).filter(Category.slug == category_slug).first()
        if cat:
            query = query.filter(Listing.category_id == cat.id)
        else:
            return [], 0

    if subcategory_slug:
        sub = db.query(Category).filter(Category.slug == subcategory_slug).first()
        if sub:
            query = query.filter(Listing.subcategory_id == sub.id)
        else:
            return [], 0

    if status:
        query = query.filter(Listing.status == status)

    if is_featured is not None:
        query = query.filter(Listing.is_featured == is_featured)

    if min_price is not None:
        query = query.filter(Listing.price >= min_price)

    if max_price is not None:
        query = query.filter(Listing.price <= max_price)

    if search:
        search_filter = or_(
            Listing.title.ilike(f"%{search}%"),
            Listing.description.ilike(f"%{search}%"),
            Listing.short_description.ilike(f"%{search}%")
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
    raw_slug_source = listing_in.slug if listing_in.slug else listing_in.title
    slug = generate_unique_slug(db, raw_slug_source)

    data = listing_in.model_dump(exclude={"slug"})
    listing = Listing(**data, slug=slug)
    db.add(listing)
    db.commit()
    db.refresh(listing)

    # Agar image_url mavjud bo'lsa, asosiy rasm sifatida ListingImage jadvaliga ham qo'shamiz
    if listing.image_url:
        main_img = ListingImage(
            listing_id=listing.id,
            image_url=listing.image_url,
            is_main=True,
            order=0
        )
        db.add(main_img)
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

def delete_listing_by_slug(db: Session, slug: str) -> bool:
    listing = get_listing_by_slug(db, slug)
    if not listing:
        return False

    db.delete(listing)
    db.commit()
    return True

def add_listing_image(
    db: Session,
    listing: Listing,
    image_url: str,
    is_main: bool = False,
    order: int = 0
) -> ListingImage:
    if is_main or not listing.image_url:
        listing.image_url = image_url

    new_img = ListingImage(
        listing_id=listing.id,
        image_url=image_url,
        is_main=is_main,
        order=order
    )
    db.add(new_img)
    db.commit()
    db.refresh(new_img)
    db.refresh(listing)
    return new_img
