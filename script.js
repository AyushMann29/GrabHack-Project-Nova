document.getElementById('loan-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('http://127.0.0.1:5000/predict', { // Replace with your Flask server URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Display metrics
        const metricsDiv = document.getElementById('metrics-data');
        metricsDiv.innerHTML = `
            <p><strong>Accuracy:</strong> ${(result.metrics.accuracy * 100).toFixed(2)}%</p>
            <p><strong>Precision:</strong> ${(result.metrics.precision * 100).toFixed(2)}%</p>
            <p><strong>Recall:</strong> ${(result.metrics.recall * 100).toFixed(2)}%</p>
            <p><strong>F1-Score:</strong> ${(result.metrics.f1_score * 100).toFixed(2)}%</p>
        `;

        // Display prediction
        const predictionDiv = document.getElementById('prediction-result');
        if (result.prediction === "eligible") {
            predictionDiv.innerHTML = "<p>🎉 Congratulations! You are eligible for a loan.</p>";
            predictionDiv.style.color = "green";
        } else {
            predictionDiv.innerHTML = "<p>😞 We're sorry, you are not eligible for a loan at this time.</p>";
            predictionDiv.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Error:', error);document.addEventListener('DOMContentLoaded', () => {
            const tabSingle = document.getElementById('tab-single');
            const tabCsv = document.getElementById('tab-csv');
            const singleEntryForm = document.getElementById('single-entry-form');
            const csvUploadForm = document.getElementById('csv-upload-form');
            const form = document.getElementById('loan-form');
            const csvForm = document.getElementById('csv-form');
            const metricsSection = document.getElementById('metrics-section');
            const metricsData = document.getElementById('metrics-data');
            const predictionResult = document.getElementById('prediction-result');
            const csvResultsTable = document.getElementById('csv-results-table');

            // Tab switching logic
            tabSingle.addEventListener('click', () => {
                tabSingle.classList.add('border-blue-600', 'text-blue-600');
                tabCsv.classList.remove('border-blue-600', 'text-blue-600');
                tabCsv.classList.add('border-transparent', 'text-gray-500', 'hover:text-gray-700');
                singleEntryForm.classList.remove('hidden');
                csvUploadForm.classList.add('hidden');
                predictionResult.classList.add('hidden');
                csvResultsTable.classList.add('hidden');
            });

            tabCsv.addEventListener('click', () => {
                tabCsv.classList.add('border-blue-600', 'text-blue-600');
                tabSingle.classList.remove('border-blue-600', 'text-blue-600');
                tabSingle.classList.add('border-transparent', 'text-gray-500', 'hover:text-gray-700');
                csvUploadForm.classList.remove('hidden');
                singleEntryForm.classList.add('hidden');
                predictionResult.classList.add('hidden');
                csvResultsTable.classList.add('hidden');
            });

            // Function to display the model metrics
            function displayMetrics(metrics) {
                metricsSection.classList.remove('hidden');
                metricsData.innerHTML = `
                    <div class="flex items-center space-x-2">
                        <svg class="h-6 w-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                        <p class="font-medium">Accuracy: <span class="text-blue-600">${(metrics.accuracy * 100).toFixed(2)}%</span></p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <svg class="h-6 w-6 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM11 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2h-2zM11 9a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2h-2zM5 9a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5z" />
                        </svg>
                        <p class="font-medium">Precision: <span class="text-blue-600">${(metrics.precision * 100).toFixed(2)}%</span></p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <svg class="h-6 w-6 text-indigo-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                            <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                        </svg>
                        <p class="font-medium">Recall: <span class="text-blue-600">${(metrics.recall * 100).toFixed(2)}%</span></p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <svg class="h-6 w-6 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M3 12a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
                            <path d="M10 3a1 1 0 011 1v12a1 1 0 11-2 0V4a1 1 0 011-1z" />
                        </svg>
                        <p class="font-medium">F1-Score: <span class="text-blue-600">${(metrics.f1_score * 100).toFixed(2)}%</span></p>
                    </div>
                `;
            }

            // Handle single entry form submission
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                predictionResult.classList.remove('hidden');
                predictionResult.innerHTML = 'Checking eligibility...';
                predictionResult.classList.remove('bg-green-100', 'bg-red-100', 'text-green-800', 'text-red-800');
                csvResultsTable.classList.add('hidden');
                
                const formData = new FormData(form);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = value;
                });
                
                const backendEndpoint = 'http://localhost:5000/predict'; 
                try {
                    const response = await fetch(backendEndpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data),
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const result = await response.json();

                    displayMetrics(result.metrics);

                    if (result.prediction === 'eligible') {
                        predictionResult.textContent = 'Congratulations! You are eligible for a loan.';
                        predictionResult.classList.add('bg-green-100', 'text-green-800');
                    } else {
                        predictionResult.textContent = "We're sorry, you are not eligible for a loan at this time.";
                        predictionResult.classList.add('bg-red-100', 'text-red-800');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    predictionResult.textContent = `There was a problem checking your eligibility. Please ensure the backend is running at ${backendEndpoint}.`;
                    predictionResult.classList.add('bg-red-100', 'text-red-800');
                }
            });

            // Handle CSV form submission
            csvForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                predictionResult.classList.remove('hidden');
                predictionResult.innerHTML = 'Processing CSV file...';
                predictionResult.classList.remove('bg-green-100', 'bg-red-100', 'text-green-800', 'text-red-800');
                csvResultsTable.classList.add('hidden');

                const csvFile = document.getElementById('csvFile').files[0];
                if (!csvFile) {
                    predictionResult.textContent = 'Please select a CSV file to upload.';
                    predictionResult.classList.add('bg-red-100', 'text-red-800');
                    return;
                }

                const formData = new FormData();
                formData.append('file', csvFile);

                const backendEndpoint = 'http://localhost:5000/predict_csv'; 
                try {
                    const response = await fetch(backendEndpoint, {
                        method: 'POST',
                        body: formData,
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const result = await response.json();

                    displayMetrics(result.metrics);
                    displayCsvResults(result.predictions);
                    
                    predictionResult.classList.add('hidden');

                } catch (error) {
                    console.error('Error:', error);
                    predictionResult.textContent = `There was a problem processing the CSV file. Please ensure the backend is running at ${backendEndpoint}.`;
                    predictionResult.classList.add('bg-red-100', 'text-red-800');
                }
            });

            function displayCsvResults(predictions) {
                csvResultsTable.classList.remove('hidden');
                let html = `<div class="overflow-x-auto rounded-lg shadow-md">
                                <table class="min-w-full table-auto divide-y divide-gray-200">
                                    <thead class="bg-gray-200">
                                        <tr>`;
                
                // Create table headers
                if (predictions.length > 0) {
                    const headers = Object.keys(predictions[0]);
                    headers.forEach(header => {
                        html += `<th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">${header}</th>`;
                    });
                }
                html += `</tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">`;

                // Create table rows with data
                predictions.forEach(row => {
                    html += `<tr>`;
                    Object.values(row).forEach(value => {
                        html += `<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${value}</td>`;
                    });
                    html += `</tr>`;
                });

                html += `</tbody></table></div>`;
                csvResultsTable.innerHTML = html;
            }
        });
        document.getElementById('prediction-result').innerHTML = "<p>There was an error with the request. Please try again.</p>";
    });
});