import json
import os

from google import genai
from google.genai import types


PROMPT = """
Analyze the provided identity document image.

Extract only the following fields:
- full_name
- document_number

Do not guess, infer, or invent missing information.
If a field is unreadable or absent, return null.

Return only a JSON object with this structure:
{
    "full_name": "string or null",
    "document_number": "string or null"
}

Preserve names and document numbers as they appear.
"""


def extract_document_data(file_content: bytes, mime_type: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
        contents=[
            types.Part.from_bytes(
                data=file_content,
                mime_type=mime_type
            ),
            PROMPT
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    data = json.loads(response.text)

    return {
        "full_name": data.get("full_name"),
        "document_number": data.get("document_number")
    }