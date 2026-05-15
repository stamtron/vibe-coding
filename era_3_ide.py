"""
Era 3: The IDE Revolution (2016-present, VS Code #1 from 2018)
=====================================
Written in VS Code or PyCharm with full IDE support:
- Autocomplete (IntelliSense) suggests methods as you type
- Linting (pylint/flake8) catches errors before you run
- Integrated debugger — set breakpoints, inspect variables
- Virtual environments — no more "works on my machine"
- Extensions: GitLens, Python Docstring Generator, etc.
- Integrated terminal — run without leaving the editor

The code is cleaner, more structured, and follows best practices
because the IDE *guides* you toward them.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_data(filepath: str) -> pd.DataFrame:
    """Load and prepare marketing campaign data."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df


def calculate_channel_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate performance metrics by channel."""
    summary = df.groupby("channel", as_index=False).agg(
        total_spend=("spend", "sum"),
        total_revenue=("revenue", "sum"),
        total_clicks=("clicks", "sum"),
        total_impressions=("impressions", "sum"),
        total_conversions=("conversions", "sum"),
    )
    summary["roi_pct"] = (
        (summary["total_revenue"] - summary["total_spend"]) / summary["total_spend"] * 100
    ).round(1)
    summary["ctr_pct"] = (
        summary["total_clicks"] / summary["total_impressions"] * 100
    ).round(2)
    return summary


def plot_spend_vs_revenue(summary: pd.DataFrame, output_dir: Path) -> None:
    """Create grouped bar chart comparing spend and revenue by channel."""
    fig, ax = plt.subplots(figsize=(10, 6))

    x = range(len(summary))
    width = 0.35

    ax.bar([i - width / 2 for i in x], summary["total_spend"], width, label="Spend", color="#cc4444")
    ax.bar([i + width / 2 for i in x], summary["total_revenue"], width, label="Revenue", color="#44aa44")

    ax.set_xlabel("Channel")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Marketing Spend vs Revenue by Channel")
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary["channel"])
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_dir / "era3_spend_vs_revenue.png", dpi=100)
    plt.close(fig)


def plot_monthly_revenue(df: pd.DataFrame, output_dir: Path) -> None:
    """Create line chart of monthly revenue trend."""
    monthly = df.resample("ME", on="date")["revenue"].sum()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly.index, monthly.values, marker="o", linewidth=2, color="#2266cc")
    ax.set_title("Monthly Revenue Trend")
    ax.set_ylabel("Revenue ($)")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_dir / "era3_monthly_revenue.png", dpi=100)
    plt.close(fig)


def plot_ctr_by_channel(summary: pd.DataFrame, output_dir: Path) -> None:
    """Create bar chart of click-through rates by channel."""
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(summary["channel"], summary["ctr_pct"], color=colors)
    ax.set_title("Click-Through Rate by Channel")
    ax.set_ylabel("CTR (%)")
    ax.grid(axis="y", alpha=0.3)

    for bar, val in zip(bars, summary["ctr_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{val}%", ha="center", va="bottom", fontsize=11)

    fig.tight_layout()
    fig.savefig(output_dir / "era3_ctr_by_channel.png", dpi=100)
    plt.close(fig)


def main() -> None:
    """Run the full marketing analysis pipeline."""
    plt.style.use("ggplot")

    output_dir = Path("plots")
    output_dir.mkdir(exist_ok=True)

    df = load_data("data/marketing_campaign.csv")
    print(f"Loaded {len(df)} rows | {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")

    summary = calculate_channel_metrics(df)
    print("\nChannel Performance:")
    print(summary[["channel", "total_spend", "total_revenue", "roi_pct", "ctr_pct"]].to_string(index=False))

    plot_spend_vs_revenue(summary, output_dir)
    plot_monthly_revenue(df, output_dir)
    plot_ctr_by_channel(summary, output_dir)

    print(f"\nPlots saved to {output_dir}/")


if __name__ == "__main__":
    main()
