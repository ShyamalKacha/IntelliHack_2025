# Anomaly Detection System for Cloud Login Patterns

## Overview
This system detects anomalous login patterns in cloud environments using machine learning. It analyzes various factors such as geographical location, device fingerprinting, login time, and data transfer patterns to identify potentially malicious login attempts.

## System Components
1. **Machine Learning Model**: A Random Forest classifier trained to detect anomalous login patterns
2. **REST API**: Flask-based API for serving the model
3. **Web Frontend**: Simple interface for testing individual logins
4. **Dashboard**: Visualization of login patterns and anomalies
5. **Batch Processor**: Script for processing multiple logins at once

## Setup Instructions
1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Train the model (if not already done):
   ```
   python main.py --train --data ../Dataset.csv
   ```

## Running the System
1. Start the API server:
   ```
   python api.py
   ```

2. Access the interfaces:
   - Frontend: http://localhost:5000
   - Dashboard: http://localhost:5000/dashboard
   - API Health Check: http://localhost:5000/health

## API Endpoints
### POST /predict
Predict if a login is anomalous.

**Request Body:**
```json
{
  "user_id": "U1234",
  "timestamp": "2025-06-15 14:30:00",
  "ip_address": "192.168.1.100",
  "geo_location": "United States of America",
  "device_id": "DF_5555",
  "login_hour": 14,
  "is_new_device": 0,
  "bytes_in": 150000,
  "bytes_out": 250000,
  "success": 1
}
```

**Response:**
```json
{
  "anomaly": 0,
  "probability_normal": 0.95,
  "probability_anomaly": 0.05
}
```

## Batch Processing
To process multiple logins at once, use the batch predictor:
```
python batch_predictor.py
```

## Model Performance
The Random Forest classifier achieved the following performance metrics on the test set:
- Accuracy: 99.98%
- Precision for anomaly detection: ~99%
- Recall for anomaly detection: ~99%

## Features Used for Detection
1. Login hour, day, month, year, and weekday
2. Whether the device is new for the user
3. Bytes transferred in and out during the session
4. Whether the login was successful
5. Geographical location of the login
6. Device identifier
7. User login frequency
8. Device login frequency
9. Location login frequency

## Extending the System
1. **Real-time Learning**: Implement online learning to adapt to new patterns
2. **Additional Features**: Incorporate IP reputation, user behavior patterns, etc.
3. **Alerting System**: Add email/SMS notifications for detected anomalies
4. **Integration**: Connect with existing authentication systems
5. **Model Improvement**: Experiment with other algorithms like neural networks