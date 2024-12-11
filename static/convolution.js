
function plotSignal(data, divId, title) {

  // Create the bar trace
  const barTrace = {
    x: data.x,
    y: data.y,
    type: 'bar', // Bar plot for impulses
    name: title,
    marker: { color: '#ffcb56' }, // Bar color
    width: 0.01, // Set the width of the bars to make them thinner
    hovertemplate: `${title}<br>Sample Index: %{x}<br>Amplitude: %{y}<extra></extra>` // Custom hover info for bars
  };

  // Create the scatter trace for circles on top of the bars
  const scatterTrace = {
    x: data.x,
    y: data.y,
    mode: 'markers', // Use markers for circles
    marker: {
      color: '#ffcb56', // Circle color
      size: 15, // Size of the circles
      symbol: 'circle' // Shape of the markers
    },
    showlegend: false, // Prevent the circles from appearing in the legend
    hoverinfo: 'none' // Disable hover info for circles
  };

  // Plot both traces
  Plotly.react(divId, [barTrace, scatterTrace], {
    title: {
        text:title,
        font: { size: 22, family: 'Courier New, monospace', color: '#0ff' }
    },
    xaxis: {
        title: { text: 'Sample Index', font: { size: 14, color: '#0ff' } },
        linecolor: '#0ff',
        gridcolor: '#055'
    },
    yaxis: {
        title: { text: 'Amplitude', font: { size: 14, color: '#0ff' } },
        linecolor: '#0ff',
        gridcolor: '#055'
    },
    margin: { t: 30, l: 50, r: 30, b: 50 },
    paper_bgcolor: '#000',     // Black container background
    plot_bgcolor: '#111',      // Slightly lighter black plot area
    showlegend: true,
    legend: { font: { size: 14, color: '#0ff' } }
});
}

  
// Fetch and plot signals when the form is submitted
document.getElementById('signal-form').onsubmit = async function (e) {
    e.preventDefault();

    const signal1 = document.getElementById('signal1').value;
    const signal2 = document.getElementById('signal2').value;

    // Check if signals are valid
    if (!signal1 || !signal2) {
        document.getElementById('visualization-container').classList.add('d-none');
        return; // Exit if signals are not valid
    }

    const response = await fetch('/process-signals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ signal1, signal2 })
    });

    const result = await response.json();
    plotSignal(result.signal1, 'plot-signal1', 'Signal 1');
    plotSignal(result.signal2, 'plot-signal2', 'Signal 2');
    plotSignal(result.output, 'plot-output', 'Convolution Output');

    // Display the output signal as text
    const outputSignalText = result.output.y.join(', '); // Assuming result.output.y contains the output signal values
    document.getElementById('output-signal-text').textContent = outputSignalText;

    // Show the visualization section
    document.getElementById('visualization-container').classList.remove('d-none');
};
    
