"""Validate and integrate customer-level RFM and segmentation features."""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

RFM_FILE = PROCESSED / "customer_rfm.csv"
SEGMENT_FILE = PROCESSED / "customer_segments.csv"
TRANSACTION_FILE = PROCESSED / "customer_transactions.csv"

OUTPUT_FILE = PROCESSED / "customer_rfm_features.csv"
METADATA_FILE = PROCESSED / "customer_rfm_features_metadata.json"
DICTIONARY_FILE = REPORTS / "rfm_feature_dictionary.md"
VALIDATION_FILE = REPORTS / "rfm_validation_report.md"


def require_columns(frame, required, filename):
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"{filename} is missing required columns: {missing}")


def main():
    for path in (RFM_FILE, SEGMENT_FILE, TRANSACTION_FILE):
        if not path.exists():
            raise FileNotFoundError(f"Required input file not found: {path}")

    rfm = pd.read_csv(RFM_FILE)
    segments = pd.read_csv(SEGMENT_FILE)
    transactions = pd.read_csv(TRANSACTION_FILE, parse_dates=["InvoiceDate"])

    require_columns(
        rfm, ["CustomerID", "Recency", "Frequency", "Monetary"],
        RFM_FILE.name
    )
    require_columns(
        segments, ["CustomerID", "Cluster", "Segment"],
        SEGMENT_FILE.name
    )
    require_columns(
        transactions, ["Customer ID", "InvoiceDate", "TotalPrice"],
        TRANSACTION_FILE.name
    )

    # Validate customer-level uniqueness before joining.
    if rfm["CustomerID"].duplicated().any():
        raise ValueError("Duplicate CustomerID values found in customer_rfm.csv")
    if segments["CustomerID"].duplicated().any():
        raise ValueError("Duplicate CustomerID values found in customer_segments.csv")

    rfm_ids = set(rfm["CustomerID"].dropna())
    segment_ids = set(segments["CustomerID"].dropna())
    transaction_ids = set(transactions["Customer ID"].dropna())

    if rfm_ids != segment_ids:
        raise ValueError("Customer IDs do not match between RFM and segment files")
    if rfm_ids != transaction_ids:
        raise ValueError(
            "Customer IDs do not match between RFM and customer transactions"
        )

    # Keep the customer-level features needed for downstream analysis.
    features = rfm.merge(
        segments[["CustomerID", "Cluster", "Segment"]],
        on="CustomerID",
        how="inner",
        validate="one_to_one"
    )

    features = features[
        ["CustomerID", "Recency", "Frequency", "Monetary", "Cluster", "Segment"]
    ].sort_values("CustomerID").reset_index(drop=True)

    if features.isna().any().any():
        raise ValueError("Missing values found in the integrated feature dataset")
    if (features["Frequency"] <= 0).any():
        raise ValueError("Frequency must be positive")
    if (features["Monetary"] <= 0).any():
        raise ValueError("Monetary must be positive")

    features.to_csv(OUTPUT_FILE, index=False)

    reference_date = (
        transactions["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)
    )

    metadata = {
        "dataset": OUTPUT_FILE.name,
        "row_count": int(len(features)),
        "column_count": int(len(features.columns)),
        "unique_customers": int(features["CustomerID"].nunique()),
        "reference_date": reference_date.strftime("%Y-%m-%d"),
        "source_files": [
            RFM_FILE.name,
            SEGMENT_FILE.name,
            TRANSACTION_FILE.name
        ],
        "columns": features.columns.tolist(),
        "important_limitation": (
            "This RFM snapshot uses the full available transaction history. "
            "It is suitable for descriptive segmentation, but must not be used "
            "directly as a historical churn-training snapshot. For churn "
            "prediction, recompute features at each historical cutoff and use "
            "only transactions available on or before that cutoff."
        )
    }
    METADATA_FILE.write_text(json.dumps(metadata, indent=4), encoding="utf-8")

    dictionary = """# Customer RFM Feature Dictionary

## Purpose
This file documents the integrated customer-level RFM and segmentation dataset.

## Output
`data/processed/customer_rfm_features.csv`

| Column | Description |
|---|---|
| `CustomerID` | Unique customer identifier |
| `Recency` | Number of days since the customer's most recent purchase at the RFM reference date |
| `Frequency` | Number of distinct invoices/orders for the customer |
| `Monetary` | Sum of customer transaction value |
| `Cluster` | K-Means cluster identifier |
| `Segment` | Business-readable customer segment assigned to the cluster |

## Snapshot limitation
The current RFM snapshot uses the full available transaction history, with a reference date one day after the latest transaction. It is intended for descriptive customer segmentation. Do not use it directly to train a historical forward-looking churn model because that can introduce future-data leakage. Recalculate RFM at a historical cutoff for churn modelling.
"""
    DICTIONARY_FILE.write_text(dictionary, encoding="utf-8")

    segment_counts = (
        features.groupby("Segment")
        .agg(
            Customers=("CustomerID", "nunique"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean")
        )
        .sort_values("Customers", ascending=False)
    )

    report = [
        "# RFM Feature Integration and Validation Report",
        "",
        "## Validation results",
        f"- Integrated customer records: {len(features):,}",
        f"- Unique customers: {features['CustomerID'].nunique():,}",
        f"- Duplicate customer IDs: {features['CustomerID'].duplicated().sum():,}",
        f"- Missing cells: {int(features.isna().sum().sum()):,}",
        f"- RFM reference date: {reference_date:%Y-%m-%d}",
        "- RFM and segment customer IDs: exact match",
        "- Transaction and RFM customer IDs: exact match",
        "- Frequency and Monetary values: positive for all records",
        "",
        "## Segment counts and average RFM values",
        (
            "| Segment | Customers | Avg Recency | Avg Frequency | Avg Monetary |\n"
            "|---|---:|---:|---:|---:|\n"
            + "\n".join(
                f"| {name} | {int(row['Customers'])} | "
                f"{row['Avg_Recency']:.2f} | "
                f"{row['Avg_Frequency']:.2f} | "
                f"{row['Avg_Monetary']:.2f} |"
                for name, row in segment_counts.round(2).iterrows()
            )
        ),
        "",
        "## Churn modelling caution",
        metadata["important_limitation"],
        ""
    ]
    VALIDATION_FILE.write_text("\n".join(report), encoding="utf-8")

    print("RFM feature integration completed successfully.")
    print(f"Output: {OUTPUT_FILE.relative_to(ROOT)}")
    print(f"Rows: {len(features):,}")
    print(f"Columns: {len(features.columns)}")
    print(f"Unique customers: {features['CustomerID'].nunique():,}")
    print(f"Missing cells: {int(features.isna().sum().sum()):,}")
    print(f"Duplicate IDs: {features['CustomerID'].duplicated().sum():,}")
    print(f"Reference date: {reference_date:%Y-%m-%d}")
    print("\nFiles generated:")
    print(f"- {OUTPUT_FILE.relative_to(ROOT)}")
    print(f"- {METADATA_FILE.relative_to(ROOT)}")
    print(f"- {DICTIONARY_FILE.relative_to(ROOT)}")
    print(f"- {VALIDATION_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
