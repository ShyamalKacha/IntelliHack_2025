@echo off
echo Starting Anomaly Detection System...

REM Change to src directory
cd src\api

REM Activate virtual environment
call ..\..\venv\Scripts\activate

REM Check if model exists, if not train it
if not exist ..\..\models\anomaly_detection_model.pkl (
    echo Model not found. Training model...
    python ..\backend\main.py --train --data ..\..\data\Dataset.csv
)

REM Start the API server
echo Starting API server...
python api.py

pause