import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def visualize_feature_importance():
    # Load the trained model
    model = joblib.load('anomaly_detection_model.pkl')
    
    # Define feature names
    features = [
        'login_hour', 'login_day', 'login_month', 'login_year', 'login_weekday',
        'is_new_device', 'bytes_in', 'bytes_out', 'success',
        'geo_location_encoded', 'device_id_encoded',
        'user_login_frequency', 'device_login_frequency', 'location_login_frequency'
    ]
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Create DataFrame for visualization
    feature_importance_df = pd.DataFrame({
        'feature': features,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    # Plot feature importances
    plt.figure(figsize=(12, 8))
    sns.barplot(data=feature_importance_df, x='importance', y='feature', palette='viridis')
    plt.title('Feature Importance for Anomaly Detection')
    plt.xlabel('Importance')
    plt.ylabel('Features')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    plt.close()
    
    # Print top features
    print("Top 10 Most Important Features:")
    print("===============================")
    for i, row in feature_importance_df.head(10).iterrows():
        print(f"{row['feature']}: {row['importance']:.4f}")
    
    print("\nFeature importance plot saved as 'feature_importance.png'")
    
    # Create correlation matrix
    # Load sample data to calculate correlations
    df = pd.read_csv('../../data/sample_dataset.csv')
    
    # Select numerical features
    numerical_features = [
        'login_hour', 'is_new_device', 'bytes_in', 'bytes_out', 'success'
    ]
    
    # Calculate correlation matrix
    corr_matrix = df[numerical_features + ['is_anomaly']].corr()
    
    # Plot correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5)
    plt.title('Correlation Matrix of Features')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    plt.close()
    
    print("\nCorrelation matrix saved as 'correlation_matrix.png'")

if __name__ == "__main__":
    visualize_feature_importance()