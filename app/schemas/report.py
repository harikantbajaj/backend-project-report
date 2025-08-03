from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ReportBase(BaseModel):
    file_name: str
    file_type: str

class ReportCreate(ReportBase):
    pass

class ReportData(BaseModel):
    parameter: str
    value: float
    unit: str
    range_min: float
    range_max: float
    classification: str  # Normal, Low, High

class ReportInsight(BaseModel):
    parameter: str
    insight: str
    recommendation: str

class Report(ReportBase):
    id: int
    user_id: int
    original_data: Optional[Dict[str, Any]] = None
    processed_data: Optional[List[ReportData]] = None
    insights: Optional[List[ReportInsight]] = None
    risk_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReportHistory(BaseModel):
    reports: List[Report]
    trends: Dict[str, List[Dict[str, Any]]]  # Parameter trends over time
