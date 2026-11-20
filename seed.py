"""
Listing API - Seed script
Ushbu skript bazaga dastlabki namunaviy ma'lumotlarni kiritish uchun ishlatiladi.
Ishga tushirish: python seed.py
"""

from app.database import SessionLocal, Base, engine
from app.models import Listing
from app.utils import custom_slugify

SEED_LISTINGS = [
    {
        "title": "MacBook Pro 16 M3 Max",
        "description": "Eng so'nggi avlod Apple M3 Max noutbuki, 36GB birlashgan xotira, 1TB tezkor SSD, Space Black rang. Qutisi va kafolati bor.",
        "price": 2899.00,
        "category": "electronics",
        "status": "active",
        "image_url": "/files/macbook-pro.jpg",
        "is_featured": True,
    },
    {
        "title": "iPhone 15 Pro Max 256GB Natural Titanium",
        "description": "Yengil titan korpus, A17 Pro chip, ajoyib 5x telephoto kamera, Dynamic Island. Holati yangi.",
        "price": 1199.00,
        "category": "smartphones",
        "status": "active",
        "image_url": "/files/iphone-15.jpg",
        "is_featured": True,
    },
    {
        "title": "Sony WH-1000XM5 Shovqinni bekor qiluvchi quloqchinlar",
        "description": "Sanoatdagi eng yaxshi Noise Cancelling texnologiyasi, 30 soat batareya, premium ovoz sifati.",
        "price": 349.99,
        "category": "audio",
        "status": "active",
        "image_url": "/files/sony-headphones.jpg",
        "is_featured": False,
    },
    {
        "title": "Herman Miller Aeron Ergonomik Kreslo",
        "description": "Dasturchilar va ofis xodimlari uchun afsonaviy qulaylik. Bel tayanchi to'liq sozlanadi.",
        "price": 850.00,
        "category": "furniture",
        "status": "active",
        "image_url": "/files/aeron-chair.jpg",
        "is_featured": False,
    },
    {
        "title": "Sony PlayStation 5 Slim 1TB Edition",
        "description": "Kompakt dizayn, ultra-tezkor SSD, 4K HDR o'yinlar, to'plamda 2 ta DualSense geympad.",
        "price": 549.00,
        "category": "gaming",
        "status": "active",
        "image_url": "/files/ps5-slim.jpg",
        "is_featured": True,
    }
]

def seed_data(db=None) -> int:
    """
    Agar baza bo'sh bo'lsa, namunaviy listinglarni qo'shadi.
    Mavjud bo'lsa hech narsa qo'shmaydi va mavjud sonni qaytaradi.
    """
    close_db = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_db = True

    try:
        count = db.query(Listing).count()
        if count > 0:
            print(f"[Seed] Bazada allaqachon {count} ta listing mavjud. O'tkazib yuborildi.")
            return count

        print("[Seed] Baza bo'sh. Namunaviy listinglar yuklanmoqda...")
        for item in SEED_LISTINGS:
            slug = custom_slugify(item["title"])
            listing = Listing(
                title=item["title"],
                slug=slug,
                description=item["description"],
                price=item["price"],
                category=item["category"],
                status=item["status"],
                image_url=item["image_url"],
                is_featured=item["is_featured"]
            )
            db.add(listing)

        db.commit()
        total_seeded = len(SEED_LISTINGS)
        print(f"[Seed] Muvaffaqiyatli {total_seeded} ta listing bazaga yuklandi!")
        return total_seeded
    except Exception as e:
        db.rollback()
        print(f"[Seed Error] Ma'lumotlarni yuklashda xatolik yuz berdi: {e}")
        raise e
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_data()
