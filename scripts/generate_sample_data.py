import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sample_data():
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate sample data
    data = []
    
    # Normal login patterns
    for i in range(8000):
        user_id = f"U{random.randint(1000, 9999):04d}"
        # Most logins during business hours
        hour = random.choices(range(24), weights=[0.5, 0.2, 0.1, 0.1, 0.1, 0.2, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.6, 0.4, 0.3])[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        # Date range
        days_ago = random.randint(0, 90)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hour, minutes=minute, seconds=second)
        
        # IP addresses (mostly from common ranges)
        ip_parts = [str(random.randint(1, 255)) for _ in range(4)]
        ip_address = ".".join(ip_parts)
        
        # Locations (mostly common)
        locations = ["United States of America", "United Kingdom", "Canada", "Germany", "France", "Australia"] + \
                   ["China", "India", "Brazil", "Japan"] * 2 + \
                   ["Russia", "South Africa", "Egypt", "Mexico"] * 3
        geo_location = random.choice(locations)
        
        # Device IDs
        device_id = f"DF_{random.randint(1000, 9999):04d}"
        
        # Mostly existing devices
        is_new_device = random.choices([0, 1], weights=[0.9, 0.1])[0]
        
        # Normal byte transfers
        bytes_in = random.randint(10000, 500000)
        bytes_out = random.randint(10000, 500000)
        
        # Mostly successful logins
        success = random.choices([0, 1], weights=[0.05, 0.95])[0]
        
        # Normal pattern (not anomalous)
        is_anomaly = 0
        
        data.append({
            "user_id": user_id,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": ip_address,
            "geo_location": geo_location,
            "device_id": device_id,
            "login_hour": hour,
            "is_new_device": is_new_device,
            "bytes_in": bytes_in,
            "bytes_out": bytes_out,
            "success": success,
            "is_anomaly": is_anomaly
        })
    
    # Anomalous login patterns
    for i in range(2000):
        user_id = f"U{random.randint(1000, 9999):04d}"
        # Unusual hours
        hour = random.choices(range(24), weights=[2, 1, 1, 1, 2, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 2])[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        # Date range
        days_ago = random.randint(0, 90)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hour, minutes=minute, seconds=second)
        
        # IP addresses (some unusual)
        if random.random() < 0.3:
            # Unusual IP ranges
            ip_parts = [str(random.randint(1, 255)) for _ in range(4)]
            ip_address = ".".join(ip_parts)
        else:
            # Common IP ranges
            ip_parts = [str(random.randint(1, 255)) for _ in range(4)]
            ip_address = ".".join(ip_parts)
        
        # Unusual locations
        locations = ["United States of America", "United Kingdom", "Canada", "Germany", "France", "Australia"] * 2 + \
                   ["North Korea", "Russia", "Iran", "Syria", "China", "India"] * 3 + \
                   ["Antarctica (the territory South of 60 deg S)", "Heard Island and McDonald Islands"] * 5
        geo_location = random.choice(locations)
        
        # Device IDs
        device_id = f"DF_{random.randint(1000, 9999):04d}"
        
        # More new devices
        is_new_device = random.choices([0, 1], weights=[0.3, 0.7])[0]
        
        # Unusual byte transfers
        if random.random() < 0.4:
            # High data transfer
            bytes_in = random.randint(1000000, 5000000)
            bytes_out = random.randint(1000000, 5000000)
        else:
            # Normal byte transfers
            bytes_in = random.randint(10000, 500000)
            bytes_out = random.randint(10000, 500000)
        
        # Some failed logins
        success = random.choices([0, 1], weights=[0.3, 0.7])[0]
        
        # Anomalous pattern
        is_anomaly = 1
        
        data.append({
            "user_id": user_id,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": ip_address,
            "geo_location": geo_location,
            "device_id": device_id,
            "login_hour": hour,
            "is_new_device": is_new_device,
            "bytes_in": bytes_in,
            "bytes_out": bytes_out,
            "success": success,
            "is_anomaly": is_anomaly
        })
    
    # Create DataFrame and shuffle
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Save to CSV
    df.to_csv("sample_dataset.csv", index=False)
    print(f"Sample dataset generated with {len(df)} records")
    print(f"Anomalous records: {df['is_anomaly'].sum()}")
    print(f"Normal records: {len(df) - df['is_anomaly'].sum()}")

if __name__ == "__main__":
    generate_sample_data()