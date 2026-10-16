from google.genai.errors import APIError
from pydantic import ValidationError

from app.exceptions import (
    BlurryImageError,
    EmptyFileError,
    FileTooLargeError,
    InvalidDocumentDataError,
    InvalidImageError,
    OcrInvalidResponseError,
    OcrServiceUnavailableError,
    UnsupportedFileTypeError,
)
from app.schemas import DocumentData
from app.services.image_validation import is_image_blurry
from app.services.ocr_service import extract_document_data

ALLOWED_IMAGE_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_image_file(content: bytes, content_type: str | None) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise UnsupportedFileTypeError()

    if not content:
        raise EmptyFileError()

    if len(content) > MAX_FILE_SIZE:
        raise FileTooLargeError()

    try:
        blurry = is_image_blurry(content)
    except ValueError as exc:
        raise InvalidImageError() from exc

    if blurry:
        raise BlurryImageError()


def extract_document_from_image(
    content: bytes,
    content_type: str | None,
) -> DocumentData:
    validate_image_file(content, content_type)

    try:
        raw_data = extract_document_data(content, content_type)
        return DocumentData.model_validate(raw_data)

    except ValidationError as exc:
        raise InvalidDocumentDataError() from exc

    except APIError as exc:
        raise OcrServiceUnavailableError() from exc

    except ValueError as exc:
        raise OcrInvalidResponseError() from exc