from flask import Flask, request, jsonify, send_file
import numpy as np
from scipy.fftpack import fft


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


def generate_signal(fs, duration, frequencies, amplitudes):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.zeros_like(t)
    for f, a in zip(frequencies, amplitudes):
        signal += a * np.sin(2 * np.pi * f * t)
    return t, signal

def low_pass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

@app.route('/process_signal1', methods=['POST'])
def process_signal1():
    fs = int(request.form['fs'])
    duration = float(request.form['duration'])
    frequencies = list(map(float, request.form['frequencies'].split(',')))
    amplitudes = list(map(float, request.form['amplitudes'].split(',')))
    cutoff = float(request.form['cutoff'])
    order = int(request.form['order'])
    
    t, signal = generate_signal(fs, duration, frequencies, amplitudes)
    filtered_signal = low_pass_filter(signal, cutoff, fs, order)
    
    return jsonify({
        'time': t.tolist(),
        'original': signal.tolist(),
        'filtered': filtered_signal.tolist()
    }   )



if __name__ == "__main__":
    app.run(debug=True)
