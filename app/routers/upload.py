import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.schemas import ImageUploadResponse

router = APIRouter(prefix="/api/v1/upload", tags=["Upload"])

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "files")

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

@router.post("/image", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED, summary="Rasm yuklash")
async def upload_image(file: UploadFile = File(..., description="Yuklanadigan rasm fayli")):
    """
    Rasm faylini (JPG, JPEG, PNG, WEBP) qabul qiladi, unikal nom berib `files/` papkasiga saqlaydi
    va tayyor URL manzilini (`/files/<filename>`) qaytaradi.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fayl nomi ko'rsatilmadi"
        )

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fayl formati noto'g'ri. Faqat {', '.join(ALLOWED_IMAGE_EXTENSIONS)} formatlari qabul qilinadi."
        )

    os.makedirs(FILES_DIR, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    destination = os.path.join(FILES_DIR, unique_filename)

    content = await file.read()
    with open(destination, "wb") as f:
        f.write(content)

    return ImageUploadResponse(
        url=f"/files/{unique_filename}",
        filename=unique_filename
    )
