@echo off
cd /d C:\Users\Admin\Desktop\Shyamal\Hackathon\IntelliHack_2025\Project\Code\anomaly_detection_model
cd src\api
call ..\..\venv\Scripts\activate.bat
echo Starting API server with CORS support...
python api.py
pause