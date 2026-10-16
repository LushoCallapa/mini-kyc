import asyncio

from fastapi import APIRouter, File, Form, Query, UploadFile, status
from pydantic import EmailStr

from app.schemas import RegistrationCreate
from app.services.registration_service import (
    list_registrations,
    register_client,
    register_from_document,
)

router = APIRouter(prefix="/registrations", tags=["Registrations"])

REGISTRATION_CREATED_MESSAGE = "Registration created successfully."


@router.get("")
def get_registrations(limit: int = Query(default=100, ge=1, le=500)):
    return list_registrations(limit)


@router.post("", status_code=status.HTTP_201_CREATED)
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


@router.post("/with-document", status_code=status.HTTP_201_CREATED)
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