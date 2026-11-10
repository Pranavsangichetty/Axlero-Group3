from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data/processed/customer_transactions.csv"
OUTPUT_DIR = ROOT / "data/processed"
REPORT_DIR = ROOT / "reports"

# Feature window: [2011-01-02, 2011-07-01)
FEATURE_START = pd.Timestamp("2011-01-02")
CUTOFF = pd.Timestamp("2011-07-01")

# Observation window: [2011-07-01, 2011-09-29)
OBSERVATION_START = CUTOFF
OBSERVATION_END = pd.Timestamp("2011-09-29")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, low_memory=False)

    required = {
        "Invoice", "StockCode", "InvoiceDate",
        "Customer ID", "Quantity", "Price", "TotalPrice"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Customer ID"] = pd.to_numeric(df["Customer ID"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["TotalPrice"] = pd.to_numeric(df["TotalPrice"], errors="coerce")

    df = df.dropna(subset=[
        "InvoiceDate", "Customer ID", "Invoice",
        "StockCode", "Quantity", "TotalPrice"
    ])

    # Restrict the data to the two defined time windows.
    feature_data = df[
        (df["InvoiceDate"] >= FEATURE_START) &
        (df["InvoiceDate"] < CUTOFF)
    ].copy()

    observation_data = df[
        (df["InvoiceDate"] >= OBSERVATION_START) &
        (df["InvoiceDate"] < OBSERVATION_END)
    ].copy()

    if feature_data.empty:
        raise ValueError("No transactions found in the feature window.")

    # Customer cohort: customers who purchased during the feature window.
    features = feature_data.groupby("Customer ID").agg(
        Recency=("InvoiceDate", lambda x: (CUTOFF - x.max()).days),
        Frequency=("Invoice", "nunique"),
        Monetary=("TotalPrice", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Unique_Products=("StockCode", "nunique"),
        Average_Order_Value=("TotalPrice", "sum"),
    )

    order_values = (
        feature_data.groupby(["Customer ID", "Invoice"])["TotalPrice"]
        .sum()
        .groupby("Customer ID")
        .mean()
    )
    features["Average_Order_Value"] = order_values

    # Label using only transactions after the feature cutoff.
    future_purchases = observation_data.groupby("Customer ID")["Invoice"].nunique()

    features["Future_Orders_90d"] = (
        future_purchases.reindex(features.index).fillna(0).astype(int)
    )
    features["Churn"] = (features["Future_Orders_90d"] == 0).astype(int)

    result = features.reset_index().rename(
        columns={"Customer ID": "CustomerID"}
    )

    # Basic integrity checks.
    if result["CustomerID"].duplicated().any():
        raise ValueError("Duplicate customer IDs found.")
    if result.isna().any().any():
        raise ValueError("Missing values found in the output.")
    if not result["Churn"].isin([0, 1]).all():
        raise ValueError("Churn label must contain only 0 and 1.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "historical_churn_dataset.csv"
    result.to_csv(output_file, index=False)

    churn_counts = result["Churn"].value_counts().sort_index()
    churn_rate = result["Churn"].mean() * 100

    metadata = {
        "feature_window_start": str(FEATURE_START.date()),
        "feature_window_end": "2011-06-30",
        "observation_window_start": str(OBSERVATION_START.date()),
        "observation_window_end": "2011-09-28",
        "customer_cohort": "Customers with at least one purchase in the feature window",
        "label_definition": {
            "1": "No purchase during the 90-day observation window",
            "0": "At least one purchase during the 90-day observation window"
        },
        "features": [
            "Recency", "Frequency", "Monetary",
            "Total_Quantity", "Unique_Products", "Average_Order_Value"
        ],
        "target": "Churn",
        "warning": (
            "Churn is a 90-day inactivity proxy, not proof of permanent churn. "
            "Features use transactions before 2011-07-01 only. "
            "Future_Orders_90d is retained for audit and must NOT be used as a model feature."
        )
    }

    metadata_file = OUTPUT_DIR / "historical_churn_dataset_metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=4))

    report = [
        "# Historical Churn Dataset Validation",
        "",
        "## Time windows",
        "- Feature window: 2011-01-02 to 2011-06-30",
        "- Observation window: 2011-07-01 to 2011-09-28",
        "",
        "## Dataset summary",
        f"- Customers: {len(result):,}",
        f"- Churned customers (label 1): {int(churn_counts.get(1, 0)):,}",
        f"- Active customers (label 0): {int(churn_counts.get(0, 0)):,}",
        f"- Churn rate: {churn_rate:.2f}%",
        f"- Duplicate customer IDs: {int(result['CustomerID'].duplicated().sum())}",
        f"- Missing output values: {int(result.isna().sum().sum())}",
        "",
        "## Model usage",
        "Use Recency, Frequency, Monetary, Total_Quantity, Unique_Products, "
        "and Average_Order_Value as candidate features.",
        "",
        "**Do not use `Future_Orders_90d` as a model feature.** It is included "
        "only to audit how the target label was assigned.",
        "",
        "Churn means no observed purchase during the 90-day observation window. "
        "It does not establish permanent customer loss.",
    ]

    report_file = REPORT_DIR / "historical_churn_dataset_validation.md"
    report_file.write_text("\n".join(report) + "\n")

    print("\nHistorical churn dataset created successfully.")
    print(f"Customers: {len(result):,}")
    print(f"Churned (1): {int(churn_counts.get(1, 0)):,}")
    print(f"Active (0): {int(churn_counts.get(0, 0)):,}")
    print(f"Churn rate: {churn_rate:.2f}%")
    print(f"Output: {output_file}")
    print(f"Metadata: {metadata_file}")
    print(f"Validation report: {report_file}")
    print("\nOutput columns:")
    print(result.columns.tolist())


if __name__ == "__main__":
    main()
