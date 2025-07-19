'''
input1: '11018_PV_CEA_Thermo_Lighting.csv'
input2: './2_Voltage/b_profiles/SolarTAC_LoadshapePV2_PU_minutely.csv'
get the value of input2, and replace the 'PV.Minute.PU' column in input1 with it.
and save it to '21018_PV_CEA_Thermo_Lighting.csv'


'''
import pandas as pd

# === Step 1: Load both CSVs ===
df1 = pd.read_csv('11018_PV_CEA_Thermo_Lighting.csv')
df2 = pd.read_csv('./2_Voltage/b_profiles/SolarTAC_LoadshapePV2_PU_minutely.csv', header=None)

# === Step 2: Replace 'PV.Minute.PU' column in df1 with values from df2 ===
if len(df1) != len(df2):
    raise ValueError(f"Row mismatch: df1 has {len(df1)} rows, df2 has {len(df2)} rows.")

df1['PV.Minute.PU'] = df2[0].values


window_size = 10 # 10 minutes in seconds
# Create a rolling window object for the moving average
original_data = df1['PV.Minute.PU']
rolling_window = original_data.rolling(window=window_size, min_periods=1)

# Calculate the moving average
window10min = rolling_window.mean()

# Calculate the difference between original data and moving average
new_data = window10min - original_data
df1['BAT.Minute.PU'] = new_data

# === Step 3: Save the updated dataframe ===
df1.to_csv('21018_PV_CEA_Thermo_Lighting.csv', index=False)

print("Saved updated file to: 21018_PV_CEA_Thermo_Lighting.csv")
