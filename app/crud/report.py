from sqlalchemy.orm import Session
from app.models.report import Report
from app.schemas.report import ReportCreate
from typing import List

def get_report(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()

def get_reports_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Report).filter(Report.user_id == user_id).offset(skip).limit(limit).all()

def create_report(db: Session, report: ReportCreate, user_id: int):
    db_report = Report(
        file_name=report.file_name,
        file_type=report.file_type,
        user_id=user_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def update_report_data(db: Session, report_id: int, original_data: dict = None, processed_data: list = None, insights: list = None, risk_score: float = None):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report:
        if original_data is not None:
            db_report.original_data = original_data
        if processed_data is not None:
            db_report.processed_data = processed_data
        if insights is not None:
            db_report.insights = insights
        if risk_score is not None:
            db_report.risk_score = risk_score
        db.commit()
        db.refresh(db_report)
    return db_report
