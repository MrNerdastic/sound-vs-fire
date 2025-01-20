import numpy as np
import matplotlib.pyplot as plt

# Define the x-axis values
t = np.linspace(0, 1, 5000)  # 0 to 1 second with 500 points

# Define the sine wave parameters
frequencies = [200]  # Frequencies of the sine waves in Hz
amplitudes = [1]  # Amplitudes of the sine waves

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each sine wave
for freq, amp in zip(frequencies, amplitudes):
    y = amp * np.sin(2 * np.pi * freq * t)
    plt.plot(t, y, label=f'{amp}*sin(2π*{freq}*t)')

# Add labels, title, and legend
plt.title('Sine Waves')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.grid(alpha=0.5)
plt.savefig("images/" + str(frequencies[0]))

# Show the plot
plt.show()