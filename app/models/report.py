from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # PDF, IMAGE, CSV
    original_data = Column(JSON, nullable=True)  # Raw extracted data
    processed_data = Column(JSON, nullable=True)  # Parsed and classified data
    insights = Column(JSON, nullable=True)  # Health insights
    risk_score = Column(Float, nullable=True)  # ML-based risk prediction
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    user = relationship("User", back_populates="reports")

# Add relationship to User model
from app.models.user import User
User.reports = relationship("Report", back_populates="user")
