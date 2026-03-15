"""
Scheme Performance Analysis
Compares scheme outcomes against baselines using indicator data.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_data():
    schemes = pd.read_csv(DATA_DIR / "schemes" / "flagship_schemes.csv")
    indicators = pd.read_csv(DATA_DIR / "indicators" / "scheme_indicators.csv")
    budgets = pd.read_csv(DATA_DIR / "budgets" / "scheme_budgets_2020_2024.csv")
    return schemes, indicators, budgets


def indicator_progress(indicators):
    """Calculate progress from baseline to latest value for each indicator."""
    df = indicators.copy()
    df["change"] = df["latest_value"] - df["baseline_value"]
    df["change_pct"] = ((df["change"] / df["baseline_value"]) * 100).round(1)

    # Flag whether change is in the right direction
    df["improving"] = df.apply(
        lambda r: (r["change"] > 0 and r["direction"] == "higher_better")
        or (r["change"] < 0 and r["direction"] == "lower_better"),
        axis=1,
    )
    return df


def scheme_scorecard(schemes, indicators, budgets):
    """Generate a summary scorecard for each scheme."""
    # Latest budget utilization
    latest_budgets = budgets[budgets["fiscal_year"] == "2023-24"].copy()
    latest_budgets["utilization_pct"] = (
        latest_budgets["budget_spent_cr"] / latest_budgets["budget_allocated_cr"] * 100
    ).round(1)

    # Indicator progress
    progress = indicator_progress(indicators)
    improving_count = (
        progress.groupby("scheme_id")["improving"]
        .agg(total="count", improving="sum")
        .reset_index()
    )

    # Merge
    scorecard = schemes[["scheme_id", "scheme_name", "sector", "launch_year"]].merge(
        latest_budgets[["scheme_id", "budget_allocated_cr", "utilization_pct"]],
        on="scheme_id",
        how="left",
    ).merge(
        improving_count, on="scheme_id", how="left"
    )
    scorecard["indicators_improving"] = scorecard.apply(
        lambda r: f"{int(r['improving'])}/{int(r['total'])}" if pd.notna(r.get("total")) else "--",
        axis=1,
    )
    return scorecard[
        ["scheme_name", "sector", "launch_year", "budget_allocated_cr", "utilization_pct", "indicators_improving"]
    ]


if __name__ == "__main__":
    schemes, indicators, budgets = load_data()

    print("=== Indicator Progress ===")
    progress = indicator_progress(indicators)
    for _, row in progress.iterrows():
        status = "IMPROVING" if row["improving"] else "WORSENING"
        print(f"  {row['scheme_id']}: {row['indicator_name']}")
        print(f"    {row['baseline_value']} ({row['baseline_year']}) -> {row['latest_value']} ({row['latest_year']}) [{status}]")
    print()

    print("=== Scheme Scorecard ===")
    scorecard = scheme_scorecard(schemes, indicators, budgets)
    print(scorecard.to_string(index=False))
