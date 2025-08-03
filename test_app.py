import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test that all modules can be imported without errors."""
    try:
        # Test core modules
        from app.main import app
        from app.core.config import settings
        from app.core.database import Base
        print("✓ Core modules imported successfully")
        
        # Test models
        from app.models.user import User
        from app.models.report import Report
        print("✓ Models imported successfully")
        
        # Test schemas
        from app.schemas.user import UserCreate
        from app.schemas.report import ReportCreate
        print("✓ Schemas imported successfully")
        
        # Test CRUD operations
        from app.crud.user import create_user
        from app.crud.report import create_report
        print("✓ CRUD operations imported successfully")
        
        # Test API routes
        from app.api.v1 import auth, users, reports
        print("✓ API routes imported successfully")
        
        # Test services
        from app.services.report_processing import process_report_file
        print("✓ Services imported successfully")
        
        # Test utilities
        from app.utils.ml_model import health_predictor
        print("✓ Utilities imported successfully")
        
        print("\n🎉 All imports successful! The application structure is correct.")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_ml_model():
    """Test the ML model functionality."""
    try:
        from app.utils.ml_model import health_predictor
        # Test prediction with sample data
        sample_data = {
            "Hemoglobin": 13.5,
            "WBC": 7.2,
            "RBC": 4.8,
            "Platelets": 250.0,
            "Glucose": 85.0,
            "Cholesterol": 180.0,
            "HDL": 55.0,
            "LDL": 110.0,
            "Triglycerides": 120.0
        }
        
        risk_score = health_predictor.predict_risk(sample_data)
        print(f"✓ ML model prediction successful. Risk score: {risk_score:.2f}")
        return True
        
    except Exception as e:
        print(f"❌ ML model test error: {e}")
        return False

if __name__ == "__main__":
    print("Testing AI-Powered Health Analytics API...\n")
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Test ML model
    if not test_ml_model():
        sys.exit(1)
    
    print("\n🎉 All tests passed! The application is ready to run.")
