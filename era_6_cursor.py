
"""
Era 6: Cursor / AI IDE (2024)
==============================

This code was written WITH an AI embedded in the editor.
The difference from ChatGPT (Era 5):

- You didn't leave your editor to write a prompt
- The AI sees your ENTIRE project: the CSV, other scripts, the plots/ dir
- You type a comment describing what you want → Tab → code appears
- You select code, press Cmd+K → "make this a stacked area chart" → done
- AI suggests the next function before you even think of it

The result: more sophisticated analysis, cleaner code, done in minutes.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

PALETTE = {
    "Email": "#FF6B6B",
    "Social": "#4ECDC4",
    "Search": "#45B7D1",
    "Display": "#FFA07A",
}


def load_and_prepare(path: str = "data/marketing_campaign.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M")
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["ctr"] = df["clicks"] / df["impressions"] * 100
    df["conversion_rate"] = df["conversions"] / df["clicks"].replace(0, np.nan) * 100
    df["roas"] = df["revenue"] / df["spend"].replace(0, np.nan)
    return df


def channel_dashboard(df: pd.DataFrame) -> None:
    """4-panel channel performance dashboard — Cmd+K: 'create a 2x2 subplot dashboard'"""
    summary = df.groupby("channel").agg(
        spend=("spend", "sum"),
        revenue=("revenue", "sum"),
        clicks=("clicks", "sum"),
        impressions=("impressions", "sum"),
        conversions=("conversions", "sum"),
    )
    summary["roi"] = (summary["revenue"] - summary["spend"]) / summary["spend"] * 100
    summary["ctr"] = summary["clicks"] / summary["impressions"] * 100
    summary["roas"] = summary["revenue"] / summary["spend"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Marketing Channel Dashboard", fontsize=16, fontweight="bold", y=1.02)

    colors = [PALETTE[ch] for ch in summary.index]

    # Panel 1: Spend vs Revenue
    ax = axes[0, 0]
    x = np.arange(len(summary))
    ax.bar(x - 0.2, summary["spend"], 0.4, label="Spend", color="#FF6B6B", alpha=0.85)
    ax.bar(x + 0.2, summary["revenue"], 0.4, label="Revenue", color="#51CF66", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(summary.index)
    ax.set_title("Spend vs Revenue")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))

    # Panel 2: ROAS
    ax = axes[0, 1]
    bars = ax.bar(summary.index, summary["roas"], color=colors, edgecolor="white")
    ax.axhline(y=1, color="gray", linestyle="--", alpha=0.5, label="Break-even")
    ax.set_title("Return on Ad Spend (ROAS)")
    ax.set_ylabel("ROAS (x)")
    for bar, val in zip(bars, summary["roas"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f"{val:.1f}x", ha="center", fontsize=10, fontweight="bold")
    ax.legend(fontsize=9)

    # Panel 3: CTR
    ax = axes[1, 0]
    bars = ax.barh(summary.index, summary["ctr"], color=colors, height=0.6)
    ax.set_title("Click-Through Rate")
    ax.set_xlabel("CTR (%)")
    for bar, val in zip(bars, summary["ctr"]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"{val:.2f}%", va="center", fontsize=10)

    # Panel 4: Conversion funnel
    ax = axes[1, 1]
    funnel_data = summary[["impressions", "clicks", "conversions"]].sum()
    stages = ["Impressions", "Clicks", "Conversions"]
    values = [funnel_data["impressions"], funnel_data["clicks"], funnel_data["conversions"]]
    bars = ax.bar(stages, values, color=["#74b9ff", "#0984e3", "#6c5ce7"], edgecolor="white")
    ax.set_title("Overall Funnel")
    ax.set_yscale("log")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.1,
                f"{val:,.0f}", ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "era6_channel_dashboard.png", dpi=150, bbox_inches="tight")
    plt.close()


def revenue_trend_with_rolling(df: pd.DataFrame) -> None:
    """Weekly revenue with 4-week rolling average — Tab-completed from a comment"""
    weekly = df.resample("W", on="date").agg(
        revenue=("revenue", "sum"),
        spend=("spend", "sum"),
    )
    weekly["rolling_revenue"] = weekly["revenue"].rolling(4).mean()
    weekly["rolling_spend"] = weekly["spend"].rolling(4).mean()

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.fill_between(weekly.index, weekly["revenue"], alpha=0.15, color="#4C6EF5")
    ax.plot(weekly.index, weekly["revenue"], alpha=0.4, color="#4C6EF5", linewidth=1)
    ax.plot(weekly.index, weekly["rolling_revenue"], color="#4C6EF5",
            linewidth=2.5, label="Revenue (4-wk avg)")
    ax.plot(weekly.index, weekly["rolling_spend"], color="#FF6B6B",
            linewidth=2, linestyle="--", label="Spend (4-wk avg)")

    ax.set_title("Weekly Revenue & Spend Trend (4-week Rolling Average)")
    ax.set_ylabel("Amount ($)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "era6_revenue_trend.png", dpi=150, bbox_inches="tight")
    plt.close()


def campaign_performance_matrix(df: pd.DataFrame) -> None:
    """Scatter plot: spend efficiency vs scale — AI suggested this analysis"""
    campaign_stats = df.groupby(["channel", "campaign_name"]).agg(
        spend=("spend", "sum"),
        revenue=("revenue", "sum"),
        conversions=("conversions", "sum"),
    ).reset_index()
    campaign_stats["roas"] = campaign_stats["revenue"] / campaign_stats["spend"].replace(0, np.nan)

    fig, ax = plt.subplots(figsize=(12, 8))

    for channel, group in campaign_stats.groupby("channel"):
        ax.scatter(group["spend"], group["roas"],
                   s=group["conversions"] * 2,
                   alpha=0.7, label=channel, color=PALETTE[channel],
                   edgecolors="white", linewidth=0.5)

    ax.axhline(y=1, color="gray", linestyle="--", alpha=0.4)
    ax.set_xlabel("Total Spend ($)")
    ax.set_ylabel("ROAS (x)")
    ax.set_title("Campaign Performance: Spend vs ROAS (bubble size = conversions)")
    ax.legend(title="Channel")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.grid(alpha=0.2)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "era6_campaign_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()


def print_summary(df: pd.DataFrame) -> None:
    summary = df.groupby("channel").agg(
        spend=("spend", "sum"), revenue=("revenue", "sum"),
        conversions=("conversions", "sum"),
    )
    summary["roas"] = (summary["revenue"] / summary["spend"]).round(2)
    total = summary.sum(numeric_only=True)

    print("=" * 60)
    print("MARKETING PERFORMANCE REPORT")
    print("=" * 60)
    print(f"Period: {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")
    print(f"Total Spend:       ${total['spend']:>12,.2f}")
    print(f"Total Revenue:     ${total['revenue']:>12,.2f}")
    print(f"Total Conversions: {int(total['conversions']):>12,}")
    print(f"Overall ROAS:      {total['revenue']/total['spend']:>12.2f}x")
    print(f"\n{summary.to_string()}")


def main():
    df = load_and_prepare()
    print_summary(df)
    channel_dashboard(df)
    revenue_trend_with_rolling(df)
    campaign_performance_matrix(df)
    print(f"\nDashboard saved to {OUTPUT_DIR}/")
    print("Time: ~5 min of Tab-accepting and Cmd+K edits")


if __name__ == "__main__":
    main()
