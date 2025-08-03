import pandas as pd
import numpy as np
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import json
from typing import List, Dict, Tuple
import io
from app.schemas.report import ReportData, ReportInsight
from app.models.report import Report
from app.utils.ml_model import health_predictor

# Normal ranges for common blood parameters (example values)
NORMAL_RANGES = {
    "Hemoglobin": {"min": 12.0, "max": 16.0, "unit": "g/dL"},
    "RBC": {"min": 4.0, "max": 5.5, "unit": "million/μL"},
    "WBC": {"min": 4.0, "max": 11.0, "unit": "thousand/μL"},
    "Platelets": {"min": 150.0, "max": 450.0, "unit": "thousand/μL"},
    "Glucose": {"min": 70.0, "max": 100.0, "unit": "mg/dL"},
    "Cholesterol": {"min": 0.0, "max": 200.0, "unit": "mg/dL"},
    "HDL": {"min": 40.0, "max": 60.0, "unit": "mg/dL"},
    "LDL": {"min": 0.0, "max": 130.0, "unit": "mg/dL"},
    "Triglycerides": {"min": 0.0, "max": 150.0, "unit": "mg/dL"},
}

# Health insights based on abnormal values
HEALTH_INSIGHTS = {
    "Hemoglobin": {
        "low": {
            "insight": "Possible anemia",
            "recommendation": "Consult a doctor for possible iron deficiency. Consider iron-rich foods like spinach, red meat, and legumes."
        },
        "high": {
            "insight": "Possible dehydration or other conditions",
            "recommendation": "Ensure adequate hydration and consult a doctor for further evaluation."
        }
    },
    "Glucose": {
        "high": {
            "insight": "Risk of diabetes",
            "recommendation": "Monitor blood sugar levels. Reduce sugar intake and consult a doctor."
        },
        "low": {
            "insight": "Possible hypoglycemia",
            "recommendation": "Eat regular meals and consult a doctor if symptoms persist."
        }
    },
    "Cholesterol": {
        "high": {
            "insight": "Risk of cardiovascular disease",
            "recommendation": "Reduce saturated fat intake, exercise regularly, and consult a doctor."
        }
    },
    "WBC": {
        "high": {
            "insight": "Possible infection or inflammation",
            "recommendation": "Monitor for signs of infection and consult a doctor if symptoms develop."
        },
        "low": {
            "insight": "Possible immune system issues",
            "recommendation": "Avoid exposure to infections and consult a doctor."
        }
    }
}

def process_report_file(file_path: str, file_type: str) -> Tuple[List[Dict], List[Dict], float]:
    """
    Process a report file (PDF, image, or CSV) and extract medical data.
    
    Returns:
        processed_data: List of ReportData objects
        insights: List of ReportInsight objects
        risk_score: Float representing overall risk score
    """
    # Extract text from file
    if file_type.startswith("image"):
        text = extract_text_from_image(file_path)
    elif file_type == "application/pdf":
        text = extract_text_from_pdf(file_path)
    elif file_type == "text/csv":
        text = extract_text_from_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Parse text to extract medical data
    extracted_data = parse_medical_data(text)
    
    # Classify data based on normal ranges
    processed_data = classify_data(extracted_data)
    
    # Generate health insights
    insights = generate_insights(processed_data)
    
    # Calculate risk score using ML model
    risk_score = calculate_ml_risk_score(extracted_data)
    
    return processed_data, insights, risk_score

def extract_text_from_image(file_path: str) -> str:
    """Extract text from an image file using OCR."""
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    pdf_document = fitz.open(file_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()
    pdf_document.close()
    return text

def extract_text_from_csv(file_path: str) -> str:
    """Extract text from a CSV file."""
    df = pd.read_csv(file_path)
    return df.to_string()

def parse_medical_data(text: str) -> Dict[str, float]:
    """
    Parse medical data from text.
    This is a simplified implementation - in practice, this would be more complex
    and might involve NLP techniques to identify parameter names and values.
    """
    # This is a simplified example - in practice, you'd want to use more sophisticated
    # NLP techniques to extract parameter names and values from the text
    data = {}
    
    # Simple keyword matching approach
    lines = text.split('\n')
    for line in lines:
        for parameter in NORMAL_RANGES.keys():
            if parameter.lower() in line.lower():
                # Try to extract a numeric value from the line
                import re
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    data[parameter] = float(numbers[0])
                    break
    
    return data

def classify_data(data: Dict[str, float]) -> List[Dict]:
    """Classify medical data based on normal ranges."""
    classified_data = []
    
    for parameter, value in data.items():
        if parameter in NORMAL_RANGES:
            range_info = NORMAL_RANGES[parameter]
            min_val = range_info["min"]
            max_val = range_info["max"]
            
            if value < min_val:
                classification = "Low"
            elif value > max_val:
                classification = "High"
            else:
                classification = "Normal"
            
            classified_data.append({
                "parameter": parameter,
                "value": value,
                "unit": range_info["unit"],
                "range_min": min_val,
                "range_max": max_val,
                "classification": classification
            })
    
    return classified_data

def generate_insights(processed_data: List[Dict]) -> List[Dict]:
    """Generate health insights based on classified data."""
    insights = []
    
    for data in processed_data:
        parameter = data["parameter"]
        classification = data["classification"]
        
        if parameter in HEALTH_INSIGHTS and classification in ["Low", "High"]:
            insight_info = HEALTH_INSIGHTS[parameter][classification.lower()]
            insights.append({
                "parameter": parameter,
                "insight": insight_info["insight"],
                "recommendation": insight_info["recommendation"]
            })
    
    return insights

def calculate_risk_score(processed_data: List[Dict]) -> float:
    """Calculate an overall risk score based on abnormal values."""
    total_abnormal = 0
    total_parameters = len(processed_data)
    
    if total_parameters == 0:
        return 0.0
    
    for data in processed_data:
        if data["classification"] in ["Low", "High"]:
            total_abnormal += 1
    
    # Risk score as percentage of abnormal parameters
    risk_score = (total_abnormal / total_parameters) * 100
    return risk_score

def calculate_ml_risk_score(extracted_data: Dict[str, float]) -> float:
    """Calculate risk score using ML model."""
    try:
        risk_score = health_predictor.predict_risk(extracted_data)
        return risk_score
    except Exception as e:
        # Fallback to rule-based risk calculation if ML model fails
        print(f"ML model prediction failed: {e}")
        return 50.0

def generate_trends(reports: List[Report]) -> Dict[str, List[Dict]]:
    """Generate trends for each parameter over time."""
    trends = {}
    
    # Collect all parameter values over time
    for report in reports:
        if report.processed_data:
            for data in report.processed_data:
                parameter = data["parameter"]
                if parameter not in trends:
                    trends[parameter] = []
                trends[parameter].append({
                    "date": report.created_at.isoformat(),
                    "value": data["value"],
                    "classification": data["classification"]
                })
    
    return trends

def generate_pdf_report(report: Report) -> bytes:
    """Generate a PDF report with the analysis results."""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    import io
    
    # Create a buffer to store the PDF
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Health Analytics Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Report metadata
    metadata = Paragraph(f"Report ID: {report.id} | Date: {report.created_at}", styles['Normal'])
    story.append(metadata)
    story.append(Spacer(1, 12))
    
    # Processed data table
    if report.processed_data:
        data = [["Parameter", "Value", "Unit", "Range", "Classification"]]
        for item in report.processed_data:
            data.append([
                item["parameter"],
                str(item["value"]),
                item["unit"],
                f"{item['range_min']}-{item['range_max']}",
                item["classification"]
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Test Results", styles['Heading2']))
        story.append(table)
        story.append(Spacer(1, 12))
    
    # Insights
    if report.insights:
        story.append(Paragraph("Health Insights", styles['Heading2']))
        for insight in report.insights:
            insight_text = f"<b>{insight['parameter']}:</b> {insight['insight']}"
            story.append(Paragraph(insight_text, styles['Normal']))
            story.append(Paragraph(f"Recommendation: {insight['recommendation']}", styles['Italic']))
            story.append(Spacer(1, 6))
    
    # Risk score
    if report.risk_score is not None:
        story.append(Paragraph("Risk Score", styles['Heading2']))
        story.append(Paragraph(f"Overall Risk Score: {report.risk_score:.2f}%", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data
