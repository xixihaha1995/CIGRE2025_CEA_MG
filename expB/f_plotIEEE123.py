import pandas as pd
import matplotlib.pyplot as plt
import re

# --- File paths ---
bus_coords_file = '../../0.archive/0.ieee/BusCoords.dat'
dss_file        = '../../0.archive/0.ieee/IEEE123Master.dss'

# --- Load bus coordinates ---
df_buses = (
    pd.read_csv(bus_coords_file, sep=r'\s+', header=None, names=['BusID', 'X', 'Y'])
      .assign(BusID_int=lambda d: d['BusID'].astype(str).str.extract(r'(\d+)').astype(int))
)
bus_coords = (
    df_buses.drop_duplicates('BusID_int', keep='first')
            .set_index('BusID_int')[['X', 'Y']]
            .to_dict('index')
)

# --- Parse DSS file for line connections ---
def base_id(s):
    m = re.match(r'(\d+)', str(s).strip())
    return int(m.group(1)) if m else None

lines = []
with open(dss_file) as f:
    for ln in f:
        if ln.strip().startswith('New Line'):
            b1 = re.search(r'Bus1=([^\s]+)', ln)
            b2 = re.search(r'Bus2=([^\s]+)', ln)
            if b1 and b2:
                id1, id2 = base_id(b1.group(1)), base_id(b2.group(1))
                if id1 is not None and id2 is not None:
                    lines.append((id1, id2))

# --- Plotting ---
fig, ax = plt.subplots(figsize=(6, 6*0.55))          # slightly smaller overall

# Buses
ax.scatter(df_buses['X'], df_buses['Y'], color='black', s=10)

# Feeder lines (thicker for clarity)
for b1, b2 in lines:
    if b1 in bus_coords and b2 in bus_coords:
        ax.plot([bus_coords[b1]['X'], bus_coords[b2]['X']],
                [bus_coords[b1]['Y'], bus_coords[b2]['Y']],
                color='blue', linewidth=1.0)

# --- Highlights ---
highlight_ids = ['25r', '300']
for bid in highlight_ids:
    row = df_buses[df_buses['BusID'] == bid]
    if not row.empty:
        x, y = row.iloc[0][['X', 'Y']]
        ax.scatter(x, y, color='red', marker='D', s=25, zorder=3)
        ax.text(x+10, y+10, bid, color='red', fontsize=7)

demand_id = '47'
row = df_buses[df_buses['BusID'] == demand_id]
if not row.empty:
    x, y = row.iloc[0][['X', 'Y']]
    ax.scatter(x, y, color='blue', marker='^', s=70, zorder=3)
    ax.text(x+10, y+10, demand_id, color='blue', fontsize=7)

sub_id = '150'
row = df_buses[df_buses['BusID'] == sub_id]
if not row.empty:
    x, y = row.iloc[0][['X', 'Y']]
    ax.scatter(x, y, color='purple', marker='*', s=120, zorder=3)

# Styling (no title per request)
ax.set_xlabel('X', fontsize=9)
ax.set_ylabel('Y', fontsize=9)
ax.tick_params(axis='both', labelsize=8)

plt.tight_layout()
plt.show()
