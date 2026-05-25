# Era 6: Cursor / AI IDE — Tab-completed, Cmd+K edited, AI-suggested

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("plots")
OUTPUT_DIR.mkdir(exist_ok=True)

PALETTE = {"Email": "#FF6B6B", "Social": "#4ECDC4", "Search": "#45B7D1", "Display": "#FFA07A"}


def load_and_prepare(path: str = "data/marketing_campaign.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df["ctr"] = df["clicks"] / df["impressions"] * 100
    df["roas"] = df["revenue"] / df["spend"].replace(0, np.nan)
    return df


def channel_dashboard(df: pd.DataFrame) -> None:
    summary = df.groupby("channel").agg(
        spend=("spend", "sum"), revenue=("revenue", "sum"),
        clicks=("clicks", "sum"), impressions=("impressions", "sum"),
    )
    summary["roas"] = summary["revenue"] / summary["spend"]
    summary["ctr"] = summary["clicks"] / summary["impressions"] * 100

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Marketing Channel Dashboard", fontsize=16, fontweight="bold", y=1.02)
    colors = [PALETTE[ch] for ch in summary.index]

    ax = axes[0, 0]
    x = np.arange(len(summary))
    ax.bar(x - 0.2, summary["spend"], 0.4, label="Spend", color="#FF6B6B", alpha=0.85)
    ax.bar(x + 0.2, summary["revenue"], 0.4, label="Revenue", color="#51CF66", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(summary.index)
    ax.set_title("Spend vs Revenue")
    ax.legend(fontsize=9)

    ax = axes[0, 1]
    bars = ax.bar(summary.index, summary["roas"], color=colors, edgecolor="white")
    ax.axhline(y=1, color="gray", linestyle="--", alpha=0.5)
    ax.set_title("ROAS")
    for bar, val in zip(bars, summary["roas"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f"{val:.1f}x", ha="center", fontsize=10, fontweight="bold")

    ax = axes[1, 0]
    ax.barh(summary.index, summary["ctr"], color=colors, height=0.6)
    ax.set_title("Click-Through Rate")
    ax.set_xlabel("CTR (%)")

    ax = axes[1, 1]
    ax.bar(summary.index, summary["spend"], color=colors, edgecolor="white")
    ax.set_title("Spend by Channel")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "era6_channel_dashboard.png", dpi=150, bbox_inches="tight")
    plt.close()


def main():
    df = load_and_prepare()
    total_spend = df["spend"].sum()
    total_rev = df["revenue"].sum()
    print(f"Period: {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")
    print(f"Total Spend: ${total_spend:,.2f} | Revenue: ${total_rev:,.2f} | ROAS: {total_rev/total_spend:.2f}x")
    channel_dashboard(df)
    print(f"\nDashboard saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
