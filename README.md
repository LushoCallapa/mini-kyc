
# Mini KYC - OCR ID

## Overview

Mini KYC is a document-based identity registration system
designed to extract and validate identity information using
Optical Character Recognition (OCR).

## Objectives

- Collect the user's email address.
- Receive an identity document.
- Extract relevant information from the document.
- Validate the extracted information.
- Store the registration data in a relational database.

## Planned Technologies

- Frontend: React and TypeScript.
- Backend: Python and Flask.
- Database: MySQL.
- Document Processing: OCR service.

## Project Structure

- `frontend/`: User interface.
- `backend/`: REST API and business logic.
- `database/`: Database schema and stored procedures.
- `docs/`: Technical documentation and design diagrams.

## Backend Setup

The backend uses Python and FastAPI.

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
python run.py.

## Database Connection

The backend connects to MySQL using SQLAlchemy and PyMySQL.

Configure the following environment variables in `backend/.env`:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

### Database Health Check

`GET /health/database` verifies the connection to MySQL.