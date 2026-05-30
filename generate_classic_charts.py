import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Dummy data if network fails
years = np.arange(1956, 2011)
miles = np.linspace(3500, 10000, len(years)) + np.sin(years)*300
gas = np.linspace(1.5, 3.0, len(years)) + np.cos(years/5.0)*0.5
df = pd.DataFrame({'year': years, 'miles': miles, 'gas': gas})

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['miles'], df['gas'], '-o', color='#2c3e50', markersize=4, linewidth=1.5, alpha=0.7)
# Annotate some years
for idx, row in df.iterrows():
    if row['year'] % 5 == 0 or row['year'] in [1973, 1979, 2008]:
        ax.annotate(str(int(row['year'])), (row['miles'], row['gas']), 
                    xytext=(5, 5), textcoords='offset points', fontsize=9, color='#e74c3c')

ax.set_title("Connected Scatterplot (Concept: Driving Shifts Into Reverse)", fontsize=14, pad=15)
ax.set_xlabel("Miles driven per person", fontsize=12)
ax.set_ylabel("Cost of gasoline ($)", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig("信息可视化/weeks/W04_AI_D3_Basics/public/slides/S03d_Connected_Scatterplot.png", dpi=300)
plt.close()

# 2. Non-linear Time Scale
fig, ax = plt.subplots(figsize=(10, 4))
# Create non-linear events
events = [1, 2, 5, 20, 50, 100, 1000]
event_labels = ['1ms', '2ms', '5ms', '20ms', '50ms', '100ms', '1s']
y = np.zeros(len(events))

ax.plot(events, y, '-o', color='#34495e', markersize=8)
for i, (txt, x_val) in enumerate(zip(event_labels, events)):
    ax.annotate(txt, (x_val, 0), xytext=(0, 15), textcoords='offset points', ha='center', fontsize=11)

ax.set_xscale('log')
ax.set_title("Non-linear Time Scale (Logarithmic Scale)", fontsize=14, pad=20)
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(1.5)
ax.set_ylim(-0.1, 0.1)
plt.tight_layout()
plt.savefig("信息可视化/weeks/W04_AI_D3_Basics/public/slides/S03d_NonLinear_TimeScale.png", dpi=300)
plt.close()

print("Charts generated successfully!")
