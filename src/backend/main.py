import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import argparse
import warnings
import os
warnings.filterwarnings('ignore')

def load_and_preprocess_data(filepath):
    """
    Load and preprocess the dataset
    """
    # Check if file exists, if not use sample dataset
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Using sample dataset instead.")
        filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'sample_dataset.csv')
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Neither {filepath} nor sample dataset found.")
    
    # Load the dataset
    df = pd.read_csv(filepath)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract time-based features
    df['login_hour'] = df['timestamp'].dt.hour
    df['login_day'] = df['timestamp'].dt.day
    df['login_month'] = df['timestamp'].dt.month
    df['login_year'] = df['timestamp'].dt.year
    df['login_weekday'] = df['timestamp'].dt.weekday
    
    # Encode categorical variables
    le_geo = LabelEncoder()
    le_device = LabelEncoder()
    
    df['geo_location_encoded'] = le_geo.fit_transform(df['geo_location'])
    df['device_id_encoded'] = le_device.fit_transform(df['device_id'])
    
    # Feature engineering
    # Calculate login frequency per user
    user_login_counts = df['user_id'].value_counts()
    df['user_login_frequency'] = df['user_id'].map(user_login_counts)
    
    # Calculate login frequency per device
    device_login_counts = df['device_id'].value_counts()
    df['device_login_frequency'] = df['device_id'].map(device_login_counts)
    
    # Calculate login frequency per location
    location_login_counts = df['geo_location'].value_counts()
    df['location_login_frequency'] = df['geo_location'].map(location_login_counts)
    
    return df, le_geo, le_device

def train_model(df):
    """
    Train the anomaly detection model
    """
    # Select features for modeling
    features = [
        'login_hour', 'login_day', 'login_month', 'login_year', 'login_weekday',
        'is_new_device', 'bytes_in', 'bytes_out', 'success',
        'geo_location_encoded', 'device_id_encoded',
        'user_login_frequency', 'device_login_frequency', 'location_login_frequency'
    ]
    
    X = df[features]
    y = df['is_anomaly']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict anomalies
    predictions = model.predict(X_test)
    
    # Evaluate model
    print("\nModel Evaluation:")
    print("Accuracy:", accuracy_score(y_test, predictions))
    print(classification_report(y_test, predictions))
    
    return model, scaler, X_train, X_test, y_train, y_test

def save_model(model, scaler, le_geo, le_device):
    """
    Save the trained model and encoders
    """
    # Create models directory if it doesn't exist
    models_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(models_dir, 'anomaly_detection_model.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(le_geo, os.path.join(models_dir, 'geo_encoder.pkl'))
    joblib.dump(le_device, os.path.join(models_dir, 'device_encoder.pkl'))
    print("\nModel and encoders saved successfully.")

def main():
    parser = argparse.ArgumentParser(description='Anomaly Detection for Cloud Login Patterns')
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--data', type=str, default=os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Dataset.csv'), help='Path to the dataset CSV file')
    
    args = parser.parse_args()
    
    if args.train:
        # Load and preprocess data
        print("Loading and preprocessing data...")
        df, le_geo, le_device = load_and_preprocess_data(args.data)
        
        # Train the model
        model, scaler, X_train, X_test, y_train, y_test = train_model(df)
        
        # Save the model
        save_model(model, scaler, le_geo, le_device)
    else:
        print("Please specify --train option to train the model.")
        print("Example: python main.py --train")
        print("To use a specific dataset: python main.py --train --data path/to/dataset.csv")

if __name__ == "__main__":
    main()