# Era 3: IDE — typed, structured, linted, autocompleted

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath, parse_dates=["date"])


def calculate_channel_metrics(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("channel", as_index=False).agg(
        total_spend=("spend", "sum"),
        total_revenue=("revenue", "sum"),
        total_clicks=("clicks", "sum"),
        total_impressions=("impressions", "sum"),
    )
    summary["roi_pct"] = (
        (summary["total_revenue"] - summary["total_spend"]) / summary["total_spend"] * 100
    ).round(1)
    summary["ctr_pct"] = (
        summary["total_clicks"] / summary["total_impressions"] * 100
    ).round(2)
    return summary


def plot_spend_vs_revenue(summary: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(summary))
    width = 0.35
    ax.bar([i - width / 2 for i in x], summary["total_spend"], width, label="Spend", color="#cc4444")
    ax.bar([i + width / 2 for i in x], summary["total_revenue"], width, label="Revenue", color="#44aa44")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Spend vs Revenue by Channel")
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary["channel"])
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "era3_spend_vs_revenue.png", dpi=100)
    plt.close(fig)


def main() -> None:
    plt.style.use("ggplot")
    output_dir = Path("plots")
    output_dir.mkdir(exist_ok=True)

    df = load_data("data/marketing_campaign.csv")
    print(f"Loaded {len(df)} rows | {df['date'].min():%Y-%m-%d} to {df['date'].max():%Y-%m-%d}")

    summary = calculate_channel_metrics(df)
    print("\nChannel Performance:")
    print(summary[["channel", "total_spend", "total_revenue", "roi_pct", "ctr_pct"]].to_string(index=False))

    plot_spend_vs_revenue(summary, output_dir)
    print(f"\nPlot saved to {output_dir}/")


if __name__ == "__main__":
    main()
