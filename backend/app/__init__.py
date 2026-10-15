from fastapi import FastAPI
from app.routes import router


def create_app():
    app = FastAPI(
        title="Mini KYC API",
        description="Identity registration and document verification API",
        version="0.1.0"
    )

    app.include_router(router)

    return app