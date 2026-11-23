# Soff Backend - Digital Marketplace API 🚀

FastAPI, SQLAlchemy 2.0 va Pydantic v2 asosida yaratilgan zamonaviy, tezkor va SEO-friendly raqamli mahsulotlar marketplace backend API loyihasi.

## 🌟 Asosiy Imkoniyatlar
- **Iyerarxik Kategoriya Tizimi**: 6 ta ota kategoriya va ularga tegishli sub-kategoriyalar iyerarxiyasi, listinglar soni hisobi.
- **Slug Architecture**: Har bir kategoriya va e'lon inson tushunadigan, SEO-mos unikal `slug` orqali ochiladi.
- **O'zbek tiliga moslashtirilgan Slugify**: O'zbek alifbosi (oʻ, gʻ, sh, ch va h.k.) va maxsus belgilar xatosiz lotin yozuviga transliteratsiya qilinadi.
- **Ko'p rasmli galereya (ListingImage) va Fayl yuklash**: Mahsulotlarga bir nechta rasm biriktirish va `/api/v1/upload/image` orqali rasmlarni yuklash.
- **SQLAlchemy 2.0**: Zamonaviy `Mapped` va `mapped_column` sintaksisi, SQLite va PostgreSQL (Render.com) bilan to'liq mos keladi.
- **Pydantic v2**: Yuqori tezlikdagi validation va `model_config = ConfigDict(from_attributes=True)`.
- **Avtomatik Idempotent Seed**: Server birinchi marta ishga tushganda 6 ta ota kategoriya, 24 ta sub-kategoriya va 120 ta sifatli mahsulot bazaga avtomatik yuklanadi.
- **Views Counter**: Mahsulot tafsilotlari sahifasi har safar ochilganda `views_count` avtomatik oshiriladi.
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
Server ishga tushishi bilan jadvallar avtomatik yaratiladi va namunaviy ma'lumotlar yuklanadi.

---

## 📚 API Hujjatlari (Swagger / OpenAPI)
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📡 Asosiy API Endpointlari

### 📂 Kategoriyalar (`/api/v1/categories`)
| Metod | Yo'l | Tavsif |
|---|---|---|
| `GET` | `/api/v1/categories` | 6 ta ota kategoriya, ularning sub-kategoriyalari va mahsulotlar soni |
| `GET` | `/api/v1/categories/{slug}` | Tanlangan kategoriya haqida to'liq ma'lumot va sub-kategoriyalari |
| `GET` | `/api/v1/categories/{slug}/subcategories` | Faqat berilgan ota kategoriyaning sub-kategoriyalari |

### 🛍 Mahsulotlar / Listinglar (`/api/v1/listings`)
| Metod | Yo'l | Tavsif |
|---|---|---|
| `GET` | `/api/v1/listings` | Mahsulotlar ro'yxati (filter, search, pagination, `category_slug`, `subcategory_slug`) |
| `POST` | `/api/v1/listings` | Yangi mahsulot yaratish (avtomatik unikal slug va kategoriya tekshiruvi) |
| `GET` | `/api/v1/listings/{slug}` | Mahsulot Detail sahifasi (views_count +1, to'liq ma'lumotlar, galereya rasmlari) |
| `PATCH` | `/api/v1/listings/{slug}` | Mahsulotni qisman yangilash (title o'zgarsa slug avtomatik yangilanadi) |
| `DELETE` | `/api/v1/listings/{slug}` | Mahsulotni bazadan o'chirish |
| `POST` | `/api/v1/listings/{slug}/images` | Mahsulotga bir yoki bir nechta rasm yuklab biriktirish |

### 🖼 Fayllar va Media (`/api/v1/upload`)
| Metod | Yo'l | Tavsif |
|---|---|---|
| `POST` | `/api/v1/upload/image` | Rasm yuklash (`multipart/form-data`) va URL olish |
| `GET` | `/files/{filename}` | Statik rasm va fayllarni yuklab olish/ko'rish |

---

## ☁️ Render.com ga Deploy qilish

1. Repozitoriyni GitHub'ga yuklang.
2. [Render.com](https://render.com) ga kiring va **New +** -> **Blueprint** ni tanlang.
3. Repozitoriyangizni ulang. Render avtomatik ravishda `render.yaml` faylini o'qiydi va deploy jarayonini boshlaydi.
4. Swagger hujjati: `https://<app-name>.onrender.com/docs`
