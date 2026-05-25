# Era 4: The Stack Overflow Loop
# The REAL workflow before ChatGPT:
#   1. Google "how to [thing] in pandas"
#   2. Click first Stack Overflow result
#   3. Copy the accepted answer (green checkmark = must be correct, right?)
#   4. Paste into your script
#   5. Modify variable names to match your data
#   6. Pray it works
#   7. If not, go back to step 1

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# SO: "how to read csv with pandas" (3.2M views)
df = pd.read_csv("data/marketing_campaign.csv")
df["date"] = pd.to_datetime(df["date"])

# SO: "pandas groupby multiple aggregations" (1.5M views)
channel_stats = df.groupby("channel").agg(
    total_spend=("spend", "sum"),
    total_revenue=("revenue", "sum"),
    total_clicks=("clicks", "sum"),
    total_impressions=("impressions", "sum"),
)

channel_stats["ROI"] = ((channel_stats["total_revenue"] - channel_stats["total_spend"])
                        / channel_stats["total_spend"] * 100).round(1)

# SO: "matplotlib two y-axes on same plot" (450K views)
# Took 3 attempts to get the legend to show both axes
fig, ax1 = plt.subplots(figsize=(10, 6))
x = np.arange(len(channel_stats))
width = 0.35

ax1.bar(x - width/2, channel_stats["total_spend"], width, label="Spend", color="#e74c3c", alpha=0.8)
ax1.bar(x + width/2, channel_stats["total_revenue"], width, label="Revenue", color="#2ecc71", alpha=0.8)
ax1.set_xlabel("Channel")
ax1.set_ylabel("Amount ($)")
ax1.set_xticks(x)
ax1.set_xticklabels(channel_stats.index)

# SO: "matplotlib add second y axis" — the twinx() trick
ax2 = ax1.twinx()
ax2.plot(x, channel_stats["ROI"], "D-", color="#3498db", linewidth=2, markersize=8, label="ROI %")
ax2.set_ylabel("ROI (%)")

# SO: "matplotlib legend for twinx two axes" (120K views)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

ax1.set_title("Spend vs Revenue with ROI Overlay")
fig.tight_layout()
fig.savefig("plots/era4_spend_revenue_roi.png", dpi=100)
plt.close()

print("Plot saved. Sources: ~8 Stack Overflow tabs open")
print("Time spent: 45 min coding, 2 hours on Stack Overflow")
