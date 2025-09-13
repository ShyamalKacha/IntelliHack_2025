import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('../Dataset.csv')

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

# Train Isolation Forest model
print("Training Isolation Forest model...")
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(X_train_scaled)

# Predict anomalies
iso_predictions = iso_forest.predict(X_test_scaled)
iso_predictions = [1 if x == -1 else 0 for x in iso_predictions]

# Evaluate Isolation Forest model
print("\nIsolation Forest Results:")
print("Accuracy:", accuracy_score(y_test, iso_predictions))
print(classification_report(y_test, iso_predictions))

# Train One-Class SVM model
print("\nTraining One-Class SVM model...")
svm_model = OneClassSVM(nu=0.1)
# Fit on normal data only
X_train_normal = X_train_scaled[y_train == 0]
svm_model.fit(X_train_normal)

# Predict anomalies
svm_predictions = svm_model.predict(X_test_scaled)
svm_predictions = [1 if x == -1 else 0 for x in svm_predictions]

# Evaluate One-Class SVM model
print("\nOne-Class SVM Results:")
print("Accuracy:", accuracy_score(y_test, svm_predictions))
print(classification_report(y_test, svm_predictions))

# Train Random Forest model (supervised approach)
print("\nTraining Random Forest model...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict anomalies
rf_predictions = rf_model.predict(X_test)

# Evaluate Random Forest model
print("\nRandom Forest Results:")
print("Accuracy:", accuracy_score(y_test, rf_predictions))
print(classification_report(y_test, rf_predictions))

# Save the best model (Random Forest)
joblib.dump(rf_model, 'anomaly_detection_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(le_geo, 'geo_encoder.pkl')
joblib.dump(le_device, 'device_encoder.pkl')

print("\nModel saved successfully.")