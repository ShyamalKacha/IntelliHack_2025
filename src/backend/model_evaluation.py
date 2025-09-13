import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def evaluate_model():
    # Load the dataset
    df = pd.read_csv('../Dataset.csv')
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract time-based features
    df['login_hour'] = df['timestamp'].dt.hour
    df['login_day'] = df['timestamp'].dt.day
    df['login_month'] = df['timestamp'].dt.month
    df['login_year'] = df['timestamp'].dt.year
    df['login_weekday'] = df['timestamp'].dt.weekday
    
    # Load encoders
    le_geo = joblib.load('geo_encoder.pkl')
    le_device = joblib.load('device_encoder.pkl')
    
    # Encode categorical variables
    df['geo_location_encoded'] = le_geo.transform(df['geo_location'])
    df['device_id_encoded'] = le_device.transform(df['device_id'])
    
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
    
    # Select features for modeling
    features = [
        'login_hour', 'login_day', 'login_month', 'login_year', 'login_weekday',
        'is_new_device', 'bytes_in', 'bytes_out', 'success',
        'geo_location_encoded', 'device_id_encoded',
        'user_login_frequency', 'device_login_frequency', 'location_login_frequency'
    ]
    
    X = df[features]
    y = df['is_anomaly']
    
    # Load the trained model
    model = joblib.load('anomaly_detection_model.pkl')
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Print classification report
    print("Model Performance Evaluation:")
    print("=============================")
    print(classification_report(y, y_pred))
    
    # Create confusion matrix
    cm = confusion_matrix(y, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Normal', 'Anomaly'], 
                yticklabels=['Normal', 'Anomaly'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    plt.close()
    
    # Analyze performance on different types of anomalies
    print("\nPerformance on Different Anomaly Types:")
    print("======================================")
    
    # Anomalies by new device usage
    new_device_anomalies = df[(df['is_anomaly'] == 1) & (df['is_new_device'] == 1)]
    new_device_normal = df[(df['is_anomaly'] == 0) & (df['is_new_device'] == 1)]
    
    if len(new_device_anomalies) > 0:
        new_device_pred = model.predict(new_device_anomalies[features])
        new_device_acc = np.mean(new_device_pred == new_device_anomalies['is_anomaly'])
        print(f"Accuracy on new device anomalies: {new_device_acc:.4f}")
    
    # Anomalies by high data transfer
    high_bytes_anomalies = df[(df['is_anomaly'] == 1) & ((df['bytes_in'] > df['bytes_in'].quantile(0.95)) | 
                                                          (df['bytes_out'] > df['bytes_out'].quantile(0.95)))]
    
    if len(high_bytes_anomalies) > 0:
        high_bytes_pred = model.predict(high_bytes_anomalies[features])
        high_bytes_acc = np.mean(high_bytes_pred == high_bytes_anomalies['is_anomaly'])
        print(f"Accuracy on high data transfer anomalies: {high_bytes_acc:.4f}")
    
    # Anomalies by unusual login hours
    unusual_hours_anomalies = df[(df['is_anomaly'] == 1) & ((df['login_hour'] < 6) | (df['login_hour'] > 22))]
    
    if len(unusual_hours_anomalies) > 0:
        unusual_hours_pred = model.predict(unusual_hours_anomalies[features])
        unusual_hours_acc = np.mean(unusual_hours_pred == unusual_hours_anomalies['is_anomaly'])
        print(f"Accuracy on unusual hour anomalies: {unusual_hours_acc:.4f}")
    
    # Anomalies by foreign locations
    # Assuming US-based company, flagging non-US logins as potentially anomalous
    foreign_anomalies = df[(df['is_anomaly'] == 1) & (df['geo_location'] != 'United States of America')]
    
    if len(foreign_anomalies) > 0:
        foreign_pred = model.predict(foreign_anomalies[features])
        foreign_acc = np.mean(foreign_pred == foreign_anomalies['is_anomaly'])
        print(f"Accuracy on foreign location anomalies: {foreign_acc:.4f}")
    
    print("\nConfusion matrix saved as 'confusion_matrix.png'")

if __name__ == "__main__":
    evaluate_model()