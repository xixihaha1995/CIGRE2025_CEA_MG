import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---------- PARAMETERS ----------
INPUT_CSV      = "21018_PV_CEA_Thermo_Lighting_Default_Demand.csv"
one_col_width  = 3.5        # in  (≈ 8.9 cm, single‑column in most journals)
aspect         = 0.55       # height / width
base_color     = "gray"
mitig_colors   = {"heat": "tab:orange", "cool": "tab:red"}
marker_every   = 30         # show a marker every 30 min
# --------------------------------

# ── Load data ───────────────────
df = pd.read_csv(INPUT_CSV)
htg_base       = df["baseline heating setpoint (C)"]
clg_base       = df["baseline cooling setpoint (C)"]
htg_mitigated  = df["smoothHtgSetC"]
clg_mitigated  = df["smoothClgSetC"]

# minute‑resolution index for a 24‑h day
t_idx = pd.date_range("00:00", periods=len(htg_base), freq="min")

# ── Filter 06:00–20:00 window ──
mask = (t_idx >= "06:00") & (t_idx <= "20:00")
t_zoom = t_idx[mask]

htg_base_zoom  = htg_base[mask]
clg_base_zoom  = clg_base[mask]
htg_mit_zoom   = htg_mitigated[mask]
clg_mit_zoom   = clg_mitigated[mask]

# ── Figure ──────────────────────
fig, ax = plt.subplots(figsize=(one_col_width, one_col_width * aspect))

# Baseline setpoints
ax.plot(t_zoom, htg_base_zoom, label="Baseline Heating",
        color=base_color, linestyle="-",  lw=1.2,
        marker="o", ms=3, markevery=marker_every)
ax.plot(t_zoom, clg_base_zoom, label="Baseline Cooling",
        color=base_color, linestyle="--", lw=1.2,
        marker="s", ms=3, markevery=marker_every)

# Mitigation setpoints
ax.plot(t_zoom, htg_mit_zoom, label="Mitigated Heating",
        color=mitig_colors["heat"], linestyle="-",  lw=1.8,
        marker="^", ms=4, markevery=marker_every)
ax.plot(t_zoom, clg_mit_zoom, label="Mitigated Cooling",
        color=mitig_colors["cool"], linestyle="--", lw=1.8,
        marker="v", ms=4, markevery=marker_every)

# ── Axis styling ────────────────
ax.set_ylabel("Temperature (°C)", fontsize=12)
xticks = pd.date_range("06:00", "20:00", freq="2h")
ax.set_xticks(xticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.tick_params(axis="x", rotation=45, labelsize=9, length=3)
ax.tick_params(axis="y", labelsize=9, length=3)

# ── Legend outside top ──────────
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05),
          ncol=2, fontsize=9, frameon=False)

# ── Layout & limits ─────────────
ax.set_ylim(16, 22)                     # adjust if necessary
plt.tight_layout(rect=[0, 0, 1, 0.97])  # leave sliver for legend
plt.show()
