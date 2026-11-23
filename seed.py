"""
Soff Backend - Seed script
Ushbu skript bazaga 6 ta ota kategoriya, 24 ta sub-kategoriya va
har bir sub-kategoriya uchun 5 tadan (jami 120 ta) real, sifatli mahsulotlarni yuklaydi.

Ishga tushirish: python seed.py
"""

from datetime import datetime, timezone
from app.database import SessionLocal, Base, engine
from app.models import Category, Listing, ListingImage
from app.utils import custom_slugify, generate_unique_slug

CATEGORIES_DATA = [
    {
        "name": "Ilmiy ishlar",
        "slug": "ilmiy-ishlar",
        "description": "Talabalar, magistrlar va tadqiqotchilar uchun ilmiy ishlar, referatlar va dissertatsiyalar",
        "icon": "academic-cap",
        "subcategories": [
            {
                "name": "Kurs ishlari",
                "slug": "kurs-ishlari",
                "description": "Barcha fan va yo'nalishlar bo'yicha sifatli, standartlarga mos kurs ishlari",
                "icon": "document-text",
                "items": [
                    {
                        "title": "Bank tizimida kredit risklarini boshqarish va baholash",
                        "short_description": "Tijorat banklarida kredit riskini tahlil qilish va kamaytirish usullari bo'yicha tayyor kurs ishi.",
                        "description": "Ushbu kurs ishi O'zbekiston Respublikasi tijorat banklari misolida kredit risklarini boshqarish tizimini o'rganadi. Barcha jadvallar, formulalar va 2024-yilgi statistik ma'lumotlar kiritilgan. Manbalar ro'yxati va ilovalar mavjud.",
                        "price": 15.00,
                        "file_format": "DOCX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Sun'iy intellektning tibbiyot diagnostikasida qo'llanilishi",
                        "short_description": "Tibbiy tasvirlarni tahlil qilishda chuqur o'rganish (Deep Learning) algoritmlari tadqiqoti.",
                        "description": "Zamonaviy sog'liqni saqlash tizimida sun'iy intellekt va kompyuter ko'rish texnologiyalarining samaradorligi. MRT va KT tasvirlarini tahlil qilish modellari solishtirilgan.",
                        "price": 18.00,
                        "file_format": "DOCX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Buxgalteriya hisobida audit va ichki nazorat mexanizmlari",
                        "short_description": "Korxonalarda moliyaviy hisobotlarning ishonchliligi va ichki audit tizimini takomillashtirish.",
                        "description": "Xalqaro moliyaviy hisobot standartlari (MHXS) asosida ichki auditni tashkil etish. Real korxona misolida balans va foyda-zarar hisoboti tahlil qilingan.",
                        "price": 12.00,
                        "file_format": "DOCX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Xalqaro savdo munosabatlarida bojxona tariflari tahlili",
                        "short_description": "Eksport va import operatsiyalarida bojxona-tarif tartibga solish tizimi samaradorligi.",
                        "description": "Jahon savdo tashkiloti (JST) talablari va O'zbekistonning tashqi savdo faoliyatida bojxona to'lovlarining o'rni to'liq yoritilgan.",
                        "price": 14.00,
                        "file_format": "DOCX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Zamonaviy pedagogik texnologiyalar va interfaol metodlar",
                        "short_description": "O'rta va oliy ta'limda interfaol metodlar hamda keys-stadilardan foydalanish metodikasi.",
                        "description": "Dars jarayonida o'quvchilar faolligini oshirish, muammoli ta'lim va blended learning (aralash ta'lim) texnologiyalarining amaliy qo'llanilishi.",
                        "price": 10.00,
                        "file_format": "DOCX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Diplom ishlari",
                "slug": "diplom-ishlari",
                "description": "Bakalavriat bitiruv malakaviy ishlari va to'liq himoya hujjatlari to'plami",
                "icon": "academic-cap",
                "items": [
                    {
                        "title": "Kompaniyalarda ERP tizimlarini joriy qilish samaradorligi",
                        "short_description": "Ishlab chiqarish jarayonlarini avtomatlashtirishda SAP va 1C tizimlarini integratsiya qilish.",
                        "description": "Bitiruv malakaviy ishi: O'rta va yirik korxonalarda ERP joriy etishning iqtisodiy samaradorligini hisoblash metodikasi, xarajatlar va daromadlar tahlili. Taqdimot va chizmalar to'liq taqdim etiladi.",
                        "price": 45.00,
                        "file_format": "DOCX, PDF, PPTX",
                        "image_url": "https://images.unsplash.com/photo-1532012164546-f432f2e37972?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Mikroservis arxitekturasi asosida fintech ilovalarini loyihalash",
                        "short_description": "Docker, Kubernetes va Kafka yordamida yuqori yuklamali to'lov tizimini ishlab chiqish.",
                        "description": "Amaliy dasturiy ta'minot loyihasi: Tranzaksiyalarni parallel qayta ishlash, ma'lumotlar izchilligi (ACID) va xavfsizlik protokollari. Manba kodi ilova qilingan.",
                        "price": 60.00,
                        "file_format": "DOCX, PDF, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "O'zbekistonda yashil energetika va quyosh panellari iqtisodiyoti",
                        "short_description": "Quyosh elektr stantsiyalarini barpo etishning texnik-iqtisodiy asoslari.",
                        "description": "Qayta tiklanuvchi energiya manbalarining O'zbekiston energetika balansidagi o'rni, investitsiyalarni qoplash muddatlari va ekologik foydasi.",
                        "price": 50.00,
                        "file_format": "DOCX, PDF, XLSX",
                        "image_url": "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Mashinali o'rganish yordamida birja narxlarini prognozlash",
                        "short_description": "LSTM neyron tarmoqlari va ARIMA modellari asosida vaqtli qatorlar bashorati.",
                        "description": "Moliyaviy bozorlarda qimmatli qog'ozlar narxi o'zgarishini aniqlash. Python tili kodi va Jupyter Notebook fayllari kiritilgan.",
                        "price": 55.00,
                        "file_format": "DOCX, PDF, IPYNB",
                        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Tijorat banklarining investitsiya portfelini optimallashtirish",
                        "short_description": "Markowitz modeli asosida bank aktivlarini diversifikatsiya qilish va riskni kamaytirish.",
                        "description": "Bank likvidligi va rentabelligini oshirishda investitsiya portfelini boshqarishning zamonaviy matematik usullari.",
                        "price": 40.00,
                        "file_format": "DOCX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Referat va taqdimotlar",
                "slug": "referat-va-taqdimotlar",
                "description": "Dolzarb mavzularda tayyorlangan referatlar, maqolalar va slaydlari",
                "icon": "presentation-chart-line",
                "items": [
                    {
                        "title": "Kiberxavfsizlik asoslari va tarmoq himoyasi taqdimoti",
                        "short_description": "Hackerlik hujumlaridan himoyalanish, shifrlash va xavfsizlik devorlari (Firewall).",
                        "description": "25 ta slayddan iborat chiroyli animatsiyali taqdimot va 15 betlik referat matni. Kibergigiena va zamonaviy tahdidlar haqida batafsil ma'lumot beradi.",
                        "price": 8.00,
                        "file_format": "PPTX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Iqtisodiy nazariya va bozor mexanizmlari referati",
                        "short_description": "Talab va taklif qonunlari, bozor muvozanati va narx shakllanishi qonuniyatlari.",
                        "description": "Klassik va neoklassik iqtisodiy maktablar qarashlari, inflyatsiya va ishsizlik o'rtasidagi bog'liqlik haqida batafsil referat.",
                        "price": 6.00,
                        "file_format": "DOCX, PPTX",
                        "image_url": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Gen muhandisligi va biotexnologiyaning zamonaviy yutuqlari",
                        "short_description": "CRISPR-Cas9 gen tahrirlash texnologiyasi va genetik modifikatsiyalangan organizmlar.",
                        "description": "Biotibbiyot va qishloq xo'jaligida gen injeneriyasi istiqbollari, bioetika masalalari yoritilgan ilmiy referat.",
                        "price": 7.50,
                        "file_format": "DOCX, PPTX",
                        "image_url": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Bulutli hisoblash (Cloud Computing) arxitekturasi va AWS",
                        "short_description": "IaaS, PaaS, SaaS modellari va Amazon Web Services asosiy xizmatlari tahlili.",
                        "description": "Serverless arxitekturasi, ma'lumotlarni saqlash va bulut xavfsizligini ta'minlash bo'yicha ilmiy taqdimot.",
                        "price": 9.00,
                        "file_format": "PPTX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Ekologik muammolar va barqaror rivojlanish maqsadlari",
                        "short_description": "Orol fojiasi oqibatlari, iqlim o'zgarishi va Orolbo'yi hududini tiklash loyihalari.",
                        "description": "BMT Barqaror Rivojlanish Maqsadlari doirasida O'zbekistonda ekologik barqarorlikni ta'minlash choralari.",
                        "price": 5.00,
                        "file_format": "PPTX, DOCX",
                        "image_url": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Dissertatsiyalar",
                "slug": "dissertatsiyalar",
                "description": "Magistrlik va PhD ilmiy dissertatsiyalari, avtoreferatlar va tadqiqotlar",
                "icon": "book-open",
                "items": [
                    {
                        "title": "Katta hajmli ma'lumotlarni qayta ishlashda taqsimlangan tizimlar tadqiqoti",
                        "short_description": "Apache Spark va Hadoop klasterlarida Big Data oqimlarini tahlil qilish algoritmlari.",
                        "description": "Magistrlik dissertatsiyasi: Katta ma'lumotlar oqimida real vaqt rejimida qaror qabul qilish tezligini 35% ga oshiruvchi yangi taqsimlangan kesh algoritmi ishlab chiqilgan.",
                        "price": 120.00,
                        "file_format": "PDF, DOCX",
                        "image_url": "https://images.unsplash.com/photo-1507842229451-79774619b06a?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Mintaqaviy iqtisodiyotni rivojlantirishda raqamli klasterlar modeli",
                        "short_description": "Hududiy iqtisodiy o'sishni ta'minlashda innovatsion sanoat klasterlari samaradorligi.",
                        "description": "PhD darajasidagi chuqur iqtisodiy tadqiqot: O'zbekiston viloyatlari misolida klasterlashuv jarayonlarining ekonometrik tahlili va prognoz modellari.",
                        "price": 110.00,
                        "file_format": "PDF, DOCX",
                        "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Sun'iy neyron tarmoqlari yordamida o'zbek tili matnlarini tahlil qilish",
                        "short_description": "O'zbek tili uchun BERT asosidagi transformator modeli va sentiment tahlili tizimi.",
                        "description": "NLP tadqiqoti: O'zbek tilidagi matnlarning tonalligini aniqlash va morfologik tahlil qilish uchun neyrotarmoq arxitekturasi va korpus ma'lumotlari.",
                        "price": 140.00,
                        "file_format": "PDF, DOCX, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Farmatsevtika sanoatida biotexnologik sintez jarayonlarini modellashtirish",
                        "short_description": "Dori vositalarini ishlab chiqarishda fermentativ reaksiyalar kinetikasi va optimallashtirish.",
                        "description": "Biokimyo va farmatsiya sohasidagi dissertatsiya ishi. Reaktorlardagi harorat va bosim parametrlarini boshqarishning matematik modellari.",
                        "price": 130.00,
                        "file_format": "PDF, DOCX",
                        "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Davlat moliyasini boshqarishda soliq mexanizmlarini takomillashtirish",
                        "short_description": "Yashirin iqtisodiyot ulushini qisqartirish va soliq bazasini kengaytirish strategiyasi.",
                        "description": "Davlat byudjeti barqarorligini ta'minlashda soliq ma'muriyatchiligini raqamlashtirishning ijtimoiy-iqtisodiy mexanizmlari.",
                        "price": 100.00,
                        "file_format": "PDF, DOCX",
                        "image_url": "https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            }
        ]
    },
    {
        "name": "Dizayn",
        "slug": "dizayn",
        "description": "Zamonaviy grafik dizayn, UI/UX interfeyslar, logotiplar va marketing materiallari",
        "icon": "paint-brush",
        "subcategories": [
            {
                "name": "UI/UX dizayn",
                "slug": "ui-ux-dizayn",
                "description": "Figma va Sketch uchun veb va mobil ilovalar interfeyslari, dizayn tizimlari",
                "icon": "device-phone-mobile",
                "items": [
                    {
                        "title": "Fintech mobil banking ilovasi to'liq UI/UX to'plami",
                        "short_description": "120+ ekran, Dark & Light mavzular, to'liq auto-layout va komponentlar tizimi.",
                        "description": "Bank ilovalari, hamyonlar va kartalar boshqaruvi uchun professional Figma dizayn to'plami. Barcha tranzaksiya ekranlari va onboarding oqimlari tayyor.",
                        "price": 35.00,
                        "file_format": "Figma",
                        "image_url": "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Zamonaviy E-commerce platformasi veb va mobil dizayni",
                        "short_description": "Kiyim va elektronika do'konlari uchun konversiyaga yo'naltirilgan UI Kit.",
                        "description": "Katalog, mahsulot sahifasi, savatcha va checkout jarayonlarini o'z ichiga olgan responsive Figma shabloni.",
                        "price": 40.00,
                        "file_format": "Figma",
                        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Tibbiy klinika va shifokorlar uchun CRM dizayn tizimi",
                        "short_description": "Bemorlar qabuli, tibbiy kartalar va jadval boshqaruvi uchun veb panel dizayni.",
                        "description": "Tibbiyot sohasi uchun murakkab jadvallar, grafiklar va statuslar bilan boyitilgan keng qamrovli Figma fayli.",
                        "price": 45.00,
                        "file_format": "Figma",
                        "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Oziq-ovqat yetkazib berish (Food Delivery) ilovasi prototipi",
                        "short_description": "Restoranlar menyusi, xarita va kuryer harakatini kuzatuvchi mobil interfeys.",
                        "description": "Jonli Figma interaktiv prototipi, mikro-animatsiyalar va 40 dan ortiq tayyor ekranlar.",
                        "price": 30.00,
                        "file_format": "Figma",
                        "image_url": "https://images.unsplash.com/photo-1526367790999-0150786686a2?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "SaaS boshqaruv paneli va analitika UI Kit",
                        "short_description": "Murakkab metrikalar, daromad grafiklari va foydalanuvchilar jadvali uchun panel.",
                        "description": "Dashboard yaratuvchilar uchun moslashuvchan, 200+ variantli komponentlar kutubxonasi.",
                        "price": 38.00,
                        "file_format": "Figma",
                        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Grafik dizayn",
                "slug": "grafik-dizayn",
                "description": "Bosma mahsulotlar, bannerlar, plakatlar va poligrafiya shablonlari",
                "icon": "photo",
                "items": [
                    {
                        "title": "Restoran va qahvaxona uchun premium menyu dizaynlari",
                        "short_description": "Elegent uslubdagi A4 va A3 buklanadigan menyu maketlari to'plami.",
                        "description": "Adobe Photoshop va Illustrator formatlarida to'liq tahrirlanadigan, CMYK bosmaga tayyor menyu shablonlari.",
                        "price": 20.00,
                        "file_format": "PSD, AI",
                        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Korporativ mahsulotlar uchun professional katalog shabloni",
                        "short_description": "24 sahifalik zamonaviy mahsulotlar taqdimoti va korporativ broshyura.",
                        "description": "Adobe InDesign va PDF formatlarida, matn va rasmlarni almashtirish juda oson bo'lgan katalog dizayni.",
                        "price": 25.00,
                        "file_format": "INDD, PDF",
                        "image_url": "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Bayram va tadbirlar uchun zamonaviy bannerlar to'plami",
                        "short_description": "Konferensiya, konsert va bayramona tadbirlar uchun rollup va tashqi bannerlar.",
                        "description": "Yuqori o'lchamdagi 10 ta tayyor reklama banneri, qatlamlari guruhlangan va qulay tartiblangan.",
                        "price": 15.00,
                        "file_format": "PSD, AI",
                        "image_url": "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Mahsulot qadoqlari (Packaging) va etiketkalar dizayn to'plami",
                        "short_description": "Qutilar, butilkalar va kofe stakanlari uchun dray-kat (dieline) chizmalari.",
                        "description": "Oziq-ovqat va kosmetika mahsulotlari uchun professional qadoq maketlari va 3D mockup fayllari.",
                        "price": 30.00,
                        "file_format": "AI, EPS, PSD",
                        "image_url": "https://images.unsplash.com/photo-1547949003-9792a18a2601?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Reklama bilbordlari va shahar formatidagi tashqi reklama maketlari",
                        "short_description": "3x6 metrli bilbordlar va avtobus bekatlari uchun yorqin reklama dizaynlari.",
                        "description": "Vektorli elementlar va yuqori aniqlikdagi PSD qatlamlariga ega tayyor tashqi reklama andozalari.",
                        "price": 22.00,
                        "file_format": "PSD, TIFF",
                        "image_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Logotip va brending",
                "slug": "logotip-va-brending",
                "description": "Korxona brendbuki, vizitkalar, firmenniy stil va vektorli logotiplar",
                "icon": "sparkles",
                "items": [
                    {
                        "title": "IT va texnologiya kompaniyalari uchun minimalist logotiplar",
                        "short_description": "15 ta unikal, zamonaviy va geometrik vektorli logotiplar to'plami.",
                        "description": "Barcha vektor formatlarda (AI, EPS, SVG) tayyorlangan. Rang va shriftlarni xohlagancha o'zgartirish mumkin.",
                        "price": 25.00,
                        "file_format": "AI, SVG, PNG",
                        "image_url": "https://images.unsplash.com/photo-1600132806370-bf17e65e942f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Qurilish va ko'chmas mulk agentliklari uchun to'liq brendbuk",
                        "short_description": "Logotip, vizitka, firma blanki, konvert va ishchi kiyimlar dizayni.",
                        "description": "Qurilish kompaniyasi uchun ishonchli va salobatli vizual stil yaratish uchun to'liq identifikatsiya paketi.",
                        "price": 35.00,
                        "file_format": "AI, PDF, PSD",
                        "image_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Kofe va qandolatchilik do'konlari uchun vizual identifikatsiya",
                        "short_description": "Iliq va shirin hissiyot uyg'otuvchi vintage & modern kofe brendingi.",
                        "description": "Kofe stakanlari, pergamot qog'ozlar va fasad yozuvlari uchun vektorli maketlar to'plami.",
                        "price": 28.00,
                        "file_format": "AI, EPS, SVG",
                        "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Kiyim brendi uchun premium logotip va firmenniy stil",
                        "short_description": "Fashion brendlar, tikuvchilik fabrikalari va atelyelar uchun nafis dizayn.",
                        "description": "Birkalar, sumkalar va lentali qadoqlar uchun tayyor monoxrom va tilla rangli logotip variantlari.",
                        "price": 32.00,
                        "file_format": "AI, PSD",
                        "image_url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Avto xizmat ko'rsatish markazlari uchun dinamik logotiplar",
                        "short_description": "Tyunig, detailing va avtoservislar uchun kuchli va tezkor logotip maketlari.",
                        "description": "Tezlik va sifat timsolini ifodalovchi 10 ta avtomobil mavzusidagi vektor logotip.",
                        "price": 20.00,
                        "file_format": "AI, SVG",
                        "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "SMM dizayn",
                "slug": "smm-dizayn",
                "description": "Instagram, Telegram va TikTok uchun postlar, stories va karusel shablonlari",
                "icon": "share",
                "items": [
                    {
                        "title": "Instagram Stories va Postlar uchun 50 ta tayyor shablon",
                        "short_description": "Canva va Photoshop formatlarida biznes, savdo va shaxsiy blog uchun.",
                        "description": "Har bir post qatlami tartiblangan, matn va fotosuratlarni 1 daqiqada almashtirib e'lon berish mumkin.",
                        "price": 18.00,
                        "file_format": "Canva, PSD",
                        "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Telegram kanallar uchun infografika va post dizaynlari",
                        "short_description": "Keng formatli infografikalar, e'lonlar va rubrikalar uchun shablonlar.",
                        "description": "O'quvchilar e'tiborini tortuvchi, statistikani oson ko'rsatuvchi 30 ta tayyor grafik qolip.",
                        "price": 15.00,
                        "file_format": "PSD, PNG",
                        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Kiyim-kechak do'konlari uchun Instagram e'lonlari to'plami",
                        "short_description": "Chegirmalar, yangi kolleksiyalar va lookbook taqdimoti uchun postlar.",
                        "description": "Moda olamiga mos zamonaviy tipografika va neytral fonga ega Canva va Figma shablonlari.",
                        "price": 16.00,
                        "file_format": "Canva, Figma",
                        "image_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "O'quv markazlari va kurslar uchun reklama postlari paketi",
                        "short_description": "Qabul boshlanishi, o'qituvchilar tanishuvi va natijalar haqidagi postlar.",
                        "description": "Ota-onalar va yoshlarni jalb qiluvchi yorqin, ishonchli ranglardagi 25 ta SMM shablon.",
                        "price": 14.00,
                        "file_format": "PSD, Canva",
                        "image_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Ekspert va shaxsiy brend uchun minimalist karusel shablonlari",
                        "short_description": "Ko'p sahifali ta'limiy karusellar uchun 10 ta uzluksiz chiziqli shablon.",
                        "description": "Instagramda saqlab olishlar (saves) sonini oshiruvchi estetik va qulay karusel dizayni.",
                        "price": 12.00,
                        "file_format": "Figma, Canva",
                        "image_url": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            }
        ]
    },
    {
        "name": "Web dasturlash",
        "slug": "web-dasturlash",
        "description": "Veb-saytlar, internet-do'konlar, admin panellar va Telegram botlar kodi",
        "icon": "code-bracket",
        "subcategories": [
            {
                "name": "Landing page",
                "slug": "landing-page",
                "description": "Konversiyasi yuqori bir sahifali saytlar, startup va xizmatlar taqdimoti",
                "icon": "globe-alt",
                "items": [
                    {
                        "title": "SaaS startaplar uchun Next.js 14 va Tailwind CSS Landing Page",
                        "short_description": "TypeScript, Framer Motion animatsiyalari, Dark mode va to'liq SEO sozlangan.",
                        "description": "Dasturiy mahsulotlar va SaaS servislar uchun mukammal landing page. Narxlar jadvali, mijozlar sharhlari va FAQ qismlari tayyor.",
                        "price": 45.00,
                        "file_format": "ZIP, Next.js, TS",
                        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Ko'chmas mulk agentligi uchun konversiyasi yuqori Landing Page",
                        "short_description": "Xonadonlar filtri, ipoteka kalkulyatori va aloqa formasi bilan birga.",
                        "description": "Toza HTML5, SCSS va JavaScript asosida yozilgan, tez yuklanadigan va mobil qurilmalarga moslashgan sayt.",
                        "price": 30.00,
                        "file_format": "HTML5, SCSS, JS",
                        "image_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Mobil ilova taqdimoti uchun animatsion Landing Page",
                        "short_description": "Ilova skrinshotlari, yuklab olish tugmalari va chiroyli 3D telefon mockup animatsiyasi.",
                        "description": "React va Tailwind CSS yordamida yaratilgan, App Store va Google Play havolalariga ega tayyor shablon.",
                        "price": 35.00,
                        "file_format": "React, Vite, CSS",
                        "image_url": "https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "IT kurslar va vebinarlar uchun ro'yxatdan o'tish sahifasi",
                        "short_description": "Vaqt hisoblagich (countdown timer), spikerlar bloki va Telegram botga ulanuvchi forma.",
                        "description": "Lead generation uchun maxsus optimallashtirilgan, har bir konversiya elementiga ega landing shabloni.",
                        "price": 25.00,
                        "file_format": "HTML, Tailwind, JS",
                        "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Restoran va kafelar uchun onlayn stol bron qilish sahifasi",
                        "short_description": "Menyu ko'rish, taomlar rasmlari va sanani tanlab stol band qilish funksiyasi.",
                        "description": "Vue 3 va Tailwind CSS yordamida ishlab chiqilgan zamonaviy restoran veb-sahifasi.",
                        "price": 32.00,
                        "file_format": "Vue 3, Tailwind",
                        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Internet do'kon (E-commerce)",
                "slug": "internet-dokon-e-commerce",
                "description": "To'liq funksional onlayn savdo platformalari, savatcha va to'lov tizimlari",
                "icon": "shopping-cart",
                "items": [
                    {
                        "title": "To'liq funksional kiyim do'koni (Next.js, FastAPI, PostgreSQL)",
                        "short_description": "Payme va Click to'lovlari, savatcha, buyurtmalar tarixi va admin paneli bilan.",
                        "description": "Monorepo arxitekturasi: Frontend Next.js 14, Backend FastAPI va PostgreSQL. Docker-compose orqali 1 daqiqada ishga tushadi.",
                        "price": 95.00,
                        "file_format": "ZIP, Docker, Python",
                        "image_url": "https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Elektronika do'koni uchun React va Node.js shabloni",
                        "short_description": "Mahsulotlar taqqoslash, sharhlar yozish va xarakteristikalar bo'yicha filter.",
                        "description": "Redux Toolkit bilan boshqariladigan zamonaviy internet-do'kon kodi. REST API to'liq sozlangan.",
                        "price": 80.00,
                        "file_format": "ZIP, React, Node",
                        "image_url": "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Gullar va sovg'alar do'koni uchun Telegram Web App (TWA) do'koni",
                        "short_description": "To'g'ridan-to'g'ri Telegram ichida ochiluvchi tezkor va chiroyli mini-ilova.",
                        "description": "Vue 3 va Python backend asosida yozilgan, foydalanuvchi manzilini avtomatik aniqlovchi TWA yechimi.",
                        "price": 65.00,
                        "file_format": "Vue 3, Python, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1561181286-d3fee7d55364?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Parfyumeriya do'koni uchun zamonaviy Tailwind e-commerce frontend",
                        "short_description": "Faqat frontend: Katalog, savatcha va buyurtma berish sahifalari.",
                        "description": "Juda chiroyli animatsiyalarga ega, har qanday backendga ulab ishlatish mumkin bo'lgan HTML/Tailwind shablon.",
                        "price": 40.00,
                        "file_format": "HTML, Tailwind, JS",
                        "image_url": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "B2B ulgurji savdo internet-do'koni shabloni",
                        "short_description": "Kompaniyalar uchun shartnomalar, hisob-fakturalar va ulgurji narxlar tizimi.",
                        "description": "Next.js va Prisma ORM bilan yozilgan, korxona va tadbirkorlar uchun moslashgan professional platforma.",
                        "price": 90.00,
                        "file_format": "Next.js, Prisma, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Admin panel & CRM",
                "slug": "admin-panel-crm",
                "description": "Ma'lumotlar bazasi boshqaruvi, statistik panellar va mijozlar hisobi tizimlari",
                "icon": "chart-pie",
                "items": [
                    {
                        "title": "Zamonaviy SaaS Admin Panel (Next.js App Router, Shadcn UI)",
                        "short_description": "To'liq tipizatsiyalangan, 20+ tayyor sahifalar, Dark mode va grafiklar.",
                        "description": "Foydalanuvchilar ro'yxati, rollar boshqaruvi, to'lovlar jadvali va analitika kartalari mavjud eng so'nggi texnologiyadagi admin panel.",
                        "price": 55.00,
                        "file_format": "ZIP, TypeScript",
                        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "O'quv markazlari uchun talabalarni boshqarish CRM tizimi",
                        "short_description": "Davomat, to'lovlar monitoringi, sms xabarnomalar va guruhlar jadvali.",
                        "description": "Vue 3 va FastAPI asosidagi yengil, tez ishlovchi o'quv markazi CRM platformasi kodi.",
                        "price": 75.00,
                        "file_format": "Vue 3, FastAPI, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Omborni boshqarish va tovarlar hisobi CRM shabloni",
                        "short_description": "Kirim-chiqim, qoldiq tovarlar ogohlantirishi va shtrix-kod integratsiyasi.",
                        "description": "React va Node.js da yaratilgan savdo va omborxona nazorati uchun to'liq yechim.",
                        "price": 70.00,
                        "file_format": "React, Node.js, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Klinikalar uchun bemorlar qabuli va xodimlar boshqaruv paneli",
                        "short_description": "Elektron navbat, shifokorlar ish jadvali va tashxislar arxivi.",
                        "description": "Tibbiyot muassasalari uchun qulay, shifokor va administrator rollari ajratilgan veb dastur.",
                        "price": 85.00,
                        "file_format": "Angular, NestJS, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1504813184591-01572f98c85f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Buyurtmalar va kuryerlar harakatini kuzatuvchi logistika paneli",
                        "short_description": "Interaktiv xarita (Leaflet), buyurtma statuslari va yetkazib berish vaqti hisobi.",
                        "description": "Yetkazib berish xizmatlari va dispetcherlar uchun maxsus tayyorlangan boshqaruv portali.",
                        "price": 60.00,
                        "file_format": "React, Tailwind, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Telegram botlar",
                "slug": "telegram-botlar",
                "description": "Python Aiogram, to'lov tizimlari va avtomatlashtirish botlari skriptlari",
                "icon": "chat-bubble-left-right",
                "items": [
                    {
                        "title": "Ko'p funksiyali Internet Do'kon Telegram Boti (Aiogram 3, Payme, Click)",
                        "short_description": "Katalog, savatcha, mahsulot qidirish, lokatsiya yuborish va avtomatik to'lov.",
                        "description": "Python 3.11 va Aiogram 3 asosida yozilgan, SQLAlchemy 2.0 va PostgreSQL bilan ishlaydigan mukammal bot kodi.",
                        "price": 50.00,
                        "file_format": "Python, PostgreSQL, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "O'quv markazlari uchun test o'tkazish va sertifikat beruvchi bot",
                        "short_description": "Savollar bazasi, vaqt chegarasi, ball hisoblash va PDF sertifikat generatsiyasi.",
                        "description": "Talabalardan avtomatik imtihon olib, natijalarni admin panelga va Excelga eksport qiluvchi bot.",
                        "price": 35.00,
                        "file_format": "Python, SQLite, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Restoranlar uchun buyurtma qabul qilish va lokatsiya oluvchi bot",
                        "short_description": "Taomlar rasmlari, narxlar, yetkazib berish manzilini xaritadan tanlash.",
                        "description": "Mijoz buyurtmasini qabul qilib, oshpaz va kuryer guruhlariga to'liq tafsiloti bilan yetkazuvchi tizim.",
                        "price": 45.00,
                        "file_format": "Aiogram 3, FastAPI, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Kanal va guruhlar uchun avtomatlashtirilgan moderator bot",
                        "short_description": "Spam va reklamalarni tozalash, yangi a'zolarni kutib olish va obuna tekshiruvi.",
                        "description": "Katta kanallar va guruhlarni 24/7 xavfsiz saqlash uchun mo'ljallangan tezkor asinxron bot.",
                        "price": 30.00,
                        "file_format": "Python, Redis, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Foydalanuvchilarni ro'yxatga oluvchi va anketa to'ldiruvchi bot",
                        "short_description": "Bosqichma-bosqich savollar, fayl va rasm qabul qilish, Google Sheets ga saqlash.",
                        "description": "Vakansiyalar va tadbirlarga qatnashuvchilardan ariza to'plovchi qulay FSM bot kodi.",
                        "price": 28.00,
                        "file_format": "Aiogram 3, SQLAlchemy, ZIP",
                        "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            }
        ]
    },
    {
        "name": "3D design",
        "slug": "3d-design",
        "description": "Blender, 3ds Max, Maya modellari, arxitektura vizualizatsiyasi va o'yin aktivlari",
        "icon": "cube",
        "subcategories": [
            {
                "name": "Interyer va arxitektura",
                "slug": "interyer-va-arxitektura",
                "description": "Xonadonlar, uylar, ofislar va landshaft dizayni fotorealistik sahnalari",
                "icon": "home",
                "items": [
                    {
                        "title": "Zamonaviy Neo-Klassika uslubidagi mehmonxona 3D interyeri",
                        "short_description": "3ds Max va Corona Renderer uchun tayyor materiallar, yorug'lik va render sozlangan.",
                        "description": "Yuqori darajadagi fotorealizmga ega yashash xonasi sahnasi. Mebel, lyustra va bezak buyumlari to'liq komplektda.",
                        "price": 50.00,
                        "file_format": "3ds Max, Corona, OBJ",
                        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Skandinaviya uslubidagi zamonaviy oshxona va studio xonadon modeli",
                        "short_description": "Blender Cycles uchun sozlangan, yog'och va marmar PBR teksturalarga ega sahna.",
                        "description": "Kompakt studio xonadon dizayni. Barcha maishiy texnika va yoritish uskunalari Blender formatida mavjud.",
                        "price": 45.00,
                        "file_format": "Blender, FBX, OBJ",
                        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Minimalist xususiy uy (Villa) 3D eksteryer va landshaft arxitekturasi",
                        "short_description": "Hovuz, bog' va 2 qavatli zamonaviy shisha fasadli villa arxitekturasi.",
                        "description": "Tashqi yoritish (HDRI), o'simliklar va yo'laklar bilan to'liq jihozlangan eksteryer sahnasi.",
                        "price": 65.00,
                        "file_format": "3ds Max, V-Ray, FBX",
                        "image_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Zamonaviy IT ofis va kovorking maydoni to'liq 3D sahnasi",
                        "short_description": "Open-space ish zonalari, majlislar xonasi va dam olish burchaklari.",
                        "description": "Ergonomik stollar, zamonaviy kreslo va o'simliklar bilan jihozlangan ofis 3D modeli.",
                        "price": 55.00,
                        "file_format": "Blender, OBJ, FBX",
                        "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Premium restoran zali va VIP xonalari 3D vizualizatsiyasi",
                        "short_description": "Tungi atmosfera, sham yorug'ligi va qimmatbaho baxmal mebellar renderi.",
                        "description": "Mehmonxona va restoran loyihalari uchun tayyor atmosfera va to'liq teksturalangan modellar to'plami.",
                        "price": 60.00,
                        "file_format": "3ds Max, Corona, FBX",
                        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "3D personajlar",
                "slug": "3d-personajlar",
                "description": "O'yinlar, animatsiyalar va filmlar uchun modellashtirilgan 3D qahramonlar",
                "icon": "user",
                "items": [
                    {
                        "title": "Kiberpank uslubidagi robot-jangchi 3D personaji (Rigged & Textured)",
                        "short_description": "Suyaklar tizimi (Rig) o'rnatilgan, animatsiyaga tayyor, 4K PBR teksturalar.",
                        "description": "Unreal Engine va Unity uchun optimallashtirilgan ilmiy-fantastik kiber jangchi modeli.",
                        "price": 40.00,
                        "file_format": "Blender, FBX, OBJ",
                        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Mobil o'yinlar uchun multfilm uslubidagi sevimli qahramon modeli",
                        "short_description": "Stylized 3D personaj, quvnoq emotsiyalar va yengil poligon to'ri (Low-poly).",
                        "description": "Kausal va arkada o'yinlar uchun mos, yugurish va sakrash bazaviy animatsiyalariga ega model.",
                        "price": 35.00,
                        "file_format": "Maya, FBX, OBJ",
                        "image_url": "https://images.unsplash.com/photo-1563089145-599997674d42?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Tarixiy sharqona jangchi personaji to'liq kiyimlari bilan",
                        "short_description": "Temuriylar davri sovutlari, dubulg'a va qilichi bilan jihozlangan personaj.",
                        "description": "ZBrush da haykaltaroshlik qilingan, Substance Painter da nozik detallari bo'yalgan ajoyib model.",
                        "price": 45.00,
                        "file_format": "ZBrush, Blender, FBX",
                        "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Fantastik ajdaho (Dragon Monster) 3D modeli animatsiyasi bilan",
                        "short_description": "Uchish, o'kirish va olov purkash animatsiyalariga ega fantastik maxluq.",
                        "description": "RPG va sarguzasht o'yinlari uchun mos, batafsil teri tangachalari teksturasiga ega maxluq.",
                        "price": 42.00,
                        "file_format": "Blender, FBX",
                        "image_url": "https://images.unsplash.com/photo-1563089145-599997674d42?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Low-poly uslubidagi 10 ta o'yin qahramoni to'plami",
                        "short_description": "Shahar aholisi: shifokor, politsiyachi, quruvchi, biznesmen va boshqalar.",
                        "description": "Giper-kausal o'yinlar uchun bitta umumiy rang palitrasiga ega yengil modellar to'plami.",
                        "price": 30.00,
                        "file_format": "FBX, OBJ, Blend",
                        "image_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "O'yin aktivlari (Game assets)",
                "slug": "oyin-aktivlari-game-assets",
                "description": "Unreal Engine va Unity uchun muhit, qurollar, transport va rekvizitlar",
                "icon": "puzzle-piece",
                "items": [
                    {
                        "title": "O'rta asrlar qal'asi va qurollar to'plami (Modular Castle Kit)",
                        "short_description": "Devorlar, minoralar, darvozalar va mash'alalar — o'z qal'angizni yarating.",
                        "description": "Unreal Engine 5 Nanite va Lumen tizimlariga to'liq moslangan, modulli o'rta asr aktivlar to'plami.",
                        "price": 50.00,
                        "file_format": "UE5, FBX, OBJ",
                        "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Poyga o'yinlari uchun 5 ta sport avtomobili modeli (Low-Poly)",
                        "short_description": "G'ildiraklari ajratilgan, salon va chiroqlari modellashtirilgan poyga mashinalari.",
                        "description": "Mobil va veb poygalar uchun tezkor yuklanuvchi, zamonaviy superkarlar modellari.",
                        "price": 38.00,
                        "file_format": "Unity, Blender, FBX",
                        "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Kosmik stantsiya va ilmiy laboratoriya modulli aktivlari",
                        "short_description": "Koridorlar, lyuklar, kompyuter terminallari va ilmiy uskunalar to'plami.",
                        "description": "Sci-Fi janridagi o'yinlar uchun PBR metall va shisha teksturalariga ega aktivlar paketi.",
                        "price": 45.00,
                        "file_format": "FBX, OBJ, PBR Textures",
                        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "O'yinlar uchun 50 ta PBR teksturali idishlar va atrof-muhit buyumlari",
                        "short_description": "Qutilar, bochkalar, palletlar, qurollar va maishiy chiqindi buyumlari.",
                        "description": "Har qanday 3D o'yin sahnasini to'ldirish va jonlantirish uchun prop aktivlar to'plami.",
                        "price": 35.00,
                        "file_format": "Blender, Unity, UE5",
                        "image_url": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Apokalipsis uslubidagi xaroba shahar modullari to'plami",
                        "short_description": "Buzilgan binolar, siniq oynalar, zanglagan avtomobillar va to'siqlar.",
                        "description": "Post-apokaliptik dunyo yaratish uchun yuqori darajada optimallashtirilgan o'yin aktivlari.",
                        "price": 48.00,
                        "file_format": "FBX, OBJ, Substance",
                        "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Mahsulot vizualizatsiyasi",
                "slug": "mahsulot-vizualizatsiyasi",
                "description": "Reklama roliklari, e'lonlar va qadoqlar uchun 3D fotorealistik sahnalar",
                "icon": "camera",
                "items": [
                    {
                        "title": "Smartfon va gadjetlar reklama vizualizatsiyasi sahnasi",
                        "short_description": "Blender Cycles studiya yoritishi, podium va aylanuvchi kamera animatsiyasi.",
                        "description": "Texnika mahsulotlarini jozibador ko'rsatish uchun tayyor professional 3D studio sahnasi.",
                        "price": 35.00,
                        "file_format": "Blender, Cycles, PSD",
                        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Parfyumeriya shishasi va suv tomchilari fotorealistik renderi",
                        "short_description": "Shisha sinishi, suyuqlik va sirtidagi real suv tomchilari generatori.",
                        "description": "Kosmetika va atir brendlari uchun qimmatbaho, premium vizual render maketi.",
                        "price": 40.00,
                        "file_format": "Cinema 4D, Octane, FBX",
                        "image_url": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Zamonaviy ergonomik soat va aksessuarlar 3D maketi",
                        "short_description": "Teri remeshok, tilla korpus va mexanik siferblatning eng mayda detallari.",
                        "description": "Zargarlik buyumlari va qo'l soatlarini reklama qilish uchun 8K teksturali model.",
                        "price": 30.00,
                        "file_format": "3ds Max, Corona, OBJ",
                        "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Ichimlik bankasi va qutilari uchun studio lighting sahnasi",
                        "short_description": "Alyuminiy banka (Can mockup) va muz bo'laklari bilan kompozitsiya.",
                        "description": "Yangi ichimlik dizaynlarini real hayotda qanday ko'rinishini ko'rsatish uchun qulay 3D maket.",
                        "price": 25.00,
                        "file_format": "Blender, PSD, OBJ",
                        "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Sport poyabzali (Sneakers) fotorealistik 3D modeli",
                        "short_description": "Mato to'qimasi, rezina taglik va iplarning batafsil 3D skaneri.",
                        "description": "Krossovka reklamasi va elektron tijorat uchun barcha burchaklardan ko'rishga mo'ljallangan model.",
                        "price": 38.00,
                        "file_format": "Blender, OBJ, 4K PBR",
                        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            }
        ]
    },
    {
        "name": "AI generation",
        "slug": "ai-generation",
        "description": "Sun'iy intellekt promptlari, AI artlar, video animatsiyalar va raqamli ovozlar",
        "icon": "cpu-chip",
        "subcategories": [
            {
                "name": "Promptlar to'plami",
                "slug": "promptlar-toplami",
                "description": "ChatGPT, Midjourney, Claude va DALL-E uchun sinovdan o'tgan master-promptlar",
                "icon": "command-line",
                "items": [
                    {
                        "title": "Midjourney v6 uchun 500 ta fotorealistik portret va interyer promptlari",
                        "short_description": "Parametrlar, yorug'lik turlari va kamera linzalari ko'rsatilgan professional qo'llanma.",
                        "description": "Studiyaviy sifatdagi inson portretlari va arxitektura durdonalarini generatsiya qilish uchun tayyor promptlar bazasi.",
                        "price": 12.00,
                        "file_format": "PDF, TXT",
                        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "ChatGPT va Claude uchun marketing va kopirayting master-promptlari",
                        "short_description": "Savdo matnlari, reklama sarlavhalari va email marketing uchun 300 ta maxsus formula.",
                        "description": "Biznes egalari va marketologlar uchun konversiya keltiruvchi matnlar yaratishda yordam beruvchi sinovdan o'tgan promptlar.",
                        "price": 15.00,
                        "file_format": "Notion, PDF",
                        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "DALL-E 3 orqali logotip va vektorli ikonalar yaratish uchun 300 prompt",
                        "short_description": "Toza fon, minimalist uslub va vektor illyustratsiyalar generatsiya qilish qoidalari.",
                        "description": "Grafik dizaynerlar uchun tezkor ilhom va vektor loyihalar uchun tayyor neyrotarmoq ko'rsatmalari.",
                        "price": 10.00,
                        "file_format": "PDF, DOCX",
                        "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Dasturchilar va kod yozish uchun maxsus AI yordamchi promptlar paketi",
                        "short_description": "Refaktoring, testlar yozish, arxitektura tahlili va buglarni tuzatish uchun.",
                        "description": "Senior dasturchi tajribasiga ega bo'lgan AI kod hamkorini sozlash bo'yicha batafsil ko'rsatmalar.",
                        "price": 14.00,
                        "file_format": "Markdown, PDF",
                        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Mahsulot reklamasi va tijorat suratlari uchun Midjourney formulalari",
                        "short_description": "E-commerce mahsulotlarini studiya sharoitida ko'rsatuvchi vizual promptlar.",
                        "description": "Kosmetika, kiyim, taqinchoq va elektronika tovarlarini qimmatbaho muhitda generatsiya qilish sirlari.",
                        "price": 16.00,
                        "file_format": "PDF, Sheets",
                        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "AI rasmlar va art",
                "slug": "ai-rasmlar-va-art",
                "description": "Neyrotarmoqlar tomonidan yaratilgan 4K/8K devor qog'ozlari, illyustratsiyalar va artlar",
                "icon": "photo",
                "items": [
                    {
                        "title": "Toshkent kelajakda: 4K sifatdagi fantastik AI konsept artlar to'plami",
                        "short_description": "Kiberpank va futuristik Toshkent ko'chalari, uchar mashinalar va yangi minoralari.",
                        "description": "50 ta ultra-yuqori aniqlikdagi san'at asari. Reklama, fon rasmlari va konseptlar uchun tayyor.",
                        "price": 20.00,
                        "file_format": "JPG, PNG 4K",
                        "image_url": "https://images.unsplash.com/photo-1686191128892-3b37add41544?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "O'zbek xalq ertaklari qahramonlarining zamonaviy AI illyustratsiyalari",
                        "short_description": "Semurg' qushi, Kenja botir va Zumrad-Qimmat qahramonlari yangi Disney uslubida.",
                        "description": "Bolalar kitoblari va animatsiyalar uchun ilhom beruvchi 40 ta rang-barang badiiy tasvir.",
                        "price": 22.00,
                        "file_format": "PNG, TIFF",
                        "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Abstrakt 3D neon va geometrik devor qog'ozlari (Wallpapers 8K)",
                        "short_description": "Ekranlar va monitorlar uchun ko'zni quvontiruvchi zamonaviy suyuq va neon shakllar.",
                        "description": "Grafik dizaynerlar va veb-saytlar foni uchun qulay bo'lgan 8K sifatdagi eksklyuziv fonlar.",
                        "price": 15.00,
                        "file_format": "JPG, PNG",
                        "image_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Kiberpank va retro anime uslubidagi personajlar to'plami",
                        "short_description": "90-yillar yapon animatsiyasi va kiberpank atmosferasi uyg'unlashgan artlar.",
                        "description": "Musiqa muqovalari, kiyim printlari va plakatlar uchun juda mos keladigan sifatli illyustratsiyalar.",
                        "price": 18.00,
                        "file_format": "PNG, PSD",
                        "image_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Arxitektura va landshaft dizayni uchun ilhomlantiruvchi AI kolleksiyasi",
                        "short_description": "Tabiat qo'ynidagi zamonaviy kottejlar va hayratlanarli landshaft kompozitsiyalari.",
                        "description": "Arxitektor va dizaynerlar uchun buyurtmachilarga g'oyalarni ko'rsatishda tayyor vizual material.",
                        "price": 16.00,
                        "file_format": "JPG 4K",
                        "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "AI video va animatsiya",
                "slug": "ai-video-va-animatsiya",
                "description": "Runway, Sora, Pika orqali yaratilgan qisqa videolar, fonlar va effektlar",
                "icon": "film",
                "items": [
                    {
                        "title": "Runway Gen-2 va Sora uslubidagi 20 ta dinamik AI video shablonlar",
                        "short_description": "4K 60fps sinematik harakatlar, kamera o'tishlari va tabiat hodisalari.",
                        "description": "Reklama videoroliklari uchun ajoyib b-roll kadrlar sifatida ishlatish mumkin bo'lgan videolar.",
                        "price": 35.00,
                        "file_format": "MP4, 4K",
                        "image_url": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "AI yordamida yaratilgan mahsulot taqdimot video-roliklari to'plami",
                        "short_description": "Tijorat tovarlarining havoda suzishi va chiroyli yorug'lik nurlari animatsiyasi.",
                        "description": "SMM roliklar va Instagram Reels uchun tayyor, musiqaga moslashtirilgan qisqa video shablonlar.",
                        "price": 40.00,
                        "file_format": "MP4, After Effects",
                        "image_url": "https://images.unsplash.com/photo-1536240478700-b869070f9279?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Ijtimoiy tarmoqlar uchun AI fon animatsiyalari va vizual effektlar",
                        "short_description": "Podkastlar va intervyular orqasiga qo'yish uchun uzluksiz aylanuvchi (loop) fonlar.",
                        "description": "Ekranni jonlantiruvchi va tomoshabin diqqatini ushlab turuvchi 15 ta zamonaviy AI video fon.",
                        "price": 25.00,
                        "file_format": "MP4, MOV",
                        "image_url": "https://images.unsplash.com/photo-1518173946687-a4c8a383392e?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Fantastik dunyolar bo'ylab sayohat: 60 FPS AI sinematik lavhalar",
                        "short_description": "Koinot, begona sayyoralar va suvosti shaharlari bo'ylab parvoz effektlari.",
                        "description": "Musiqiy kliplar va YouTube videolari uchun tayyorlangan hayajonli video montaj bo'laklari.",
                        "price": 30.00,
                        "file_format": "MP4, 4K",
                        "image_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "AI neyrotarmoqlar harakatini tasvirlovchi 3D abstrakt video fonlar",
                        "short_description": "Ma'lumotlar oqimi, kiber makon va sun'iy idrok ramzlarini ifodalovchi vizuallar.",
                        "description": "Texnologik konferensiyalar va IT loyihalar videolari uchun ayni muddao bo'lgan animatsiyalar.",
                        "price": 28.00,
                        "file_format": "MP4, ProRes",
                        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "AI ovoz va avatarlar",
                "slug": "ai-ovoz-va-avatarlar",
                "description": "O'zbek va xalqaro tillarda sintez qilingan AI diktor ovozlari va virtual avatarlar",
                "icon": "speaker-wave",
                "items": [
                    {
                        "title": "ElevenLabs uchun o'zbek tiliga moslashtirilgan diktor ovoz profillari",
                        "short_description": "Erkak va ayol ovozlari, ravon intonatsiya va emotsiyalarni to'g'ri yetkazish parametrlari.",
                        "description": "Matnlarni audio formatga o'tkazishda tabiiy va ta'sirchan jaranglovchi professional sozlamalar to'plami.",
                        "price": 25.00,
                        "file_format": "WAV, MP3, JSON",
                        "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Reklama roliklari uchun tayyor professional AI diktor ovozlari to'plami",
                        "short_description": "Energetik, ishonchli va tantanali ohangdagi 50 ta tayyor audio jumlalar.",
                        "description": "Radio va televideniye reklamalari, YouTube e'lonlari uchun tozalangan studiyaviy audio fayllar.",
                        "price": 30.00,
                        "file_format": "WAV, 24-bit",
                        "image_url": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "HeyGen va D-ID uchun 5 ta realizm darajasi yuqori video avatarlar",
                        "short_description": "Lab harakati (Lip-sync) mukammal sozlangan virtual boshlovchilar modeli.",
                        "description": "Kompaniya yangiliklari va o'quv darslarini olib borish uchun zamonaviy kiyingan AI suxandonlar.",
                        "price": 35.00,
                        "file_format": "MP4, PSD",
                        "image_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Podcast va audiokitoblar uchun sokin va ta'sirchan AI ovoz to'plami",
                        "short_description": "Uzoq matnlarni eshituvchini charchatmasdan o'qib beruvchi bariton ovoz.",
                        "description": "Adabiy asarlar va meditatsion audio kurslar yaratish uchun maxsus tayyorlangan vokal modeli.",
                        "price": 22.00,
                        "file_format": "WAV, MP3",
                        "image_url": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "YouTube Shorts va Reels uchun tezkor dublyaj AI ovoz shablonlari",
                        "short_description": "Qiziqarli faktlar va mem-videolar uchun ommabop, quloqqa yoquvchi ohanglar.",
                        "description": "Qisqa videolarda tomoshabin diqqatini birinchi soniyadanoq tortuvchi jarangdor audio to'plam.",
                        "price": 20.00,
                        "file_format": "MP3, WAV",
                        "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            }
        ]
    },
    {
        "name": "Shablonlar",
        "slug": "shablonlar",
        "description": "PowerPoint, Keynote, Rezyume (CV), Excel jadvallari va Notion shablonlari",
        "icon": "document-duplicate",
        "subcategories": [
            {
                "name": "PowerPoint & Keynote",
                "slug": "powerpoint-keynote",
                "description": "Biznes taqdimotlar, pitch deck, korporativ hisobotlar va slayd shablonlari",
                "icon": "presentation-chart-bar",
                "items": [
                    {
                        "title": "Startap va investitsiya jalb qilish uchun professional Pitch Deck",
                        "short_description": "Investorlar oldida chiqish qilish uchun 60 ta sinovdan o'tgan slayd maketi.",
                        "description": "Muammo, yechim, bozor hajmi (TAM, SAM, SOM) va moliya rejasini ko'rsatuvchi mukammal prezentatsiya.",
                        "price": 25.00,
                        "file_format": "PPTX, Keynote",
                        "image_url": "https://images.unsplash.com/photo-1542744094-3a31f272c490?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Yillik biznes hisobot va moliyaviy tahlil taqdimot shabloni (100+ slayd)",
                        "short_description": "Grafiklar, infografika, xaritalar va jadvallar bilan to'la boyitilgan shablon.",
                        "description": "Kompaniya rahbariyati va aksiyadorlariga yillik natijalarni chiroyli yetkazish uchun eng yaxshi slaydlar to'plami.",
                        "price": 22.00,
                        "file_format": "PPTX, Google Slides",
                        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Universitet va ilmiy konferensiyalar uchun minimalist akademik taqdimot",
                        "short_description": "Ortiqcha bezaklarsiz, ilmiy ma'lumotlarni aniq ko'rsatuvchi oq va ko'k rangli slaydlar.",
                        "description": "Magistrlik va doktorlik himoyalari uchun standartlarga to'liq mos keladigan akademik shablon.",
                        "price": 15.00,
                        "file_format": "PPTX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Marketing strategiyasi va savdo voronkasi vizual taqdimoti",
                        "short_description": "Brendni ilgari surish, mijoz portreti va reklama byudjeti taqsimoti slaydlari.",
                        "description": "Marketologlar va SMM agentliklari uchun mijozlarga strategiyani tushuntirishda eng qulay vosita.",
                        "price": 20.00,
                        "file_format": "PPTX, Keynote",
                        "image_url": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Kompaniya va mahsulot brend-prezentatsiyasi premium shabloni",
                        "short_description": "Qora va tilla ranglar uyg'unligidagi hashamatli mahsulot taqdimoti.",
                        "description": "Zargarlik, avtomobil yoki qimmatbaho xizmatlar taqdimoti uchun maxsus ishlab chiqilgan premium slaydlar.",
                        "price": 18.00,
                        "file_format": "PPTX, Canva",
                        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Rezyume (CV) shablonlari",
                "slug": "rezyume-cv-shablonlari",
                "description": "Ishga kirish imkoniyatini oshiruvchi zamonaviy, ATS-mos rezyume va portfolio andozalari",
                "icon": "identification",
                "items": [
                    {
                        "title": "Dasturchilar va IT mutaxassislari uchun ATS-mos professional Rezyume",
                        "short_description": "Kompaniyalar skaner tizimidan (ATS) 100% o'tadigan, tuzilishi aniq va toza shablon.",
                        "description": "Microsoft Word va Figma formatida, ko'nikmalar, loyihalar va tajribani ixcham ifodalovchi andoza.",
                        "price": 10.00,
                        "file_format": "DOCX, PDF, Figma",
                        "image_url": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Dizaynerlar va ijodiy kasblar uchun zamonaviy infografik portfolio CV",
                        "short_description": "O'ziga xos vizual estetika, yutuqlar ko'rsatkichi va loyihalar havolalari.",
                        "description": "Ish beruvchining diqqatini birinchi qarashdayoq tortuvchi, ijodiy erkinlikka ega dizayner rezyumesi.",
                        "price": 12.00,
                        "file_format": "Figma, PSD, PDF",
                        "image_url": "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Boshqaruvchilar (Management & HR) uchun klassik Yevropa standarti CV",
                        "short_description": "Menejerlar, rahbarlar va konsultantlar uchun rasmiy, obro'li 2 sahifalik shablon.",
                        "description": "Yetakchilik fazilatlari, boshqaruv ko'rsatkichlari va tavsiyanomalar blokiga ega klassik rezyume.",
                        "price": 8.00,
                        "file_format": "DOCX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Yangi bitiruvchilar va talabalar uchun ixcham 1 sahifalik rezyume",
                        "short_description": "Ish tajribasi kam bo'lgan yoshlar uchun ta'lim, amaliyot va yutuqlarni ko'rsatish.",
                        "description": "Boshlang'ich lavozimlarga (Junior / Intern) topshirish uchun qulay va to'ldirish oson andoza.",
                        "price": 6.00,
                        "file_format": "DOCX, Google Docs",
                        "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Xalqaro kompaniyalar (FAANG) uchun muvaffaqiyatli rezyume andozasi",
                        "short_description": "Google, Meta, Amazon talablariga mos, yutuqlarni raqamlar orqali ko'rsatish modeli.",
                        "description": "Garvard standarti asosidagi struktura, professional fe'llar ro'yxati va namunaviy matnlar kiritilgan.",
                        "price": 14.00,
                        "file_format": "DOCX, LaTeX, PDF",
                        "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Excel & Notion shablonlari",
                "slug": "excel-notion-shablonlari",
                "description": "Moliyaviy rejalashtirish, biznes boshqaruvi, CRM va vaqtni boshqarish tizimlari",
                "icon": "table-cells",
                "items": [
                    {
                        "title": "Shaxsiy moliya, daromad va xarajatlarni to'liq hisoblovchi Excel tizimi",
                        "short_description": "Avtomatik diagrammalar, oylik byudjet limiti va jamg'armalar monitoringi.",
                        "description": "Shaxsiy mablag'larni oqilona boshqarish, kutilmagan xarajatlarni aniqlash va tejash imkonini beruvchi formula va jadvallar.",
                        "price": 15.00,
                        "file_format": "XLSX, Google Sheets",
                        "image_url": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Notion uchun keng qamrovli Life & Business OS shabloni",
                        "short_description": "Vazifalar, maqsadlar, odatlar, kitoblar arxivi va loyihalar bir joyda.",
                        "description": "Kun tartibini rejalashtirish, loyihalar holatini kuzatish va shaxsiy samaradorlikni 2 barobar oshiruvchi Notion tizimi.",
                        "price": 20.00,
                        "file_format": "Notion Template",
                        "image_url": "https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Kichik biznes uchun ombor va savdo hisob-kitob Excel jadvali",
                        "short_description": "Tovarlar kirim-chiqimi, foyda va zarar (P&L) hisoboti, qarzdorliklar daftari.",
                        "description": "Qimmat CRM tizimlarini sotib olmasdan biznesni qulay boshqarish uchun avtomatlashtirilgan formula bilan to'ldirilgan jadval.",
                        "price": 18.00,
                        "file_format": "XLSX",
                        "image_url": "https://images.unsplash.com/photo-1543286386-713bdd548da4?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Frilanserlar uchun mijozlar va loyihalar boshqaruvi Notion CRM",
                        "short_description": "Mijozlar kontaktlari, to'lovlar holati, shartnomalar va portfolio havolalari.",
                        "description": "Buyurtmalar oqimini tartibga solish va muddatlarni (deadlines) o'tkazib yubormaslik uchun maxsus frilanserlar tizimi.",
                        "price": 16.00,
                        "file_format": "Notion Template",
                        "image_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Loyiha boshqaruvi va Gantt diagrammasi avtomatlashtirilgan Excel shabloni",
                        "short_description": "Vazifalar taqvimi, mas'ullar belgilanishi va loyiha bosqichlari foiz ko'rsatkichi.",
                        "description": "Scrum va Waterfall metodologiyalari asosida jamoaviy loyihalarni nazorat qilish uchun qulay shablon.",
                        "price": 14.00,
                        "file_format": "XLSX, Sheets",
                        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            },
            {
                "name": "Video montaj shablonlari",
                "slug": "video-montaj-shablonlari",
                "description": "Premiere Pro, After Effects va DaVinci Resolve uchun titrlar, o'tishlar va LUTs",
                "icon": "video-camera",
                "items": [
                    {
                        "title": "YouTube videolar uchun 50 ta dinamik sarlavha va subtitr shablonlari",
                        "short_description": "Premiere Pro MOGRT formatida, shrift va ranglarni bir tugma bilan o'zgartirish.",
                        "description": "Videoblogerlar uchun ko'rishlar sonini oshiruvchi trenddagi matn animatsiyalari va pastki uchinchi (lower third) titrlar.",
                        "price": 22.00,
                        "file_format": "Premiere Pro, MOGRT",
                        "image_url": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=800&q=80",
                        "is_featured": True
                    },
                    {
                        "title": "Instagram Reels va TikTok uchun o'ta dinamik trend o'tishlar (Transitions)",
                        "short_description": "Zoom, glitch, pan va whip o'tish effektlari to'plami audio effektlari (SFX) bilan.",
                        "description": "Qisqa videolarni professional montaj qilish va dinamikasini oshirish uchun qulay presetlar.",
                        "price": 18.00,
                        "file_format": "Premiere Pro, DaVinci",
                        "image_url": "https://images.unsplash.com/photo-1536240478700-b869070f9279?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Podkastlar va intervyular uchun animatsion pastki uchinchi (Lower Thirds)",
                        "short_description": "Spikerlar ismi, kasbi va ijtimoiy tarmoq nishonlari ko'rsatilgan nafis titrlar.",
                        "description": "YouTube podkastlari va suhbat videolari uchun minimalistik va professional animatsion maketlar.",
                        "price": 16.00,
                        "file_format": "After Effects, MOGRT",
                        "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Mahsulot reklamasi uchun tayyor 3D matn va logo animatsiyalari",
                        "short_description": "After Effects da yaratilgan aylanuvchi va porlovchi logo kirish (Intro) shablonlari.",
                        "description": "Har qanday kompaniya logotipini video boshida jozibali chiqarish uchun mo'ljallangan loyiha.",
                        "price": 24.00,
                        "file_format": "After Effects, AEP",
                        "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    },
                    {
                        "title": "Sinematik rang berish uchun 40 ta professional LUTs to'plami",
                        "short_description": "Sony, Canon, iPhone va Blackmagic kameralari uchun kino ranglari (Color Grading).",
                        "description": "Oddiy videoni Gollivud filmlari darajasidagi chuqur ranglar va kontrastga olib chiquvchi CUBE fayllar.",
                        "price": 15.00,
                        "file_format": "CUBE, 3DL",
                        "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=800&q=80",
                        "is_featured": False
                    }
                ]
            }
        ]
    }
]

def seed_data(db=None) -> dict:
    """
    Bazaga 6 ta ota kategoriya, 24 ta sub-kategoriya va 120 ta sifatli mahsulotni yuklaydi.
    Idempotent: Mavjud bo'lgan yozuvlarni qayta yaratmaydi va dublikat hosil qilmaydi.
    """
    close_db = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_db = True

    try:
        total_categories_created = 0
        total_subcategories_created = 0
        total_listings_created = 0

        for parent_data in CATEGORIES_DATA:
            # 1. Ota kategoriyani tekshirish yoki yaratish
            parent_slug = parent_data["slug"]
            parent = db.query(Category).filter(Category.slug == parent_slug).first()
            if not parent:
                parent = Category(
                    name=parent_data["name"],
                    slug=parent_slug,
                    description=parent_data.get("description"),
                    icon=parent_data.get("icon"),
                    parent_id=None
                )
                db.add(parent)
                db.commit()
                db.refresh(parent)
                total_categories_created += 1

            # 2. Sub-kategoriyalarni ko'rib chiqish
            for sub_data in parent_data.get("subcategories", []):
                sub_slug = sub_data["slug"]
                sub = db.query(Category).filter(Category.slug == sub_slug).first()
                if not sub:
                    sub = Category(
                        name=sub_data["name"],
                        slug=sub_slug,
                        description=sub_data.get("description"),
                        icon=sub_data.get("icon"),
                        parent_id=parent.id
                    )
                    db.add(sub)
                    db.commit()
                    db.refresh(sub)
                    total_subcategories_created += 1

                # 3. Sub-kategoriya ichidagi mahsulotlarni yuklash
                for item_data in sub_data.get("items", []):
                    item_slug = custom_slugify(item_data["title"])
                    existing_listing = db.query(Listing).filter(Listing.slug == item_slug).first()
                    if not existing_listing:
                        listing = Listing(
                            title=item_data["title"],
                            slug=item_slug,
                            short_description=item_data.get("short_description"),
                            description=item_data.get("description"),
                            price=item_data["price"],
                            file_format=item_data.get("file_format"),
                            image_url=item_data.get("image_url"),
                            is_featured=item_data.get("is_featured", False),
                            status="active",
                            views_count=15,
                            category_id=parent.id,
                            subcategory_id=sub.id,
                            created_at=datetime.now(timezone.utc),
                            updated_at=datetime.now(timezone.utc)
                        )
                        db.add(listing)
                        db.commit()
                        db.refresh(listing)

                        # Mahsulot uchun 2 ta galereya rasmini biriktirish
                        main_image_url = item_data.get("image_url")
                        if main_image_url:
                            img1 = ListingImage(
                                listing_id=listing.id,
                                image_url=main_image_url,
                                is_main=True,
                                order=0
                            )
                            db.add(img1)

                            # Qo'shimcha galereya rasmi
                            img2 = ListingImage(
                                listing_id=listing.id,
                                image_url=main_image_url,
                                is_main=False,
                                order=1
                            )
                            db.add(img2)
                            db.commit()

                        total_listings_created += 1

        print(f"[Seed] Yakunlandi! Yangi yaratildi: {total_categories_created} ota kategoriya, {total_subcategories_created} sub-kategoriya, {total_listings_created} listing.")
        return {
            "categories_created": total_categories_created,
            "subcategories_created": total_subcategories_created,
            "listings_created": total_listings_created
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
