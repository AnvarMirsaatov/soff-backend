import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base, SessionLocal
from app.routers import listings, categories, upload
from seed import seed_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan: Server ishga tushganda va to'xtaganda bajariladigan amallar.
    1. Barcha jadvallarni yaratadi (Base.metadata.create_all).
    2. Agar baza bo'sh bo'lsa, seed.py orqali barcha 6 ta ota kategoriya,
       sub-kategoriyalar va sifatli namunaviy listinglarni avtomatik yuklaydi.
    """
    print("[Lifespan] Server ishga tushmoqda...")
    # 1. Jadvallarni yaratish
    Base.metadata.create_all(bind=engine)
    print("[Lifespan] Jadvallar tekshirildi/yaratildi.")

    # 2. Baza bo'sh bo'lsa avtomatik seed qilish
    db = SessionLocal()
    try:
        seed_data(db)
    except Exception as e:
        print(f"[Lifespan Seed Error] Xatolik yuz berdi: {e}")
    finally:
        db.close()

    yield
    print("[Lifespan] Server to'xtatildi.")

app = FastAPI(
    title="Soff Backend - Digital Marketplace API",
    description=(
        "FastAPI + SQLAlchemy 2.0 + Pydantic v2 asosida ishlab chiqilgan raqamli mahsulotlar va listinglar API si.\n\n"
        "Asosiy imkoniyatlar:\n"
        "- 6 ta asosiy va iyerarxik Sub-kategoriyalar tizimi\n"
        "- O'zbek tiliga moslashtirilgan unikal **Slug Architecture**\n"
        "- Ko'p rasmli galereya (ListingImage) va fayl yuklash (/upload)\n"
        "- Filtratsiya, qidiruv, narx bo'yicha saralash va sahifalash (Pagination)\n"
        "- Mahsulot ko'rishlar soni hisoblagichi (views_count)\n"
        "- Render.com va PostgreSQL ga to'liq moslashgan"
    ),
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. CORS Middleware sozlamasi (Frontend integratsiyasi uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Statik fayllarni /files/ yo'nalishiga ulash
FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "files")
os.makedirs(FILES_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=FILES_DIR), name="files")

# 3. Routerlarni ulash
app.include_router(categories.router)
app.include_router(listings.router)
app.include_router(upload.router)

# 4. Asosiy va sog'liqni tekshirish (Health check) endpointlari
@app.get("/", tags=["Root"])
def root():
    return {
        "name": "Soff Backend - Digital Marketplace API",
        "status": "online",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "categories": "/api/v1/categories",
            "category_detail": "/api/v1/categories/{slug}",
            "subcategories": "/api/v1/categories/{slug}/subcategories",
            "listings": "/api/v1/listings",
            "listing_detail": "/api/v1/listings/{slug}",
            "upload_image": "/api/v1/upload/image",
            "static_files": "/files/"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    Server va ma'lumotlar bazasi holatini tekshirish uchun endpoint (Render health check).
    """
    db_type = "sqlite" if "sqlite" in str(engine.url) else "postgresql"
    return {
        "status": "ok",
        "database_type": db_type
    }
