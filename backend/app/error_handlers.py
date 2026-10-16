from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    BlurryImageError,
    DatabaseUnavailableError,
    DomainError,
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

STATUS_BY_ERROR: dict[type[DomainError], int] = {
    UnsupportedFileTypeError: 415,
    EmptyFileError: 400,
    FileTooLargeError: 413,
    InvalidImageError: 400,
    BlurryImageError: 422,
    InvalidDocumentDataError: 422,
    OcrServiceUnavailableError: 503,
    OcrInvalidResponseError: 502,
    DuplicateRegistrationError: 409,
    RegistrationPersistenceError: 500,
    DatabaseUnavailableError: 503,
}


async def domain_error_handler(request: Request, exc: DomainError):
    status_code = STATUS_BY_ERROR.get(type(exc), 500)

    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message},
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)