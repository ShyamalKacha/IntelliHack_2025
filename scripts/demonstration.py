import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetector:
    def __init__(self):
        """
        Initialize the anomaly detector with trained model and encoders
        """
        # Load the trained model and encoders
        self.model = joblib.load('anomaly_detection_model.pkl')
        self.geo_encoder = joblib.load('geo_encoder.pkl')
        self.device_encoder = joblib.load('device_encoder.pkl')
        
    def preprocess_single_record(self, record):
        """
        Preprocess a single login record for prediction
        """
        # Convert to DataFrame
        df = pd.DataFrame([record])
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extract time-based features
        df['login_hour'] = df['timestamp'].dt.hour
        df['login_day'] = df['timestamp'].dt.day
        df['login_month'] = df['timestamp'].dt.month
        df['login_year'] = df['timestamp'].dt.year
        df['login_weekday'] = df['timestamp'].dt.weekday
        
        # Encode categorical variables (handle unseen categories)
        try:
            df['geo_location_encoded'] = self.geo_encoder.transform(df['geo_location'])
        except ValueError:
            df['geo_location_encoded'] = -1  # Unknown category
            
        try:
            df['device_id_encoded'] = self.device_encoder.transform(df['device_id'])
        except ValueError:
            df['device_id_encoded'] = -1  # Unknown category
        
        # Feature engineering (simplified for single prediction)
        # In a real application, you would need to maintain running counts
        df['user_login_frequency'] = 1  # Placeholder
        df['device_login_frequency'] = 1  # Placeholder
        df['location_login_frequency'] = 1  # Placeholder
        
        # Select features for modeling
        features = [
            'login_hour', 'login_day', 'login_month', 'login_year', 'login_weekday',
            'is_new_device', 'bytes_in', 'bytes_out', 'success',
            'geo_location_encoded', 'device_id_encoded',
            'user_login_frequency', 'device_login_frequency', 'location_login_frequency'
        ]
        
        return df[features]
    
    def predict_single(self, record):
        """
        Predict if a single login record is anomalous
        """
        # Preprocess the record
        processed_data = self.preprocess_single_record(record)
        
        # Make prediction
        prediction = self.model.predict(processed_data)
        probability = self.model.predict_proba(processed_data)
        
        # Return results
        return {
            'is_anomaly': bool(prediction[0]),
            'probability_normal': float(probability[0][0]),
            'probability_anomaly': float(probability[0][1])
        }
    
    def predict_batch(self, records):
        """
        Predict if multiple login records are anomalous
        """
        # Convert to DataFrame
        df = pd.DataFrame(records)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extract time-based features
        df['login_hour'] = df['timestamp'].dt.hour
        df['login_day'] = df['timestamp'].dt.day
        df['login_month'] = df['timestamp'].dt.month
        df['login_year'] = df['timestamp'].dt.year
        df['login_weekday'] = df['timestamp'].dt.weekday
        
        # Encode categorical variables (handle unseen categories)
        df['geo_location_encoded'] = df['geo_location'].apply(
            lambda x: self.geo_encoder.transform([x])[0] if x in self.geo_encoder.classes_ else -1
        )
        
        df['device_id_encoded'] = df['device_id'].apply(
            lambda x: self.device_encoder.transform([x])[0] if x in self.device_encoder.classes_ else -1
        )
        
        # Feature engineering (simplified for batch prediction)
        # In a real application, you would need to maintain running counts
        df['user_login_frequency'] = 1  # Placeholder
        df['device_login_frequency'] = 1  # Placeholder
        df['location_login_frequency'] = 1  # Placeholder
        
        # Select features for modeling
        features = [
            'login_hour', 'login_day', 'login_month', 'login_year', 'login_weekday',
            'is_new_device', 'bytes_in', 'bytes_out', 'success',
            'geo_location_encoded', 'device_id_encoded',
            'user_login_frequency', 'device_login_frequency', 'location_login_frequency'
        ]
        
        # Make predictions
        predictions = self.model.predict(df[features])
        probabilities = self.model.predict_proba(df[features])
        
        # Return results
        results = []
        for i in range(len(records)):
            results.append({
                'is_anomaly': bool(predictions[i]),
                'probability_normal': float(probabilities[i][0]),
                'probability_anomaly': float(probabilities[i][1])
            })
        
        return results

# Example usage
if __name__ == "__main__":
    # Initialize the detector
    detector = AnomalyDetector()
    
    # Example single prediction
    print("Single Prediction Example:")
    print("=========================")
    
    normal_record = {
        'user_id': 'U1234',
        'timestamp': '2025-06-15 14:30:00',
        'ip_address': '192.168.1.100',
        'geo_location': 'United States of America',
        'device_id': 'DF_5555',
        'login_hour': 14,
        'is_new_device': 0,
        'bytes_in': 150000,
        'bytes_out': 250000,
        'success': 1
    }
    
    result = detector.predict_single(normal_record)
    print(f"Record: {normal_record['user_id']} at {normal_record['timestamp']}")
    print(f"Is Anomaly: {result['is_anomaly']}")
    print(f"Probability of Normal: {result['probability_normal']:.4f}")
    print(f"Probability of Anomaly: {result['probability_anomaly']:.4f}")
    
    print("\nBatch Prediction Example:")
    print("=========================")
    
    # Example batch prediction
    batch_records = [
        {
            'user_id': 'U1234',
            'timestamp': '2025-06-15 14:30:00',
            'ip_address': '192.168.1.100',
            'geo_location': 'United States of America',
            'device_id': 'DF_5555',
            'login_hour': 14,
            'is_new_device': 0,
            'bytes_in': 150000,
            'bytes_out': 250000,
            'success': 1
        },
        {
            'user_id': 'U5678',
            'timestamp': '2025-06-15 03:15:00',
            'ip_address': '10.0.0.50',
            'geo_location': 'Russia',
            'device_id': 'DF_6666',
            'login_hour': 3,
            'is_new_device': 1,
            'bytes_in': 2000000,
            'bytes_out': 3000000,
            'success': 1
        }
    ]
    
    results = detector.predict_batch(batch_records)
    for i, (record, result) in enumerate(zip(batch_records, results)):
        print(f"\nRecord {i+1}: {record['user_id']} at {record['timestamp']}")
        print(f"  Location: {record['geo_location']}")
        print(f"  Is Anomaly: {result['is_anomaly']}")
        print(f"  Probability of Normal: {result['probability_normal']:.4f}")
        print(f"  Probability of Anomaly: {result['probability_anomaly']:.4f}")