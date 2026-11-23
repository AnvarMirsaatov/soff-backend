# Soff Backend - Digital Marketplace API 🚀

FastAPI, SQLAlchemy 2.0 va Pydantic v2 asosida yaratilgan zamonaviy, tezkor va SEO-friendly raqamli mahsulotlar marketplace backend API loyihasi.

## 🌟 Asosiy Imkoniyatlar
- **3 Darajali Kategoriya Iyerarxiyasi**:
  - **1-daraja (Ota kategoriya)**: 6 ta asosiy yo'nalish (*Ilmiy ishlar, Dizayn, Web dasturlash, 3D design, AI generation, Shablonlar*).
  - **2-daraja (Ichki kategoriya)**: Har bir ota kategoriyada aynan 10 tadan mos ichki kategoriya (jami 60 ta).
  - **3-daraja (Sub-kategoriya)**: Har bir ichki kategoriyada 2 tadan aniq sub-kategoriya (jami 120 ta).
- **Rekursiv Slug Bo'yicha Cardlarni Olish**: Ota, ichki yoki sub-kategoriya `slug`i yuborilganda tegishli barcha cardlar (mahsulotlar) avtomatik iyerarxiya bo'yicha yig'ib qaytariladi.
- **Slug Architecture**: Har bir kategoriya va e'lon inson tushunadigan, SEO-mos unikal `slug` orqali ochiladi.
- **O'zbek tiliga moslashtirilgan Slugify**: O'zbek alifbosi (oʻ, gʻ, sh, ch va h.k.) va maxsus belgilar xatosiz lotin yozuviga transliteratsiya qilinadi.
- **Ko'p rasmli galereya (ListingImage) va Fayl yuklash**: Mahsulotlarga bir nechta rasm biriktirish va `/api/v1/upload/image` orqali rasmlarni yuklash.
- **SQLAlchemy 2.0**: Zamonaviy `Mapped` va `mapped_column` sintaksisi, SQLite va PostgreSQL (Render.com) bilan to'liq mos keladi.
- **Pydantic v2**: Yuqori tezlikdagi validation va `model_config = ConfigDict(from_attributes=True)`.
- **Avtomatik Idempotent Seed**: 6 ta ota, 60 ta ichki, 120 ta sub-kategoriya va 120 ta to'liq o'zbek tilidagi sifatli mahsulot avtomatik yuklanadi.
- **Views Counter**: Mahsulot tafsilotlari sahifasi har safar ochilganda `views_count` avtomatik +1 ga oshiriladi.
- **CORS va StaticFiles**: Frontend bilan to'liq integratsiya va `/files/` orqali statik fayllarni tarqatish.
- **Render.com Blueprint**: `render.yaml` orqali bir tugma bilan serverga deploy qilish.

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
Server ishga tushishi bilan jadvallar avtomatik yaratiladi va 3 darajali namunaviy ma'lumotlar yuklanadi.

---

## 📚 API Hujjatlari (Swagger / OpenAPI)
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📡 Asosiy API Endpointlari

### 📂 Kategoriyalar (`/api/v1/categories`)
| Metod | Yo'l | Tavsif |
|---|---|---|
| `GET` | `/api/v1/categories` | 6 ta ota kategoriya ro'yxati (`include_children=true` berilsa to'liq 3 darajali daraxt qaytadi) |
| `GET` | `/api/v1/categories/{slug}` | Kategoriya ma'lumotlari va uning ichidagi bolalari (`children`) |
| `GET` | `/api/v1/categories/{slug}/subcategories` | Berilgan kategoriyaning quyi bolalari |
| `GET` | `/api/v1/categories/{slug}/listings` | Shu kategoriyaga (va uning barcha quyi bolalariga) tegishli cardlar |

### 🛍 Mahsulotlar / Listinglar (`/api/v1/listings`)
| Metod | Yo'l | Tavsif |
|---|---|---|
| `GET` | `/api/v1/listings` | Mahsulotlar ro'yxati (rekursiv `category_slug`, filter, search, pagination) |
| `POST` | `/api/v1/listings` | Yangi mahsulot yaratish (avtomatik unikal slug va kategoriya tekshiruvi) |
| `GET` | `/api/v1/listings/{slug}` | Mahsulot Detail sahifasi (views_count +1, to'liq iyerarxiya, galereya rasmlari) |
| `PATCH` | `/api/v1/listings/{slug}` | Mahsulotni qisman yangilash |
| `DELETE` | `/api/v1/listings/{slug}` | Mahsulotni bazadan o'chirish |
| `POST` | `/api/v1/listings/{slug}/images` | Mahsulotga bir yoki bir nechta rasm biriktirish |

### 🖼 Fayllar va Media (`/api/v1/upload`)
| Metod | Yo'l | Tavsif |
|---|---|---|
| `POST` | `/api/v1/upload/image` | Rasm yuklash (`multipart/form-data`) va URL olish |
| `GET` | `/files/{filename}` | Statik rasm va fayllarni yuklab olish/ko'rish |
