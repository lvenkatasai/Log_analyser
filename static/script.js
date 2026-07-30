document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const loading = document.getElementById('loading');
    const dashboard = document.getElementById('dashboard');
    let chartInstance = null;

    // Trigger file input on click
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) handleFile(files[0]);
    });

    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) handleFile(this.files[0]);
    });

    function handleFile(file) {
        if (!file.name.endsWith('.log') && !file.name.endsWith('.txt')) {
            alert("Please upload a .log or .txt file.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        // UI Updates
        dropZone.classList.add('hidden');
        loading.classList.remove('hidden');
        dashboard.classList.add('hidden');

        fetch('/api/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error("Server error");
            return response.json();
        })
        .then(data => {
            updateDashboard(data);
            loading.classList.add('hidden');
            dashboard.classList.remove('hidden');
        })
        .catch(error => {
            console.error(error);
            alert("An error occurred during analysis.");
            loading.classList.add('hidden');
            dropZone.classList.remove('hidden');
        });
    }

    function updateDashboard(data) {
        // Animate numbers (simple implementation)
        document.getElementById('total-logs').textContent = data.total_logs;
        document.getElementById('total-anomalies').textContent = data.total_anomalies;

        // Render Anomaly List
        const anomalyList = document.getElementById('anomaly-list');
        anomalyList.innerHTML = '';
        
        if (Object.keys(data.error_signatures).length === 0) {
            anomalyList.innerHTML = '<li><span class="name">No anomalies found</span></li>';
        } else {
            Object.entries(data.error_signatures)
                .sort((a, b) => b[1] - a[1])
                .forEach(([sig, count]) => {
                    if (count > 0) {
                        const li = document.createElement('li');
                        li.innerHTML = `<span class="name">${formatSignature(sig)}</span><span class="count">${count}</span>`;
                        anomalyList.appendChild(li);
                    }
                });
        }

        // Render Chart
        renderChart(data.level_counts);
    }

    function formatSignature(sig) {
        return sig.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }

    function renderChart(levelCounts) {
        const ctx = document.getElementById('levelChart').getContext('2d');
        
        const labels = Object.keys(levelCounts);
        const data = Object.values(levelCounts);
        
        // Custom colors based on severity
        const colors = labels.map(level => {
            switch(level) {
                case 'INFO': return '#3b82f6';
                case 'DEBUG': return '#94a3b8';
                case 'WARNING': return '#f59e0b';
                case 'ERROR': return '#ef4444';
                case 'CRITICAL': return '#b91c1c';
                default: return '#6366f1';
            }
        });

        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Log Count',
                    data: data,
                    backgroundColor: colors,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                const total = context.chart._metasets[context.datasetIndex].total;
                                const percentage = ((value / total) * 100).toFixed(1) + '%';
                                return `Count: ${value} (${percentage})`;
                            }
                        }
                    }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: '#e5e5e5' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
});
