from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Category, Listing, ListingImage
from app.schemas import ListingCreate, ListingUpdate, CategoryCreate, CategoryUpdate
from app.utils import generate_unique_slug, generate_unique_category_slug

# ==========================================
# Category Helpers & CRUD
# ==========================================

def get_category_descendant_ids(db: Session, category_id: int) -> List[int]:
    """
    Kategoriya va uning barcha quyi (bolalar, nabiralar va h.k.) ID larini rekursiv yig'adi.
    """
    ids = [category_id]
    to_visit = [category_id]
    while to_visit:
        curr_id = to_visit.pop(0)
        children = db.query(Category.id).filter(Category.parent_id == curr_id).all()
        for (c_id,) in children:
            ids.append(c_id)
            to_visit.append(c_id)
    return ids

def count_listings_for_category(db: Session, category_id: int) -> int:
    """
    Kategoriya va uning ostidagi barcha quyi kategoriyalarga tegishli mahsulotlar sonini hisoblaydi.
    """
    descendant_ids = get_category_descendant_ids(db, category_id)
    return db.query(Listing).filter(
        or_(
            Listing.category_id.in_(descendant_ids),
            Listing.inner_category_id.in_(descendant_ids),
            Listing.subcategory_id.in_(descendant_ids)
        )
    ).count()

def build_category_node(db: Session, category: Category, include_children: bool = True) -> dict:
    """
    Bitta kategoriyani va (agar include_children=True bo'lsa) uning barcha bolalarini
    rekursiv daraxt (tree) ko'rinishida shakllantiradi.
    """
    cat_count = count_listings_for_category(db, category.id)
    children_list = []

    if include_children and category.children:
        for child in category.children:
            child_node = build_category_node(db, child, include_children=True)
            children_list.append(child_node)

    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "icon": category.icon,
        "level": category.level,
        "parent_id": category.parent_id,
        "listings_count": cat_count,
        "children": children_list,
        "subcategories": children_list
    }

def get_parent_categories(db: Session, include_children: bool = False) -> List[dict]:
    """
    Barcha 6 ta 1-darajali (ota) kategoriyani qaytaradi.
    Agar include_children=True bo'lsa, 10 ta ichki kategoriya va ularning sub-kategoriyalarini
    to'liq rekursiv daraxt sifatida yuklaydi.
    """
    parents = (
        db.query(Category)
        .filter(Category.parent_id == None)
        .order_by(Category.id.asc())
        .all()
    )

    result = []
    for parent in parents:
        node = build_category_node(db, parent, include_children=include_children)
        result.append(node)
    return result

def get_category_by_slug(db: Session, slug: str) -> Optional[dict]:
    """
    Slug bo'yicha kategoriyani qidiradi.
    Uning darajasidan qat'i nazar (ota, ichki yoki sub), uning ma'lumotlarini
    va bevosita ichidagi bolalarini (children) qaytaradi.
    """
    category = db.query(Category).filter(Category.slug == slug).first()
    if not category:
        return None

    return build_category_node(db, category, include_children=True)

def get_subcategories_by_parent_slug(db: Session, parent_slug: str) -> Optional[List[dict]]:
    """
    Berilgan kategoriya slugiga asosan faqat uning bevosita bolalarini (children) qaytaradi.
    """
    parent = db.query(Category).filter(Category.slug == parent_slug).first()
    if not parent:
        return None

    result = []
    for child in parent.children:
        child_node = build_category_node(db, child, include_children=True)
        result.append(child_node)
    return result

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

    # 1. category_slug bo'yicha rekursiv qidiruv
    if category_slug:
        cat = db.query(Category).filter(Category.slug == category_slug).first()
        if cat:
            descendant_ids = get_category_descendant_ids(db, cat.id)
            query = query.filter(
                or_(
                    Listing.category_id.in_(descendant_ids),
                    Listing.inner_category_id.in_(descendant_ids),
                    Listing.subcategory_id.in_(descendant_ids)
                )
            )
        else:
            return [], 0

    # 2. subcategory_slug bo'yicha qidiruv (aniq sub-kategoriya berilganda)
    if subcategory_slug:
        sub = db.query(Category).filter(Category.slug == subcategory_slug).first()
        if sub:
            descendant_ids = get_category_descendant_ids(db, sub.id)
            query = query.filter(
                or_(
                    Listing.subcategory_id.in_(descendant_ids),
                    Listing.inner_category_id.in_(descendant_ids)
                )
            )
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

    # Agar image_url mavjud bo'lsa, asosiy rasm sifatida ListingImage ga qo'shamiz
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
