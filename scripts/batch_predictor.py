import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class BatchAnomalyDetector:
    def __init__(self):
        # Load the trained model and encoders
        self.model = joblib.load('anomaly_detection_model.pkl')
        self.geo_encoder = joblib.load('geo_encoder.pkl')
        self.device_encoder = joblib.load('device_encoder.pkl')
        
    def preprocess_data(self, df):
        """
        Preprocess the input data for prediction
        """
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
        
        return df[features]
    
    def predict(self, df):
        """
        Predict if logins are anomalous
        """
        # Preprocess the data
        processed_data = self.preprocess_data(df)
        
        # Make predictions
        predictions = self.model.predict(processed_data)
        probabilities = self.model.predict_proba(processed_data)
        
        # Add predictions to the original dataframe
        df['is_anomaly_predicted'] = predictions
        df['probability_normal'] = probabilities[:, 0]
        df['probability_anomaly'] = probabilities[:, 1]
        
        return df

# Example usage
if __name__ == "__main__":
    # Initialize the detector
    detector = BatchAnomalyDetector()
    
    # Create sample data for prediction
    sample_data = pd.DataFrame({
        'user_id': ['U9999', 'U8888', 'U7777'],
        'timestamp': ['2025-09-10 15:30:00', '2025-09-10 16:45:00', '2025-09-10 17:00:00'],
        'ip_address': ['192.168.1.100', '10.0.0.50', '172.16.0.25'],
        'geo_location': ['United States of America', 'Germany', 'Japan'],
        'device_id': ['DF_9999', 'DF_8888', 'DF_7777'],
        'login_hour': [15, 16, 17],
        'is_new_device': [0, 1, 0],
        'bytes_in': [100000, 500000, 250000],
        'bytes_out': [200000, 1000000, 500000],
        'success': [1, 1, 0]
    })
    
    # Make predictions
    results = detector.predict(sample_data)
    
    # Display results
    print("Batch Prediction Results:")
    print(results[['user_id', 'geo_location', 'is_new_device', 'is_anomaly_predicted', 'probability_anomaly']])