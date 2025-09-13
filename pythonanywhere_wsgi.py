# CloudShield AI - Anomaly Detection System
# PythonAnywhere WSGI Configuration

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/cloudshield-ai'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask app
from src.api.api import app as application

# For debugging purposes, you can set the logging level
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)