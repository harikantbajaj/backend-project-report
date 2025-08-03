from sqlalchemy import create_engine
from app.core.database import Base
from app.core.config import settings
import os

def init_db():
    """Initialize the database tables."""
    # Create models
    from app.models import user, report
    
    engine = create_engine(settings.DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def load_env():
    """Load environment variables from .env file."""
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

if __name__ == "__main__":
    load_env()
    init_db()
