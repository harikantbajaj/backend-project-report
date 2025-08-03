# AI-Powered Health Analytics API

A backend API that allows users to upload their blood test reports in various formats (PDF, image, or text). The system extracts relevant medical data, compares them against normal clinical ranges, and classifies each parameter as Normal, Low, or High.

## Features

- User Authentication & Management (JWT-based)
- Report Upload & Processing (PDF, image, or CSV files)
- OCR for text extraction from PDFs/images
- Range Validation & Classification
- Health Insights Engine
- User Health History & Trends
- Report Generation (PDF)
- ML-Based Risk Prediction

## Tech Stack

- Backend Framework: FastAPI
- Data Processing: Pandas, NumPy
- Database: PostgreSQL
- Authentication: JWT with FastAPI's security module
- OCR: Tesseract + PyMuPDF
- ML Model: Scikit-learn
- Report Generation: ReportLab
- Visualization: Matplotlib

## API Endpoints

- `POST /auth/signup` - Register user
- `POST /auth/login` - Login user
- `POST /report/upload` - Upload blood report
- `GET /report/{id}` - Get report details
- `GET /report/history` - Fetch all user reports with trends
- `GET /report/{id}/download` - Download PDF report

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file:
   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/health_db
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
app/
├── main.py              # Application entry point
├── core/                # Core configurations
├── api/                 # API routes
├── models/              # Database models
├── schemas/             # Pydantic schemas
├── crud/                # Database operations
├── services/            # Business logic
└── utils/               # Utility functions
