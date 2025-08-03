import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib
from typing import Dict, List, Tuple

class HealthRiskPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_data(self, reports_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for training the model.
        In a real implementation, this would use actual historical data.
        """
        # This is a simplified example - in practice, you would have real historical data
        # For demonstration, we'll create synthetic data
        np.random.seed(42)
        
        # Generate synthetic data for training
        n_samples = 1000
        data = {
            'hemoglobin': np.random.normal(14, 2, n_samples),
            'wbc': np.random.normal(7.5, 2, n_samples),
            'rbc': np.random.normal(4.7, 0.5, n_samples),
            'platelets': np.random.normal(300, 100, n_samples),
            'glucose': np.random.normal(90, 20, n_samples),
            'cholesterol': np.random.normal(180, 50, n_samples),
            'hdl': np.random.normal(50, 15, n_samples),
            'ldl': np.random.normal(100, 40, n_samples),
            'triglycerides': np.random.normal(120, 60, n_samples),
        }
        
        # Create a risk factor based on abnormal values
        risk_factors = (
            (data['hemoglobin'] < 12) | (data['hemoglobin'] > 16) |
            (data['wbc'] < 4) | (data['wbc'] > 11) |
            (data['glucose'] > 100) |
            (data['cholesterol'] > 200)
        )
        
        # Convert to risk (1 = high risk, 0 = low risk)
        y = (risk_factors.sum() > 2).astype(int)
        
        # Create feature matrix
        X = np.column_stack([
            data['hemoglobin'],
            data['wbc'],
            data['rbc'],
            data['platelets'],
            data['glucose'],
            data['cholesterol'],
            data['hdl'],
            data['ldl'],
            data['triglycerides']
        ])
        
        return X, y
    
    def train_model(self, reports_data: List[Dict] = None):
        """
        Train the health risk prediction model.
        """
        # Prepare data
        X, y = self.prepare_data(reports_data)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = LogisticRegression(random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.is_trained = True
        
        return accuracy
    
    def predict_risk(self, report_data: Dict) -> float:
        """
        Predict health risk score for a given report.
        """
        if not self.is_trained or self.model is None:
            # If model is not trained, return a default risk score
            return 50.0
        
        # Extract features from report data
        features = []
        parameters = ['Hemoglobin', 'WBC', 'RBC', 'Platelets', 'Glucose', 'Cholesterol', 'HDL', 'LDL', 'Triglycerides']
        
        for param in parameters:
            if param in report_data:
                features.append(report_data[param])
            else:
                # Use default values if parameter not found
                default_values = {
                    'Hemoglobin': 14.0,
                    'WBC': 7.5,
                    'RBC': 4.7,
                    'Platelets': 300.0,
                    'Glucose': 90.0,
                    'Cholesterol': 180.0,
                    'HDL': 50.0,
                    'LDL': 100.0,
                    'Triglycerides': 120.0
                }
                features.append(default_values.get(param, 0.0))
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict probability
        risk_probability = self.model.predict_proba(features_scaled)[0][1]  # Probability of high risk
        risk_score = risk_probability * 100  # Convert to percentage
        
        return risk_score
    
    def save_model(self, filepath: str):
        """
        Save the trained model to a file.
        """
        if self.is_trained and self.model is not None:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """
        Load a trained model from a file.
        """
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.is_trained = model_data['is_trained']

# Initialize and train the model
health_predictor = HealthRiskPredictor()

# For demonstration, we'll train the model with synthetic data
# In a real implementation, this would be done with actual historical data
try:
    accuracy = health_predictor.train_model()
    print(f"Model trained with accuracy: {accuracy:.2f}")
    
    # Save the model
    health_predictor.save_model("health_risk_model.pkl")
except Exception as e:
    print(f"Error training model: {e}")
