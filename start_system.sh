#!/bin/bash
echo "Starting Anomaly Detection System..."

# Change to src/api directory
cd src/api

# Activate virtual environment
source ../../venv/bin/activate

# Check if model exists, if not train it
if [ ! -f ../../models/anomaly_detection_model.pkl ]; then
    echo "Model not found. Training model..."
    python ../backend/main.py --train --data ../../data/Dataset.csv
fi

# Start the API server
echo "Starting API server..."
python api.py