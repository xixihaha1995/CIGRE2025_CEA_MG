'''
_input = r'./1a_cea/TCL_htgClg_base.csv'
_colPV = 'PV.Minute.PU'
Normalized instantaneous PV panel irradiance load shape.
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Input and column setup ---
_input = './21018_PV_CEA_Thermo_Lighting.csv'
_colPV = 'PV.Minute.PU'

# --- Load data ---
df = pd.read_csv(_input)
pv_pu = df[_colPV]
time_index = pd.date_range(start='00:00', periods=len(pv_pu), freq='T')

# --- Plotting ---
fig, ax = plt.subplots(figsize=(3.5, 2.2))  # two-column fit

ax.plot(time_index, pv_pu, color='black')
ax.set_ylim(0, 1.05)
ax.set_ylabel('Normalized\nPV Irradiance', fontsize=10)
ax.set_yticks([0, 0.5, 1.0])
ax.set_xticks(pd.date_range(start='00:00', end='23:59', freq='3H'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.tick_params(axis='x', rotation=45)
ax.tick_params(labelsize=8)

# Layout adjustment
plt.tight_layout()
plt.show()
