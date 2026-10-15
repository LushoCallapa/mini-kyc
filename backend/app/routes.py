from fastapi import APIRouter, HTTPException, File, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from app.services.ocr_service import extract_document_data
from app.database import check_database_connection

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mini-kyc-api"
    }


@router.get("/health/database")
def database_health_check():
    try:
        check_database_connection()
        return {
            "status": "ok",
            "database": "connected"
        }
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )


@router.post("/ocr/extract")
async def extract_document_text(file: UploadFile = File(...)):
    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="Only JPEG, PNG, and WebP images are supported."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="The uploaded file exceeds the 5 MB limit."
        )

    try:
        document_data = extract_document_data(content, file.content_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "filename": file.filename,
        "document_data": document_data
    }
