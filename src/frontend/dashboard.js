// Dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    let anomalyChart, hourlyChart, geoChart;
    
    // Fetch and display stats
    function fetchStats() {
        fetch('/predictions/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-predictions').textContent = data.total_predictions;
                document.getElementById('anomaly-count').textContent = data.anomaly_count;
                document.getElementById('accuracy').textContent = (data.accuracy * 100).toFixed(1) + '%';
                document.getElementById('response-time').textContent = '45ms'; // Simulated
                
                // Update charts
                updateAnomalyChart(data);
                updateHourlyChart(data);
                updateGeoChart(data);
            })
            .catch(error => {
                console.error('Error fetching stats:', error);
            });
    }
    
    // Fetch and display recent predictions
    function fetchRecentPredictions() {
        fetch('/predictions/history')
            .then(response => response.json())
            .then(data => {
                const predictionsBody = document.getElementById('predictions-body');
                predictionsBody.innerHTML = '';
                
                // Show last 10 predictions
                const recentPredictions = data.slice(-10).reverse();
                
                recentPredictions.forEach(prediction => {
                    const row = document.createElement('div');
                    row.className = 'table-row';
                    
                    const timestamp = new Date(prediction.timestamp).toLocaleString();
                    const userId = prediction.input_data.user_id || 'Unknown';
                    const location = prediction.input_data.geo_location || 'Unknown';
                    const device = prediction.input_data.device_id || 'Unknown';
                    const status = prediction.prediction.anomaly === 1 ? 'Anomaly' : 'Normal';
                    const statusClass = prediction.prediction.anomaly === 1 ? 'status-anomaly' : 'status-normal';
                    
                    row.innerHTML = `
                        <div>${timestamp}</div>
                        <div>${userId}</div>
                        <div>${location}</div>
                        <div>${device}</div>
                        <div class="${statusClass}">${status}</div>
                    `;
                    
                    predictionsBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching predictions:', error);
            });
    }
    
    // Update anomaly distribution chart
    function updateAnomalyChart(data) {
        const ctx = document.getElementById('anomalyChart').getContext('2d');
        
        if (anomalyChart) {
            anomalyChart.destroy();
        }
        
        anomalyChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Normal', 'Anomaly'],
                datasets: [{
                    data: [data.normal_count, data.anomaly_count],
                    backgroundColor: [
                        'rgba(0, 255, 157, 0.7)',
                        'rgba(255, 77, 77, 0.7)'
                    ],
                    borderColor: [
                        'rgba(0, 255, 157, 1)',
                        'rgba(255, 77, 77, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#e0e0ff',
                            font: {
                                family: 'Orbitron'
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Update hourly activity chart
    function updateHourlyChart(data) {
        const ctx = document.getElementById('hourlyChart').getContext('2d');
        
        if (hourlyChart) {
            hourlyChart.destroy();
        }
        
        // Prepare data for chart
        const hours = Array.from({length: 24}, (_, i) => i);
        const counts = hours.map(hour => data.hourly_distribution[hour] || 0);
        
        hourlyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Login Attempts',
                    data: counts,
                    backgroundColor: 'rgba(0, 243, 255, 0.7)',
                    borderColor: 'rgba(0, 243, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#e0e0ff'
                        },
                        grid: {
                            color: 'rgba(0, 243, 255, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#e0e0ff'
                        },
                        grid: {
                            color: 'rgba(0, 243, 255, 0.1)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#e0e0ff',
                            font: {
                                family: 'Orbitron'
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Update geographic distribution chart
    function updateGeoChart(data) {
        const ctx = document.getElementById('geoChart').getContext('2d');
        
        if (geoChart) {
            geoChart.destroy();
        }
        
        // Get top 5 locations
        const locations = Object.entries(data.geographic_distribution)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);
        
        const labels = locations.map(loc => loc[0]);
        const counts = locations.map(loc => loc[1]);
        
        geoChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        'rgba(0, 243, 255, 0.7)',
                        'rgba(255, 0, 200, 0.7)',
                        'rgba(0, 255, 157, 0.7)',
                        'rgba(255, 204, 0, 0.7)',
                        'rgba(102, 51, 153, 0.7)'
                    ],
                    borderColor: [
                        'rgba(0, 243, 255, 1)',
                        'rgba(255, 0, 200, 1)',
                        'rgba(0, 255, 157, 1)',
                        'rgba(255, 204, 0, 1)',
                        'rgba(102, 51, 153, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#e0e0ff',
                            font: {
                                family: 'Orbitron'
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Initial data load
    fetchStats();
    fetchRecentPredictions();
    
    // Refresh data every 30 seconds
    setInterval(() => {
        fetchStats();
        fetchRecentPredictions();
    }, 30000);
});