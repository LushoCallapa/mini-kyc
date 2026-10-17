# Mini KYC

Identity registration and document verification using OCR and artificial intelligence.

Mini KYC is a web application that allows users to register their identity by providing an email address and an image of an identity document. The backend extracts the document information using Google's Gemini API, validates the extracted data, and stores the registration in a MySQL database through a stored procedure.

## Features

- **Identity registration:** Register users using an email address and identity document.
- **OCR integration:** Extract the full name and document number from document images using Gemini.
- **Blurry image detection:** Reject low-quality images before calling the OCR service.
- **Data validation:** Validate extracted fields before saving them.
- **Duplicate prevention:** Enforce unique email addresses and document numbers.
- **Stored procedure persistence:** Registrations are saved through `sp_create_onboarding_record`.
- **REST API:** Provide endpoints for registration, OCR extraction, and health checks, documented with Swagger.
- **Frontend validation:** Validate email addresses, file types, and image sizes.
- **Environment configuration:** All settings and credentials are loaded from environment variables.
- **CORS configuration:** Allowed origins are configurable through `CORS_ORIGINS`.

## Technologies

### Frontend
- React
- TypeScript
- Vite
- Formik
- Yup
- CSS

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- PyMySQL
- Pydantic and pydantic-settings
- OpenCV (blur detection)
- Google Gen AI SDK

### Database and infrastructure
- MySQL 8.4
- Docker Compose
- Google Gemini API

## Stack justification

- **React + TypeScript + Vite:** component-based UI with static typing and a fast development workflow.
- **Formik + Yup:** declarative form handling and a validation schema kept outside the component.
- **FastAPI:** native `multipart/form-data` support, Pydantic validation, and automatic Swagger documentation.
- **MySQL + stored procedures:** relational model with unique constraints and persistence encapsulated in the database.
- **Gemini:** multimodal model that extracts structured fields directly from the document image.
- **Docker Compose:** reproducible local database.

## Architecture

The backend separates responsibilities into layers. Each layer only depends on the one below it.

```text
Router  ->  Service  ->  Repository  ->  Stored procedure (MySQL)
                |
                +------>  OCR service (Gemini)
```

- **Routers (`routers/`):** receive HTTP requests, read uploaded files, and return responses. They contain no business logic.
- **Services (`services/`):** business logic. File validation, blur detection, OCR extraction, and registration flow. They know nothing about HTTP.
- **Repositories (`repositories/`):** data access. Calls the stored procedure and translates database errors into domain errors.
- **Exceptions (`exceptions.py`):** domain errors raised by services and repositories.
- **Error handlers (`error_handlers.py`):** a single place that maps domain errors to HTTP responses.
- **Config (`config.py`):** all settings are read once from environment variables.

The frontend follows the same idea:

- **Components:** presentation only.
- **Hooks:** state and side effects (`useRegistration`, `useFilePreview`, `useScrollIntoViewOnMobile`).
- **Services:** HTTP communication (`apiClient`, `registrationService`).
- **Validation and config:** form schema and constants kept outside components.

## Project structure

```text
mini-kyc/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   ├── ocr.py
│   │   │   └── registrations.py
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   ├── image_validation.py
│   │   │   ├── ocr_service.py
│   │   │   └── registration_service.py
│   │   ├── repositories/
│   │   │   └── registration_repository.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── error_handlers.py
│   │   ├── exceptions.py
│   │   └── schemas.py
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── database/
│   └── schema.sql
├── docs/
│   ├── data-model.mmd
│   └── sequence-diagram.mmd
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── icons/
│   │   │   ├── FileUploadField.tsx
│   │   │   ├── Navbar.tsx
│   │   │   ├── RecognitionResult.tsx
│   │   │   └── RegistrationForm.tsx
│   │   ├── config/
│   │   │   ├── env.ts
│   │   │   ├── layout.ts
│   │   │   └── upload.ts
│   │   ├── hooks/
│   │   │   ├── useFilePreview.ts
│   │   │   ├── useRegistration.ts
│   │   │   └── useScrollIntoViewOnMobile.ts
│   │   ├── services/
│   │   │   ├── apiClient.ts
│   │   │   └── registrationService.ts
│   │   ├── types/
│   │   ├── validation/
│   │   │   └── registrationSchema.ts
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── main.tsx
│   ├── .env.example
│   └── package.json
├── .env.example
├── .gitignore
├── compose.yaml
├── README.md
└── ...
```

## Requirements

Install the following tools before running the project:

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) and npm
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

## Configuration

### 1. Clone the repository

```bash
git clone https://github.com/LushoCallapa/mini-kyc.git
cd mini-kyc
```

### 2. Configure the root environment

Create a `.env` file in the project root using `.env.example` as a template.

```dotenv
MYSQL_ROOT_PASSWORD=your_mysql_password
```

Use a secure password of your choice.

### 3. Configure the backend environment

Create `backend/.env` using `backend/.env.example` as a template.

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=mini_kyc
DB_USER=root
DB_PASSWORD=your_mysql_password

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.1-flash-lite

CORS_ORIGINS=http://localhost:5173
```

Make sure `DB_PASSWORD` matches `MYSQL_ROOT_PASSWORD` and replace the Gemini API key with your own.

All variables are required. The API will not start if one is missing.

`CORS_ORIGINS` accepts several origins separated by commas. When you deploy, set it to the public URL of the frontend.

The Gemini model shown above is an example. Use a model ID currently supported by your API key and account.

### 4. Configure the frontend environment

Create `frontend/.env` using `frontend/.env.example` as a template.

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

This variable defines the base URL used by the frontend to communicate with the backend.

## Database setup

### 1. Start MySQL

From the project root, run:

```bash
docker compose up -d mysql
```

Verify that the container is running:

```bash
docker compose ps
```

### 2. Create the database tables

Apply the SQL schema:

```bash
docker exec -e MYSQL_PWD=your_mysql_password -i mini-kyc-mysql mysql -u root < database/schema.sql
```

Replace `your_mysql_password` with the value configured in the root `.env` file.

The schema creates the `mini_kyc` database, the `onboarding_records` table (with unique constraints for email addresses and document numbers), and the `sp_create_onboarding_record` stored procedure.

> **Note:** If your existing database already contains data, review the SQL before applying any changes that could delete or recreate tables.

## Backend setup

### 1. Open the backend directory

```bash
cd backend
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, activate the environment using the appropriate method for your system.

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the API

```bash
python run.py
```

The backend will be available at:

- API base URL: `http://127.0.0.1:8000`
- Interactive API documentation (Swagger): `http://127.0.0.1:8000/docs`

## Frontend setup

Open a separate terminal.

### 1. Navigate to the frontend

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

Vite will display the local URL, usually:

`http://localhost:5173`

Open that address in your browser.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check API availability. |
| `GET` | `/health/database` | Check database connectivity. |
| `POST` | `/ocr/extract` | Extract identity information from an image. |
| `POST` | `/registrations` | Create a registration using JSON data. |
| `POST` | `/registrations/with-document` | Extract document information and create a registration. |

### Registration with an identity document

The endpoint `POST /registrations/with-document` expects a `multipart/form-data` request with:

- `email`: user's email address.
- `file`: identity document image.

Supported image formats are JPEG, PNG, and WebP, with a maximum size of 5 MB.

The backend validates the image, extracts the data with Gemini, validates the extracted fields, and saves the registration in MySQL. Duplicate email addresses or document numbers are rejected.

### Example request

```bash
curl -X POST \
  http://127.0.0.1:8000/registrations/with-document \
  -F "email=user@example.com" \
  -F "file=@document.jpg"
```

Replace `document.jpg` with the path to an image you are authorized to use for testing.

## Application workflow

1. The user enters an email address and selects an identity document image.
2. The frontend validates the email, file type, and file size.
3. The frontend sends the form to the FastAPI backend.
4. The backend validates the file type, size, and sharpness.
5. The backend sends the image to Gemini for OCR extraction.
6. The backend validates the extracted full name and document number.
7. The repository calls the stored procedure, which checks database constraints and saves the registration.
8. The API returns the registration result or an appropriate error response.
9. The frontend displays the result to the user.

## Validation and error handling

The application validates data at both the frontend and backend levels. The backend never returns a generic 500 for invalid input: services raise domain errors and a global handler converts them into controlled responses.

| Case | HTTP status |
|---|---|
| Unsupported file type | 415 |
| Empty file | 400 |
| File larger than 5 MB | 413 |
| File is not a valid image | 400 |
| Blurry image | 422 |
| Incomplete or invalid extracted data | 422 |
| OCR service unavailable | 503 |
| OCR service invalid response | 502 |
| Duplicate email or document number | 409 |
| Could not save the registration | 500 |
| Database unavailable | 503 |

## Development status

Mini KYC is under development. The current implementation includes the registration frontend, FastAPI backend, MySQL persistence, and Gemini-based OCR integration.

Further improvements may include automated tests, stronger runtime response validation, production deployment configuration, and additional document verification checks.