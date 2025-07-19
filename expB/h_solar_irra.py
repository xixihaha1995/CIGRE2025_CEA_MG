'''
input:./SolarTAC_PretendJuly8.csv
open it, get its column "Global Horizontal [W/m^2]",
normalize it (divide by its max value),
save it to (without header and index): './2_Voltage/b_profiles/SolarTAC_LoadshapePV2_PU_minutely.csv'
'''
import pandas as pd

# === Step 1: Load the CSV ===
input_path = './SolarTAC_PretendJuly8.csv'
df = pd.read_csv(input_path)

# === Step 2: Extract and normalize the "Global Horizontal [W/m^2]" column ===
ghi_col = 'Global Horizontal [W/m^2]'
ghi = df[ghi_col]
ghi_normalized = ghi / ghi.max()

# === Step 3: Save to new file (no header, no index) ===
output_path = './2_Voltage/b_profiles/SolarTAC_LoadshapePV2_PU_minutely.csv'
ghi_normalized.to_csv(output_path, index=False, header=False)

print(f"Normalized GHI saved to: {output_path}")
