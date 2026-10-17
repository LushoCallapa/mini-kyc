import logging

from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from app.database import check_database_connection
from app.exceptions import DatabaseUnavailableError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check():
    return {
        "status": "ok",
        "service": "mini-kyc-api",
    }


@router.get("/database")
def database_health_check():
    try:
        check_database_connection()
    except SQLAlchemyError as exc:
        logger.exception("Database health check failed.")
        raise DatabaseUnavailableError() from exc

    return {
        "status": "ok",
        "database": "connected",
    }