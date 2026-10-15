
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
