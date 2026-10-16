from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database import engine
from app.exceptions import (
    DatabaseUnavailableError,
    DuplicateRegistrationError,
    RegistrationPersistenceError,
)


def create_onboarding_record(
    email: str,
    full_name: str,
    document_number: str,
) -> dict:
    query = text("""
        CALL sp_create_onboarding_record(
            :p_email,
            :p_full_name,
            :p_document_number
        )
    """)

    try:
        with engine.begin() as connection:
            result = connection.execute(
                query,
                {
                    "p_email": email,
                    "p_full_name": full_name,
                    "p_document_number": document_number,
                },
            )

            try:
                record = result.mappings().first()
            finally:
                result.close()

    except IntegrityError as exc:
        raise DuplicateRegistrationError() from exc

    except SQLAlchemyError as exc:
        raise RegistrationPersistenceError() from exc

    if record is None:
        raise RegistrationPersistenceError(
            "Could not retrieve the created registration."
        )

    return dict(record)


def list_onboarding_records(limit: int) -> list[dict]:
    query = text("""
        SELECT id, email, full_name, document_number, created_at
        FROM onboarding_records
        ORDER BY created_at DESC, id DESC
        LIMIT :limit
    """)

    try:
        with engine.connect() as connection:
            rows = connection.execute(query, {"limit": limit}).mappings().all()
    except SQLAlchemyError as exc:
        raise DatabaseUnavailableError() from exc

    return [dict(row) for row in rows]