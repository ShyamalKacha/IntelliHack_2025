import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import OneClassSVM
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('../Dataset.csv')

# Display basic information about the dataset
print("Dataset Shape:", df.shape)
print("\nDataset Info:")
print(df.info())
print("\nFirst few rows:")
print(df.head())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check the distribution of the target variable
print("\nAnomaly distribution:")
print(df['is_anomaly'].value_counts())

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract time-based features
df['login_hour'] = df['timestamp'].dt.hour
df['login_day'] = df['timestamp'].dt.day
df['login_month'] = df['timestamp'].dt.month
df['login_year'] = df['timestamp'].dt.year
df['login_weekday'] = df['timestamp'].dt.weekday

# Encode categorical variables
le_geo = LabelEncoder()
le_device = LabelEncoder()

df['geo_location_encoded'] = le_geo.fit_transform(df['geo_location'])
df['device_id_encoded'] = le_device.fit_transform(df['device_id'])

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

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nFeature engineering completed.")
print("Training set shape:", X_train.shape)
print("Test set shape:", X_test.shape)