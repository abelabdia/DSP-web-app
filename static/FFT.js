document.getElementById('fftForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const func = document.getElementById('function').value;

    fetch('/calculate-fft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ function: func })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        // Plot the function
        const functionPlot = {
            x: data.x,
            y: data.y,
            type: 'scatter',
            mode: 'lines',
            name: 'Function',
            line: { color: 'blue' }
        };

        Plotly.newPlot('functionPlot', [functionPlot], {
            title: 'Function Plot',
            xaxis: { title: 'x' },
            yaxis: { title: 'y' }
        });

        // Plot the FFT amplitude
        const fftPlot = {
            x: data.fft_freq,
            y: data.fft_amp,
            type: 'scatter',
            mode: 'lines',
            name: 'FFT Amplitude',
            line: { color: 'red' }
        };

        Plotly.newPlot('fftPlot', [fftPlot], {
            title: 'FFT Amplitude Plot',
            xaxis: { title: 'Frequency (Hz)' },
            yaxis: { title: 'Amplitude' }
        });
    })
    .catch(error => {
        alert('Error: ' + error.message);
    });
});