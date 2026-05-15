"""
Era 4: The Stack Overflow Era (2008-2023, peaked ~2014)
==========================================
The workflow:
  1. Google "how to [thing] in pandas"
  2. Click first Stack Overflow result
  3. Copy the accepted answer (green checkmark = must be correct, right?)
  4. Paste into your script
  5. Modify variable names to match your data
  6. Pray it works
  7. If not, go back to step 1

This script is assembled from real Stack Overflow patterns.
Each block has a comment referencing the type of SO question it came from.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# SO: "how to read csv with pandas" (3.2M views, answered 2012)
# Accepted answer: pd.read_csv() — easy one
df = pd.read_csv("data/marketing_campaign.csv")

# SO: "how to convert string to datetime in pandas" (4.1M views)
# Top answer: pd.to_datetime() — had to scroll past 3 wrong answers first
df["date"] = pd.to_datetime(df["date"])

# SO: "pandas check for missing values" (2.8M views)
# Accepted answer says use isnull().sum()
print("Missing values:")
print(df.isnull().sum())
print()

# ============================================================================
# SO: "pandas groupby multiple aggregations" (1.5M views, answered 2015)
# The second answer was better than the accepted one — used named agg
# https://stackoverflow.com/questions/pandas-groupby-aggregate-multiple-columns
# ============================================================================
channel_stats = df.groupby("channel").agg(
    total_spend=("spend", "sum"),
    total_revenue=("revenue", "sum"),
    total_clicks=("clicks", "sum"),
    total_impressions=("impressions", "sum"),
    total_conversions=("conversions", "sum"),
)

# SO: "how to add calculated column to pandas dataframe" (800K views)
channel_stats["ROI"] = ((channel_stats["total_revenue"] - channel_stats["total_spend"])
                        / channel_stats["total_spend"] * 100).round(1)
channel_stats["CTR"] = (channel_stats["total_clicks"]
                        / channel_stats["total_impressions"] * 100).round(2)
channel_stats["CPA"] = (channel_stats["total_spend"]
                        / channel_stats["total_conversions"]).round(2)

print("Channel Performance:")
print(channel_stats.to_string())
print()

# ============================================================================
# SO: "matplotlib two y-axes on same plot" (450K views)
# Accepted answer used twinx() — copy-pasted and modified colors
# Took 3 attempts to get the legend to show both axes
# ============================================================================
fig, ax1 = plt.subplots(figsize=(10, 6))

x = np.arange(len(channel_stats))
width = 0.35

bars1 = ax1.bar(x - width/2, channel_stats["total_spend"], width,
                label="Spend", color="#e74c3c", alpha=0.8)
bars2 = ax1.bar(x + width/2, channel_stats["total_revenue"], width,
                label="Revenue", color="#2ecc71", alpha=0.8)

ax1.set_xlabel("Channel")
ax1.set_ylabel("Amount ($)")
ax1.set_xticks(x)
ax1.set_xticklabels(channel_stats.index)

# SO: "matplotlib add second y axis" — the twinx() trick
ax2 = ax1.twinx()
ax2.plot(x, channel_stats["ROI"], "D-", color="#3498db", linewidth=2,
         markersize=8, label="ROI %", zorder=5)
ax2.set_ylabel("ROI (%)")

# SO: "matplotlib legend for twinx two axes" (120K views)
# This was the annoying part — had to combine handles manually
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

ax1.set_title("Spend vs Revenue with ROI Overlay")
ax1.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("plots/era4_spend_revenue_roi.png", dpi=100)
plt.close()

# ============================================================================
# SO: "pandas resample time series by month" (320K views)
# Had to figure out that 'M' means month-end, 'MS' means month-start
# ============================================================================
monthly = df.set_index("date").resample("ME").agg({
    "revenue": "sum",
    "spend": "sum",
    "conversions": "sum"
})

# SO: "matplotlib fill between two lines" (180K views)
# Makes the profit/loss area visually obvious
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly.index, monthly["revenue"], label="Revenue", color="#2ecc71", linewidth=2)
ax.plot(monthly.index, monthly["spend"], label="Spend", color="#e74c3c", linewidth=2)

# SO: "matplotlib fill_between with condition color" (95K views)
ax.fill_between(monthly.index, monthly["revenue"], monthly["spend"],
                where=(monthly["revenue"] >= monthly["spend"]),
                interpolate=True, alpha=0.3, color="#2ecc71", label="Profit")
ax.fill_between(monthly.index, monthly["revenue"], monthly["spend"],
                where=(monthly["revenue"] < monthly["spend"]),
                interpolate=True, alpha=0.3, color="#e74c3c", label="Loss")

ax.set_title("Monthly Revenue vs Spend (Profit/Loss)")
ax.set_ylabel("Amount ($)")
ax.legend()
ax.grid(alpha=0.3)

# SO: "matplotlib format y axis as currency" (75K views)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))

fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("plots/era4_monthly_profit_loss.png", dpi=100)
plt.close()

# ============================================================================
# SO: "seaborn heatmap from pandas pivot table" (400K views)
# Actually gave up on seaborn import issues and did it with matplotlib
# SO: "matplotlib imshow heatmap with annotations" (200K views)
# ============================================================================
pivot = df.pivot_table(values="conversions", index="channel",
                       columns=df["date"].dt.month_name(), aggfunc="sum")

month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
pivot = pivot[[m for m in month_order if m in pivot.columns]]

fig, ax = plt.subplots(figsize=(14, 5))
im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, rotation=45, ha="right")
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)

# SO: "add text annotations to matplotlib heatmap" — the nested loop approach
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.values[i, j]
        color = "white" if val > pivot.values.max() * 0.7 else "black"
        ax.text(j, i, f"{int(val)}", ha="center", va="center", color=color, fontsize=9)

fig.colorbar(im, label="Conversions")
ax.set_title("Conversions Heatmap: Channel x Month")
fig.tight_layout()
fig.savefig("plots/era4_conversions_heatmap.png", dpi=100)
plt.close()

print("Plots saved to plots/")
print("Sources: ~8 Stack Overflow tabs open")
print("Time spent: 45 min coding, 2 hours on Stack Overflow")
