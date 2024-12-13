from flask import Flask, request, jsonify, send_file
import numpy as np
from numpy import sin, cos,pi
from scipy.fftpack import fft
from scipy.signal import butter, lfilter


app = Flask(__name__)

@app.route("/")
def home():
    return send_file("Convolution.html") 

@app.route("/fft")
def fftpage():
    return send_file("FFT.html")     

@app.route("/filters")
def filterpage():
    return send_file("Filters.html") 



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

  




# Route pour calculer le spectre FFT d'une fonction continue
@app.route('/calculate-fft', methods=['POST'])
def calculate_fft():
    data = request.get_json()
    func = data['function']
    x = np.linspace(0, 10, 1000)  # Domaine de définition de la fonction
    try:
        # Évalue la fonction continue
        y = eval(func)
    except Exception as e:
        return jsonify({"error": f"Erreur dans la fonction saisie : {e}"})

    # Calcul de la FFT
    fft_result = fft(y)
    freq = np.fft.fftfreq(len(y), d=(x[1] - x[0]))

    # Préparer les données pour l'affichage
    result = {
        "x": list(x),
        "y": list(y),
        "fft_freq": list(freq[:len(freq)//2]),
        "fft_amp": list(abs(fft_result)[:len(fft_result)//2])
    }
    return jsonify(result)



# Helper function: Signal generation
def generate_signal(fs, duration, frequencies, amplitudes):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = sum(amplitude * np.sin(2 * np.pi * freq * t) for freq, amplitude in zip(frequencies, amplitudes))
    return t, signal

# Helper function: Low-pass filter
def low_pass_filter(data, cutoff, fs, order):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

@app.route('/process_signal1', methods=['POST'])
def process_signal1():
    try:
        # Parse input values
        fs = int(request.form['fs'])
        duration = float(request.form['duration'])
        frequencies = list(map(float, request.form['frequencies'].split(',')))
        amplitudes = list(map(float, request.form['amplitudes'].split(',')))
        cutoff = float(request.form['cutoff'])
        order = int(request.form['order'])

        # Validate inputs
        if len(frequencies) != len(amplitudes):
            raise ValueError("Frequencies and amplitudes must have the same length.")
        if fs <= 0 or duration <= 0 or cutoff <= 0 or order <= 0:
            raise ValueError("All input values must be positive numbers.")
        if cutoff >= fs / 2:
            raise ValueError("Cutoff frequency must be less than Nyquist frequency (fs/2).")

        # Generate and filter the signal
        t, signal = generate_signal(fs, duration, frequencies, amplitudes)
        filtered_signal = low_pass_filter(signal, cutoff, fs, order)

        # Return JSON response
        return jsonify({
            'time': t.tolist(),
            'original': signal.tolist(),
            'filtered': filtered_signal.tolist()
        })

    except Exception as e:
        # Log the error and return error message
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

