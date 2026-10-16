from app.repositories.registration_repository import create_onboarding_record
from app.services.document_service import extract_document_from_image


def register_client(
    email: str,
    full_name: str,
    document_number: str,
) -> dict:
    return create_onboarding_record(
        email=email,
        full_name=full_name,
        document_number=document_number,
    )


def register_from_document(
    email: str,
    content: bytes,
    content_type: str | None,
) -> dict:
    document = extract_document_from_image(content, content_type)

    return register_client(
        email=email,
        full_name=document.full_name,
        document_number=document.document_number,
    )