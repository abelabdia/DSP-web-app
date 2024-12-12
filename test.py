from app import generate_signal, low_pass_filter
t, signal = generate_signal(1000, 1.0, [10, 20], [1, 0.5])
filtered_signal = low_pass_filter(signal, 15, 1000, 2)
print(t, signal, filtered_signal)
