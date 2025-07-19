import pandas as pd
import numpy as np

_input = r'./21018_PV_CEA_Thermo_Lighting.csv'
_output_day = r'./21018_PV_CEA_Thermo_Lighting_Default_Demand.csv'
_output_year = r'./21018_PV_CEA_Thermo_Lighting_Default_Demand_Yearly.csv'
df = pd.read_csv(_input, header=0)

'''
['Date/Time', 'PV.Minute.PU', 'BAT.Minute.PU',
       'baseline heating setpoint (C)', 'baseline cooling setpoint (C)',
       'base LED intensity (-)']
'''
turninWeightForLED = 5E-2
turningWeightThermo = 1E-2
noiseThreshold = 1e-2

fluxParamVals = df['BAT.Minute.PU'].values  # BAT.Minute.PU
baselineHtgSetC = df['baseline heating setpoint (C)'].values
baselineClgSetC = df['baseline cooling setpoint (C)'].values
baseLEDIntensity = df['base LED intensity (-)'].values  # base LED intensity (-)
maxHtg = np.max(baselineHtgSetC)  # Heating:Electricity [J](TimeStep)
maxClg = np.max(baselineClgSetC)  # Cooling:Electricity [J](TimeStep)

# Compute the turning magnitude across all time steps
magnitudeThermo = turningWeightThermo * fluxParamVals
clgMagnitude = magnitudeThermo * maxClg
htgMagnitude = magnitudeThermo * maxHtg
ledMagnitude = turninWeightForLED * fluxParamVals

def threshold_filter(arr, threshold=0.5):
    return np.where(np.abs(arr) < threshold, 0, arr)

clgMagnitude = threshold_filter(clgMagnitude, noiseThreshold)  # Apply threshold filter
htgMagnitude = threshold_filter(htgMagnitude, noiseThreshold)  # Apply threshold filter

newClg = baselineClgSetC.astype(float).copy()
newClg = baselineClgSetC.astype(float).copy()
newHtg = baselineHtgSetC.astype(float).copy()
newLED = baseLEDIntensity.astype(float).copy()

for t in range(1, 1080):
    newClg[t] = newClg[t-1] + clgMagnitude[t]
    newHtg[t] = newHtg[t-1] - htgMagnitude[t]
for t in range(1, 959):
    newLED[t] = newLED[t-1] - ledMagnitude[t]
    # newLED[t] = 0.5 - ledMagnitude[t]
conflict_indices = newHtg > newClg
newHtg[conflict_indices] = newClg[conflict_indices] - 1E-3
df['smoothHtgSetC'] = newHtg
df['smoothClgSetC'] = newClg
df['smoothLEDIntensity'] = newLED
df['clgMagnitude'] = clgMagnitude
df['htgMagnitude'] = htgMagnitude
df['ledMagnitude'] = ledMagnitude

df.to_csv(_output_day, index=False)


# Load original 1-day data
df = pd.read_csv(_output_day, header=0)
df=df[['Date/Time', 'smoothHtgSetC', 'smoothClgSetC', 'smoothLEDIntensity']]
# Number of minutes in a year
minutes_per_year = 365 * 24 * 60
# Repeat the data 365 times (assuming input has 1440 rows = 1 day)
df_year = pd.concat([df] * 365, ignore_index=True)
# Create a date range for one year with minute frequency
date_rng = pd.date_range(start='2024-01-01', periods=minutes_per_year, freq='min')
# Replace the first column with the new timestamps
df_year.iloc[:, 0] = date_rng
# Save to CSV
df_year.to_csv(_output_year, index=False)

