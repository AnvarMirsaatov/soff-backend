import re
import unicodedata
from typing import Optional
from sqlalchemy.orm import Session

try:
    from slugify import slugify as py_slugify
    HAS_SLUGIFY = True
except ImportError:
    HAS_SLUGIFY = False

def custom_slugify(text: str) -> str:
    """
    O'zbek va xalqaro belgilarni to'g'ri URL slug ko'rinishiga keltiradi.
    Misol: "O'zbekiston & Toshkent №1!" -> "ozbekiston-and-toshkent-no1"
    """
    if not text:
        return "item"

    # O'zbek tili va maxsus harflar uchun mapping
    replacements = {
        "oʻ": "o", "o'": "o", "o`": "o", "o‘": "o",
        "gʻ": "g", "g'": "g", "g`": "g", "g‘": "g",
        "Oʻ": "o", "O'": "o", "O`": "o", "O‘": "o",
        "Gʻ": "g", "G'": "g", "G`": "g", "G‘": "g",
        "sh": "sh", "ch": "ch", "yo": "yo", "yu": "yu", "ya": "ya",
        "Sh": "sh", "Ch": "ch", "Yo": "yo", "Yu": "yu", "Ya": "ya",
        "SH": "sh", "CH": "ch", "YO": "yo", "YU": "yu", "YA": "ya",
        "&": "and", "@": "at", "%": "percent", "#": "num"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    if HAS_SLUGIFY:
        slug = py_slugify(text, lowercase=True)
    else:
        text_lower = text.lower()
        normalized = unicodedata.normalize("NFKD", text_lower)
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^\w\s-]", "", ascii_text).strip()
        slug = re.sub(r"[-\s]+", "-", slug)

    return slug or "item"

def generate_unique_slug(db: Session, text: str, current_id: Optional[int] = None) -> str:
    """
    Bazada unikal bo'lgan Listing slug hosil qiladi.
    Agar 'kurs-ishi' mavjud bo'lsa -> 'kurs-ishi-1', 'kurs-ishi-2' ...
    """
    from app.models import Listing

    base_slug = custom_slugify(text)
    candidate = base_slug
    counter = 1

    while True:
        query = db.query(Listing).filter(Listing.slug == candidate)
        if current_id is not None:
            query = query.filter(Listing.id != current_id)
        exists = query.first()
        if not exists:
            return candidate

        candidate = f"{base_slug}-{counter}"
        counter += 1

def generate_unique_category_slug(db: Session, text: str, current_id: Optional[int] = None) -> str:
    """
    Bazada unikal bo'lgan Category slug hosil qiladi.
    """
    from app.models import Category

    base_slug = custom_slugify(text)
    candidate = base_slug
    counter = 1

    while True:
        query = db.query(Category).filter(Category.slug == candidate)
        if current_id is not None:
            query = query.filter(Category.id != current_id)
        exists = query.first()
        if not exists:
            return candidate

        candidate = f"{base_slug}-{counter}"
        counter += 1
