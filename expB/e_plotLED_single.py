import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---------- PARAMETERS ----------
INPUT_CSV   = "21018_PV_CEA_Thermo_Lighting_Default_Demand.csv"
one_col_w   = 3.5       # in (≈ 8.9 cm, single-column)
aspect      = 0.45      # height / width
zoom_start  = "06:00"
zoom_end    = "20:00"
PPFD_FACTOR = 2 * 347.2
# ---------------------------------

# ── Load data ────────────────────
df          = pd.read_csv(INPUT_CSV)
base_led    = df["base LED intensity (-)"] * PPFD_FACTOR
smooth_led  = df["smoothLEDIntensity"] * PPFD_FACTOR

t_full      = pd.date_range("00:00", periods=len(base_led), freq="min")

# ── Zoom to 06:00–20:00 ──────────
mask        = (t_full >= zoom_start) & (t_full <= zoom_end)
t_zoom      = t_full[mask]
base_zoom   = base_led[mask]
smooth_zoom = smooth_led[mask]

# ── Figure ───────────────────────
fig, ax = plt.subplots(figsize=(one_col_w, one_col_w * aspect))

ax.step(t_zoom, base_zoom,
        label="Baseline LED", color="black", lw=2.2, where="post")
ax.step(t_zoom, smooth_zoom,
        label="Smoothed LED", color="gray", linestyle="--", lw=1.6, where="post")

# ── Axis styling ─────────────────
ax.set_ylabel("LED Intensity\n (µmol∙m⁻²∙s⁻¹)", fontsize=12)

ax.set_xticks(pd.date_range(zoom_start, zoom_end, freq="2h"))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.tick_params(axis="x", rotation=45, labelsize=9, length=3)
ax.tick_params(axis="y", labelsize=9, length=3)
ax.set_ylim(-10, PPFD_FACTOR + 10)

# ── Legend outside ───────────────
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05),
          ncol=2, fontsize=9, frameon=False)

# ── Layout ───────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.97])  # leave sliver for legend
plt.show()
