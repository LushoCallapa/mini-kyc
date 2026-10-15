from pydantic import BaseModel, EmailStr, Field, field_validator


class DocumentData(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    document_number: str = Field(min_length=1, max_length=50)

    @field_validator("full_name", "document_number")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be blank.")

        return value


class RegistrationCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=200)
    document_number: str = Field(min_length=1, max_length=50)

    @field_validator("full_name", "document_number")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be blank.")

        return value