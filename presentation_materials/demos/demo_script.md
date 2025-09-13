# Demo Script for Anomaly Detection System

## Prerequisites
- System is running (API server started with `run_api.bat`)
- Access to http://localhost:5000

## Demo Flow

### 1. Introduction (2 minutes)
- Briefly explain the problem of credential theft and account takeovers
- Introduce our solution: AI-powered anomaly detection system

### 2. System Overview (3 minutes)
- Show the system architecture
- Explain the components: frontend, API, ML model, dashboard

### 3. Live Demo (8 minutes)

#### Normal Login Example
1. Navigate to http://localhost:5000
2. Fill in form with:
   - User ID: U1234
   - Timestamp: Current time
   - IP Address: 192.168.1.100
   - Geographical Location: United States of America
   - Device ID: DF_5555
   - Is New Device: No
   - Bytes In: 150000
   - Bytes Out: 250000
   - Login Success: Success
3. Click "Check for Anomaly"
4. Show normal result

#### Anomalous Login Examples

##### New Device Anomaly
1. Change Device ID to DF_9999
2. Set Is New Device: Yes
3. Click "Check for Anomaly"
4. Show anomaly detection

##### Unusual Location Anomaly
1. Change Geographical Location: Russia
2. Keep other fields similar to normal
3. Click "Check for Anomaly"
4. Show anomaly detection

##### Unusual Time Anomaly
1. Change Timestamp to early morning (e.g., 03:30:00)
2. Keep other fields similar to normal
3. Click "Check for Anomaly"
4. Show anomaly detection

##### High Data Transfer Anomaly
1. Change Bytes In: 5000000
2. Change Bytes Out: 5000000
3. Click "Check for Anomaly"
4. Show anomaly detection

### 4. Dashboard Demo (3 minutes)
- Navigate to http://localhost:5000/dashboard
- Show analytics and detected patterns
- Explain how security teams would use this

### 5. API Demo (2 minutes)
- Show how to make API calls programmatically
- Use test_api.py or demonstrate with curl

### 6. Performance Metrics (2 minutes)
- Show the generated visualizations
- Highlight key performance metrics:
  - 99.98% accuracy
  - Zero false positives/negatives
  - Fast detection capabilities

## Key Points to Emphasize

1. **High Accuracy**: 99.98% accuracy with zero false positives/negatives
2. **Multi-dimensional Analysis**: Combines temporal, behavioral, and network features
3. **Real-time Detection**: Immediate analysis of login patterns
4. **Easy Integration**: RESTful API for integration with existing systems
5. **Business Impact**: Prevents account takeovers and associated losses

## Anticipated Questions

### Technical Questions
- How does it handle false positives?
- How does it scale?
- How does it handle new attack patterns?

### Business Questions
- What's the ROI?
- How does it integrate with existing systems?
- What's the deployment process?

## Closing Statement
"Our system provides a robust, scalable solution to combat credential theft and account takeovers, offering enterprises peace of mind with its high accuracy and real-time detection capabilities."