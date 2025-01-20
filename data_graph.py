import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def dba_to_db(dba, frequency):
    """
    Converts dBA (A-weighted decibels) to dB (unweighted decibels) based on the frequency.
    Args:
        dba (float): Sound level in dBA.
        frequency (float): Frequency of the sound in Hz.
    Returns:
        float: Approximate sound level in dB.
    """
    # ISO 226:2003 A-weighting adjustment factors (in dB) at standard frequencies
    a_weighting_table = {
        10: -70.4, 12.5: -63.4, 16: -56.7, 20: -50.5, 25: -44.7, 
        31.5: -39.4, 40: -34.6, 50: -30.2, 63: -26.2, 80: -22.5, 
        100: -19.1, 125: -16.1, 160: -13.4, 200: -10.9, 250: -8.6, 
        315: -6.6, 400: -4.8, 500: -3.2, 630: -1.9, 800: -0.8, 
        1000: 0.0, 1250: 0.6, 1600: 1.0, 2000: 1.2, 2500: 1.3, 
        3150: 1.2, 4000: 1.0, 5000: 0.5, 6300: -0.1, 8000: -1.1, 
        10000: -2.5, 12500: -4.3, 16000: -6.6, 20000: -9.3
    }
    
    # Interpolate the A-weighting adjustment for the given frequency
    freq_list = np.array(list(a_weighting_table.keys()))
    weight_list = np.array(list(a_weighting_table.values()))
    adjustment = np.interp(frequency, freq_list, weight_list)
    
    # Convert dBA to dB
    db = dba - adjustment
    return db

# Load data
file_path = 'data.csv'
data = pd.read_csv(file_path, delimiter=';', header=None)

# Extract frequencies and dBA values
frequencies = list(map(int, data.iloc[0, 1:].dropna()))
dba_values = data.iloc[1:, 1:].applymap(float)

# Convert dBA to dB
db_values = dba_values.copy()
for i, frequency in enumerate(frequencies):
    db_values.iloc[:, i] = dba_values.iloc[:, i].apply(lambda dba: dba_to_db(dba, frequency))

# Compute average dB per frequency
average_db_per_frequency = {
    frequency: sum(column_data) / len(column_data)
    for frequency, column_data in zip(frequencies, db_values.T.values)
}

# Save average dB values
average_df = pd.DataFrame(list(average_db_per_frequency.items()), columns=["Frequency (Hz)", "Average dB"])
output_path = "average_db_per_frequency.csv"
average_df.to_csv(output_path, index=False)

# Plot all datasets in dB
plt.figure(figsize=(12, 6))
for index, row in db_values.iterrows():
    plt.plot(frequencies, row, label=f"Dataset {index}")

# Add graph aesthetics
plt.xlabel("Frequency (Hz)")
plt.ylabel("Sound Level (dB)")
plt.title("Frequency vs. Sound Level (in dB)")
plt.legend()
plt.grid(True)

# Save and display the plot
plt.savefig("Hz_to_dBA")
plt.show()

print(f"Averages saved to: {output_path}")
