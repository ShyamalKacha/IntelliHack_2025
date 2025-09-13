import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetector:
    def __init__(self):
        # Load the trained model and encoders
        self.model = joblib.load('anomaly_detection_model.pkl')
        self.scaler = joblib.load('scaler.pkl')
        self.geo_encoder = joblib.load('geo_encoder.pkl')
        self.device_encoder = joblib.load('device_encoder.pkl')
        
    def preprocess_data(self, data):
        """
        Preprocess the input data for prediction
        """
        # Convert timestamp to datetime
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Extract time-based features
        data['login_hour'] = data['timestamp'].dt.hour
        data['login_day'] = data['timestamp'].dt.day
        data['login_month'] = data['timestamp'].dt.month
        data['login_year'] = data['timestamp'].dt.year
        data['login_weekday'] = data['timestamp'].dt.weekday
        
        # Encode categorical variables (handle unseen categories)
        data['geo_location_encoded'] = data['geo_location'].apply(
            lambda x: self.geo_encoder.transform([x])[0] if x in self.geo_encoder.classes_ else -1
        )
        
        data['device_id_encoded'] = data['device_id'].apply(
            lambda x: self.device_encoder.transform([x])[0] if x in self.device_encoder.classes_ else -1
        )
        
        # Feature engineering (simplified for single prediction)
        # In a real application, you would need to maintain running counts
        data['user_login_frequency'] = 1  # Placeholder
        data['device_login_frequency'] = 1  # Placeholder
        data['location_login_frequency'] = 1  # Placeholder
        
        # Select features for modeling
        features = [
            'login_hour', 'login_day', 'login_month', 'login_year', 'login_weekday',
            'is_new_device', 'bytes_in', 'bytes_out', 'success',
            'geo_location_encoded', 'device_id_encoded',
            'user_login_frequency', 'device_login_frequency', 'location_login_frequency'
        ]
        
        return data[features]
    
    def predict(self, data):
        """
        Predict if a login is anomalous
        """
        # Preprocess the data
        processed_data = self.preprocess_data(data)
        
        # Make prediction
        prediction = self.model.predict(processed_data)
        
        # Return prediction (1 for anomaly, 0 for normal)
        return prediction
    
    def predict_proba(self, data):
        """
        Get prediction probabilities
        """
        # Preprocess the data
        processed_data = self.preprocess_data(data)
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(processed_data)
        
        # Return probabilities
        return probabilities

# Example usage
if __name__ == "__main__":
    # Initialize the detector
    detector = AnomalyDetector()
    
    # Create sample data for prediction
    sample_data = pd.DataFrame({
        'user_id': ['U9999'],
        'timestamp': ['2025-09-10 15:30:00'],
        'ip_address': ['192.168.1.100'],
        'geo_location': ['United States of America'],
        'device_id': ['DF_9999'],
        'login_hour': [15],
        'is_new_device': [0],
        'bytes_in': [100000],
        'bytes_out': [200000],
        'success': [1]
    })
    
    # Make prediction
    prediction = detector.predict(sample_data)
    probabilities = detector.predict_proba(sample_data)
    
    print("Sample prediction:")
    print(f"Anomaly: {prediction[0]}")
    print(f"Probability of normal: {probabilities[0][0]:.2f}")
    print(f"Probability of anomaly: {probabilities[0][1]:.2f}")