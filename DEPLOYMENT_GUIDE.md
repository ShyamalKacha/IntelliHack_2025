# Deploying CloudShield AI to PythonAnywhere

## Overview
This guide explains how to deploy the CloudShield AI anomaly detection system to PythonAnywhere.

## Prerequisites
- A PythonAnywhere account (free or paid tier)
- Basic familiarity with PythonAnywhere web interface

## Deployment Steps

### 1. Upload Your Files
1. Log into PythonAnywhere
2. Go to the **Files** tab
3. Upload your project files to a directory like `/home/yourusername/cloudshield-ai/`
4. Your directory structure should look like:
   ```
   cloudshield-ai/
   ├── src/
   │   ├── api/
   │   │   └── api.py
   │   ├── backend/
   │   └── frontend/
   │       ├── frontend.html
   │       ├── dashboard.html
   │       └── api_docs.html
   ├── models/
   │   ├── anomaly_detection_model.pkl
   │   ├── scaler.pkl
   │   ├── geo_encoder.pkl
   │   └── device_encoder.pkl
   ├── requirements.txt
   └── pythonanywhere_wsgi.py
   ```

### 2. Set Up Virtual Environment
1. Go to the **Consoles** tab
2. Start a new Bash console
3. Create a virtual environment:
   ```bash
   mkvirtualenv cloudshield-ai --python=python3.10
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure the Web Application
1. Go to the **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration** (not the Flask auto-setup)
4. Select **Python 3.10** as the Python version
5. In the **Virtualenv** section, enter:
   ```
   /home/yourusername/.virtualenvs/cloudshield-ai
   ```
6. In the **Code** section, set the **WSGI configuration file** to:
   ```
   /home/yourusername/cloudshield-ai/pythonanywhere_wsgi.py
   ```

### 4. Update the WSGI Configuration File
1. Go to the **Files** tab
2. Open `/home/yourusername/cloudshield-ai/pythonanywhere_wsgi.py`
3. Update the `project_home` path to match your actual project location:
   ```python
   project_home = '/home/yourusername/cloudshield-ai'
   ```

### 5. Reload the Application
1. Go back to the **Web** tab
2. Click the **Reload** button for your web app
3. Your application should now be accessible at:
   `http://yourusername.pythonanywhere.com`

## Accessing Different Parts of the Application

- Main application: `http://yourusername.pythonanywhere.com/`
- Dashboard: `http://yourusername.pythonanywhere.com/dashboard`
- API documentation: `http://yourusername.pythonanywhere.com/api-docs`
- API health check: `http://yourusername.pythonanywhere.com/health`
- API endpoint: `http://yourusername.pythonanywhere.com/predict` (POST)

## API Usage Examples

### Python Example
```python
import requests

url = "http://yourusername.pythonanywhere.com/predict"
data = {
    "user_id": "U1234",
    "timestamp": "2025-06-15 14:30:00",
    "ip_address": "192.168.1.100",
    "geo_location": "United States of America",
    "device_id": "DF_5555",
    "is_new_device": 0,
    "bytes_in": 150000,
    "bytes_out": 250000,
    "success": 1
}

response = requests.post(url, json=data)
result = response.json()
print(result)
```

### cURL Example
```bash
curl -X POST http://yourusername.pythonanywhere.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "U1234",
    "timestamp": "2025-06-15 14:30:00",
    "ip_address": "192.168.1.100",
    "geo_location": "United States of America",
    "device_id": "DF_5555",
    "is_new_device": 0,
    "bytes_in": 150000,
    "bytes_out": 250000,
    "success": 1
  }'
```

## Troubleshooting

### Common Issues
1. **500 Internal Server Error**: Check the error log in the Web tab for details
2. **Import Errors**: Verify that all paths in the WSGI file are correct
3. **Module Not Found**: Ensure all dependencies are installed in the virtual environment
4. **Permission Errors**: Make sure all files have appropriate read permissions

### Checking Logs
1. Go to the **Web** tab
2. Scroll down to the **Log files** section
3. Check `error.log` for application errors
4. Check `access.log` for request information

## Updating the Application

To update your application after making changes:

1. Upload your updated files
2. Go to the **Web** tab
3. Click **Reload** to restart the application

Note: If you've changed the model files or any core components, you might need to restart the application for changes to take effect.