from flask import Flask, request, jsonify, send_file
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("Convolution.html")  # Serve the HTML file

@app.route("/process-signals", methods=["POST"])
def process_signals():
    # Get the signals from the request
    data = request.json
    signal1 = [float(x) for x in data["signal1"].split(",")]
    signal2 = [float(x) for x in data["signal2"].split(",")]

    # Calculate the convolution
    output = np.convolve(signal1, signal2).tolist()

    # Prepare the response data for Plotly as bar plots
    response = {
        "signal1": {"x": list(range(len(signal1))), "y": signal1, "type": "bar"},
        "signal2": {"x": list(range(len(signal2))), "y": signal2, "type": "bar"},
        "output": {"x": list(range(len(output))), "y": output, "type": "bar"},
    }

    return jsonify(response)
if __name__ == "__main__":
    app.run(debug=True)
