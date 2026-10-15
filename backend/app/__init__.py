from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router


def create_app():
    app = FastAPI(
        title="Mini KYC API",
        description="Identity registration and document verification API",
        version="0.1.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app