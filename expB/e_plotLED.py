'''
INPUT_CSV      = "11018_PV_CEA_Thermo_Lighting_Default_Demand.csv"
'base LED intensity (-)'
'smoothLEDIntensity'
zoom in hour period [0900,2000]
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -------------- USER PARAMETERS ---------------------------------
INPUT_CSV  = "11018_PV_CEA_Thermo_Lighting_Default_Demand.csv"
start_zoom = "06:00"
end_zoom   = "20:00"
two_col_w  = 7.0      # inches (≈ 17‑18 cm)
aspect     = 0.35     # height / width, tweak if you need more space
n_xticks   = 4        # number of x‑ticks between 09:00 and 20:00
# ----------------------------------------------------------------

# ── Load data ───────────────────────────────────────────────────
df = pd.read_csv(INPUT_CSV)

base_led   = df["base LED intensity (-)"]
smooth_led = df["smoothLEDIntensity"]

# Dummy minute‑index covering 24 h
t_idx = pd.date_range("00:00", periods=len(base_led), freq="min")

# Zoom to 09:00–20:00
mask        = (t_idx >= start_zoom) & (t_idx <= end_zoom)
t_zoom      = t_idx[mask]
base_zoom   = base_led[mask]
smooth_zoom = smooth_led[mask]

# ── Plot ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(two_col_w, two_col_w * aspect))

ax.step(t_zoom, base_zoom,
        label="Baseline LED", color="black", linewidth=3, where="post")
ax.step(t_zoom, smooth_zoom,
        label="Smoothed LED", color="gray", linestyle="--", linewidth=2, where="post")

# Axis labels & title
ax.set_ylabel("LED Intensity (‑)", fontsize=14)
# ax.set_title("LED Intensity – Baseline vs. Smoothed", fontsize=16, pad=8)

# X‑axis ticks & formatter
locator   = mdates.AutoDateLocator(minticks=2, maxticks=n_xticks)
formatter = mdates.DateFormatter("%H:%M")
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
fig.autofmt_xdate(rotation=30)

ax.tick_params(axis="both", labelsize=11)
ax.grid(False)

# Legend above plot
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.22),
          ncol=2, fontsize=11, frameon=False)
ax.set_ylim(0.0, 1.0)  # Adjust y‑limits to fit LED intensity range

plt.tight_layout(rect=[0, 0, 1, 0.95])   # leave space for legend
plt.show()
