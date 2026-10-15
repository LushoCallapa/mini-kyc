from fastapi import APIRouter, HTTPException, File, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from app.services.ocr_service import extract_document_data
from app.database import check_database_connection, engine
from pydantic import ValidationError
from app.schemas import DocumentData, RegistrationCreate
from sqlalchemy import text

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

        validated_data = DocumentData.model_validate(document_data)

    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail="The document data is incomplete or invalid."
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc

    finally:
        await file.close()

    return {
        "filename": file.filename,
        "document_data": validated_data.model_dump()
    }

@router.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(registration: RegistrationCreate):
    query = text("""
        INSERT INTO onboarding_records (
            email,
            full_name,
            document_number
        )
        VALUES (
            :email,
            :full_name,
            :document_number
        )
    """)

    try:
        with engine.begin() as connection:
            result = connection.execute(
                query,
                {
                    "email": str(registration.email),
                    "full_name": registration.full_name,
                    "document_number": registration.document_number
                }
            )

            registration_id = result.lastrowid

        return {
            "id": registration_id,
            "email": str(registration.email),
            "full_name": registration.full_name,
            "document_number": registration.document_number,
            "message": "Registration created successfully."
        }

    except Exception as exc:
        from sqlalchemy.exc import IntegrityError

        if isinstance(exc, IntegrityError):
            raise HTTPException(
                status_code=409,
                detail="Email or document number already registered."
            ) from exc

        raise HTTPException(
            status_code=500,
            detail="Could not save the registration."
        ) from exc