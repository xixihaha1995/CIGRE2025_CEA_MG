'''

input: r"../../3.smoothing./USA_CO_Denver.Intl.AP.725650_TMY3.epw"
input2: r"./20240101.csv"
output: r"./SolarTAC_USA_CO_Denver.Intl.AP.725650_TMY3.epw"
'''
import pandas as pd
import numpy as np

# ==== File paths ====
epw_path = "../../3.smoothing./USA_CO_Denver.Intl.AP.725650_TMY3.epw"
csv_path = "./20240101.csv"
output_path = "./SolarTAC_USA_CO_Denver.Intl.AP.725650_TMY3.epw"

# ==== Step 1: Read EPW file ====
with open(epw_path, 'r') as f:
    epw_lines = f.readlines()

epw_header = epw_lines[:8]
epw_data = [line.strip().split(',') for line in epw_lines[8:]]
epw_df = pd.DataFrame(epw_data)

# ==== Step 2: Read new CSV file ====
df_new = pd.read_csv(csv_path)

# Parse date and hour to create datetime
df_new['date_only'] = pd.to_datetime(df_new['DATE (MM/DD/YYYY)'], format='%m/%d/%Y')
df_new['datetime'] = df_new['date_only'] + pd.to_timedelta(df_new['HOUR-MST'], unit='h')

# Extract time parts for alignment if needed
df_new['hour'] = df_new['datetime'].dt.hour
df_new['month'] = df_new['datetime'].dt.month
df_new['day'] = df_new['datetime'].dt.day

# ==== Step 3: Map real columns to EPW fields ====
columns_to_update = {
    6: 'Avg Air Temperature [deg C]',               # Dry Bulb Temp (°C)
    7: 'Avg Dew Point Temp [deg C]',                # Dew Point Temp (°C)
    8: 'Avg Rel Humidity [%]',                      # Relative Humidity (%)
    9: 'Avg Station Pressure [mBar]',               # Pressure (Pa) → convert to Pa
    13: 'Avg Global Horizontal [W/m^2]',            # GHI (Wh/m2)
    14: 'Avg Direct Normal [W/m^2]',                # DNI (Wh/m2)
    15: 'Avg Diffuse Horizontal [W/m^2]',           # DHI (Wh/m2)
    21: 'Avg Avg Wind Speed @ 10m [m/s]'            # Wind Speed (m/s)
}

# Convert pressure from mBar to Pa (1 mBar = 100 Pa)
df_new['Avg Station Pressure [mBar]'] = df_new['Avg Station Pressure [mBar]'] * 100

# ==== Step 4: Replace EPW fields ====
n_rows = min(len(df_new), len(epw_df), 8760)  # just to be extra safe

for i in range(n_rows):
    row = df_new.iloc[i]
    for col_index, col_name in columns_to_update.items():
        new_val = row.get(col_name, '')
        if pd.isna(new_val):
            continue
        epw_df.iat[i, col_index] = f"{float(new_val):.1f}"


# ==== Step 5: Write updated EPW ====
with open(output_path, 'w') as f:
    for line in epw_header:
        f.write(line)
    for i in range(len(epw_df)):
        line = ",".join(epw_df.iloc[i].astype(str)) + "\n"
        f.write(line)

print(f"Updated EPW file saved to: {output_path}")
