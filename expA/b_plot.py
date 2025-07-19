import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file
df = pd.read_excel('expA.xlsx', parse_dates=['date'])

def plot_data(start_date=None, end_date=None, n_xticks=4, xformat='datetime'):
    """
    Plot three subplots:
    1. Unit LMP ($/MWh)
    2. Energy Use (J)
    3. Energy Cost ($)

    Parameters:
    - start_date (str): e.g., '2024-07-01'
    - end_date (str): e.g., '2024-07-07'
    - n_xticks (int): number of x-axis ticks (default = 4)
    - xformat (str): 'datetime' (default), 'date', or 'time'
    """
    # Select formatter string
    if xformat == 'date':
        xfmt_str = '%m-%d'
    elif xformat == 'time':
        xfmt_str = '%H:%M'
    else:
        xfmt_str = '%m-%d %H:%M'

    plot_df = df.copy()
    if start_date:
        plot_df = plot_df[plot_df['date'] >= pd.to_datetime(start_date)]
    if end_date:
        plot_df = plot_df[plot_df['date'] <= pd.to_datetime(end_date)]

    fig, axes = plt.subplots(3, 1, figsize=(7.0, 7.5), sharex=True)

    # 1. Unit Price ($/MWh)
    axes[0].step(plot_df['date'], plot_df['dayAheadLMPDollarPerMWh'],
                 label='Day-Ahead LMP ($/MWh)', color='black', linewidth=3, where='post')

    axes[0].step(plot_df['date'], plot_df['realTimeLMPDollarPerMWh'],
                 label='Real-Time LMP ($/MWh)', color='gray', linewidth=2, linestyle='--', where='post')

    axes[0].set_ylabel('Unit Price ($/MWh)', fontsize=14)
    axes[0].legend(fontsize=11)
    axes[0].tick_params(labelsize=11)
    axes[0].set_title('Real-Time vs Day-Ahead LMP', fontsize=16)
    axes[0].grid(False)

    # 2. Energy Use (J)
    axes[1].step(plot_df['date'], plot_df['fixedJ'],
                 label='Fixed Energy (J)', color='black', linewidth=3, where='post')
    axes[1].step(plot_df['date'], plot_df['shiftJ'],
                 label='Shifted Energy (J)', color='gray', linewidth=2, linestyle='--', where='post')

    axes[1].set_ylabel('Energy (J)', fontsize=14)
    axes[1].legend(fontsize=11)
    axes[1].tick_params(labelsize=11)
    axes[1].set_title('Energy Consumption', fontsize=16)
    axes[1].grid(False)

    # 3. Energy Cost ($)
    axes[2].step(plot_df['date'], plot_df['fixedDollar'],
                 label='Fixed Energy Cost ($)', color='black', linewidth=3, where='post')
    axes[2].step(plot_df['date'], plot_df['shiftDollar'],
                 label='Shifted Energy Cost ($)', color='gray', linewidth=2, linestyle='--', where='post')
    axes[2].set_ylabel('Cost ($)', fontsize=14)
    axes[2].set_xlabel('Date', fontsize=14)
    axes[2].legend(fontsize=11)
    axes[2].tick_params(labelsize=11)
    axes[2].set_title('Energy Cost Comparison', fontsize=16)
    axes[2].grid(False)

    # Format x-axis
    locator = mdates.AutoDateLocator(minticks=2, maxticks=n_xticks)
    formatter = mdates.DateFormatter(xfmt_str)
    axes[2].xaxis.set_major_locator(locator)
    axes[2].xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate(rotation=30)

    plt.tight_layout()
    plt.show()

# Example usage:
plot_data('2024-07-06 00:00:00', '2024-07-06 23:59:59', n_xticks=6, xformat='time')
