import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def dba_to_db(dba, frequency):
    """
    Converts dBA (A-weighted decibels) to dB (unweighted decibels) based on the frequency.
    Args:
        dba (float): Sound level in dBA (between 5 and 120 dBA).
        frequency (float): Frequency of the sound in Hz (within 10 Hz to 20,000 Hz range).
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
    
    # Extract frequencies and corresponding A-weighting adjustments
    freq_list = np.array(list(a_weighting_table.keys()))
    weight_list = np.array(list(a_weighting_table.values()))
    
    # Interpolate the A-weighting adjustment for the given frequency
    adjustment = np.interp(frequency, freq_list, weight_list)
    
    # Convert dBA to dB by reversing the A-weighting adjustment
    db = dba - adjustment
    return db

# Load the average dBA data
file_path = "average_dba_per_frequency.csv"
average_data = pd.read_csv(file_path)

# Convert Average dBA to Average dB
average_data["Average dB"] = average_data.apply(
    lambda row: dba_to_db(row["Average dBA"], row["Frequency (Hz)"]), axis=1
)

# Plot the Average dB vs Frequency
plt.figure(figsize=(12, 6))
plt.plot(average_data["Frequency (Hz)"], average_data["Average dB"], marker='o', color='blue', label="Average dB")

plt.xlabel("Frequency (Hz)")
plt.ylabel("Average Sound Level (dB)")
plt.title("Average dB vs. Frequency")
plt.legend()
plt.grid(True)
plt.savefig("average")
plt.show()
