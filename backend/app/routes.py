import asyncio

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from google.genai.errors import APIError
from pydantic import EmailStr, ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database import (
    check_database_connection,
    create_onboarding_record,
)
from app.schemas import DocumentData, RegistrationCreate
from app.services.ocr_service import extract_document_data

router = APIRouter()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mini-kyc-api",
    }


@router.get("/health/database")
def database_health_check():
    try:
        check_database_connection()
        return {
            "status": "ok",
            "database": "connected",
        }
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed.",
        ) from exc


async def extract_uploaded_document(file: UploadFile) -> DocumentData:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Only JPEG, PNG, and WebP images are supported.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The uploaded file exceeds the 5 MB limit.",
        )

    try:
        document_data = await asyncio.to_thread(
            extract_document_data,
            content,
            file.content_type,
        )
        return DocumentData.model_validate(document_data)

    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail="The document data is incomplete or invalid.",
        ) from exc

    except APIError as exc:
        raise HTTPException(
            status_code=503,
            detail="The OCR service is temporarily unavailable. Please try again later.",
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail="The OCR service returned an invalid response.",
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail="The OCR service is not configured.",
        ) from exc


def save_registration(
    email: str,
    full_name: str,
    document_number: str,
) -> dict:
    try:
        return create_onboarding_record(
            email=email,
            full_name=full_name,
            document_number=document_number,
        )

    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Email or document number already registered.",
        ) from exc

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not save the registration.",
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve the created registration.",
        ) from exc


@router.post("/ocr/extract")
async def extract_document_text(file: UploadFile = File(...)):
    try:
        document_data = await extract_uploaded_document(file)

        return {
            "filename": file.filename,
            "document_data": document_data.model_dump(),
        }
    finally:
        await file.close()


@router.post(
    "/registrations",
    status_code=status.HTTP_201_CREATED,
)
def create_registration(registration: RegistrationCreate):
    record = save_registration(
        email=str(registration.email),
        full_name=registration.full_name,
        document_number=registration.document_number,
    )

    return {
        **record,
        "message": "Registration created successfully.",
    }


@router.post(
    "/registrations/with-document",
    status_code=status.HTTP_201_CREATED,
)
async def create_registration_with_document(
    email: EmailStr = Form(...),
    file: UploadFile = File(...),
):
    try:
        document_data = await extract_uploaded_document(file)

        record = await asyncio.to_thread(
            save_registration,
            str(email),
            document_data.full_name,
            document_data.document_number,
        )

        return {
            **record,
            "message": "Registration created successfully.",
        }
    finally:
        await file.close()
