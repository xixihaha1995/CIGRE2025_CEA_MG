'''
_input = r'./1a_cea/TCL_htgClg_baseFlex.csv'
baseline heating setpoint (C), baseline cooling setpoint (C)
smoothHtgSetC,smoothClgSetC
The comparison of thermostat setpoints for both original setting and Thermostat-Assisted mitigation setting is shown in Figure 8.w
'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# -------------- PARAMETERS ---------------------------------
INPUT_CSV      = "11018_PV_CEA_Thermo_Lighting_Default_Demand.csv"
two_col_width  = 7.0        # in  (≈ 17‑18 cm, typical two‑column width)
aspect         = 0.45       # height / width (shorter chart looks cleaner)
base_color     = "gray"
mitig_colors   = {"heat": "tab:orange", "cool": "tab:red"}
marker_every   = 30         # show a marker every 30 min
# -----------------------------------------------------------

# ── Load data ───────────────────────────────────────────────
df = pd.read_csv(INPUT_CSV)
htg_base       = df["baseline heating setpoint (C)"]
clg_base       = df["baseline cooling setpoint (C)"]
htg_mitigated  = df["smoothHtgSetC"]
clg_mitigated  = df["smoothClgSetC"]
t_idx = pd.date_range("00:00", periods=len(htg_base), freq="min")  # ‹‑‑ 'min'

# ── Create figure ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(two_col_width, two_col_width * aspect))

# Baseline setpoints
ax.plot(t_idx, htg_base, label="Baseline Heating",
        color=base_color, linestyle="-",  linewidth=1.2,
        marker="o", markersize=3, markevery=marker_every)
ax.plot(t_idx, clg_base, label="Baseline Cooling",
        color=base_color, linestyle="--", linewidth=1.2,
        marker="s", markersize=3, markevery=marker_every)

# Mitigation setpoints
ax.plot(t_idx, htg_mitigated, label="Mitigated Heating",
        color=mitig_colors["heat"], linestyle="-",  linewidth=1.8,
        marker="^", markersize=4, markevery=marker_every)
ax.plot(t_idx, clg_mitigated, label="Mitigated Cooling",
        color=mitig_colors["cool"], linestyle="--", linewidth=1.8,
        marker="v", markersize=4, markevery=marker_every)

# ── Axis styling ────────────────────────────────────────────
ax.set_ylabel("Temperature (°C)", fontsize=12)
xticks = pd.date_range(start="00:00", periods=5, freq="6h")  # note the lowercase 'h'
ax.set_xticks(xticks)
# ------------------------------------------------------------------
# Build a dummy 24‑hour, minute‑resolution index


# … plotting code …

# X‑axis ticks every 6 hours (00:00, 06:00, 12:00, 18:00)
xticks = pd.date_range("00:00", "23:59", freq="3h")                # ‹‑‑ 'h'
ax.set_xticks(xticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

ax.tick_params(axis="x", rotation=45, labelsize=10, length=4, width=0.8)
ax.tick_params(axis="y", labelsize=10, length=4, width=0.8)

# ── Legend ─────────────────────────────────────────────────
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.02),
          ncol=2, fontsize=10, frameon=False)

# ── Grid & layout ──────────────────────────────────────────
# ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.4)
ax.set_ylim(16, 22)  # Adjust y‑axis limits as needed
plt.tight_layout(rect=[0, 0, 1, 0.95])  # top room for legend

plt.show()
