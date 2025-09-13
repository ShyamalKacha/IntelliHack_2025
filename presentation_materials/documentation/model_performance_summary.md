# Model Performance Summary

## Overall Performance
- **Accuracy**: 99.98%
- **Precision**: ~99%
- **Recall**: ~99%
- **F1-Score**: ~99%

## Confusion Matrix
```
                 Predicted
               Normal  Anomaly
Actual Normal   9323      0
     Anomaly      0     677
```

## Performance on Different Anomaly Types
- **New Device Anomalies**: 100% accuracy
- **High Data Transfer Anomalies**: 100% accuracy
- **Unusual Hour Anomalies**: 100% accuracy
- **Foreign Location Anomalies**: 99.94% accuracy

## Top 10 Most Important Features
1. Bytes out: 0.3775
2. Bytes in: 0.3565
3. Is new device: 0.1149
4. Success: 0.0818
5. Device login frequency: 0.0638
6. Device ID encoded: 0.0014
7. Location login frequency: 0.0012
8. Geo-location encoded: 0.0009
9. User login frequency: 0.0007
10. Login day: 0.0005

## Dataset Information
- **Total Samples**: 50,000
- **Normal Logins**: 46,616 (93.2%)
- **Anomalous Logins**: 3,384 (6.8%)