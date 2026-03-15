"""
Budget Analysis for Indian Government Schemes
Reads scheme and budget CSVs, produces summary statistics and visualisations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"


def load_data():
    schemes = pd.read_csv(DATA_DIR / "schemes" / "flagship_schemes.csv")
    budgets = pd.read_csv(DATA_DIR / "budgets" / "scheme_budgets_2020_2024.csv")
    return schemes, budgets


def utilization_summary(schemes, budgets):
    """Calculate budget utilization rates by scheme and year."""
    merged = budgets.merge(schemes[["scheme_id", "scheme_name", "sector"]], on="scheme_id")
    merged["utilization_pct"] = (
        merged["budget_spent_cr"] / merged["budget_allocated_cr"] * 100
    ).round(1)
    return merged


def sector_spending(merged):
    """Aggregate spending by sector for the latest fiscal year."""
    latest = merged[merged["fiscal_year"] == "2023-24"]
    return (
        latest.groupby("sector")
        .agg(
            schemes=("scheme_id", "nunique"),
            total_allocated=("budget_allocated_cr", "sum"),
            total_spent=("budget_spent_cr", "sum"),
        )
        .assign(
            utilization_pct=lambda df: (df["total_spent"] / df["total_allocated"] * 100).round(1)
        )
        .sort_values("total_allocated", ascending=False)
    )


def top_schemes_by_budget(merged, year="2023-24"):
    """Rank schemes by budget allocation for a given year."""
    year_data = merged[merged["fiscal_year"] == year]
    return (
        year_data[["scheme_name", "sector", "budget_allocated_cr", "budget_spent_cr", "utilization_pct"]]
        .sort_values("budget_allocated_cr", ascending=False)
        .reset_index(drop=True)
    )


def plot_budget_trends(merged, scheme_id, output_path=None):
    """Plot allocated vs spent budget over time for a single scheme."""
    data = merged[merged["scheme_id"] == scheme_id].sort_values("fiscal_year")
    if data.empty:
        print(f"No budget data for {scheme_id}")
        return

    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(data))
    ax.bar([i - 0.15 for i in x], data["budget_allocated_cr"], 0.3, label="Allocated", color="#93c5fd")
    ax.bar([i + 0.15 for i in x], data["budget_spent_cr"], 0.3, label="Spent", color="#1a56db")
    ax.set_xticks(x)
    ax.set_xticklabels(data["fiscal_year"], rotation=45, ha="right")
    ax.set_ylabel("Rs Crores")
    ax.set_title(f"Budget Trend: {data['scheme_name'].iloc[0]}")
    ax.legend()
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150)
        print(f"Saved: {output_path}")
    else:
        plt.show()
    plt.close()


def plot_utilization_heatmap(merged, output_path=None):
    """Heatmap of utilization rates by scheme and year."""
    pivot = merged.pivot_table(
        index="scheme_name", columns="fiscal_year", values="utilization_pct"
    )
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="RdYlGn", vmin=50, vmax=100, ax=ax)
    ax.set_title("Budget Utilization (%) by Scheme and Year")
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150)
        print(f"Saved: {output_path}")
    else:
        plt.show()
    plt.close()


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    schemes, budgets = load_data()
    merged = utilization_summary(schemes, budgets)

    print("=== Sector Spending (2023-24) ===")
    print(sector_spending(merged).to_string())
    print()

    print("=== Top Schemes by Budget (2023-24) ===")
    print(top_schemes_by_budget(merged).to_string())
    print()

    # Generate charts
    plot_utilization_heatmap(merged, OUTPUT_DIR / "utilization_heatmap.png")
    for sid in ["mgnrega", "pmkisan", "jjm"]:
        plot_budget_trends(merged, sid, OUTPUT_DIR / f"budget_trend_{sid}.png")
