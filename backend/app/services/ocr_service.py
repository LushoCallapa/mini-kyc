import json
import logging

from google import genai
from google.genai import types

from app.config import get_settings

logger = logging.getLogger(__name__)

PROMPT = """
Analyze the provided identity document image.

Extract only these fields:
- full_name
- document_number

Do not guess or invent missing information.
If a field is unreadable or absent, return null.

Return only a JSON object:
{
  "full_name": "string or null",
  "document_number": "string or null"
}

Preserve names and document numbers as they appear.
"""


def extract_document_data(file_content: bytes, mime_type: str) -> dict:
    settings = get_settings()
    client = genai.Client(api_key=settings.gemini_api_key)

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[
                types.Part.from_bytes(
                    data=file_content,
                    mime_type=mime_type,
                ),
                PROMPT,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0,
            ),
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        data = json.loads(response.text)

        if not isinstance(data, dict):
            raise ValueError("Gemini did not return a JSON object.")

        return {
            "full_name": data.get("full_name"),
            "document_number": data.get("document_number"),
        }

    except Exception:
        logger.exception("Gemini OCR failed. Model: %s", settings.gemini_model)
        raise