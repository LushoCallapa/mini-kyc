# Mini KYC

Identity registration and document verification using OCR and artificial intelligence.

Mini KYC is a web application that allows users to register their identity by providing an email address and an image of an identity document. The backend extracts the document information using Google's Gemini API, validates the extracted data, and stores the registration in a MySQL database.

## Features

- **Identity registration:** Register users using an email address and identity document.
- **OCR integration:** Extract the full name and document number from document images using Gemini.
- **Data validation:** Validate extracted fields before saving them.
- **Duplicate prevention:** Enforce unique email addresses and document numbers.
- **REST API:** Provide endpoints for registration, OCR extraction, and health checks.
- **Frontend validation:** Validate email addresses, file types, and image sizes.
- **Environment configuration:** Keep API URLs and credentials configurable through environment variables.
- **CORS configuration:** Allow requests from the local frontend development server.

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
- Pydantic
- Google Gen AI SDK

### Database and infrastructure
- MySQL 8.4
- Docker Compose
- Google Gemini API

## Project structure

```text
mini-kyc/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   └── ocr_service.py
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── routes.py
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
│   │   ├── config/
│   │   ├── services/
│   │   ├── types/
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
git clone <REPOSITORY_URL>
cd mini-kyc
```

Replace `<REPOSITORY_URL>` with the URL of your repository.

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
```

Make sure `DB_PASSWORD` matches `MYSQL_ROOT_PASSWORD` and replace the Gemini API key with your own.

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

The schema creates the `mini_kyc` database and the `onboarding_records` table, including unique constraints for email addresses and document numbers.

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
- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Alternative API documentation: `http://127.0.0.1:8000/redoc`

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

The backend processes the image, validates the extracted fields, and attempts to save the registration in MySQL. Duplicate email addresses or document numbers are rejected.

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
4. The backend sends the image to Gemini for OCR extraction.
5. The backend validates the extracted full name and document number.
6. The backend checks database constraints and saves the registration.
7. The API returns the registration result or an appropriate error response.
8. The frontend displays the result to the user.

## Validation and error handling

The application validates data at both the frontend and backend levels.

- Invalid email addresses are rejected.
- Empty extracted fields are rejected.
- Unsupported image formats are rejected.
- Images larger than 5 MB are rejected.
- Duplicate emails and document numbers are rejected.
- OCR service failures are handled by the backend.
- Database connection and persistence errors are handled by the API.


## Development status

Mini KYC is under development. The current implementation includes the registration frontend, FastAPI backend, MySQL persistence, and Gemini-based OCR integration.

Further improvements may include automated tests, stronger runtime response validation, production deployment configuration, and additional document verification checks.
