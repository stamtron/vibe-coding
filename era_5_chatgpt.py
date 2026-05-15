"""
Era 5: The ChatGPT Era (2023)
==============================

PROMPT USED:
-----------
"I have a CSV file called marketing_campaign.csv with columns: date, channel,
campaign_name, impressions, clicks, conversions, spend, revenue.

Can you write a Python script that:
1. Loads the data and shows basic statistics
2. Creates a bar chart of spend vs revenue by channel
3. Creates a monthly revenue trend line chart
4. Creates a pie chart of spend distribution by channel
5. Calculates ROI and CTR for each channel
6. Saves all plots to a plots/ directory

Use pandas and matplotlib. Make the plots look professional."

RESPONSE TIME: ~15 seconds (vs 2+ hours in the Stack Overflow era)

Below is what ChatGPT generated — pasted directly, ran on first try.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
})

output_dir = Path("plots")
output_dir.mkdir(exist_ok=True)

df = pd.read_csv("data/marketing_campaign.csv", parse_dates=["date"])

print("=" * 60)
print("MARKETING CAMPAIGN ANALYSIS")
print("=" * 60)
print(f"\nDataset: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Date range: {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")
print(f"Total spend: ${df['spend'].sum():,.2f}")
print(f"Total revenue: ${df['revenue'].sum():,.2f}")
print(f"Overall ROI: {(df['revenue'].sum() - df['spend'].sum()) / df['spend'].sum() * 100:.1f}%")

channel_metrics = df.groupby("channel").agg(
    spend=("spend", "sum"),
    revenue=("revenue", "sum"),
    impressions=("impressions", "sum"),
    clicks=("clicks", "sum"),
    conversions=("conversions", "sum"),
).round(2)

channel_metrics["ROI (%)"] = ((channel_metrics["revenue"] - channel_metrics["spend"])
                               / channel_metrics["spend"] * 100).round(1)
channel_metrics["CTR (%)"] = (channel_metrics["clicks"] / channel_metrics["impressions"] * 100).round(2)
channel_metrics["Conv Rate (%)"] = (channel_metrics["conversions"] / channel_metrics["clicks"] * 100).round(2)
channel_metrics["CPA ($)"] = (channel_metrics["spend"] / channel_metrics["conversions"]).round(2)

print("\n📊 Channel Performance Summary:")
print(channel_metrics.to_string())

# --- Plot 1: Spend vs Revenue by Channel ---
fig, ax = plt.subplots()
x = range(len(channel_metrics))
width = 0.35

ax.bar([i - width/2 for i in x], channel_metrics["spend"], width,
       label="Spend", color="#FF6B6B", edgecolor="white")
ax.bar([i + width/2 for i in x], channel_metrics["revenue"], width,
       label="Revenue", color="#51CF66", edgecolor="white")

ax.set_xlabel("Channel")
ax.set_ylabel("Amount ($)")
ax.set_title("Marketing Spend vs Revenue by Channel")
ax.set_xticks(list(x))
ax.set_xticklabels(channel_metrics.index)
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.tight_layout()
plt.savefig(output_dir / "era5_spend_vs_revenue.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Plot 2: Monthly Revenue Trend ---
monthly_revenue = df.resample("ME", on="date")["revenue"].sum()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_revenue.index, monthly_revenue.values,
        marker="o", linewidth=2.5, color="#4C6EF5", markersize=6)
ax.fill_between(monthly_revenue.index, monthly_revenue.values,
                alpha=0.15, color="#4C6EF5")
ax.set_title("Monthly Revenue Trend")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "era5_monthly_revenue.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Plot 3: Spend Distribution Pie Chart ---
fig, ax = plt.subplots(figsize=(8, 8))
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
wedges, texts, autotexts = ax.pie(
    channel_metrics["spend"],
    labels=channel_metrics.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
for autotext in autotexts:
    autotext.set_fontweight("bold")
ax.set_title("Spend Distribution by Channel")

plt.tight_layout()
plt.savefig(output_dir / "era5_spend_distribution.png", dpi=150, bbox_inches="tight")
plt.close()

# --- Plot 4: ROI Comparison ---
fig, ax = plt.subplots()
colors_roi = ["#FF6B6B" if roi < 0 else "#51CF66" for roi in channel_metrics["ROI (%)"]]
bars = ax.barh(channel_metrics.index, channel_metrics["ROI (%)"], color=colors_roi,
               edgecolor="white", height=0.6)

for bar, val in zip(bars, channel_metrics["ROI (%)"]):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontweight="bold")

ax.set_xlabel("ROI (%)")
ax.set_title("Return on Investment by Channel")
ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "era5_roi_comparison.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"\n✅ All plots saved to {output_dir}/")
print("Time to generate this script: ~15 seconds with ChatGPT")
print("Time to run: < 2 seconds")
