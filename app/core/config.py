from pydantic import BaseSettings
from typing import List, Optional
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Health Analytics API"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "health_db"
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Tesseract OCR
    TESSERACT_CMD: str = "tesseract"
    
    class Config:
        case_sensitive = True

settings = Settings()
