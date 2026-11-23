"""
Soff Backend - 3-Darajali Iyerarxik Seed Skripti
6 ta ota kategoriya, 60 ta ichki kategoriya, 120 ta sub-kategoriya va
har bir sub-kategoriyada kamida 1 tadan (jami 120 ta) real, sifatli mahsulot.

Ishga tushirish: python seed.py
"""

from datetime import datetime, timezone
from app.database import SessionLocal, Base, engine
from app.models import Category, Listing, ListingImage
from app.utils import custom_slugify

# 6 ta ota kategoriya -> har birida 10 ta ichki kategoriya -> har birida 2 ta sub-kategoriya -> mahsulot
CATEGORIES_TREE = [
    {
        "name": "Ilmiy ishlar",
        "slug": "ilmiy-ishlar",
        "description": "Talabalar, magistrlar va tadqiqotchilar uchun ilmiy ishlar, referatlar va dissertatsiyalar",
        "icon": "academic-cap",
        "inner_categories": [
            {
                "name": "Iqtisodiyot va moliya",
                "slug": "iqtisodiyot-va-moliya",
                "description": "Bank ishi, moliya bozori, soliqlar va investitsiyalar tahlili",
                "icon": "banknotes",
                "subcategories": [
                    {
                        "name": "Kurs ishlari",
                        "slug": "iqtisodiyot-kurs-ishlari",
                        "product": {
                            "title": "Tijorat banklarida kredit risklarini boshqarish va minimallashtirish",
                            "short_description": "Tijorat banklarida kredit portfelini tahlil qilish va muammoli kreditlarni kamaytirish usullari.",
                            "description": "Ushbu ilmiy kurs ishi O'zbekiston bank tizimi misolida kredit risklarini baholash va boshqarish metodlarini o'rganadi. Barcha hisob-kitoblar, statistik jadvallar va manbalar ro'yxati to'liq kiritilgan.",
                            "price": 15.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Diplom ishlari",
                        "slug": "iqtisodiyot-diplom-ishlari",
                        "product": {
                            "title": "O'zbekistonda raqamli iqtisodiyot va bank xizmatlarini modernizatsiya qilish",
                            "short_description": "Fintech ilovalari va onlayn to'lov tizimlarining iqtisodiyotdagi samaradorligi.",
                            "description": "Bitiruv malakaviy ishi: Tijorat banklarida raqamli transformatsiya jarayonlari, masofaviy xizmat ko'rsatish va xalqaro tajriba tahlili. Taqdimot va ilovalar mavjud.",
                            "price": 45.00,
                            "file_format": "DOCX, PDF, PPTX",
                            "image_url": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    }
                ]
            },
            {
                "name": "Axborot texnologiyalari va dasturlash",
                "slug": "axborot-texnologiyalari-va-dasturlash",
                "description": "Dasturiy ta'minot, kiberxavfsizlik, tarmoqlar va sun'iy intellekt",
                "icon": "cpu-chip",
                "subcategories": [
                    {
                        "name": "Bitiruv malakaviy ishlari",
                        "slug": "it-bitiruv-malakaviy-ishlari",
                        "product": {
                            "title": "Mikroservis arxitekturasi asosida fintech to'lov tizimini ishlab chiqish",
                            "short_description": "Docker, Kubernetes va Kafka yordamida yuqori yuklamali to'lov tizimini loyihalash.",
                            "description": "Amaliy dasturiy ta'minot BMI: Tranzaksiyalarni parallel qayta ishlash, ma'lumotlar xavfsizligi va ACID talablari to'liq yoritilgan. Dastur kodi ilova qilingan.",
                            "price": 55.00,
                            "file_format": "DOCX, PDF, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Ilmiy maqolalar",
                        "slug": "it-ilmiy-maqolalar",
                        "product": {
                            "title": "Katta hajmli ma'lumotlarni qayta ishlashda taqsimlangan tizimlar samaradorligi",
                            "short_description": "Apache Spark va Hadoop klasterlarida Big Data oqimlarini tahlil qilish algoritmlari.",
                            "description": "Scopus va OAK jurnallari talablariga mos ilmiy maqola. Klasterlash algoritmlari va taqsimlangan kesh mexanizmlari qiyosiy tahlil qilingan.",
                            "price": 20.00,
                            "file_format": "PDF, DOCX",
                            "image_url": "https://images.unsplash.com/photo-1507842229451-79774619b06a?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Pedagogika va psixologiya",
                "slug": "pedagogika-va-psixologiya",
                "description": "Ta'lim metodikasi, yosh psixologiyasi va interfaol o'qitish",
                "icon": "user-group",
                "subcategories": [
                    {
                        "name": "Metodik qo'llanmalar",
                        "slug": "pedagogika-metodik-qollanmalar",
                        "product": {
                            "title": "Oliy ta'limda interfaol ta'lim texnologiyalari va keys-stadilar to'plami",
                            "short_description": "Darslarda talabalar faolligini oshirish bo'yicha amaliy mashg'ulotlar qo'llanmasi.",
                            "description": "Zamonaviy pedagogik metodlar: Blended learning, muammoli vaziyatlar va guruhlarda ishlash metodikasi haqida to'liq qo'llanma.",
                            "price": 14.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Referat va taqdimotlar",
                        "slug": "pedagogika-referat-va-taqdimotlar",
                        "product": {
                            "title": "Zamonaviy shaxs psixologiyasida stress va hissiy charchoqni yengish",
                            "short_description": "Emotsional barqarorlik, kognitiv xulq-atvor terapiyasi asoslari va amaliy tavsiyalar.",
                            "description": "20 slayddan iborat chiroyli animatsiyali taqdimot va 12 betlik referat matni.",
                            "price": 10.00,
                            "file_format": "PPTX, DOCX",
                            "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Huquqshunoslik va yurisprudensiya",
                "slug": "huquqshunoslik-va-yurisprudensiya",
                "description": "Fuqarolik, jinoiy, xalqaro huquq va sud amaliyoti",
                "icon": "scale",
                "subcategories": [
                    {
                        "name": "Sud amaliyoti tahlili",
                        "slug": "huquq-sud-amaliyoti-tahlili",
                        "product": {
                            "title": "Fuqarolik ishlarida shartnoma majburiyatlarini buzish oqibatlari",
                            "short_description": "Majburiyatlarni bajarmaslik tufayli yetkazilgan zararni undirish sud amaliyoti tahlili.",
                            "description": "O'zbekiston Respublikasi Fuqarolik kodeksi va Oliy sud plenum qarorlari asosida tayyorlangan tahliliy hujjat.",
                            "price": 22.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Qonunchilik dissertatsiyalari",
                        "slug": "huquq-dissertatsiyalari",
                        "product": {
                            "title": "Xalqaro tijorat arbitrajida nizolarni hal qilish mexanizmlari",
                            "short_description": "Investitsiyaviy va savdo nizolarini xalqaro arbitrajda ko'rib chiqish huquqiy asoslari.",
                            "description": "Magistrlik dissertatsiyasi: Nyu-York konvensiyasi qoidalari va xorijiy arbitraj qarorlarini tan olish hamda ijroga qaratish masalalari.",
                            "price": 90.00,
                            "file_format": "PDF, DOCX",
                            "image_url": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Tibbiyot va farmatsevtika",
                "slug": "tibbiyot-va-farmatsevtika",
                "description": "Klinik diagnostika, anatomiya, farmakologiya va terapiya",
                "icon": "heart",
                "subcategories": [
                    {
                        "name": "Klinik tadqiqotlar",
                        "slug": "tibbiyot-klinik-tadqiqotlar",
                        "product": {
                            "title": "Yurak-qon tomir kasalliklarini erta aniqlashda biofizik parametrlar tahlili",
                            "short_description": "Arterial gipertenziya va aterosklerozni erta bosqichda aniqlash laboratoriya usullari.",
                            "description": "Tibbiyot oliygohlari talabalari va magistrlari uchun klinik tajribalar, bemorlar tahlillari va diagrammalar jamlangan ilmiy ish.",
                            "price": 30.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Farmatsevtik ishlanmalar",
                        "slug": "tibbiyot-farmatsevtik-ishlanmalar",
                        "product": {
                            "title": "Mahalliy dorivor o'simliklar asosida fitopreparatlar texnologiyasi",
                            "short_description": "O'zbekistonda o'suvchi giyohlardan ekstraksiya olish va dori shakllarini yaratish.",
                            "description": "Dorivor giyohlardan biologik faol moddalarni ajratish, standartlash va sifat nazorati metodlari.",
                            "price": 35.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Filologiya va tilshunoslik",
                "slug": "filologiya-va-tilshunoslik",
                "description": "O'zbek, ingliz va jahon tillari grammatikasi, adabiyotshunoslik",
                "icon": "book-open",
                "subcategories": [
                    {
                        "name": "Qiyosiy tilshunoslik ishlari",
                        "slug": "filologiya-qiyosiy-tilshunoslik",
                        "product": {
                            "title": "Ingliz va o'zbek tillarida frazeologik birliklarning qiyosiy tipologiyasi",
                            "short_description": "Ikki tildagi maqollar, iboralar va idiomalarning semantik-uslubiy o'ziga xosligi.",
                            "description": "Tilshunoslik yo'nalishidagi kurs ishi: Madaniyatlararo muloqotda frazeologizmlarning roli va tarjima muammolari to'liq o'rganilgan.",
                            "price": 16.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Adabiyotshunoslik referatlari",
                        "slug": "filologiya-adabiyotshunoslik",
                        "product": {
                            "title": "Jadid adabiyotida ma'rifatparvarlik g'oyalari va milliy o'zlik",
                            "short_description": "Fitrat, Cho'lpon va Abdulla Qodiriy asarlarida ozodlik va ma'rifat mavzulari.",
                            "description": "20-asr boshlari o'zbek adabiyotidagi islohotlar va milliy uyg'onish davri asarlari tahlili.",
                            "price": 8.00,
                            "file_format": "DOCX, PPTX",
                            "image_url": "https://images.unsplash.com/photo-1532012164546-f432f2e37972?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Tarix va falsafa",
                "slug": "tarix-va-falsafa",
                "description": "O'zbekiston va jahon tarixi, Sharq mutafakkirlari falsafasi",
                "icon": "globe-alt",
                "subcategories": [
                    {
                        "name": "O'zbekiston tarixi tadqiqotlari",
                        "slug": "tarix-tadqiqotlari",
                        "product": {
                            "title": "Buyuk Ipak yo'lida So'g'd savdo koloniyalarining ijtimoiy-madaniy o'rni",
                            "short_description": "Milodiy V-VIII asrlarda Markaziy Osiyo savdo yo'llari va xalqaro aloqalar tarixi.",
                            "description": "Arxeologik topilmalar, yozma manbalar va tangalar asosida So'g'd sivilizatsiyasi ta'siri chuqur tahlil qilingan.",
                            "price": 18.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Sharq falsafasi ocherklari",
                        "slug": "sharq-falsafasi",
                        "product": {
                            "title": "Al-Forobiy va Ibn Sinoning fozil jamiyat haqidagi ta'limoti",
                            "short_description": "Sharq Renessansi allomalarining davlat boshqaruvi va axloq falsafasi.",
                            "description": "Falsafa fani bo'yicha ilmiy referat: Fozil insonlar shahri konsepsiyasi va zamonaviy jamiyat taraqqiyoti.",
                            "price": 12.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Muhandislik va arxitektura",
                "slug": "muhandislik-va-arxitektura",
                "description": "Qurilish texnologiyalari, mexanika va konstruksiyalar hisobi",
                "icon": "wrench-screwdriver",
                "subcategories": [
                    {
                        "name": "Konstruktorlik hisob-kitoblari",
                        "slug": "muhandislik-konstruktorlik-hisoblari",
                        "product": {
                            "title": "Ko'p qavatli monolit binolarning seysmik barqarorligini hisoblash",
                            "short_description": "9 ballik seysmik hududlar uchun monolit temir-beton karkaslarni hisoblash metodikasi.",
                            "description": "LIRA-SAPR dasturi natijalari, yuklamalar jadvali va chizmalarni o'z ichiga olgan hisob-kitob loyihasi.",
                            "price": 50.00,
                            "file_format": "DWG, PDF",
                            "image_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Qurilish loyihalari",
                        "slug": "muhandislik-qurilish-loyihalari",
                        "product": {
                            "title": "Zamonaviy shaharsozlikda ekologik qulay uy-joy komplekslari loyihasi",
                            "short_description": "Energiya tejamkor materiallar va quyosh panellari integratsiyalashgan arxitektura loyihasi.",
                            "description": "Arxitektura kafedrasi bitiruv loyihasi: Bosh reja, qavatlar plani, fasadlar va 3D vizual tasvirlar to'liq taqdim etiladi.",
                            "price": 60.00,
                            "file_format": "DWG, DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Tabiiy fanlar (Fizika, Kimyo, Biologiya)",
                "slug": "tabiiy-fanlar",
                "description": "Ekologiya, organik kimyo, kvant fizikasi va genetika",
                "icon": "beaker",
                "subcategories": [
                    {
                        "name": "Laboratoriya hisobotlari",
                        "slug": "tabiiy-fanlar-laboratoriya",
                        "product": {
                            "title": "Organik kimyoda polimer moddalarning spektral tahlili laboratoriya ishlari",
                            "short_description": "IQ-spektroskopiya va xromatografiya yordamida polimerlar tarkibini aniqlash.",
                            "description": "Kimyo fakulteti talabalari uchun 10 ta to'liq tayyorlangan laboratoriya ishi bayonnomasi.",
                            "price": 12.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Ekologik tadqiqotlar",
                        "slug": "tabiiy-fanlar-ekologiya",
                        "product": {
                            "title": "Orolbo'yi mintaqasida tuproq sho'rlanishini kamaytirish choralari",
                            "short_description": "Sho'rga chidamli galofit o'simliklarni ekish orqali yer unumdorligini tiklash.",
                            "description": "Ekologiya yo'nalishidagi ilmiy ish: Tuproq namunalari tahlili, melioratsiya tadbirlari va xaritalar kiritilgan.",
                            "price": 25.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Menejment va marketing",
                "slug": "menejment-va-marketing",
                "description": "Biznes boshqaruvi, bozor tahlili, strategik rejalashtirish",
                "icon": "chart-bar",
                "subcategories": [
                    {
                        "name": "Biznes-rejalar",
                        "slug": "menejment-biznes-rejalar",
                        "product": {
                            "title": "Issiqxona xo'jaligini tashkil etish bo'yicha to'liq investitsion biznes-reja",
                            "short_description": "Gidroponika usulida pomidor va bodring yetishtirish loyihasining moliyaviy modeli.",
                            "description": "Bankdan kredit olish uchun tayyorlangan professional biznes-reja. Xarajatlar, daromadlar va o'zini qoplash muddati Excel jadvallari bilan keltirilgan.",
                            "price": 40.00,
                            "file_format": "DOCX, XLSX",
                            "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Bozor tahlili ishlari",
                        "slug": "menejment-bozor-tahlili",
                        "product": {
                            "title": "O'zbekistonda kuryerlik xizmatlari bozorining raqobatbardoshlik tahlili",
                            "short_description": "Yetkazib berish servislari: Express pochta va agregatorlar faoliyati marketing tahlili.",
                            "description": "SWOT, PESTEL va Porter besh kuch tahlillari asosida tayyorlangan marketing tadqiqot ishi.",
                            "price": 28.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            }
        ]
    },
    {
        "name": "Dizayn",
        "slug": "dizayn",
        "description": "Grafik dizayn, UI/UX, brending, SMM dizayn va poligrafiya shablonlari",
        "icon": "paint-brush",
        "inner_categories": [
            {
                "name": "UI/UX dizayn",
                "slug": "ui-ux-dizayn",
                "description": "Mobil va veb ilovalar uchun Figma interfeyslari",
                "icon": "device-phone-mobile",
                "subcategories": [
                    {
                        "name": "Mobil ilovalar interfeysi",
                        "slug": "ui-ux-mobil-ilovalar",
                        "product": {
                            "title": "Fintech va neobank mobil ilovasi uchun 120+ ekranli Figma UI Kit",
                            "short_description": "To'liq auto-layout, Dark va Light mavzular, kartalar va to'lovlar oqimi.",
                            "description": "Bank va elektron hamyon ilovalari uchun tayyor komponentlar tizimi. Mikro-interaksiyalar va onboarding to'liq sozlangan.",
                            "price": 45.00,
                            "file_format": "Figma",
                            "image_url": "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Veb-saytlar va CRM interfeyslari",
                        "slug": "ui-ux-veb-crm",
                        "product": {
                            "title": "SaaS loyihalar va korxona analitikasi uchun keng qamrovli Dashboard UI",
                            "short_description": "Murakkab metrikalar, daromad jadvallari va foydalanuvchilar boshqaruvi paneli.",
                            "description": "200 dan ortiq moslashuvchan komponentlarga ega Figma dizayn tizimi. Dasturchilar uchun qulay tokens va uslublar mavjud.",
                            "price": 50.00,
                            "file_format": "Figma",
                            "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    }
                ]
            },
            {
                "name": "Grafik dizayn va poligrafiya",
                "slug": "grafik-dizayn-va-poligrafiya",
                "description": "Bosma mahsulotlar, menyular, flayerlar va broshyuralar",
                "icon": "photo",
                "subcategories": [
                    {
                        "name": "Flayer va bukletlar",
                        "slug": "grafik-flayer-va-bukletlar",
                        "product": {
                            "title": "Biznes konferensiya va forumlar uchun korporativ flayer va broshyura maketi",
                            "short_description": "A4 va Evro-buklet formatlarida, CMYK bosmaga tayyor Photoshop va Illustrator fayllari.",
                            "description": "Qatlamlari tartiblangan, rang va shriftlarni osongina almashtirish mumkin bo'lgan poligrafiya andozasi.",
                            "price": 20.00,
                            "file_format": "PSD, AI",
                            "image_url": "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Restoran menyulari",
                        "slug": "grafik-restoran-menyulari",
                        "product": {
                            "title": "Premium restoran va lounge-bar uchun ko'p sahifali estetik menyu dizayni",
                            "short_description": "Elegent tipografika, taomlar suratlari va narxlar bloki bilan to'ldirilgan maket.",
                            "description": "InDesign va Photoshop dasturlarida tayyorlangan, CMYK 300 DPI bosma standarti menyu shabloni.",
                            "price": 25.00,
                            "file_format": "PSD, INDD, PDF",
                            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Logotip va brending",
                "slug": "logotip-va-brending",
                "description": "Korxona brendbuki, firmenniy stil va vektorli logotiplar",
                "icon": "sparkles",
                "subcategories": [
                    {
                        "name": "Korporativ brendbuklar",
                        "slug": "brending-brendbuklar",
                        "product": {
                            "title": "Logistika va transport kompaniyasi uchun to'liq firmenniy stil va brendbuk",
                            "short_description": "Logotip, ranglar palitrasi, ish yuritish blankalari, vizitkalar va avtomashinalar brendingi.",
                            "description": "30 sahifalik keng qamrovli Brand Guidelines hujjati. Barcha vektor elementlar ilova qilingan.",
                            "price": 60.00,
                            "file_format": "AI, PDF, PSD",
                            "image_url": "https://images.unsplash.com/photo-1600132806370-bf17e65e942f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Minimalist logotiplar",
                        "slug": "brending-minimalist-logotiplar",
                        "product": {
                            "title": "Zamonaviy IT startaplar uchun 20 ta unikal minimalist vektor logotip",
                            "short_description": "Geometrik shakllar, neytral ranglar va zamonaviy tipografikaga ega logotiplar.",
                            "description": "AI, EPS va SVG formatlarida yaratilgan, o'lchamini istalgancha o'zgartirish mumkin bo'lgan vektor to'plam.",
                            "price": 30.00,
                            "file_format": "AI, SVG, PNG",
                            "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "SMM dizayn",
                "slug": "smm-dizayn",
                "description": "Instagram, Telegram va TikTok uchun postlar va karusellar",
                "icon": "share",
                "subcategories": [
                    {
                        "name": "Instagram post va karusellar",
                        "slug": "smm-instagram-postlar",
                        "product": {
                            "title": "E-commerce va do'konlar uchun 60 ta trenddagi Instagram post va karusel",
                            "short_description": "Canva va Figma formatlarida, savdoni oshirish va aksiyalar e'loni uchun mo'ljallangan.",
                            "description": "Rasmlar va matnlarni 1 daqiqada almashtirib tayyor post chiqarish mumkin bo'lgan SMM shablonlar paketi.",
                            "price": 22.00,
                            "file_format": "Canva, Figma",
                            "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Telegram kanal dizaynlari",
                        "slug": "smm-telegram-kanal-dizayni",
                        "product": {
                            "title": "Yangiliklar va biznes kanallari uchun infografika, avatar va post shablonlari",
                            "short_description": "Telegram kanalingizni professional ko'rinishga keltiruvchi grafik elementlar to'plami.",
                            "description": "Avatar, banner va 20 ta turli rubrikalar uchun maxsus moslangan PSD va PNG maketlar.",
                            "price": 18.00,
                            "file_format": "PSD, PNG",
                            "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Mahsulot qadoqlash (Packaging)",
                "slug": "mahsulot-qadoqlash",
                "description": "Quti, etiketka, sumka va idishlar qadoq dizaynlari",
                "icon": "cube",
                "subcategories": [
                    {
                        "name": "Quti va paketlar dizayni",
                        "slug": "qadoq-quti-va-paketlar",
                        "product": {
                            "title": "Organik choy va qahva qadoqlari uchun dray-kat (dieline) dizayni",
                            "short_description": "To'liq kesish chiziqlari (Dielines) va 3D vizual mockup fayllari kiritilgan.",
                            "description": "Illustrator formatida ishlab chiqarish fabrikasiga to'g'ridan-to'g'ri yuborishga tayyor qadoq andozasi.",
                            "price": 35.00,
                            "file_format": "AI, EPS, PSD",
                            "image_url": "https://images.unsplash.com/photo-1547949003-9792a18a2601?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Mahsulot etiketkalari",
                        "slug": "qadoq-etiketkalar",
                        "product": {
                            "title": "Tabiiy kosmetika va shampun idishlari uchun estetik etiketkalar to'plami",
                            "short_description": "Butilkalar va kremlar uchun minimalist, oltin va kumush shtampga mos dizayn.",
                            "description": "Kosmetik vositalar ishlab chiqaruvchilar uchun 10 ta tahrirlanadigan etiketka maketi.",
                            "price": 28.00,
                            "file_format": "AI, PSD",
                            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Illyustratsiya va vektor san'ati",
                "slug": "illyustratsiya-va-vektor-sanati",
                "description": "Kitob rasmlari, saytlar uchun qahramonlar va vektor art",
                "icon": "pencil",
                "subcategories": [
                    {
                        "name": "Vektorli illyustratsiyalar",
                        "slug": "vektor-illyustratsiyalar",
                        "product": {
                            "title": "Veb-sayt qahramonlari va Empty state holatlari uchun 30 ta vektor art",
                            "short_description": "Zamonaviy IT, moliya va jamoaviy ish mavzusidagi yassi (flat) illyustratsiyalar.",
                            "description": "Sayt va mobil ilovaning bo'sh sahifalari, 404 xatoliklari va yuklanish ekranlari uchun rasmlar.",
                            "price": 24.00,
                            "file_format": "SVG, AI, PNG",
                            "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Kitob va ertak rasmlari",
                        "slug": "ertak-rasmlari",
                        "product": {
                            "title": "Bolalar ertaklari uchun akvarel uslubidagi 15 ta jozibali illyustratsiya",
                            "short_description": "O'rmon jonzotlari va ertak qahramonlari aks ettirilgan iliq ranglardagi rasmlar.",
                            "description": "Bolalar kitoblari nashriyoti va jurnallar uchun yuqori aniqlikdagi san'at asarlari.",
                            "price": 32.00,
                            "file_format": "PSD, PNG",
                            "image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Tashqi reklama dizayni",
                "slug": "tashqi-reklama-dizayni",
                "description": "Bilbordlar, pilonlar, avtomobillar va do'kon peshtoqlari",
                "icon": "megaphone",
                "subcategories": [
                    {
                        "name": "Bilbord va bannerlar",
                        "slug": "tashqi-bilbord-va-bannerlar",
                        "product": {
                            "title": "Shahar bilbordlari va LED ekranlar uchun yorqin reklama bannerlari",
                            "short_description": "3x6 metrli bilbordlar va video ekranlar uchun ko'zni tortuvchi reklama shabloni.",
                            "description": "Uzoq masofadan yaxshi o'qiluvchi kontrast ranglar va katta shriftlar bilan ishlangan maket.",
                            "price": 25.00,
                            "file_format": "PSD, TIFF",
                            "image_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Avtotransport brendingi",
                        "slug": "avtotransport-brendingi",
                        "product": {
                            "title": "Kuryerlik furgonlari va yengil avtomobillarni to'liq brendlash maketi",
                            "short_description": "Avtomobilning barcha tomonlaridan o'lchamlari olingan 1:1 masshtabdagi dizayn.",
                            "description": "Plenka bosish va avtomobilga yopishtirish uchun tayyor vektorli chizmalar to'plami.",
                            "price": 30.00,
                            "file_format": "AI, EPS",
                            "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Shriftlar va tipografika",
                "slug": "shriftlar-va-tipografika",
                "description": "Mualliflik shriftlari, kirill-lotin harflari va kaligrafiya",
                "icon": "language",
                "subcategories": [
                    {
                        "name": "Kirill va lotin shriftlari",
                        "slug": "kirill-va-lotin-shriftlari",
                        "product": {
                            "title": "Zamonaviy geometrik sans-serif sarlavha shrifti (Bold, Regular, Light)",
                            "short_description": "O'zbek alifbosidagi oʻ va gʻ harflari to'liq qo'llab-quvvatlanadigan sarlavha shrifti.",
                            "description": "Veb va bosma materiallar uchun mukammal, toza geometrik proporsiyalarga ega yangi shrift oilasi.",
                            "price": 25.00,
                            "file_format": "OTF, TTF, WOFF2",
                            "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Xattotlik va kaligrafiya",
                        "slug": "xattotlik-va-kaligrafiya",
                        "product": {
                            "title": "Milliy sharqona naqshlar va arab yozuvidagi bayram tabriknomalari",
                            "short_description": "Ramazon va Hayit bayramlari uchun tilla rangli qo'lda chizilgan nafis kaligrafiya.",
                            "description": "Vektorli shakllar va yuqori aniqlikdagi shaffof fonli PNG fayllar.",
                            "price": 20.00,
                            "file_format": "AI, PNG, PSD",
                            "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Elektron tijorat (Marketplace) dizayni",
                "slug": "marketplace-dizayni",
                "description": "Uzum, Wildberries, Ozon tovar kartochkalari va bannerlari",
                "icon": "shopping-bag",
                "subcategories": [
                    {
                        "name": "Wildberries va Uzum kartochkalari",
                        "slug": "uzum-va-wb-kartochkalari",
                        "product": {
                            "title": "Uzum va Wildberries tovarlari uchun konversiyali 50 ta infografika shabloni",
                            "short_description": "Tovar afzalliklari, o'lchamlari va xususiyatlarini ko'rsatuvchi tayyor shablonlar.",
                            "description": "Marketplaceda sotuvlarni bir necha barobar oshirishga yordam beruvchi qulay Figma va PSD andozalari.",
                            "price": 22.00,
                            "file_format": "Figma, PSD",
                            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Banner va aksiyalar dizayni",
                        "slug": "marketplace-aksiyalar-dizayni",
                        "product": {
                            "title": "Mega-chegirmalar va mavsumiy aksiyalar uchun savdo bannerlari to'plami",
                            "short_description": "11.11, Yangi yil va Black Friday savdolari uchun e'lonlar maketi.",
                            "description": "Mijozlar diqqatini tortuvchi neon va yorqin ranglardagi 20 ta tayyor banner.",
                            "price": 18.00,
                            "file_format": "PSD, Canva",
                            "image_url": "https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Motion dizayn",
                "slug": "motion-dizayn",
                "description": "Animatsion logotiplar, After Effects promo roliklar",
                "icon": "film",
                "subcategories": [
                    {
                        "name": "Animatsiyalangan logotiplar",
                        "slug": "motion-animatsion-logotiplar",
                        "product": {
                            "title": "After Effects da logotipning 3D aylanuvchi kirish (Intro) animatsiyasi",
                            "short_description": "YouTube kanallar va videolar boshlanishi uchun yaltiroq metall va neon intro.",
                            "description": "Logotipingizni joylashtirsangiz kifoya — After Effects avtomatik ravishda 4K animatsiya render qiladi.",
                            "price": 30.00,
                            "file_format": "AEP, MP4",
                            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Qisqa promo roliklar",
                        "slug": "motion-qisqa-promo-roliklar",
                        "product": {
                            "title": "Mobil ilovalar va yangi mahsulotlar taqdimoti uchun 15 soniyalik promo rolik",
                            "short_description": "Instagram Stories va Reels uchun vertikal formatdagi dinamik promo shablon.",
                            "description": "Matnlar va skrinshotlarni tezkor almashtirish uchun sozlangan After Effects loyihasi.",
                            "price": 35.00,
                            "file_format": "After Effects, MP4",
                            "image_url": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            }
        ]
    },
    {
        "name": "Web dasturlash",
        "slug": "web-dasturlash",
        "description": "Veb-saytlar, internet-do'konlar, admin panellar, botlar va to'lov integratsiyalari",
        "icon": "code-bracket",
        "inner_categories": [
            {
                "name": "Landing page va bir sahifalik saytlar",
                "slug": "landing-page-saytlar",
                "description": "Konversiyasi yuqori mahsulot va xizmatlar taqdimoti sahifalari",
                "icon": "globe-alt",
                "subcategories": [
                    {
                        "name": "SaaS mahsulotlar landingi",
                        "slug": "landing-saas-mahsulotlar",
                        "product": {
                            "title": "Next.js 14, Tailwind CSS va Framer Motion asosidagi premium SaaS landing",
                            "short_description": "TypeScript, Dark mode, interaktiv narxlar kalkulyatori va to'liq SEO sozlangan.",
                            "description": "Dasturiy xizmatlar va startaplar uchun mukammal bir sahifalik sayt kodi. Har bir bo'lim alohida komponentlarga ajratilgan.",
                            "price": 45.00,
                            "file_format": "ZIP, Next.js, TS",
                            "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Xizmatlar va tadbirlar sayti",
                        "slug": "landing-xizmatlar-va-tadbirlar",
                        "product": {
                            "title": "Biznes forumlar va tadbirlar uchun ro'yxatdan o'tish bir sahifalik sayti",
                            "short_description": "Vaqt hisoblagich (Countdown), spikerlar ro'yxati va Telegram botga ulanuvchi forma.",
                            "description": "Tez yuklanuvchi sof HTML5, SCSS va JavaScript kodi. Barcha mobil ekranlarga to'liq moslashgan.",
                            "price": 30.00,
                            "file_format": "HTML, SCSS, JS",
                            "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Internet do'kon (E-commerce)",
                "slug": "internet-dokon-e-commerce",
                "description": "Onlayn savdo platformalari, savatcha va to'lov shlyuzlari",
                "icon": "shopping-cart",
                "subcategories": [
                    {
                        "name": "Kiyim va tovarlar do'koni",
                        "slug": "dokon-kiyim-va-tovarlar",
                        "product": {
                            "title": "Next.js, FastAPI va PostgreSQL da yaratilgan to'liq funksional onlayn do'kon",
                            "short_description": "Payme va Click to'lovlari, savatcha, buyurtmalar tarixi va admin paneli bilan.",
                            "description": "Monorepo arxitekturasi: Frontend Next.js 14, Backend FastAPI. Docker-compose orqali 1 daqiqada ishga tushadi.",
                            "price": 95.00,
                            "file_format": "ZIP, Docker, Python",
                            "image_url": "https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Buyurtma va to'lov tizimli do'kon",
                        "slug": "dokon-buyurtma-va-tolov",
                        "product": {
                            "title": "Click va Payme to'lovlari, savatcha va buyurtma boshqaruvi bilan do'kon",
                            "short_description": "React va Node.js Express da yozilgan tezkor internet-do'kon shabloni.",
                            "description": "Redux Toolkit orqali boshqariluvchi savatcha va to'lov webhooklari to'liq integratsiya qilingan.",
                            "price": 85.00,
                            "file_format": "React, Node.js, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Admin panellar va CRM",
                "slug": "admin-panellar-va-crm",
                "description": "Statistik panellar, foydalanuvchilar va buyurtmalar hisobi",
                "icon": "chart-pie",
                "subcategories": [
                    {
                        "name": "O'quv markazi CRM tizimi",
                        "slug": "crm-oquv-markazi",
                        "product": {
                            "title": "Talabalar hisobi, guruhlar jadvali va to'lovlar monitoringi CRM paneli",
                            "short_description": "Vue 3 va FastAPI asosidagi yengil, tez ishlovchi o'quv markazi platformasi.",
                            "description": "Davomat belgilash, oylik to'lovlar qarzdorligi va o'qituvchilar dars jadvallari modullari to'liq ishlaydi.",
                            "price": 75.00,
                            "file_format": "Vue 3, FastAPI, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Ombor va savdo hisobi paneli",
                        "slug": "crm-ombor-va-savdo",
                        "product": {
                            "title": "Kirim-chiqim, tovarlar qoldig'i va shtrix-kod integratsiyali admin tizim",
                            "short_description": "React va Node.js da yaratilgan chakana savdo va omborxona nazorati shabloni.",
                            "description": "Tovarlar qoldig'i kamayganda ogohlantirish, chek chiqarish va kunlik kassa hisoboti funksiyalari mavjud.",
                            "price": 70.00,
                            "file_format": "React, Node.js, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Telegram botlar",
                "slug": "telegram-botlar",
                "description": "Aiogram 3, asinxron botlar va Telegram Web Apps (TWA)",
                "icon": "chat-bubble-left-right",
                "subcategories": [
                    {
                        "name": "To'lovli internet do'kon botlari",
                        "slug": "bot-internet-dokon",
                        "product": {
                            "title": "Aiogram 3, Click va Payme to'lovlari bilan ishlovchi Telegram do'kon boti",
                            "short_description": "Katalog, savatcha, buyurtmani rasmiylashtirish va avtomatik to'lov tekshiruvi.",
                            "description": "Python 3.11 va Aiogram 3 asosidagi asinxron bot. SQLite va PostgreSQL bazalariga to'liq moslashgan.",
                            "price": 50.00,
                            "file_format": "Python, PostgreSQL, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Avtomatlashtirilgan xizmat botlari",
                        "slug": "bot-xizmat-avtomatlashtirish",
                        "product": {
                            "title": "Mijozlar arizasini qabul qilish va navbatga yozish uchun Telegram bot",
                            "short_description": "Go'zallik salonlari, stomatologiya va ustaxonalar uchun navbat olish boti.",
                            "description": "Bo'sh vaqtlarni taqvimdan tanlash va administratorga yangi arizalarni yetkazish mexanizmi.",
                            "price": 35.00,
                            "file_format": "Python, Aiogram, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Backend va API xizmatlari",
                "slug": "backend-va-api-xizmatlari",
                "description": "FastAPI, Django REST, Express va mikroservislar arxitekturasi",
                "icon": "server",
                "subcategories": [
                    {
                        "name": "FastAPI va Django REST loyihalari",
                        "slug": "backend-fastapi-django",
                        "product": {
                            "title": "JWT autentifikatsiya, rollar va ma'lumotlar keshiga ega tayyor FastAPI backend",
                            "short_description": "SQLAlchemy 2.0, Pydantic v2, Alembic migratsiyalari va Redis kesh integratsiyasi.",
                            "description": "Har qanday yangi loyiha uchun mustahkam poydevor: Swagger hujjati, xavfsizlik filtrlari va testlar kiritilgan.",
                            "price": 40.00,
                            "file_format": "Python, FastAPI, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Node.js va Express mikroxizmatlari",
                        "slug": "backend-nodejs-express",
                        "product": {
                            "title": "Dockerlashtirilgan RESTful mikroservislar arxitekturasi shabloni",
                            "short_description": "TypeScript, Express, Prisma ORM va RabbitMQ bilan voqealarga asoslangan xizmat.",
                            "description": "Yuqori yuklamalarga chidamli, modulli va kengayuvchan korporativ API andozasi.",
                            "price": 45.00,
                            "file_format": "Node.js, Express, TS",
                            "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Frontend shablonlar (React / Next.js)",
                "slug": "frontend-shablonlar-react-next",
                "description": "Next.js App Router, Vue 3, Shadcn UI va Tailwind komponentlari",
                "icon": "computer-desktop",
                "subcategories": [
                    {
                        "name": "Next.js 14 App Router shablonlari",
                        "slug": "frontend-nextjs-shablonlar",
                        "product": {
                            "title": "Shadcn UI, Dark mode va to'liq tipizatsiyalangan Next.js boshlang'ich qolipi",
                            "short_description": "Server Actions, Lucide ikonalar va zamonaviy UI komponentlar kutubxonasi.",
                            "description": "Dasturchilar vaqti tejash uchun yaratilgan, ishlab chiqarishga (Production) tayyor frontend shabloni.",
                            "price": 35.00,
                            "file_format": "TypeScript, Next.js, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Vue 3 va Vite komponentlari",
                        "slug": "frontend-vue-vite",
                        "product": {
                            "title": "Pinia va Tailwind CSS integratsiya qilingan Vue 3 komponentlar to'plami",
                            "short_description": "Modallar, jadvallar, dropdownlar va formalar uchun 40+ moslashuvchan komponent.",
                            "description": "Composition API uslubida yozilgan, engil va chaqqon ishlovchi Vue 3 shabloni.",
                            "price": 30.00,
                            "file_format": "Vue 3, Vite, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "WordPress va CMS tizimlari",
                "slug": "wordpress-va-cms-tizimlari",
                "description": "Elementor mavzulari, WooCommerce plaginlari va bloglar",
                "icon": "window",
                "subcategories": [
                    {
                        "name": "WordPress mavzulari va plaginlari",
                        "slug": "wordpress-mavzulari",
                        "product": {
                            "title": "Elementor uchun moslashgan, tez yuklanuvchi zamonaviy korporativ WP mavzusi",
                            "short_description": "Kod yozmasdan tahrirlash mumkin bo'lgan, mobil moslashuvchan WordPress mavzusi.",
                            "description": "Biznes va xizmatlar sayti uchun tayyor sahifalar va bog'lanish formalari mavjud.",
                            "price": 40.00,
                            "file_format": "PHP, WordPress, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Yangiliklar va blog portallari",
                        "slug": "wordpress-yangiliklar-portali",
                        "product": {
                            "title": "SEO uchun optimallashgan, reklama bloklari qulay joylashgan portal kodi",
                            "short_description": "Kun.uz va Daryo.uz uslubidagi yangiliklar saytining to'liq WordPress shabloni.",
                            "description": "Kategoriyalar, ommabop yangiliklar va fotoreportajlar bloklari bilan jihozlangan.",
                            "price": 38.00,
                            "file_format": "PHP, CSS, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1504813184591-01572f98c85f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Mobil ilovalar (React Native & Flutter)",
                "slug": "mobil-ilovalar-kodi",
                "description": "Kross-platforma mobil dasturlar manba kodi",
                "icon": "device-tablet",
                "subcategories": [
                    {
                        "name": "Flutter kross-platforma ilovalar",
                        "slug": "flutter-kross-platforma",
                        "product": {
                            "title": "Bloc state management va toza arxitekturali kross-platforma Flutter ilovasi",
                            "short_description": "iOS va Android uchun bitta kod bazasidan ishlovchi elektron do'kon mobil ilovasi.",
                            "description": "Clean Architecture qoidalari asosida yozilgan, testlar bilan qoplangan Flutter loyihasi.",
                            "price": 65.00,
                            "file_format": "Dart, Flutter, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "React Native mobil andozalari",
                        "slug": "react-native-andozalari",
                        "product": {
                            "title": "iOS va Android uchun tayyor navigatsiya va API ulanishli mobil shablon",
                            "short_description": "Expo va React Navigation 6 asosida yaratilgan zamonaviy foydalanuvchi interfeysi.",
                            "description": "Mobil dasturchilar yangi loyihani bir necha soatda tayyorlab mijozga taqdim etishi uchun shablon.",
                            "price": 60.00,
                            "file_format": "React Native, TS, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Veb-skreyping va avtomatlashtirish",
                "slug": "veb-skreyping-avtomatlashtirish",
                "description": "Parserlar, ma'lumot yig'ish va avtomatlashtirish skriptlari",
                "icon": "command-line",
                "subcategories": [
                    {
                        "name": "Ma'lumot yig'uvchi parserlar",
                        "slug": "skreyping-parserlar",
                        "product": {
                            "title": "Ko'chmas mulk va avtomobil e'lonlarini avtomatik yig'uvchi asinxron Python parser",
                            "short_description": "Playwright va BeautifulSoup yordamida e'lonlar narxi va tavsiflarini Excelga yozuvchi skript.",
                            "description": "Bloklanishdan himoyalangan, proxy va user-agentlarni almashtiruvchi ishonchli parser.",
                            "price": 30.00,
                            "file_format": "Python, Scripts, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "E-mail va SMS avtomatizatsiya",
                        "slug": "skreyping-sms-avtomatizatsiya",
                        "product": {
                            "title": "Mijozlarga avtomatik eslatma va bildirishnomalar yuboruvchi xizmat kodi",
                            "short_description": "Celery va Redis yordamida kechiktirilgan vazifalarni bajarish va xabarnomalar.",
                            "description": "Har qanday backend loyihasiga qo'shib ishlatish oson bo'lgan asinxron xabarlar moduli.",
                            "price": 28.00,
                            "file_format": "Python, Celery, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "API integratsiyalari va to'lov shlyuzlari",
                "slug": "api-integratsiyalari-tolov",
                "description": "Payme, Click, Uzum Pay va SMS shlyuzlari integratsiya modullari",
                "icon": "credit-card",
                "subcategories": [
                    {
                        "name": "Payme va Click integratsiya modullari",
                        "slug": "tolov-payme-click",
                        "product": {
                            "title": "FastAPI va Django uchun tayyor to'lov tekshiruvi va webhook qabul qilish moduli",
                            "short_description": "Payme va Click protokoli: tranzaksiyani yaratish, bekor qilish va tasdiqlash.",
                            "description": "To'liq testlar bilan ta'minlangan, xatoliklarni xavfsiz qayta ishlovchi ochiq kodli modul.",
                            "price": 35.00,
                            "file_format": "Python, FastAPI, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1556742049-0a67c5574f73?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "SMS provayderlar va xabarnomalar",
                        "slug": "tolov-sms-provayderlar",
                        "product": {
                            "title": "Eskiz va PlayMobile SMS shlyuzlari bilan ishlovchi Python kutubxonasi",
                            "short_description": "Telefon raqamiga tasdiqlash kodlari va reklama xabarlari yuborish integratsiyasi.",
                            "description": "Tokenlarni avtomatik yangilash va hisobdagi qoldiq SMS larni tekshirish funksiyalari mavjud.",
                            "price": 25.00,
                            "file_format": "Python, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            }
        ]
    },
    {
        "name": "3D design",
        "slug": "3d-design",
        "description": "Blender, 3ds Max modellari, arxitektura vizualizatsiyasi, o'yin aktivlari va personajlar",
        "icon": "cube",
        "inner_categories": [
            {
                "name": "Interyer vizualizatsiyasi",
                "slug": "interyer-vizualizatsiyasi",
                "description": "Xonadon, mehmonxona va ofislar 3D sahnalari",
                "icon": "home",
                "subcategories": [
                    {
                        "name": "Xonadon va mehmonxona interyeri",
                        "slug": "3d-xonadon-interyeri",
                        "product": {
                            "title": "Modern klassika uslubidagi 3 xonali xonadon 3D interyer sahnasi",
                            "short_description": "3ds Max va Corona Renderer uchun tayyor materiallar, yorug'lik va render sozlangan.",
                            "description": "Yuqori darajadagi fotorealizmga ega yashash xonasi va oshxona sahnasi. Mebellar to'liq komplektda.",
                            "price": 55.00,
                            "file_format": "3ds Max, Corona, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Ofis va kovorking maydonlari",
                        "slug": "3d-ofis-kovorking",
                        "product": {
                            "title": "Zamonaviy IT ofis, majlislar zali va ochiq ish maydoni renderi",
                            "short_description": "Blender Cycles uchun sozlangan, ergonomik stollar va zamonaviy yorug'lik sahnasi.",
                            "description": "Katta korporativ ofislar loyihasi uchun tayyor teksturalar va yuqori poligonli modellar to'plami.",
                            "price": 50.00,
                            "file_format": "Blender, Cycles, FBX",
                            "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Eksteryer va me'morchilik",
                "slug": "eksteryer-va-memorchilik",
                "description": "Hovlilar, villalar, zamonaviy binolar va fasadlar",
                "icon": "building-office",
                "subcategories": [
                    {
                        "name": "Zamonaviy hovli va villalar",
                        "slug": "3d-hovli-va-villalar",
                        "product": {
                            "title": "Hovuz va shinam landshaftga ega 2 qavatli zamonaviy villa modeli",
                            "short_description": "Tashqi yoritish (HDRI), daraxtlar va yo'laklar bilan to'liq jihozlangan eksteryer sahnasi.",
                            "description": "Arxitektura taqdimotlari uchun 8K teksturalar bilan boyitilgan V-Ray va Corona sahnasi.",
                            "price": 65.00,
                            "file_format": "3ds Max, V-Ray, FBX",
                            "image_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Ko'p qavatli binolar eksteryeri",
                        "slug": "3d-kop-qavatli-binolar",
                        "product": {
                            "title": "Biznes markaz va savdo majmuasining fotorealistik fasad arxitekturasi",
                            "short_description": "Shisha va metall fasadli 16 qavatli osmono'par bino 3D render maketi.",
                            "description": "Atrofdagi yo'llar, avtomobillar va ko'cha chiroqlari bilan birga to'liq shahar kompozitsiyasi.",
                            "price": 70.00,
                            "file_format": "3ds Max, FBX, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "3D personajlar",
                "slug": "3d-personajlar",
                "description": "O'yinlar va animatsiyalar uchun qahramonlar va mavjudotlar",
                "icon": "user",
                "subcategories": [
                    {
                        "name": "O'yinlar uchun rig personajlar",
                        "slug": "3d-rig-personajlar",
                        "product": {
                            "title": "Kiberpank jangchi personaji to'liq skelet (Rig) va animatsiyalari bilan",
                            "short_description": "Unreal Engine 5 va Unity uchun sozlangan, 4K PBR teksturali personaj modeli.",
                            "description": "Yugurish, zarba berish va sakrash animatsiyalari tayyor bo'lgan yuqori sifatli qahramon.",
                            "price": 45.00,
                            "file_format": "Blender, FBX, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Multfilm uslubidagi qahramonlar",
                        "slug": "3d-multfilm-qahramonlar",
                        "product": {
                            "title": "Mobil o'yinlar uchun multfilm qahramoni modeli va teksturalari",
                            "short_description": "Stylized 3D personaj, quvnoq emotsiyalar va yengil poligon to'ri (Low-poly).",
                            "description": "Kausal o'yinlar yaratuvchilar uchun mos, tekstura xaritasi optimallashtirilgan model.",
                            "price": 38.00,
                            "file_format": "Maya, FBX, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1563089145-599997674d42?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "O'yin aktivlari (Game assets)",
                "slug": "oyin-aktivlari-game-assets",
                "description": "Qurollar, tabiat, rekvizitlar va modulli atrof-muhit",
                "icon": "puzzle-piece",
                "subcategories": [
                    {
                        "name": "Qurol-aslaha va harbiy texnika",
                        "slug": "3d-qurollar-texnika",
                        "product": {
                            "title": "Shooter o'yinlari uchun 10 ta PBR teksturali zamonaviy o'qotar qurollar",
                            "short_description": "Avtomatlar, to'pponchalar va snayper miltiqlari 3D modellari to'plami.",
                            "description": "O'qlarni qayta o'qlash animatsiyalariga mos ajratilgan qismlar va 4K teksturalar.",
                            "price": 50.00,
                            "file_format": "UE5, FBX, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Atrof-muhit va tabiat rekvizitlari",
                        "slug": "3d-tabiat-rekvizitlari",
                        "product": {
                            "title": "O'rmon va qoyalar: daraxtlar, toshlar va o'simliklar modulli to'plami",
                            "short_description": "O'yinlarda realistik tabiat yaratish uchun shamol animatsiyali o'simliklar.",
                            "description": "Unity va Unreal Engine uchun Nanite optimizatsiyasi bilan tayyorlangan tabiat aktivlari.",
                            "price": 42.00,
                            "file_format": "Unity, Blender, FBX",
                            "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Mahsulot vizualizatsiyasi",
                "slug": "mahsulot-vizualizatsiyasi",
                "description": "Elektronika, parfyumeriya va gadjetlar 3D reklamasi",
                "icon": "camera",
                "subcategories": [
                    {
                        "name": "Smartfon va elektronika 3D renderi",
                        "slug": "3d-smartfon-elektronika",
                        "product": {
                            "title": "Flagman smartfon va simsiz quloqchinlar studiya yoritish sahnasi",
                            "short_description": "Blender Cycles studiya yoritishi, podium va aylanuvchi kamera animatsiyasi.",
                            "description": "Reklama roliklari va e'lonlar uchun tayyor studio sahnasi va materiallar.",
                            "price": 35.00,
                            "file_format": "Blender, Cycles, PSD",
                            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Parfyumeriya va kosmetika sahnasi",
                        "slug": "3d-parfyumeriya-kosmetika",
                        "product": {
                            "title": "Atir shishasi, suyuqlik va suv tomchilari generatori sahnasi",
                            "short_description": "Shisha sinishi, suyuqlik va fotorealistik suv tomchilari procedurial shaderi.",
                            "description": "Kosmetika brendlari uchun qimmatbaho, premium vizual render maketi.",
                            "price": 40.00,
                            "file_format": "Cinema 4D, Octane, FBX",
                            "image_url": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Mebel va interyer elementlari",
                "slug": "mebel-va-interyer-elementlari",
                "description": "Divanlar, stollar, lyustralar va bezak buyumlari",
                "icon": "squares-2x2",
                "subcategories": [
                    {
                        "name": "Zamonaviy divan va kreslolar",
                        "slug": "3d-divan-va-kreslolar",
                        "product": {
                            "title": "Baxmal matoli burchak divan va ergonomik dam olish kreslolari to'plami",
                            "short_description": "Mato burmalari realistik skaner qilingan, barcha teksturalar 4K sifatda.",
                            "description": "Interyer dizaynerlari uchun har qanday xonaga mos tushuvchi zamonaviy yumshoq mebel.",
                            "price": 28.00,
                            "file_format": "3ds Max, Corona, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Yoritish uskunalari va lyustralar",
                        "slug": "3d-lyustralar-lampalar",
                        "product": {
                            "title": "Zamonaviy LED lyustralar, pol lampalari va bra 3D modellari",
                            "short_description": "IES yorug'lik profillari sozlangan 15 ta dizaynerlik chiroqlari to'plami.",
                            "description": "Shinam atmosfera yaratuvchi tilla, qora metall va shisha materialli yoritgichlar.",
                            "price": 25.00,
                            "file_format": "Blender, FBX, IES",
                            "image_url": "https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Transport va avtomobillar",
                "slug": "transport-va-avtomobillar",
                "description": "Avtomobillar, sportkarlar, samolyotlar va kema modellari",
                "icon": "truck",
                "subcategories": [
                    {
                        "name": "Sportkarlar va avtomobillar",
                        "slug": "3d-sportkarlar",
                        "product": {
                            "title": "Yuqori poligonli superkar 3D modeli (Salon va dvigatel qismlari bilan)",
                            "short_description": "Batafsil salon, charm o'rindiqlar va ochiluvchi eshiklar mexanizmi.",
                            "description": "Avtomobil renderlari va animatsion filmlar uchun to'liq sozlangan fotorealistik model.",
                            "price": 45.00,
                            "file_format": "Blender, FBX, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Koinot kemalari va samolyotlar",
                        "slug": "3d-koinot-kemalari",
                        "product": {
                            "title": "Fantastik ilmiy-koinot transporti 3D modeli va 4K PBR teksturalari",
                            "short_description": "Sci-Fi janridagi o'yinlar uchun yulduzlararo transport vositasi modeli.",
                            "description": "Substance Painter da bo'yalgan, metall sinishi va yonish effektlari sozlangan model.",
                            "price": 40.00,
                            "file_format": "FBX, OBJ, Substance",
                            "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Zargarlik buyumlari va aksessuarlar",
                "slug": "zargarlik-buyumlari-va-aksessuarlar",
                "description": "Uzuklar, tilla buyumlar, soatlar va qimmatbaho taqinchoqlar",
                "icon": "sparkles",
                "subcategories": [
                    {
                        "name": "Uzuk va tilla buyumlar modellari",
                        "slug": "3d-uzuk-tilla-buyumlar",
                        "product": {
                            "title": "Brilliant ko'zli nishon uzugi va sirg'alar 3D zargarlik maketi",
                            "short_description": "Qimmatbaho toshlar sinishi (Dispersion) va oq oltin materiali sozlangan render.",
                            "description": "Zargarlik do'konlari katalogi va ijtimoiy tarmoq reklama roliklari uchun ajoyib render.",
                            "price": 35.00,
                            "file_format": "Rhino, Matrix, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Soatlar va bilaguzuklar",
                        "slug": "3d-soatlar-va-bilaguzuklar",
                        "product": {
                            "title": "Klassik mexanik erkaklar qo'l soati fotorealistik 3D modeli",
                            "short_description": "Siferblat, mexanizm tishli g'ildiraklari va charm remeshokning eng mayda detallari.",
                            "description": "Zargarlik buyumlari va qo'l soatlarini reklama qilish uchun 8K teksturali model.",
                            "price": 32.00,
                            "file_format": "3ds Max, Corona, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "3D bosib chiqarish (3D Print) modellari",
                "slug": "3d-bosib-chiqarish-print",
                "description": "3D printerlar uchun STL fayllar, haykallar va qismlar",
                "icon": "printer",
                "subcategories": [
                    {
                        "name": "Haykalchalar va suvenirlar",
                        "slug": "3d-print-haykalchalar",
                        "product": {
                            "title": "3D printerda chiqarish uchun tayyor qahramonlar va büstlar to'plami",
                            "short_description": "Topologiyasi to'g'rilangan, teshiklarsiz (Watertight) STL va OBJ fayllari.",
                            "description": "FDM va SLA printerlarida qulay chop etish uchun qo'llab-quvvatlash nuqtalari hisoblangan.",
                            "price": 20.00,
                            "file_format": "STL, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1563089145-599997674d42?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Muhandislik ehtiyot qismlari",
                        "slug": "3d-print-muhandislik-qismlar",
                        "product": {
                            "title": "Mexanik mexanizmlar va reduktor tishli g'ildiraklari 3D bosma fayllari",
                            "short_description": "Aniq toleranslar bilan modellashtirilgan ehtiyot qismlar va korpuslar.",
                            "description": "Robototexnika va prototiplash loyihalari uchun tayyor muhandislik 3D fayllari.",
                            "price": 25.00,
                            "file_format": "STEP, STL",
                            "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "VFX va simulyatsiyalar",
                "slug": "vfx-va-simulyatsiyalar",
                "description": "Tutun, olov, portlash, suyuqlik va matolar fizikasi",
                "icon": "fire",
                "subcategories": [
                    {
                        "name": "Suyuqlik va tutun effektlari",
                        "slug": "vfx-suyuqlik-va-tutun",
                        "product": {
                            "title": "Portlash, tutun va quyuq suyuqlik simulyatsiyasi VDB fayllari to'plami",
                            "short_description": "Houdini va Blender uchun tayyor OpenVDB volumetrik fayllar to'plami.",
                            "description": "Kino va videolarda ajoyib maxsus effektlar yaratish uchun eng yuqori aniqlikdagi simulyatsiya.",
                            "price": 48.00,
                            "file_format": "VDB, Houdini, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Matolar va kiyimlar fizikasi",
                        "slug": "vfx-matolar-va-kiyimlar",
                        "product": {
                            "title": "Marvelous Designer da yaratilgan zamonaviy kiyimlar va pardalar simulyatsiyasi",
                            "short_description": "Shamol harakatida hilpiraydigan pardalar va inson qomatiga mos tushgan kiyimlar.",
                            "description": "O'yinlar va 3D renderlar uchun kiyimlar tikish andozasi va simulyatsiyasi.",
                            "price": 35.00,
                            "file_format": "ZPrj, FBX, OBJ",
                            "image_url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            }
        ]
    },
    {
        "name": "AI generation",
        "slug": "ai-generation",
        "description": "Sun'iy intellekt promptlari, AI artlar, video, ovoz modellari va virtual avatarlar",
        "icon": "sparkles",
        "inner_categories": [
            {
                "name": "Midjourney promptlar to'plami",
                "slug": "midjourney-promptlar",
                "description": "Midjourney v6 uchun sinovdan o'tgan master-promptlar",
                "icon": "command-line",
                "subcategories": [
                    {
                        "name": "Fotorealistik portret promptlari",
                        "slug": "mj-portret-promptlari",
                        "product": {
                            "title": "Kamera linzalari va studiya nurlari ko'rsatilgan 400 ta portret prompti",
                            "short_description": "Inson emotsiyalari, terining mayda g'ovaklari va ko'z jilosini chiqaruvchi promptlar.",
                            "description": "Haqiqiy studiya fotosuratchisi kabi natija beruvchi professional Midjourney ko'rsatmalari to'plami.",
                            "price": 14.00,
                            "file_format": "PDF, TXT",
                            "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Arxitektura va interyer promptlari",
                        "slug": "mj-arxitektura-promptlari",
                        "product": {
                            "title": "Kelajak me'morchiligi va hashamatli villalar yaratish promptlari",
                            "short_description": "Zaha Hadid uslubidagi egriliklar va tabiat qo'ynidagi zamonaviy kottejlar formulalari.",
                            "description": "Arxitektorlar va dizaynerlar uchun yangi g'oyalar generatsiya qiluvchi sinovdan o'tgan promptlar.",
                            "price": 16.00,
                            "file_format": "Notion, PDF",
                            "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "ChatGPT va LLM master-promptlari",
                "slug": "chatgpt-master-promptlar",
                "description": "Biznes, marketing, kopirayting va dasturlash promptlari",
                "icon": "chat-bubble-bottom-center-text",
                "subcategories": [
                    {
                        "name": "Marketing va kopirayting promptlari",
                        "slug": "chatgpt-marketing-promptlari",
                        "product": {
                            "title": "Mijozlarni jalb qiluvchi savdo matnlari va takliflar uchun 250 master-prompt",
                            "short_description": "AIDA va PAS formulalari asosida konversiyali e'lonlar yaratish bo'yicha ko'rsatmalar.",
                            "description": "Kopirayterlar va marketologlar uchun yozish vaqtini 5 barobar qisqartiruvchi tizimli promptlar.",
                            "price": 15.00,
                            "file_format": "Notion, PDF",
                            "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Dasturlash va kod yozish promptlari",
                        "slug": "chatgpt-dasturlash-promptlari",
                        "product": {
                            "title": "Kod arxitekturasi, testlash va optimallashtirish uchun AI promptlar",
                            "short_description": "Senior dasturchi sifatida refaktoring qilish va arxitektura tanlash uchun ko'rsatmalar.",
                            "description": "Python, JavaScript, Go va SQL so'rovlarini tahlil qilish hamda xavfsizlikni tekshirish andozalari.",
                            "price": 18.00,
                            "file_format": "Markdown, PDF",
                            "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "DALL-E va Stable Diffusion",
                "slug": "dalle-stable-diffusion",
                "description": "Vektorli logotiplar, san'at asarlari va ilmiy artlar",
                "icon": "photo",
                "subcategories": [
                    {
                        "name": "Logotip va vektor art promptlari",
                        "slug": "dalle-logotip-promptlari",
                        "product": {
                            "title": "Minimalist logotiplar va vektor ikonalar yaratish uchun DALL-E formulalari",
                            "short_description": "Oq fon, toza chiziqlar va aniq ramzlar bilan logotip generatsiya qilish sirlari.",
                            "description": "Dizaynerlar uchun tezkor brend konseptlari ishlab chiqishda ajoyib yordamchi vosita.",
                            "price": 12.00,
                            "file_format": "PDF, TXT",
                            "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Fantastika va ilmiy artlar",
                        "slug": "sd-fantastika-artlar",
                        "product": {
                            "title": "Stable Diffusion XL uchun sinematik kosmik sahnalar promptlari",
                            "short_description": "Koinot stantsiyalari, begona sayyoralar va kiber shahar manzaralari yaratish qoidalari.",
                            "description": "Negative promptlar va parametrlar to'liq sozlangan, yuqori sifat kafolatlangan to'plam.",
                            "price": 15.00,
                            "file_format": "TXT, PNG",
                            "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "AI rasmlar va san'at (Art)",
                "slug": "ai-rasmlar-va-sanat",
                "description": "4K/8K devor qog'ozlari, milliy artlar va kiberpank illyustratsiyalar",
                "icon": "paint-brush",
                "subcategories": [
                    {
                        "name": "O'zbekiston madaniyati AI artlari",
                        "slug": "ai-ozbekiston-madaniyati",
                        "product": {
                            "title": "Qadimiy Samarqand va Buxoro kelajak kiberpank nigohida: 8K artlar",
                            "short_description": "Minoralar, moviy gumbazlar va kelajak texnologiyalari uyg'unlashgan 40 ta san'at asari.",
                            "description": "Plakatlar, fon rasmlari va konseptlar uchun tayyor yuqori sifatli badiiy to'plam.",
                            "price": 22.00,
                            "file_format": "JPG, PNG 8K",
                            "image_url": "https://images.unsplash.com/photo-1686191128892-3b37add41544?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Kiberpank va futuristik rasmlar",
                        "slug": "ai-kiberpank-rasmlar",
                        "product": {
                            "title": "Neon shahar ko'chalari va robotlar hayoti mavzusidagi rasmlar to'plami",
                            "short_description": "Tungi yomg'ir, neon akslari va uchar mashinalar tasvirlangan sinematik artlar.",
                            "description": "Musiqa albomlari muqovasi va YouTube fonlari uchun ideal bo'lgan raqamli san'at.",
                            "price": 18.00,
                            "file_format": "PNG 4K",
                            "image_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "AI video va animatsiyalar",
                "slug": "ai-video-va-animatsiyalar",
                "description": "Runway Gen-2, Sora va Pika orqali yaratilgan videolar",
                "icon": "film",
                "subcategories": [
                    {
                        "name": "Runway va Sora video shablonlari",
                        "slug": "ai-video-shablonlar",
                        "product": {
                            "title": "4K 60fps sinematik harakatlar va dinamik o'tishlarga ega AI video kliplar",
                            "short_description": "Tabiat hodisalari, portlashlar va parvoz kadrlari aks etgan 25 ta b-roll video.",
                            "description": "Reklama videoroliklarida qimmatbaho tasvirlar sifatida ishlatish uchun tayyor qisqa videolar.",
                            "price": 35.00,
                            "file_format": "MP4, 4K",
                            "image_url": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Reklama uchun harakatli AI lavhalar",
                        "slug": "ai-reklama-lavhalari",
                        "product": {
                            "title": "Tovar va xizmatlarni ijtimoiy tarmoqda reklama qilish uchun video lavhalar",
                            "short_description": "Mahsulotlar atrofida aylanuvchi kamera va yorug'lik nurlari animatsiyalari.",
                            "description": "Instagram Reels va TikTok da tomoshabinlar e'tiborini tortuvchi harakatli vizuallar.",
                            "price": 30.00,
                            "file_format": "MP4, MOV",
                            "image_url": "https://images.unsplash.com/photo-1536240478700-b869070f9279?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "AI ovoz va audio profillar",
                "slug": "ai-ovoz-va-audio",
                "description": "ElevenLabs diktor ovozlari va audiokitob modellari",
                "icon": "speaker-wave",
                "subcategories": [
                    {
                        "name": "O'zbekcha diktor ovoz modellari",
                        "slug": "ai-ozbekcha-diktor-ovoz",
                        "product": {
                            "title": "ElevenLabs uchun tabiiy va professional jaranglovchi o'zbekcha diktor profili",
                            "short_description": "Erkak va ayol ovozlari, aniq diksiya va to'g'ri urg'ular bilan o'qish parametrlari.",
                            "description": "Matnlarni audio formatga o'tkazishda robot ohangisiz tabiiy eshitiluvchi ovoz profili.",
                            "price": 25.00,
                            "file_format": "WAV, JSON",
                            "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Podkast va kitob o'quvchi ovozlar",
                        "slug": "ai-kitob-oquvchi-ovozlar",
                        "product": {
                            "title": "Tinchlantiruvchi va ta'sirchan audiokitob suxandoni ovoz sozlamalari",
                            "short_description": "Uzoq adabiy asarlar va ertaklarni charchatmasdan o'qib beruvchi sokin bariton ovoz.",
                            "description": "Audiokitoblar yaratish va meditatsiya kurslari uchun maxsus sinovdan o'tgan model.",
                            "price": 20.00,
                            "file_format": "MP3, WAV",
                            "image_url": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Virtual avatarlar (HeyGen / D-ID)",
                "slug": "virtual-avatarlar",
                "description": "Jonli suxandonlar, dars beruvchi virtual boshlovchilar",
                "icon": "user-circle",
                "subcategories": [
                    {
                        "name": "Korporativ AI suxandonlar",
                        "slug": "ai-korporativ-suxandonlar",
                        "product": {
                            "title": "Video e'lonlar va yangiliklar uchun realistik ko'rinishdagi AI boshlovchi modeli",
                            "short_description": "Lab harakati (Lip-sync) matnga mukammal mos tushuvchi professional boshlovchi.",
                            "description": "Kompaniya hisobotlari va taqdimotlarini videoga aylantirish uchun tayyor avatarlar.",
                            "price": 38.00,
                            "file_format": "MP4, PSD",
                            "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Ta'lim va dars beruvchi avatarlar",
                        "slug": "ai-talim-avatarlari",
                        "product": {
                            "title": "Onlayn kurslar va darsliklar olib borish uchun virtual o'qituvchi avatar",
                            "short_description": "Kamera oldida turib talabalarga dars tushuntiruvchi muloyim virtual murabbiy.",
                            "description": "O'quv markazlari va repititorlar uchun video darslar yaratish jarayonini tezlashtiradi.",
                            "price": 35.00,
                            "file_format": "MP4, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Musiqa va saundtreklar (Suno / Udio)",
                "slug": "musiqa-va-saundtreklar",
                "description": "Fon musiqalari, lo-fi treklari va reklama audio ritmlari",
                "icon": "musical-note",
                "subcategories": [
                    {
                        "name": "Fon musiqalari va lo-fi treklari",
                        "slug": "ai-lofi-musiqa",
                        "product": {
                            "title": "YouTube videolari va podkastlar uchun mualliflik huquqisiz 20 ta lo-fi trek",
                            "short_description": "Tinchlantiruvchi gitara va pianino akkordlari bilan boyitilgan instrumental kuylar.",
                            "description": "Monetizatsiya qilinadigan videolarda bemalol ishlatish mumkin bo'lgan studiyaviy audio fayllar.",
                            "price": 24.00,
                            "file_format": "WAV, MP3",
                            "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Reklama uchun dinamik kuylar",
                        "slug": "ai-reklama-kuylari",
                        "product": {
                            "title": "Tijoriy roliklar uchun baquvvat bas va zamonaviy ritmli saundtreklar",
                            "short_description": "Televideniye va internet reklamalari uchun 15 va 30 soniyalik dinamik kuylar.",
                            "description": "Tomoshabin e'tiborini darhol jalb qiluvchi baquvvat ritmlar to'plami.",
                            "price": 26.00,
                            "file_format": "WAV, 24-bit",
                            "image_url": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "AI biznes avtomatlashtirish",
                "slug": "ai-biznes-avtomatlashtirish",
                "description": "AI agentlar, avtomatlashtirilgan kontent va ma'lumotlar tahlili",
                "icon": "bolt",
                "subcategories": [
                    {
                        "name": "ChatGPT asosidagi AI agentlar",
                        "slug": "ai-agentlar-kodi",
                        "product": {
                            "title": "Mijozlar bilan 24/7 muloqot qiluvchi va buyurtma oluvchi AI agent kodi",
                            "short_description": "LangChain va OpenAI API asosida kompaniyangiz ma'lumotlari bo'yicha javob beruvchi bot.",
                            "description": "Savollarga javob berish va ma'lumotlar bazasiga buyurtmalarni kiritish funksiyasiga ega.",
                            "price": 45.00,
                            "file_format": "Python, LangChain, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Kontent-reja generatsiya tizimlari",
                        "slug": "ai-kontent-reja-tizimi",
                        "product": {
                            "title": "SMM mutaxassislari uchun 1 oylik kontent-rejani 5 daqiqada tuzuvchi tizim",
                            "short_description": "Mavzular, sarlavhalar va to'liq post matnlarini avtomatik chiqarib beruvchi qolip.",
                            "description": "Google Sheets va Notion shabloniga integratsiya qilingan sun'iy idrok yordamchisi.",
                            "price": 22.00,
                            "file_format": "Notion, Sheets",
                            "image_url": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Neyrotarmoqlar uchun LoRA modellari",
                "slug": "lora-modellari",
                "description": "Stable Diffusion uchun maxsus milliy uslub va shaxsiy LoRA vaznlari",
                "icon": "finger-print",
                "subcategories": [
                    {
                        "name": "Milliy liboslar LoRA modellari",
                        "slug": "lora-milliy-liboslar",
                        "product": {
                            "title": "O'zbek atlas va adras liboslarini aniq chizuvchi SDXL LoRA vaznlari",
                            "short_description": "Milliy naqshlar, choponlar va do'ppilarni 100% o'xshatib chizuvchi neyrotarmoq modeli.",
                            "description": "Moda dizaynerlari va illyustratorlar uchun bebaho vosita bo'lgan maxsus o'qitilgan model.",
                            "price": 30.00,
                            "file_format": "Safetensors, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Shaxsiy brend foto LoRA paketi",
                        "slug": "lora-shaxsiy-brend",
                        "product": {
                            "title": "Har qanday inson fotosuratlaridan yuqori sifatli fotosessiya generatsiya qilish modeli",
                            "short_description": "15 ta oddiy rasm asosida professional studiya fotosessiyasi tayyorlash qo'llanmasi.",
                            "description": "O'z suratingizni kiritib istalgan kiyim va lokatsiyada rasmlar olish bo'yicha to'liq qo'llanma.",
                            "price": 32.00,
                            "file_format": "Safetensors, PDF",
                            "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            }
        ]
    },
    {
        "name": "Shablonlar",
        "slug": "shablonlar",
        "description": "PowerPoint, Rezyume (CV), Excel, Notion, shartnomalar va video montaj shablonlari",
        "icon": "document-duplicate",
        "inner_categories": [
            {
                "name": "PowerPoint & Keynote taqdimotlar",
                "slug": "powerpoint-keynote-taqdimotlar",
                "description": "Pitch Deck, biznes hisobotlar va akademik taqdimot slaydlar",
                "icon": "presentation-chart-bar",
                "subcategories": [
                    {
                        "name": "Startap va investitsiya Pitch Deck",
                        "slug": "pitch-deck-taqdimotlar",
                        "product": {
                            "title": "Investorlar oldida chiqish qilish uchun 70 ta zamonaviy Pitch Deck slaydlari",
                            "short_description": "Muammo, yechim, bozor hajmi (TAM/SAM/SOM) va moliyaviy prognoz bloklari.",
                            "description": "Startapingizga investitsiya jalb qilish uchun sinovdan o'tgan, jozibador prezentatsiya andozasi.",
                            "price": 25.00,
                            "file_format": "PPTX, Keynote",
                            "image_url": "https://images.unsplash.com/photo-1542744094-3a31f272c490?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Yillik hisobot va biznes taqdimotlar",
                        "slug": "biznes-hisobot-taqdimotlar",
                        "product": {
                            "title": "Kompaniya yillik moliyaviy hisoboti uchun 100+ infografik slaydlar",
                            "short_description": "Daromadlar, o'sish dinamikasi va xaritalar bilan to'ldirilgan korporativ shablon.",
                            "description": "Raqamlarni chiroyli va tushunarli grafiklar orqali ko'rsatish uchun eng yaxshi slaydlar to'plami.",
                            "price": 22.00,
                            "file_format": "PPTX, Google Slides",
                            "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Rezyume (CV) shablonlari",
                "slug": "rezyume-cv-shablonlari",
                "description": "ATS-mos, dasturchi, dizayner va rahbarlar rezyume andozalari",
                "icon": "identification",
                "subcategories": [
                    {
                        "name": "Dasturchilar uchun ATS rezyumelar",
                        "slug": "cv-dasturchilar-ats",
                        "product": {
                            "title": "Kompaniyalar skaner tizimidan (ATS) 100% o'tuvchi professional IT rezyume",
                            "short_description": "Word va Figma formatlarida, ko'nikmalar va loyihalarni aniq ko'rsatuvchi andoza.",
                            "description": "Xalqaro kompaniyalarga ishga topshirishda tavsiya etiladigan toza va standartlarga mos rezyume.",
                            "price": 10.00,
                            "file_format": "DOCX, PDF, Figma",
                            "image_url": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Dizaynerlar uchun ijodiy portfolio CV",
                        "slug": "cv-dizaynerlar-portfolio",
                        "product": {
                            "title": "Dizaynerlar va ijodiy mutaxassislar uchun vizual jozibador portfolio andozasi",
                            "short_description": "Loyihalar skrinshotlari, uslub va yutuqlarni ko'rsatish uchun nafis dizayn.",
                            "description": "Ish beruvchining diqqatini birinchi qarashdayoq tortuvchi kreativ rezyume shabloni.",
                            "price": 12.00,
                            "file_format": "Figma, PSD, PDF",
                            "image_url": "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Excel va Google Sheets jadvallari",
                "slug": "excel-va-google-sheets",
                "description": "Moliya hisobi, savdo, ombor va xarajatlar jadvallari",
                "icon": "table-cells",
                "subcategories": [
                    {
                        "name": "Shaxsiy byudjet va moliya hisobi",
                        "slug": "excel-shaxsiy-byudjet",
                        "product": {
                            "title": "Daromad va xarajatlarni to'liq hisoblovchi, avtomatik diagrammali moliya jadvali",
                            "short_description": "Oylik jamg'armalar, kreditlar va rejalashtirilgan xarajatlar monitoringi.",
                            "description": "Pullaringiz qayerga ketayotganini aniq ko'rsatuvchi va tejashga yordam beruvchi qulay Excel fayl.",
                            "price": 15.00,
                            "file_format": "XLSX, Sheets",
                            "image_url": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Kichik biznes ombor va savdo jadvali",
                        "slug": "excel-biznes-ombor",
                        "product": {
                            "title": "Tovarlar kirim-chiqimi, foyda va qarzdorliklar hisobi bo'yicha tayyor jadval",
                            "short_description": "Avtomatik formulalar bilan jihozlangan savdo va qoldiq tovarlar daftari.",
                            "description": "Katta xarajat qilmasdan o'z do'koni va omborini tartibli yuritishni istagan tadbirkorlar uchun.",
                            "price": 18.00,
                            "file_format": "XLSX",
                            "image_url": "https://images.unsplash.com/photo-1543286386-713bdd548da4?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Notion shablonlari",
                "slug": "notion-shablonlari",
                "description": "Life OS, frilanser boshqaruvi, CRM va maqsadlar tizimi",
                "icon": "clipboard-document-check",
                "subcategories": [
                    {
                        "name": "Life & Work OS keng qamrovli tizim",
                        "slug": "notion-life-os",
                        "product": {
                            "title": "Kundalik vazifalar, loyihalar va odatlar monitoringi uchun universal Notion OS",
                            "short_description": "Shaxsiy samaradorlikni oshiruvchi vazifalar taqvimi va kitoblar arxivi.",
                            "description": "Barcha maqsad va rejalarni bitta chiroyli va qulay joyda boshqarish tizimi.",
                            "price": 20.00,
                            "file_format": "Notion Template",
                            "image_url": "https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Frilanserlar uchun loyiha boshqaruvi",
                        "slug": "notion-frilanser-boshqaruvi",
                        "product": {
                            "title": "Mijozlar bazasi, to'lovlar va topshiriqlarni boshqarish Notion CRM",
                            "short_description": "Frilanserlar uchun shartnomalar, buyurtmalar oqimi va hisob-fakturalar portali.",
                            "description": "Muddatlarni o'tkazib yubormaslik va mijozlar bilan munosabatni tartibga solish tizimi.",
                            "price": 16.00,
                            "file_format": "Notion Template",
                            "image_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Shartnomalar va huquqiy hujjatlar",
                "slug": "shartnomalar-va-huquqiy-hujjatlar",
                "description": "Xizmat ko'rsatish, IT shartnomalar, tijoriy takliflar",
                "icon": "document-text",
                "subcategories": [
                    {
                        "name": "IT xizmat ko'rsatish shartnomalari",
                        "slug": "shartnoma-it-xizmatlar",
                        "product": {
                            "title": "Veb-sayt va dasturiy ta'minot ishlab chiqish bo'yicha ikki tomonlama shartnoma",
                            "short_description": "Texnik topshiriq (TZ), to'lov bosqichlari va mualliflik huquqini himoya qiluvchi shartnoma.",
                            "description": "Dasturchi va mijoz o'rtasidagi kelishmovchiliklarning oldini oluvchi yuridik puxta hujjat.",
                            "price": 15.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Tijorat takliflari va aktlar",
                        "slug": "shartnoma-tijorat-takliflari",
                        "product": {
                            "title": "Kompaniyalar uchun xizmat ko'rsatish tijoriy taklifi va bajarilgan ishlar dalolatnomasi",
                            "short_description": "B2B mijozlarga xizmatlarni professional taqdim etish andozalari.",
                            "description": "Zamonaviy formatdagi rasmiy tijorat taklifi (Commercial Proposal) va schyot-faktura andozalari.",
                            "price": 12.00,
                            "file_format": "DOCX, PDF",
                            "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Video montaj (Premiere & After Effects)",
                "slug": "video-montaj-shablonlari",
                "description": "MOGRT titrlar, o'tishlar va audio-vizual effektlar",
                "icon": "video-camera",
                "subcategories": [
                    {
                        "name": "YouTube dinamik titr va subtitrlar",
                        "slug": "video-youtube-titrlar",
                        "product": {
                            "title": "Premiere Pro uchun 40 ta animatsion sarlavha va zamonaviy subtitr shablonlari",
                            "short_description": "MOGRT formatida, rang va shriftlarni bir tugma bilan o'zgartirish imkoniyati.",
                            "description": "Videoblogerlar uchun ko'rishlar sonini oshiruvchi trenddagi pastki uchinchi (lower third) titrlar.",
                            "price": 20.00,
                            "file_format": "Premiere Pro, MOGRT",
                            "image_url": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=800&q=80",
                            "is_featured": True
                        }
                    },
                    {
                        "name": "Reels va TikTok trend o'tishlar",
                        "slug": "video-reels-otishlar",
                        "product": {
                            "title": "Qisqa videolar uchun tezkor glitch va zoom o'tish effektlari to'plami",
                            "short_description": "Ovoz effektlari (SFX) bilan boyitilgan 50 ta dinamik transition presetlari.",
                            "description": "Reels va TikTok videolarini qiziqarli va professional montaj qilish andozalari.",
                            "price": 18.00,
                            "file_format": "Premiere Pro, DaVinci",
                            "image_url": "https://images.unsplash.com/photo-1536240478700-b869070f9279?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "DaVinci Resolve va rang berish (LUTs)",
                "slug": "davinci-resolve-va-luts",
                "description": "Kinematografik LUTs, rang korreksiyasi va profillar",
                "icon": "adjustments-horizontal",
                "subcategories": [
                    {
                        "name": "Kinematografik rang berish LUTs",
                        "slug": "luts-kino-ranglari",
                        "product": {
                            "title": "Kino uslubidagi boy ranglar va kontrast beruvchi 35 ta professional LUTs",
                            "short_description": "Sony, Canon va iPhone log profillari uchun maxsus tayyorlangan CUBE fayllar.",
                            "description": "Oddiy videolarni Gollivud filmlari darajasidagi chuqur tusga olib chiquvchi ranglar to'plami.",
                            "price": 16.00,
                            "file_format": "CUBE, 3DL",
                            "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "YouTube videolari uchun rang presetlari",
                        "slug": "luts-youtube-ranglari",
                        "product": {
                            "title": "Vlog va intervyu videolarini jonli ko'rsatuvchi rang berish profillari",
                            "short_description": "Terining tabiiy rangini saqlab, yorug'lik va kontrastni to'g'rilovchi andozalar.",
                            "description": "DaVinci Resolve va Premiere Pro da 1 daqiqada rang berish uchun qulay presetlar.",
                            "price": 14.00,
                            "file_format": "CUBE, DRP",
                            "image_url": "https://images.unsplash.com/photo-1518173946687-a4c8a383392e?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "Canva shablonlari",
                "slug": "canva-shablonlari",
                "description": "SMM, sertifikatlar, taqdimotlar va bayram tabriklari",
                "icon": "sparkles",
                "subcategories": [
                    {
                        "name": "Ijtimoiy tarmoqlar uchun dizaynlar",
                        "slug": "canva-ijtimoiy-tarmoqlar",
                        "product": {
                            "title": "Biznes va savdo uchun 50 ta tezkor tahrirlanadigan Canva post shablonlari",
                            "short_description": "Telefon orqali matn va rasmlarni almashtirib tayyor post chiqarish imkoni.",
                            "description": "Dizayner xizmatisiz o'z sahifangizni estetik yuritish uchun tayyor Canva andozalari.",
                            "price": 15.00,
                            "file_format": "Canva Template",
                            "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Sertifikat va diplom shablonlari",
                        "slug": "canva-sertifikatlar",
                        "product": {
                            "title": "O'quv kurslari va tadbirlar uchun bosmaga tayyor elegant sertifikat andozalari",
                            "short_description": "A4 formatdagi 10 ta tilla naqshli diplom va sertifikat andozasi.",
                            "description": "Ism-familiyani o'zgartirib PDF formatida chop etish yoki onlayn yuborish mumkin.",
                            "price": 12.00,
                            "file_format": "Canva, PDF",
                            "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "E-mail marketing shablonlari",
                "slug": "email-marketing-shablonlari",
                "description": "HTML e-mail xabarlar, savdo va taklif xatlari maketlari",
                "icon": "envelope",
                "subcategories": [
                    {
                        "name": "HTML e-mail xabarnomalar",
                        "slug": "email-html-xabarnomalar",
                        "product": {
                            "title": "Barcha pochtalarda (Gmail, Outlook) to'g'ri ochiluvchi responsive e-mail shablonlari",
                            "short_description": "Mobil va kompyuterda mukammal ko'rinuvchi toza HTML/CSS xabarnomalar kodi.",
                            "description": "Mailchimp, Brevo va boshqa servislar bilan to'liq mos keluvchi 5 ta zamonaviy maket.",
                            "price": 18.00,
                            "file_format": "HTML, MJML, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Savdo va tabrik xatlari",
                        "slug": "email-savdo-tabriklar",
                        "product": {
                            "title": "Aksiyalar va bayram chegirmalari haqida xabar beruvchi chiroyli xat maketlari",
                            "short_description": "Mijozlarni xaridga undovchi tugmalar (CTA) va chegirma kuponlari bloki.",
                            "description": "E-mail marketing kampaniyalari konversiyasini oshirish uchun sinovdan o'tgan andoza.",
                            "price": 14.00,
                            "file_format": "HTML, ZIP",
                            "image_url": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            },
            {
                "name": "O'quv va darslik shablonlari",
                "slug": "oquv-va-darslik-shablonlari",
                "description": "Ish daftarlari, metodik qo'llanmalar va darslik maketlari",
                "icon": "academic-cap",
                "subcategories": [
                    {
                        "name": "O'quv qo'llanmalari va ish daftarlari",
                        "slug": "darslik-ish-daftarlari",
                        "product": {
                            "title": "O'quv markazlari uchun darslik va amaliy mashg'ulotlar ish daftari andozasi",
                            "short_description": "InDesign va Word da tahrirlanadigan, chop etishga tayyor 50 sahifalik maket.",
                            "description": "Mashqlar, qoidalar va eslatmalar bloklari qulay ajratilgan metodik andoza.",
                            "price": 22.00,
                            "file_format": "INDD, PDF, DOCX",
                            "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    },
                    {
                        "name": "Interaktiv test va viktorina andozalari",
                        "slug": "darslik-test-viktorinalar",
                        "product": {
                            "title": "Talabalar bilimini tekshirish uchun chiroyli bezatilgan savol-javob maketlari",
                            "short_description": "Ko'p variantli testlar, to'g'ri javoblar kaliti va ballar hisoblash jadvali.",
                            "description": "O'qituvchilar va murabbiylar uchun imtihonlarni qiziqarli o'tkazish vositasi.",
                            "price": 10.00,
                            "file_format": "DOCX, PPTX",
                            "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80",
                            "is_featured": False
                        }
                    }
                ]
            }
        ]
    }
]

def seed_data(db=None) -> dict:
    """
    3 Darajali Iyerarxiya bo'yicha ma'lumotlarni bazaga yuklaydi:
    - 6 ta 1-darajali (ota) kategoriya
    - 60 ta 2-darajali (ichki) kategoriya (har bir ota kategoriyada 10 tadan)
    - 120 ta 3-darajali (sub) kategoriya (har bir ichki kategoriyada 2 tadan)
    - 120 ta sifatli mahsulot (har bir sub-kategoriyada 1 tadan)
    Idempotent: qayta ishga tushirilganda mavjud bo'lganlarni qayta yaratmaydi.
    """
    close_db = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_db = True

    try:
        created_p = 0
        created_inner = 0
        created_sub = 0
        created_items = 0

        for parent_item in CATEGORIES_TREE:
            # 1. Ota kategoriya (Level 1)
            p_slug = parent_item["slug"]
            parent = db.query(Category).filter(Category.slug == p_slug).first()
            if not parent:
                parent = Category(
                    name=parent_item["name"],
                    slug=p_slug,
                    description=parent_item.get("description"),
                    icon=parent_item.get("icon"),
                    level=1,
                    parent_id=None
                )
                db.add(parent)
                db.commit()
                db.refresh(parent)
                created_p += 1

            # 2. Ichki kategoriyalar (Level 2)
            for inner_item in parent_item.get("inner_categories", []):
                in_slug = inner_item["slug"]
                inner = db.query(Category).filter(Category.slug == in_slug).first()
                if not inner:
                    inner = Category(
                        name=inner_item["name"],
                        slug=in_slug,
                        description=inner_item.get("description"),
                        icon=inner_item.get("icon"),
                        level=2,
                        parent_id=parent.id
                    )
                    db.add(inner)
                    db.commit()
                    db.refresh(inner)
                    created_inner += 1

                # 3. Sub-kategoriyalar (Level 3)
                for sub_item in inner_item.get("subcategories", []):
                    sub_slug = sub_item["slug"]
                    sub = db.query(Category).filter(Category.slug == sub_slug).first()
                    if not sub:
                        sub = Category(
                            name=sub_item["name"],
                            slug=sub_slug,
                            description=sub_item.get("description", f"{sub_item['name']} bo'yicha mahsulotlar"),
                            icon=sub_item.get("icon", inner.icon),
                            level=3,
                            parent_id=inner.id
                        )
                        db.add(sub)
                        db.commit()
                        db.refresh(sub)
                        created_sub += 1

                    # 4. Mahsulot (Card)
                    prod_data = sub_item.get("product")
                    if prod_data:
                        prod_slug = custom_slugify(prod_data["title"])
                        listing = db.query(Listing).filter(Listing.slug == prod_slug).first()
                        if not listing:
                            listing = Listing(
                                title=prod_data["title"],
                                slug=prod_slug,
                                short_description=prod_data.get("short_description"),
                                description=prod_data.get("description"),
                                price=prod_data["price"],
                                file_format=prod_data.get("file_format"),
                                image_url=prod_data.get("image_url"),
                                is_featured=prod_data.get("is_featured", False),
                                status="active",
                                views_count=10,
                                category_id=parent.id,
                                inner_category_id=inner.id,
                                subcategory_id=sub.id,
                                created_at=datetime.now(timezone.utc),
                                updated_at=datetime.now(timezone.utc)
                            )
                            db.add(listing)
                            db.commit()
                            db.refresh(listing)

                            # ListingImage galereyasi
                            main_url = prod_data.get("image_url")
                            if main_url:
                                img1 = ListingImage(
                                    listing_id=listing.id,
                                    image_url=main_url,
                                    is_main=True,
                                    order=0
                                )
                                db.add(img1)
                                img2 = ListingImage(
                                    listing_id=listing.id,
                                    image_url=main_url,
                                    is_main=False,
                                    order=1
                                )
                                db.add(img2)
                                db.commit()

                            created_items += 1

        print(f"[Seed 3-Level] Yakunlandi! Yangi yaratildi: {created_p} ota, {created_inner} ichki, {created_sub} sub-kategoriya, {created_items} listing.")
        return {
            "parents_created": created_p,
            "inner_created": created_inner,
            "sub_created": created_sub,
            "listings_created": created_items
        }

    except Exception as e:
        db.rollback()
        print(f"[Seed Error] Xatolik yuz berdi: {e}")
        raise e
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_data()
