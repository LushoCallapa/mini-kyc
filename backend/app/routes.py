import asyncio

from fastapi import APIRouter, File, Form, UploadFile, status
from google.genai.errors import APIError
from pydantic import EmailStr, ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database import (
    check_database_connection,
    create_onboarding_record,
)
from app.exceptions import (
    BlurryImageError,
    DatabaseUnavailableError,
    DuplicateRegistrationError,
    EmptyFileError,
    FileTooLargeError,
    InvalidDocumentDataError,
    InvalidImageError,
    OcrInvalidResponseError,
    OcrServiceUnavailableError,
    RegistrationPersistenceError,
    UnsupportedFileTypeError,
)
from app.schemas import DocumentData, RegistrationCreate
from app.services.image_validation import is_image_blurry
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
    except SQLAlchemyError as exc:
        raise DatabaseUnavailableError() from exc

    return {
        "status": "ok",
        "database": "connected",
    }


async def extract_uploaded_document(file: UploadFile) -> DocumentData:
    if file.content_type not in ALLOWED_TYPES:
        raise UnsupportedFileTypeError()

    content = await file.read()

    if not content:
        raise EmptyFileError()

    if len(content) > MAX_FILE_SIZE:
        raise FileTooLargeError()

    try:
        blurry = await asyncio.to_thread(is_image_blurry, content)
    except ValueError as exc:
        raise InvalidImageError() from exc

    if blurry:
        raise BlurryImageError()

    try:
        document_data = await asyncio.to_thread(
            extract_document_data,
            content,
            file.content_type,
        )

        return DocumentData.model_validate(document_data)

    except ValidationError as exc:
        raise InvalidDocumentDataError() from exc

    except APIError as exc:
        raise OcrServiceUnavailableError() from exc

    except ValueError as exc:
        raise OcrInvalidResponseError() from exc


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
        raise DuplicateRegistrationError() from exc

    except SQLAlchemyError as exc:
        raise RegistrationPersistenceError() from exc

    except RuntimeError as exc:
        raise RegistrationPersistenceError(
            "Could not retrieve the created registration."
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