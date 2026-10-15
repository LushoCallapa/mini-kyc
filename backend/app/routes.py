import asyncio

from fastapi import APIRouter, HTTPException, File, UploadFile, status, Form
from google.genai.errors import APIError
from pydantic import EmailStr, ValidationError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database import check_database_connection, engine
from app.schemas import DocumentData, RegistrationCreate
from app.services.ocr_service import extract_document_data

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
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        ) from exc


@router.post("/ocr/extract")
async def extract_document_text(file: UploadFile = File(...)):
    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    try:
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
            document_data = await asyncio.to_thread(
                extract_document_data,
                content,
                file.content_type
            )

            validated_data = DocumentData.model_validate(document_data)

        except ValidationError as exc:
            raise HTTPException(
                status_code=422,
                detail="The document data is incomplete or invalid."
            ) from exc

        except APIError as exc:
            raise HTTPException(
                status_code=503,
                detail="The OCR service is temporarily unavailable. Please try again later."
            ) from exc

        except ValueError as exc:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an invalid response."
            ) from exc

        except RuntimeError as exc:
            raise HTTPException(
                status_code=500,
                detail="The OCR service is not configured."
            ) from exc

        return {
            "filename": file.filename,
            "document_data": validated_data.model_dump()
        }

    finally:
        await file.close()


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

    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Email or document number already registered."
        ) from exc

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not save the registration."
        ) from exc


@router.post(
    "/registrations/with-document",
    status_code=status.HTTP_201_CREATED
)
async def create_registration_with_document(
    email: EmailStr = Form(...),
    file: UploadFile = File(...)
):
    try:
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
            document_data = await asyncio.to_thread(
                extract_document_data,
                content,
                file.content_type
            )

            validated_data = DocumentData.model_validate(document_data)

        except ValidationError as exc:
            raise HTTPException(
                status_code=422,
                detail="The document data is incomplete or invalid."
            ) from exc

        except APIError as exc:
            raise HTTPException(
                status_code=503,
                detail="The OCR service is temporarily unavailable. Please try again later."
            ) from exc

        except ValueError as exc:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an invalid response."
            ) from exc

        except RuntimeError as exc:
            raise HTTPException(
                status_code=500,
                detail="The OCR service is not configured."
            ) from exc

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
                        "email": str(email),
                        "full_name": validated_data.full_name,
                        "document_number": validated_data.document_number
                    }
                )

                registration_id = result.lastrowid

        except IntegrityError as exc:
            raise HTTPException(
                status_code=409,
                detail="Email or document number already registered."
            ) from exc

        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=500,
                detail="Could not save the registration."
            ) from exc

        return {
            "id": registration_id,
            "email": str(email),
            "full_name": validated_data.full_name,
            "document_number": validated_data.document_number,
            "message": "Registration created successfully."
        }

    finally:
        await file.close()