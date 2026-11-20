# Listing API - Slug Architecture 🚀

FastAPI, SQLAlchemy 2.0 va Pydantic v2 asosida yaratilgan zamonaviy, tezkor va SEO-friendly listing boshqaruv backend API loyihasi.

## 🌟 Imkoniyatlar
- **Slug Architecture**: Har bir e'lon (listing) unikal, inson tushunadigan va SEO-mos `slug` orqali ochiladi (masalan: `/api/v1/listings/macbook-pro-16-m3-max`).
- **SQLAlchemy 2.0**: Zamonaviy `Mapped` va `mapped_column` sintaksisi, SQLite va PostgreSQL (Render.com) bilan to'liq mos keladi.
- **Pydantic v2**: Yuqori tezlikdagi validation va `model_config = ConfigDict(from_attributes=True)`.
- **Avtomatik Seed**: Server birinchi marta ishga tushganda baza bo'sh bo'lsa, namunaviy ma'lumotlar avtomatik yuklanadi.
- **CORS va StaticFiles**: Frontend bilan to'liq integratsiya va `/files/` orqali statik fayllarni tarqatish.
- **Render.com Blueprint**: `render.yaml` orqali bir tugma bilan tekin serverga deploy qilish.

---

## 🛠 Mahalliy muhitda ishga tushirish (Local Development)

### 1. Virtual muhit yaratish va faollashtirish:
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# yoki Windows da: .venv\Scripts\activate
```

### 2. Kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 3. Serverni ishga tushirish:
```bash
uvicorn app.main:app --reload --port 8000
```
Server ishga tushishi bilan jadvallar avtomatik yaratiladi va namunaviy ma'lumotlar yuklanadi.

---

## 📚 API Hujjatlari (Swagger / OpenAPI)
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📡 API Endpointlari

| Metod | Yo'l | Tavsif |
|---|---|---|
| `GET` | `/` | API statusi va asosiy ma'lumotlar |
| `GET` | `/health` | Server va DB holati (Health check) |
| `GET` | `/api/v1/listings` | Listinglar ro'yxati (filter & pagination) |
| `POST` | `/api/v1/listings` | Yangi listing yaratish (avtomatik unikal slug) |
| `GET` | `/api/v1/listings/{slug}` | Slug bo'yicha bitta listingni olish |
| `PATCH` | `/api/v1/listings/{slug}` | Slug bo'yicha listingni yangilash |
| `GET` | `/files/{filename}` | Statik fayllarni ko'rish |

---

## ☁️ Render.com ga Deploy qilish

1. Loyihani GitHub'ga yuklang.
2. [Render.com](https://render.com) ga kiring va **New +** -> **Blueprint** ni tanlang.
3. GitHub repozitoriyangizni ulang. Render avtomatik ravishda `render.yaml` faylini aniqlaydi va deploy jarayonini boshlaydi.
4. Deploy tugagach, sizga `https://<app-name>.onrender.com` manzilidagi jonli havola beriladi.
5. Swagger hujjati: `https://<app-name>.onrender.com/docs`
