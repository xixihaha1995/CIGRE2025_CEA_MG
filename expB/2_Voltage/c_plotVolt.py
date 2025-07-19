import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def plot_voltage_profiles_stacked(csv_name,
                                  voltage_columns=None,
                                  ylim_mode='fixed'):
    """
    Stacked per‑unit voltage profiles for a two‑column paper.

    Parameters
    ----------
    csv_name : str
        File name inside the 'c_postprocess' folder.
    voltage_columns : list[str]
        Columns to plot.  Default plots Baseline & Smoothing.
    ylim_mode : {'fixed', 'auto'}
        'fixed' ⇒ y‑range 0.97–0.995.
        'auto'  ⇒ subplot‑specific min/max with dashed guides.
    """

    if voltage_columns is None:
        voltage_columns = ['V1 CEABaseline', 'V1 CEASmoothing']

    # ── Scenario maps ───────────────────────────────────────────
    labels = {
        'CEABaseline' : 'Baseline Mitigation',
        'CEASmoothing': 'CEA‑Assisted Mitigation',
    }
    colors  = {'CEABaseline': 'tab:red',   'CEASmoothing': 'tab:green'}
    markers = {'CEABaseline': 'o',         'CEASmoothing': 's'}

    # ── Load data ───────────────────────────────────────────────
    path = os.path.join('c_postprocess', csv_name)
    df   = pd.read_csv(path)
    idx  = pd.date_range('00:00', periods=len(df), freq='min')

    # ── Figure setup (two‑column width) ────────────────────────
    fig_w = 7.0                               # inches
    aspect = 0.50                             # height / width
    fig, axes = plt.subplots(
        nrows=2, ncols=1, sharex=True,
        figsize=(fig_w, fig_w * aspect),
    )

    # ── Plot each column ───────────────────────────────────────
    for i, col in enumerate(voltage_columns):
        if col not in df.columns:
            print(f"[Warning] Column “{col}” not found.")
            continue

        series    = df[col]
        key       = col.replace('V1 ', '')
        ax        = axes[i]

        ax.plot(
            idx, series,
            label=labels.get(key, key),
            color=colors.get(key, 'gray'),
            linewidth=2.0,                     # thicker line
            marker=markers.get(key, 'o'),
            markersize=6,                      # bigger marker
            markevery=60,
        )

        # ── y‑limits & dashed guides ─────────────────────────
        if ylim_mode == 'auto':
            lo, hi = series.min(), series.max()
            pad = 0.01
            ax.set_ylim(lo - pad, hi + pad)
            for y in (lo, hi):
                ax.axhline(y, color='black', ls='--', lw=0.9)
                xoff = 0.01 * (ax.get_xlim()[1] - ax.get_xlim()[0])
                ax.text(ax.get_xlim()[0] - xoff, y + 1e-3,
                        f"{y:.3f}", ha='right', va='center',
                        fontsize=8, color='blue')
        else:
            ax.set_ylim(0.97, 1)           # ← tighter fixed range

        # ── cosmetic tweaks ───────────────────────────────────
        ax.set_ylabel('Voltage (p.u.)', fontsize=14)
        ax.set_title(labels.get(key, key), fontsize=16, pad=3)
        ax.tick_params(axis='both', labelsize=10, length=4)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))

    # ── shared x‑label ────────────────────────────────────────
    axes[-1].set_xlabel('Time (HH:MM)', fontsize=14)

    plt.tight_layout(h_pad=1.3)
    plt.subplots_adjust(top=0.94)             # room for titles
    plt.show()

# Example call
plot_voltage_profiles_stacked(
    csv_name='11018_PV_CEA_VoltageProfile.csv',
    voltage_columns=['V1 CEABaseline', 'V1 CEASmoothing'],
    ylim_mode='fixed',                        # use 'auto' if preferred
)
