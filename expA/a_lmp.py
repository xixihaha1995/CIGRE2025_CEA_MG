'''
da_hrl_lmps_5021520.csv
the first row is the header, then it got another 8761 rows value, we only need the first 8760 rows of data
datetime_beginning_ept
total_lmp_da, with unit $/MWh
output file: da_hrl_lmps_5021520_sch.csv
datetime_beginning_ept,total_lmp_da,LED_Sch:
    Specifically for LED_Sch, the value is 1 if current time corresponds the lowest 12 hours total_lmp_da for that day,
    otherwise 0.
'''
import pandas as pd, os, numpy as np, datetime

_input = os.path.join('expA/da_hrl_lmps_8761_5021520.csv')
_output = os.path.join('expA/da_hrl_lmps_5021520_sch.csv')
photoperiod = 16
# Read the CSV file
df = pd.read_csv(_input, header=0)

# Extract the first 8760 rows
df = df.iloc[:8760]

# Make sure datetime is in datetime format
df['datetime_beginning_ept'] = pd.to_datetime(df['datetime_beginning_ept'])

# Create a new column for LED_Sch, initialize with 0
df['LED_Sch'] = 0

# Group by each day
df['date'] = df['datetime_beginning_ept'].dt.date
for date, group in df.groupby('date'):
    # Get the indices of the 12 lowest total_lmp_da values
    idx = group.nsmallest(photoperiod, 'total_lmp_da').index
    # Set LED_Sch to 1 for these indices
    df.loc[idx, 'LED_Sch'] = 1

# Drop the helper 'date' column
df = df[['datetime_beginning_ept', 'total_lmp_da', 'LED_Sch']]

# Save to output CSV
df.to_csv(_output, index=False)
