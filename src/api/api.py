from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# File to store prediction history
PREDICTIONS_HISTORY_FILE = '../../data/predictions_history.json'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the trained model and encoders from models directory
model_path = os.path.join(current_dir, '..', '..', 'models', 'anomaly_detection_model.pkl')
scaler_path = os.path.join(current_dir, '..', '..', 'models', 'scaler.pkl')
geo_encoder_path = os.path.join(current_dir, '..', '..', 'models', 'geo_encoder.pkl')
device_encoder_path = os.path.join(current_dir, '..', '..', 'models', 'device_encoder.pkl')

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
geo_encoder = joblib.load(geo_encoder_path)
device_encoder = joblib.load(device_encoder_path)

def preprocess_data(data):
    """
    Preprocess the input data for prediction
    """
    # Convert to DataFrame
    df = pd.DataFrame([data])
    
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
        df['geo_location_encoded'] = geo_encoder.transform(df['geo_location'])
    except ValueError:
        df['geo_location_encoded'] = -1  # Unknown category
    
    try:
        df['device_id_encoded'] = device_encoder.transform(df['device_id'])
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

def load_prediction_history():
    """
    Load prediction history from file
    """
    try:
        if os.path.exists(PREDICTIONS_HISTORY_FILE):
            with open(PREDICTIONS_HISTORY_FILE, 'r') as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"Error loading prediction history: {e}")
        return []

def save_prediction_to_history(prediction_data):
    """
    Save prediction to history file
    """
    try:
        # Load existing history
        history = load_prediction_history()
        
        # Add timestamp to the prediction
        prediction_data['timestamp'] = datetime.now().isoformat()
        
        # Add to history
        history.append(prediction_data)
        
        # Keep only the last 1000 predictions to avoid file growing too large
        if len(history) > 1000:
            history = history[-1000:]
        
        # Save back to file
        with open(PREDICTIONS_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving prediction to history: {e}")
        return False

def calculate_prediction_stats():
    """
    Calculate statistics about predictions
    """
    try:
        # Load prediction history
        history = load_prediction_history()
        
        # Calculate basic stats
        total_predictions = len(history)
        anomaly_count = sum(1 for pred in history if pred['prediction']['anomaly'] == 1)
        normal_count = total_predictions - anomaly_count
        
        # Calculate accuracy (assuming normal predictions are correct)
        accuracy = normal_count / total_predictions if total_predictions > 0 else 0
        
        # Calculate hourly distribution
        hourly_counts = {hour: 0 for hour in range(24)}
        geo_counts = {}
        
        for pred in history:
            # Parse timestamp and extract hour
            try:
                timestamp = pred.get('timestamp') or pred['input_data'].get('timestamp')
                if timestamp:
                    hour = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).hour
                    hourly_counts[hour] += 1
            except Exception:
                # If we can't parse the timestamp, skip this record
                pass
            
            # Count geographic locations
            geo_location = pred['input_data'].get('geo_location')
            if geo_location:
                geo_counts[geo_location] = geo_counts.get(geo_location, 0) + 1
        
        return {
            'total_predictions': total_predictions,
            'anomaly_count': anomaly_count,
            'normal_count': normal_count,
            'accuracy': accuracy,
            'hourly_distribution': hourly_counts,
            'geographic_distribution': geo_counts
        }
    except Exception as e:
        print(f"Error calculating prediction stats: {e}")
        return {
            'total_predictions': 0,
            'anomaly_count': 0,
            'normal_count': 0,
            'accuracy': 0,
            'hourly_distribution': {hour: 0 for hour in range(24)},
            'geographic_distribution': {}
        }

@app.route('/')
def index():
    """
    Serve the frontend HTML file
    """
    return send_from_directory('../frontend', 'frontend.html')

@app.route('/dashboard')
def dashboard_route():
    """
    Serve the dashboard HTML file
    """
    return send_from_directory('../frontend', 'dashboard.html')

@app.route('/api-docs')
def api_docs():
    """
    Serve the API documentation HTML file
    """
    return send_from_directory('../frontend', 'api_docs.html')

@app.route('/predict')
def predict_page():
    """
    Serve the prediction HTML file
    """
    return send_from_directory('../frontend', 'predict.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """
    Serve static files (CSS, JS, etc.)
    """
    return send_from_directory('../frontend', filename)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict if a login is anomalous
    """
    try:
        # Get data from request
        data = request.json
        
        # Preprocess the data
        processed_data = preprocess_data(data)
        
        # Make prediction
        prediction = model.predict(processed_data)
        probability = model.predict_proba(processed_data)
        
        # Prepare response
        result = {
            'anomaly': int(prediction[0]),
            'probability_normal': float(probability[0][0]),
            'probability_anomaly': float(probability[0][1])
        }
        
        # Save prediction to history (include input data)
        prediction_record = {
            'input_data': data,
            'prediction': result
        }
        save_prediction_to_history(prediction_record)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy'})

@app.route('/predictions/history', methods=['GET'])
def get_predictions_history():
    """
    Get prediction history
    """
    try:
        history = load_prediction_history()
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predictions/stats', methods=['GET'])
def get_predictions_stats():
    """
    Get statistics about predictions
    """
    try:
        stats = calculate_prediction_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)