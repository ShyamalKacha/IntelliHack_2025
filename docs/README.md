# Anomaly Detection System for Cloud Login Patterns

## Table of Contents
1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [System Architecture](#system-architecture)
5. [Setup Instructions](#setup-instructions)
6. [Usage](#usage)
7. [API Documentation](#api-documentation)
8. [Model Performance](#model-performance)
9. [Features](#features)
10. [Future Improvements](#future-improvements)

## Overview
This project implements an AI/ML system that detects anomalous login patterns in cloud environments to prevent account takeovers. The system analyzes various factors including geo-location, device fingerprinting, login time, and data transfer patterns to identify potentially malicious login attempts.

## Problem Statement
With the rise of remote work and cloud services, stolen credentials pose a significant security threat. Attackers often log in from unusual locations, devices, or times, but traditional security systems often fail to flag these subtle anomalies, leading to account takeovers.

## Solution
Our system uses machine learning to detect anomalous login patterns that may indicate compromised accounts. It provides real-time alerts to security teams and can be integrated with existing authentication systems.

## System Architecture
```
┌─────────────────┐    ┌──────────────┐    ┌──────────────────┐
│   Login Data    │───▶│ Data Preproc.│───▶│    ML Model      │
└─────────────────┘    └──────────────┘    └──────────────────┘
                                                    │
                                                    ▼
┌─────────────────┐    ┌──────────────┐    ┌──────────────────┐
│   Frontend      │◀──▶│    API       │◀──▶│   Dashboard      │
└─────────────────┘    └──────────────┘    └──────────────────┘
                                                    │
                                                    ▼
                                       ┌─────────────────────┐
                                       │ Batch Processing    │
                                       └─────────────────────┘
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps
1. Clone the repository:
   ```
   git clone <repository-url>
   cd anomaly_detection_model
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

5. Train the model (if not already done):
   ```
   python main.py --train
   ```

## Usage

### Starting the System
Run the startup script:
```bash
start_system.bat  # Windows
# OR
./start_system.sh # macOS/Linux
```

### Manual Startup
1. Start the API server:
   ```
   python api.py
   ```

2. Access the interfaces:
   - Frontend: http://localhost:5000
   - Dashboard: http://localhost:5000/dashboard
   - API Health Check: http://localhost:5000/health

### Testing the Model
1. **Single Prediction**: Use the frontend interface to test individual logins
2. **Batch Processing**: Use the batch predictor script:
   ```
   python batch_predictor.py
   ```
3. **Programmatic Access**: Use the demonstration script:
   ```
   python demonstration.py
   ```

## API Documentation

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

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Model Performance
The Random Forest classifier achieved the following performance metrics on the test set:
- **Accuracy**: 99.98%
- **Precision for anomaly detection**: ~99%
- **Recall for anomaly detection**: ~99%
- **F1-Score for anomaly detection**: ~99%

### Confusion Matrix
```
                 Predicted
               Normal  Anomaly
Actual Normal   9323      0
     Anomaly      0     677
```

## Features Used for Detection
1. **Temporal Features**:
   - Login hour, day, month, year, and weekday
   - Unusual login times (early morning/late night)

2. **Device Features**:
   - Device fingerprinting
   - New device detection
   - Device usage patterns

3. **Network Features**:
   - Bytes transferred in and out
   - Data transfer anomalies

4. **Geographical Features**:
   - Geo-location of login
   - Unusual locations
   - Cross-border login detection

5. **Behavioral Features**:
   - User login frequency
   - Device login frequency
   - Location login frequency

6. **Authentication Features**:
   - Login success/failure
   - Password reset attempts

## Feature Importance
The most important features for anomaly detection are:
1. Geo-location encoded
2. Login hour
3. Bytes out
4. Bytes in
5. Is new device
6. Device ID encoded
7. Login weekday
8. Success
9. User login frequency
10. Device login frequency

## Future Improvements
1. **Real-time Learning**: Implement online learning to adapt to new patterns
2. **Advanced Algorithms**: Experiment with deep learning models like LSTM for sequence detection
3. **Additional Features**: Incorporate IP reputation, user behavior patterns, and historical login sequences
4. **Alerting System**: Add email/SMS notifications for detected anomalies with severity levels
5. **Integration**: Connect with existing authentication systems (OAuth, SAML, LDAP)
6. **Scalability**: Implement distributed processing for large-scale deployments
7. **Explainability**: Add SHAP values to explain why a login was flagged as anomalous
8. **Multi-tenant Support**: Extend the system to support multiple organizations
9. **Mobile Integration**: Develop mobile apps for real-time alerts
10. **Compliance Reporting**: Generate reports for regulatory compliance (GDPR, HIPAA, etc.)

## Technologies Used
- **Backend**: Python, Flask
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Visualization**: Matplotlib, Seaborn
- **Data Storage**: CSV files (can be extended to databases)
- **Deployment**: Virtual environments, batch scripts

## Project Structure
```
anomaly_detection_model/
├── api.py                 # Flask API server
├── main.py                # Main training script
├── batch_predictor.py     # Batch prediction processor
├── demonstration.py       # Usage examples
├── feature_visualization.py # Feature importance visualization
├── model_evaluation.py    # Model performance evaluation
├── generate_sample_data.py # Sample data generator
├── frontend.html          # Web frontend
├── dashboard.html         # Analytics dashboard
├── requirements.txt       # Python dependencies
├── start_system.bat       # Startup script
├── README.md             # This file
├── SYSTEM_DOCS.md        # Detailed system documentation
├── sample_dataset.csv     # Sample data for testing
├── anomaly_detection_model.pkl  # Trained model
├── scaler.pkl             # Feature scaler
├── geo_encoder.pkl        # Geo-location encoder
└── device_encoder.pkl     # Device ID encoder
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions or support, please contact the development team.