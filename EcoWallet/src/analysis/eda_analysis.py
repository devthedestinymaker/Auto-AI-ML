"""Exploratory analysis of EcoWallet transaction carbon footprints."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "transactions.csv"
PLOT_PATH = PROJECT_ROOT / "data" / "carbon_footprint_distribution.png"


def summarize_footprint(transactions: pd.DataFrame) -> pd.Series:
    """Return descriptive statistics for transaction emissions in kg CO2."""
    footprint = transactions["carbon_kg"]
    return pd.Series(
        {
            "count": footprint.count(),
            "mean": footprint.mean(),
            "median": footprint.median(),
            "sample_std_dev": footprint.std(),
            "skewness": footprint.skew(),
            "minimum": footprint.min(),
            "25th_percentile": footprint.quantile(0.25),
            "75th_percentile": footprint.quantile(0.75),
            "maximum": footprint.max(),
        }
    )


def summarize_by_category(transactions: pd.DataFrame) -> pd.DataFrame:
    """Summarize transaction count and carbon emissions by category."""
    return (
        transactions.groupby("category", as_index=False)
        .agg(
            transaction_count=("carbon_kg", "count"),
            total_carbon_kg=("carbon_kg", "sum"),
            mean_carbon_kg=("carbon_kg", "mean"),
        )
        .sort_values("total_carbon_kg", ascending=False)
    )


def save_footprint_distribution(
    transactions: pd.DataFrame, output_path: Path
) -> None:
    """Save a histogram and density curve for transaction emissions."""
    mean = transactions["carbon_kg"].mean()
    median = transactions["carbon_kg"].median()

    sns.set_theme(style="whitegrid")
    _, axis = plt.subplots(figsize=(10, 6))
    sns.histplot(data=transactions, x="carbon_kg", bins=30, kde=True, ax=axis)
    axis.axvline(mean, color="tab:red", linestyle="--", label=f"Mean: {mean:.2f} kg")
    axis.axvline(
        median, color="tab:green", linestyle=":", label=f"Median: {median:.2f} kg"
    )
    axis.set(
        title="Distribution of Transaction Carbon Footprints",
        xlabel="Carbon footprint (kg CO2)",
        ylabel="Number of transactions",
    )
    axis.legend()
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.close()


def main() -> None:
    """Load the transaction dataset, report EDA, and save its distribution plot."""
    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Transaction data not found at {DATA_PATH}. "
            "Generate it with `python EcoWallet/src/data_gen/transaction_data.py`."
        )

    transactions = pd.read_csv(DATA_PATH)
    required_columns = {"category", "carbon_kg"}
    missing_columns = required_columns.difference(transactions.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Transaction data is missing required columns: {missing}")
    if transactions.empty:
        raise ValueError(f"Transaction data is empty: {DATA_PATH}")
    if transactions["category"].isna().any():
        raise ValueError("Transaction data contains missing categories.")

    try:
        transactions["carbon_kg"] = pd.to_numeric(
            transactions["carbon_kg"], errors="raise"
        )
    except (TypeError, ValueError) as error:
        raise ValueError("The carbon_kg column must contain numeric values.") from error

    footprint = transactions["carbon_kg"]
    if footprint.isna().any() or not np.isfinite(footprint).all():
        raise ValueError("The carbon_kg column contains missing or non-finite values.")
    if (footprint < 0).any():
        raise ValueError("Carbon footprint values cannot be negative.")

    print(f"Exploratory analysis: {len(transactions):,} transactions")
    print("\nCarbon footprint statistics (kg CO2):")
    print(summarize_footprint(transactions).to_string(float_format=lambda value: f"{value:,.2f}"))
    print("\nEmissions by category (highest total first):")
    print(
        summarize_by_category(transactions).to_string(
            index=False, float_format=lambda value: f"{value:,.2f}"
        )
    )

    save_footprint_distribution(transactions, PLOT_PATH)
    print(f"\nDistribution plot saved to: {PLOT_PATH}")


if __name__ == "__main__":
    main()
