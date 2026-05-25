# Era 5: ChatGPT — pasted directly from the response, ran on first try

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

plt.style.use("seaborn-v0_8-whitegrid")
output_dir = Path("plots")
output_dir.mkdir(exist_ok=True)

df = pd.read_csv("data/marketing_campaign.csv", parse_dates=["date"])

print(f"Dataset: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Date range: {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")
print(f"Total spend: ${df['spend'].sum():,.2f}")
print(f"Total revenue: ${df['revenue'].sum():,.2f}")
print(f"Overall ROI: {(df['revenue'].sum() - df['spend'].sum()) / df['spend'].sum() * 100:.1f}%")

channel_metrics = df.groupby("channel").agg(
    spend=("spend", "sum"),
    revenue=("revenue", "sum"),
    clicks=("clicks", "sum"),
    impressions=("impressions", "sum"),
    conversions=("conversions", "sum"),
).round(2)

channel_metrics["ROI (%)"] = ((channel_metrics["revenue"] - channel_metrics["spend"])
                               / channel_metrics["spend"] * 100).round(1)
channel_metrics["CTR (%)"] = (channel_metrics["clicks"] / channel_metrics["impressions"] * 100).round(2)

print(f"\nChannel Performance:\n{channel_metrics.to_string()}")

fig, ax = plt.subplots(figsize=(10, 6))
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

print(f"\nPlot saved to {output_dir}/")
print("Time to generate this script: ~15 seconds with ChatGPT")
