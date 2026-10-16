import asyncio

from fastapi import APIRouter, File, Form, UploadFile, status
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError

from app.database import check_database_connection
from app.exceptions import DatabaseUnavailableError
from app.schemas import RegistrationCreate
from app.services.document_service import extract_document_from_image
from app.services.registration_service import (
    register_client,
    register_from_document,
)

router = APIRouter()

REGISTRATION_CREATED_MESSAGE = "Registration created successfully."


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


@router.post("/ocr/extract")
async def extract_document_text(file: UploadFile = File(...)):
    try:
        content = await file.read()

        document_data = await asyncio.to_thread(
            extract_document_from_image,
            content,
            file.content_type,
        )

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
    record = register_client(
        email=str(registration.email),
        full_name=registration.full_name,
        document_number=registration.document_number,
    )

    return {
        **record,
        "message": REGISTRATION_CREATED_MESSAGE,
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
        content = await file.read()

        record = await asyncio.to_thread(
            register_from_document,
            str(email),
            content,
            file.content_type,
        )

        return {
            **record,
            "message": REGISTRATION_CREATED_MESSAGE,
        }
    finally:
        await file.close()