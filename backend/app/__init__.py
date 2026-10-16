from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.error_handlers import register_error_handlers
from app.routers import health, ocr, registrations


def create_app():
    settings = get_settings()

    app = FastAPI(
        title="Mini KYC API",
        description="Identity registration and document verification API",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_error_handlers(app)

    app.include_router(health.router)
    app.include_router(ocr.router)
    app.include_router(registrations.router)

    return app