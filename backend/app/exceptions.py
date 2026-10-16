class DomainError(Exception):
    """Base class for expected, controlled application errors."""

    default_message = "An unexpected error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class UnsupportedFileTypeError(DomainError):
    default_message = "Only JPEG, PNG, and WebP images are supported."


class EmptyFileError(DomainError):
    default_message = "The uploaded file is empty."


class FileTooLargeError(DomainError):
    default_message = "The uploaded file exceeds the 5 MB limit."


class InvalidImageError(DomainError):
    default_message = "The uploaded file is not a valid image."


class BlurryImageError(DomainError):
    default_message = "The image is too blurry. Please upload a clearer image."


class InvalidDocumentDataError(DomainError):
    default_message = "The document data is incomplete or invalid."


class OcrServiceUnavailableError(DomainError):
    default_message = (
        "The OCR service is temporarily unavailable. Please try again later."
    )


class OcrInvalidResponseError(DomainError):
    default_message = "The OCR service returned an invalid response."


class DuplicateRegistrationError(DomainError):
    default_message = "Email or document number already registered."


class RegistrationPersistenceError(DomainError):
    default_message = "Could not save the registration."


class DatabaseUnavailableError(DomainError):
    default_message = "Database connection failed."