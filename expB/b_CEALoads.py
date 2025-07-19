'''
./0_BaseMitigation/CEA_Denver 0509_expB_BaseMitigation.csv
./1_CEAMitigation/CEA_Denver 0509_expB_CEAMitigation.csv
TimeStep = 1 minute = 60 second, 'Electricity:Facility [J](TimeStep) '
Find out max(max(baseline), max(smoothing)) for all timesteps
Then normalize both baseline and smoothing to that max value
output_temp:
./2_Voltage/b_profiles/May9_cea_baseline.csv
./2_Voltage/b_profiles/May9_cea_smoothing.csv
'''
import pandas as pd
import numpy as np

# Input paths
baseline_path = './0_BaseMitigation/CEA_Denver 0509_expB_BaseMitigation.csv'
smoothing_path = './1_CEAMitigation/CEA_Denver 0509_expB_CEAMitigation.csv'

# Output paths
baseline_out = './2_Voltage/b_profiles/SolarTAC_May9_cea_baseline.csv'
smoothing_out = './2_Voltage/b_profiles/SolarTAC_May9_cea_smoothing.csv'

# Column name to extract
energy_col = 'Electricity:Facility [J](TimeStep) '

# Load CSVs
baseline_df = pd.read_csv(baseline_path)
smoothing_df = pd.read_csv(smoothing_path)

# Get the maximum value across both datasets
max_val = max(baseline_df[energy_col].max(), smoothing_df[energy_col].max())

# Normalize
baseline_df['Normalized'] = baseline_df[energy_col] / max_val
smoothing_df['Normalized'] = smoothing_df[energy_col] / max_val

# Save the normalized profiles
baseline_df[['Normalized']].to_csv(baseline_out, index=False, header=False)
smoothing_df[['Normalized']].to_csv(smoothing_out, index=False, header=False)

print("Normalization complete. Output saved.")
