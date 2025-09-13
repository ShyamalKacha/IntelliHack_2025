import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('../data/sample_dataset.csv')

# Set up the plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create a figure with multiple subplots
fig = plt.figure(figsize=(20, 15))

# 1. Anomaly distribution
ax1 = plt.subplot(3, 3, 1)
anomaly_counts = df['is_anomaly'].value_counts()
bars = plt.bar(['Normal', 'Anomalous'], [anomaly_counts[0], anomaly_counts[1]], 
               color=['#4CAF50', '#F44336'])
plt.title('Distribution of Login Patterns')
plt.ylabel('Count')
# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom')

# 2. Login hours distribution
ax2 = plt.subplot(3, 3, 2)
normal_hours = df[df['is_anomaly'] == 0]['login_hour']
anomalous_hours = df[df['is_anomaly'] == 1]['login_hour']
plt.hist([normal_hours, anomalous_hours], bins=24, 
         label=['Normal', 'Anomalous'], alpha=0.7, color=['#4CAF50', '#F44336'])
plt.title('Login Hours Distribution')
plt.xlabel('Hour of Day')
plt.ylabel('Frequency')
plt.legend()

# 3. Bytes in distribution (log scale)
ax3 = plt.subplot(3, 3, 3)
normal_bytes_in = df[df['is_anomaly'] == 0]['bytes_in']
anomalous_bytes_in = df[df['is_anomaly'] == 1]['bytes_in']
plt.hist([normal_bytes_in, anomalous_bytes_in], bins=50, 
         label=['Normal', 'Anomalous'], alpha=0.7, color=['#4CAF50', '#F44336'])
plt.title('Bytes In Distribution')
plt.xlabel('Bytes In')
plt.ylabel('Frequency')
plt.yscale('log')
plt.legend()

# 4. Bytes out distribution (log scale)
ax4 = plt.subplot(3, 3, 4)
normal_bytes_out = df[df['is_anomaly'] == 0]['bytes_out']
anomalous_bytes_out = df[df['is_anomaly'] == 1]['bytes_out']
plt.hist([normal_bytes_out, anomalous_bytes_out], bins=50, 
         label=['Normal', 'Anomalous'], alpha=0.7, color=['#4CAF50', '#F44336'])
plt.title('Bytes Out Distribution')
plt.xlabel('Bytes Out')
plt.ylabel('Frequency')
plt.yscale('log')
plt.legend()

# 5. New device usage
ax5 = plt.subplot(3, 3, 5)
normal_new_device = df[(df['is_anomaly'] == 0) & (df['is_new_device'] == 1)].shape[0]
anomalous_new_device = df[(df['is_anomaly'] == 1) & (df['is_new_device'] == 1)].shape[0]
normal_old_device = df[(df['is_anomaly'] == 0) & (df['is_new_device'] == 0)].shape[0]
anomalous_old_device = df[(df['is_anomaly'] == 1) & (df['is_new_device'] == 0)].shape[0]

plt.bar(['Normal\n(New Device)', 'Anomalous\n(New Device)', 'Normal\n(Old Device)', 'Anomalous\n(Old Device)'], 
        [normal_new_device, anomalous_new_device, normal_old_device, anomalous_old_device], 
        color=['#4CAF50', '#F44336', '#81C784', '#EF5350'])
plt.title('New Device Usage')
plt.ylabel('Count')
plt.xticks(rotation=45)

# 6. Success vs Failure
ax6 = plt.subplot(3, 3, 6)
normal_success = df[(df['is_anomaly'] == 0) & (df['success'] == 1)].shape[0]
anomalous_success = df[(df['is_anomaly'] == 1) & (df['success'] == 1)].shape[0]
normal_failure = df[(df['is_anomaly'] == 0) & (df['success'] == 0)].shape[0]
anomalous_failure = df[(df['is_anomaly'] == 1) & (df['success'] == 0)].shape[0]

plt.bar(['Normal\n(Success)', 'Anomalous\n(Success)', 'Normal\n(Failure)', 'Anomalous\n(Failure)'], 
        [normal_success, anomalous_success, normal_failure, anomalous_failure], 
        color=['#4CAF50', '#F44336', '#81C784', '#EF5350'])
plt.title('Login Success vs Failure')
plt.ylabel('Count')
plt.xticks(rotation=45)

# 7. Geographic distribution of anomalies
ax7 = plt.subplot(3, 3, 7)
geo_anomalies = df[df['is_anomaly'] == 1]['geo_location'].value_counts().head(10)
plt.barh(geo_anomalies.index, geo_anomalies.values, color='#F44336')
plt.title('Top 10 Locations for Anomalous Logins')
plt.xlabel('Count')

# 8. Device distribution of anomalies
ax8 = plt.subplot(3, 3, 8)
device_anomalies = df[df['is_anomaly'] == 1]['device_id'].value_counts().head(10)
plt.barh(device_anomalies.index, device_anomalies.values, color='#F44336')
plt.title('Top 10 Devices for Anomalous Logins')
plt.xlabel('Count')

# 9. Weekday distribution
ax9 = plt.subplot(3, 3, 9)
# Convert timestamp to datetime to extract weekday
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['weekday'] = df['timestamp'].dt.weekday
normal_weekday = df[df['is_anomaly'] == 0]['weekday'].value_counts().sort_index()
anomalous_weekday = df[df['is_anomaly'] == 1]['weekday'].value_counts().sort_index()
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
plt.plot(weekdays, normal_weekday.values, marker='o', label='Normal', linewidth=2, color='#4CAF50')
plt.plot(weekdays, anomalous_weekday.values, marker='o', label='Anomalous', linewidth=2, color='#F44336')
plt.title('Login Patterns by Weekday')
plt.ylabel('Count')
plt.legend()

plt.tight_layout()
plt.savefig('data_insights.png', dpi=300, bbox_inches='tight')
plt.close()

print("Data insights visualization saved as 'data_insights.png'")