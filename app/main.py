import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base, SessionLocal
from app.routers import listings
from seed import seed_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan: Server ishga tushganda va to'xtaganda bajariladigan amallar.
    1. Barcha jadvallarni yaratadi (Base.metadata.create_all).
    2. Agar baza bo'sh bo'lsa, seed.py orqali namunaviy ma'lumotlarni yuklaydi.
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
    title="Listing API - Slug Architecture",
    description=(
        "FastAPI + SQLAlchemy 2.0 + Pydantic v2 asosida ishlab chiqilgan Listing API.\n\n"
        "Asosiy xususiyatlari:\n"
        "- SEO-friendly unikal **Slug Architecture**\n"
        "- Pagination va filtratsiya (kategoriya, status, qidiruv)\n"
        "- Render.com va PostgreSQL ga to'liq moslashgan\n"
        "- Statik fayllar (/files) qo'llab-quvvatlovi"
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. CORS Middleware sozlamasi (Frontend bemalol ulana olishi uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Productionda xohishga ko'ra aniq domainlar kiritilishi mumkin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Statik fayllarni /files/ yo'nalishiga ulash
FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "files")
os.makedirs(FILES_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=FILES_DIR), name="files")

# 3. Routerlarni ulash
app.include_router(listings.router)

# 4. Asosiy va sog'liqni tekshirish (Health check) endpointlari
@app.get("/", tags=["Root"])
def root():
    return {
        "name": "Listing API - Slug Architecture",
        "status": "online",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "list_and_create": "/api/v1/listings",
            "detail_and_update": "/api/v1/listings/{slug}",
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
