document.getElementById('fft-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

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

        // Make the visualization container visible
        const container = document.getElementById('visualization-container');
        container.classList.remove('d-none');

        // Plot the original function
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

        // Resize the plots to ensure they fit their containers
        window.setTimeout(() => {
            Plotly.Plots.resize(document.getElementById('functionPlot'));
            Plotly.Plots.resize(document.getElementById('fftPlot'));
        }, 100); // Delay to allow container layout to stabilize
    })
    .catch(error => {
        alert('Error: ' + error.message);
    });
});
const plus = document.querySelector(".plus"),
minus = document.querySelector(".minus"),
num = document.querySelector(".num");
let a = 1;
plus.addEventListener("click", ()=>{
  a++;
  a = (a < 10) ? "0" + a : a;
  num.innerText = a;
});
minus.addEventListener("click", ()=>{
  if(a > 1){
    a--;
    a = (a < 10) ? "0" + a : a;
    num.innerText = a;
  }
});



