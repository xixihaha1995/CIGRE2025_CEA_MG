'''
./0_fixed/CEA_Denver 0509_expA_fixed.csv Electricity:Facility [J](TimeStep) (it's 8761 rows with header, first 8760 values)
./1_shifted/CEA_Denver 0509_expA_shifted.csv Electricity:Facility [J](TimeStep) (it's 8761 rows with header, first 8760 values)
./rt_hrl_lmps_8762_5021520.csv total_lmp_rt (it's 8762 rows with header, first 8760 values)

output: expA.xlsx
columns: date, fixedJ, shiftJ, realTimeLMPDollarPerMWh
let's make a dummy date for year 2024 8760 hours
Great let's add two more columns:
fixedDollar, shiftDollar

./eplusout_April_24/CEA_Denver 0424_expMeter_fixed.xlsx
total_lmp_da($/MWh)
Cost($)_fixed
Cost($)_shift
GROWINGAREA1F:ZONE1:Zone Air Temperature [C](Hourly)_fixed
GROWINGAREA1F:ZONE1:Zone Air Temperature [C](Hourly)_shift
'''

import pandas as pd

# Load data
fixed = pd.read_csv('./0_fixed/CEA_Denver 0509_expA_fixed.csv')
shifted = pd.read_csv('./1_shifted/CEA_Denver 0509_expA_shifted.csv')
lmpRT = pd.read_csv('./rt_hrl_lmps_8762_5021520.csv')
lmpDA = pd.read_csv('./da_hrl_lmps_5021520_sch.csv')


# Extract first 8760 values
fixedJ = fixed['Electricity:Facility [J](TimeStep) '].iloc[:8760]
shiftJ = shifted['Electricity:Facility [J](TimeStep) '].iloc[:8760]
'IndoorLivingWall:InteriorLights:Electricity [J](TimeStep)'
shiftLightJ = shifted['IndoorLivingWall:InteriorLights:Electricity [J](TimeStep)'].iloc[:8760]
lmp_rt_values = lmpRT['total_lmp_rt'].iloc[:8760]
lmp_da_values = lmpDA['total_lmp_da'].iloc[:8760]

# Generate datetime index for every hour of 2024
date_range = pd.date_range(start='2024-01-01 00:00', periods=8760, freq='h')

# Compute dollar values
fixedDollar = fixedJ / 3.6e9 * lmp_rt_values
shiftDollar = shiftJ / 3.6e9 * lmp_rt_values

# Combine into a DataFrame
df = pd.DataFrame({
    'date': date_range,
    'fixedJ': fixedJ.values,
    'shiftJ': shiftJ.values,
    'shiftLightJ': shiftLightJ.values,
    'realTimeLMPDollarPerMWh': lmp_rt_values.values,
    'dayAheadLMPDollarPerMWh': lmp_da_values.values,
    'fixedDollar': fixedDollar.values,
    'shiftDollar': shiftDollar.values
})

# Output to Excel
df.to_excel('expA.xlsx', index=False)
total_fixed_cost = df['fixedDollar'].sum()
total_shift_cost = df['shiftDollar'].sum()

# Compute percentage savings
savings_pct = 100 * (total_fixed_cost - total_shift_cost) / total_fixed_cost

# Print summary
print(f"Total Fixed Cost:  ${total_fixed_cost:,.2f}")
print(f"Total Shifted Cost: ${total_shift_cost:,.2f}")
print(f"Cost Savings:       {savings_pct:.2f}%")