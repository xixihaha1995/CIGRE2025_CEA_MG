import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.dates as mdates

def plot_tap_operations_stacked(csv_name, monitor_mode='Tap (pu) ', operations=None):
    """
    Plot stacked tap operations for different mitigation strategies
    with styling for two-column publication formatting.

    Parameters:
    - csv_name: CSV file name inside 'c_postprocess'
    - monitor_mode: Column prefix (e.g., 'Tap (pu) ')
    - operations: List of scenarios (e.g., ['CEABaseline', 'CEASmoothing'])
    """

    if operations is None:
        operations = ['CEABaseline', 'CEASmoothing']

    scenario_labels = {
        'CEABaseline': 'Baseline Mitigation',
        'CEASmoothing': 'CEA-Assisted Mitigation'
    }

    color_map = {
        'CEABaseline': 'tab:red',
        'CEASmoothing': 'tab:green'
    }

    linestyle_map = {
        'CEABaseline': '-',
        'CEASmoothing': '--'
    }

    # --- Load Data ---
    file_path = os.path.join('c_postprocess', csv_name)
    data = pd.read_csv(file_path)
    time_index = pd.date_range(start='00:00', periods=len(data), freq='min')

    # --- Figure settings for two-column paper ---
    fig_width_in = 7.0
    aspect_ratio = 0.50
    fig, axes = plt.subplots(
        nrows=2, ncols=1, sharex=True,
        figsize=(fig_width_in, fig_width_in * aspect_ratio)
    )

    for i, op in enumerate(operations):
        col_name = monitor_mode + op
        if col_name not in data.columns:
            print(f"[Warning] Column '{col_name}' not found.")
            continue

        ax = axes[i]
        tap_series = data[col_name]
        num_operations = (tap_series != tap_series.shift()).sum()
        label = scenario_labels.get(op, op)

        ax.plot(
            time_index,
            tap_series,
            label=label,
            color=color_map.get(op, 'gray'),
            linewidth=2.0,
            linestyle=linestyle_map.get(op, '-'),
            marker=None
        )

        # --- Style each subplot ---
        ax.set_ylabel('Tap (p.u.)', fontsize=14)
        ax.set_title(f'{label} — {num_operations} Operations', fontsize=16, pad=3)
        ax.tick_params(axis='both', labelsize=10, length=4)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))

    axes[-1].set_xlabel('Time (HH:MM)', fontsize=14)

    # Layout
    plt.tight_layout(h_pad=1.3)
    plt.subplots_adjust(top=0.94)
    plt.show()

# Example usage
plot_tap_operations_stacked(
    csv_name='11018_PV_CEA_TapOperations.csv',
    monitor_mode='Tap (pu) ',
    operations=['CEABaseline', 'CEASmoothing']
)
