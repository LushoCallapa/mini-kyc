import asyncio

from fastapi import APIRouter, File, UploadFile

from app.services.document_service import extract_document_from_image

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/extract")
async def extract_document_text(file: UploadFile = File(...)):
    try:
        content = await file.read()

        document_data = await asyncio.to_thread(
            extract_document_from_image,
            content,
            file.content_type,
        )

        return {
            "filename": file.filename,
            "document_data": document_data.model_dump(),
        }
    finally:
        await file.close()