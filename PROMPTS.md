# PROMPTS

Prompt used with the AI/OCR service (Google Gemini) in the Mini KYC project.

- **Where it lives:** `backend/app/services/ocr_service.py`
- **Model:** configured through the `GEMINI_MODEL` environment variable
- **Settings:** `temperature=0` and `response_mime_type="application/json"`

## Identity document extraction

```text
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
```

## Design decisions

- Only two fields are requested, which keeps the output small and reliable.
- The model is told not to guess. A `null` value is rejected by the backend schema validation, so incomplete data is never stored.
- JSON-only output avoids parsing free text.

## Coding assistant

Claude (Anthropic) was used as a coding assistant. Prompts were written in Spanish and are translated here.

**1. Separation of responsibilities (requirement R3.8)**

```text
Here is the assignment PDF and my GitHub repository. What is missing for
"Best practices and architecture: separation of responsibilities"?
```

Follow-up: refactor the frontend and backend step by step (hooks, API client, centralized settings, domain exceptions, repository, services, routers). All configuration must come from the `.env` file, with no default values in the code.

**2. Registered users tab**

```text
I want to add a new tab that shows the registered users.
```

Result: a `GET /registrations` endpoint (router, service, repository) and a "Registered users" tab in the frontend.