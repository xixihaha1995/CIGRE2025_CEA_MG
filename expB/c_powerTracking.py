'''
With header:
'./1a_cea/TCL_htgClg_base.csv', PV.Minute.PU, BAT.Minute.PU
Without header:
output_dir_base = '../../ieee33/b_1_bs2025/normalized/base/base_1.csv'
output_dir_flexible = '../../ieee33/b_1_bs2025/normalized/flexible/flexible_1.csv'

All the data about to plot is minute-based 24-hour data,
please plot them into one figure, but give me option to choose which bldID to plot.
'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -------------- USER‑SET PARAMETERS --------------
bldID        = 1          # choose which building ID if you add that later
start_zoom   = '10:00'    # zoom window
end_zoom     = '11:00'
two_col_w_in = 7.0        # figure width for two‑column papers (inches)
aspect       = 0.55       # height / width ratio
# -------------------------------------------------

# File paths
header_file         = './21018_PV_CEA_Thermo_Lighting_Default_Demand.csv'
output_dir_base     = './2_Voltage/b_profiles/SolarTAC_May9_cea_baseline.csv'
output_dir_flexible = './2_Voltage/b_profiles/SolarTAC_May9_cea_smoothing.csv'

# --- Load data -----------------------------------------------------------
time_index = pd.date_range('00:00', periods=1440, freq='T')  # 24 h, 1‑min steps

df_header = pd.read_csv(header_file)
pv_pu  = df_header['PV.Minute.PU']
bat_pu = df_header['BAT.Minute.PU']           # (still loaded in case you want it)

base = pd.read_csv(output_dir_base, header=None).squeeze()
flex = pd.read_csv(output_dir_flexible, header=None).squeeze()
diff = flex - base

# --- Apply zoom window ---------------------------------------------------
mask     = (time_index >= start_zoom) & (time_index <= end_zoom)
t_zoom   = time_index[mask]
pv_zoom  = pv_pu[mask]
diff_zoom = diff[mask]

# --- Helper for y‑limits -------------------------------------------------
def bounds(series, pad=0.05):
    lo, hi = series.min(), series.max()
    rng     = hi - lo
    return lo - pad*rng, hi + pad*rng if rng else (lo-0.1, hi+0.1)

# ------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(two_col_w_in, two_col_w_in*aspect))

# PV (left axis)
ax1.plot(t_zoom, pv_zoom, color='black', linewidth=2.5, label='PV')
ax1.set_ylabel('PV irradiance', fontsize=14)
ax1.tick_params(axis='y', labelsize=12)
ax1.set_ylim(*bounds(pv_zoom))

# Shared x‑axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.tick_params(axis='x', rotation=45, labelsize=12)
ax1.set_xlabel('')

# Load‑difference (right axis)
ax2 = ax1.twinx()                       # only one twin axis now
# ax2.spines['right'].set_position(('outward', 60))
ax2.plot(
    t_zoom, diff_zoom,
    color='red', linestyle='--', linewidth=1.5,
    marker='o', markersize=6, markevery=3,
    label='Normalized Load Difference'
)
ax2.set_ylabel('Normalized Load Difference', fontsize=14)
ax2.tick_params(axis='y', labelsize=12)
ax2.set_ylim(*bounds(diff_zoom))

# Combined legend
lines  = ax1.lines + ax2.lines
labels = [ln.get_label() for ln in lines]
fig.legend(lines, labels, ncol=2, fontsize=10, frameon=False,
           loc='upper center', bbox_to_anchor=(0.5, 1.12))

plt.tight_layout()
plt.show()

