// Prediction functionality
document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.getElementById('prediction-form');
    const predictionResult = document.getElementById('prediction-result');
    
    // Set default timestamp to current time
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    
    document.getElementById('timestamp').value = `${year}-${month}-${day}T${hours}:${minutes}`;
    
    // Handle form submission
    predictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(predictionForm);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            // Convert numeric fields to numbers
            if (['login_hour', 'is_new_device', 'bytes_in', 'bytes_out', 'success'].includes(key)) {
                data[key] = parseInt(value);
            } else {
                data[key] = value;
            }
        }
        
        // Show loading state
        predictionResult.querySelector('.result-content').innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Analyzing login data...</p>
            </div>
        `;
        
        // Send prediction request
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            displayPredictionResult(result);
        })
        .catch(error => {
            console.error('Error:', error);
            displayError('Failed to analyze login data. Please try again.');
        });
    });
    
    // Display prediction result
    function displayPredictionResult(result) {
        const resultContent = predictionResult.querySelector('.result-content');
        
        if (result.error) {
            displayError(result.error);
            return;
        }
        
        const isAnomaly = result.anomaly === 1;
        const probability = isAnomaly ? result.probability_anomaly : result.probability_normal;
        const status = isAnomaly ? 'Anomaly Detected' : 'Normal Login';
        const statusClass = isAnomaly ? 'anomaly' : 'normal';
        
        resultContent.innerHTML = `
            <div class="result-header ${statusClass}">
                <h4>${status}</h4>
                <p>Confidence: ${(probability * 100).toFixed(2)}%</p>
            </div>
            <div class="result-details">
                <div class="probability-bar">
                    <div class="probability-label">Normal</div>
                    <div class="probability-bar-container">
                        <div class="probability-fill" style="width: ${(result.probability_normal * 100)}%; background-color: ${isAnomaly ? '#00ff9d' : '#00f3ff'}"></div>
                    </div>
                    <div class="probability-label">Anomaly</div>
                </div>
                <div class="probability-values">
                    <div>Normal: ${(result.probability_normal * 100).toFixed(2)}%</div>
                    <div>Anomaly: ${(result.probability_anomaly * 100).toFixed(2)}%</div>
                </div>
            </div>
            <div class="result-actions">
                <button id="reset-form" class="btn btn-secondary">Reset Form</button>
            </div>
        `;
        
        // Add event listener to reset button
        document.getElementById('reset-form').addEventListener('click', function() {
            predictionForm.reset();
            // Reset timestamp to current time
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            document.getElementById('timestamp').value = `${year}-${month}-${day}T${hours}:${minutes}`;
            
            resultContent.innerHTML = '<p>Enter login data and click "Run Detection" to analyze for anomalies.</p>';
        });
    }
    
    // Display error message
    function displayError(message) {
        const resultContent = predictionResult.querySelector('.result-content');
        resultContent.innerHTML = `
            <div class="error">
                <h4>Error</h4>
                <p>${message}</p>
                <button id="reset-form" class="btn btn-secondary">Reset Form</button>
            </div>
        `;
        
        // Add event listener to reset button
        document.getElementById('reset-form').addEventListener('click', function() {
            predictionForm.reset();
            // Reset timestamp to current time
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            document.getElementById('timestamp').value = `${year}-${month}-${day}T${hours}:${minutes}`;
            
            resultContent.innerHTML = '<p>Enter login data and click "Run Detection" to analyze for anomalies.</p>';
        });
    }
});