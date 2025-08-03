from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud import report as crud_report
from app.schemas.report import Report, ReportCreate, ReportHistory
from app.api.deps import get_current_user
from app.models.user import User
from app.services import report_processing

router = APIRouter()

@router.post("/upload", response_model=Report)
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save file temporarily
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Create report entry
    report_create = ReportCreate(
        file_name=file.filename,
        file_type=file.content_type
    )
    db_report = crud_report.create_report(db=db, report=report_create, user_id=current_user.id)
    
    # Process the report
    try:
        processed_data, insights, risk_score = report_processing.process_report_file(file_location, file.content_type)
        
        # Update report with processed data
        updated_report = crud_report.update_report_data(
            db=db,
            report_id=db_report.id,
            original_data={"file_name": file.filename},
            processed_data=processed_data,
            insights=insights,
            risk_score=risk_score
        )
        
        # Clean up temp file
        import os
        os.remove(file_location)
        
        return updated_report
    except Exception as e:
        # Clean up temp file
        import os
        os.remove(file_location)
        raise HTTPException(status_code=500, detail=f"Error processing report: {str(e)}")

@router.get("/{report_id}", response_model=Report)
def read_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_report = crud_report.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if db_report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this report")
    return db_report

@router.get("/history", response_model=ReportHistory)
def get_report_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reports = crud_report.get_reports_by_user(db, user_id=current_user.id)
    
    # Generate trends
    trends = report_processing.generate_trends(db_reports)
    
    return ReportHistory(reports=db_reports, trends=trends)

@router.get("/{report_id}/download")
def download_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_report = crud_report.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if db_report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this report")
    
    # Generate and return PDF
    pdf_data = report_processing.generate_pdf_report(db_report)
    
    from fastapi.responses import Response
    return Response(content=pdf_data, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=report_{report_id}.pdf"
    })
