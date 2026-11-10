
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAW_PATH = Path("data/raw/online_retail_II.csv")
CLEAN_PATH = Path("data/interim/cleaned_transactions.csv")
CUSTOMER_PATH = Path("data/processed/customer_transactions.csv")
LOG_PATH = Path("reports/cleaning_log.csv")
SUMMARY_PATH = Path("reports/cleaning_summary.csv")

REPORT_DIR = Path("reports")
RESULTS_PATH = REPORT_DIR / "week1_validation_results.csv"
REPORT_PATH = REPORT_DIR / "week1_data_validation_report.md"

REQUIRED_COLUMNS = [
    "Invoice", "StockCode", "Description", "Quantity",
    "InvoiceDate", "Price", "Customer ID", "Country",
    "TotalPrice"
]

results = []


def record_check(name, passed, observed, expected, details=""):
    results.append({
        "Check": name,
        "Status": "PASS" if passed else "FAIL",
        "Observed": str(observed),
        "Expected": str(expected),
        "Details": details
    })

    symbol = "PASS" if passed else "FAIL"
    print(f"[{symbol}] {name}: {details}")


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading Week 1 validation datasets...")

    required_files = [
        RAW_PATH, CLEAN_PATH, CUSTOMER_PATH,
        LOG_PATH, SUMMARY_PATH
    ]

    missing_files = [str(path) for path in required_files if not path.exists()]

    if missing_files:
        raise FileNotFoundError(
            "Required files are missing: " + ", ".join(missing_files)
        )

    raw = pd.read_csv(RAW_PATH)
    clean = pd.read_csv(CLEAN_PATH)
    customers = pd.read_csv(CUSTOMER_PATH)
    log = pd.read_csv(LOG_PATH)
    summary = pd.read_csv(SUMMARY_PATH)

    # Normalize fields for reliable validation.
    for df in [clean, customers]:
        df["InvoiceDate"] = pd.to_datetime(
            df["InvoiceDate"], errors="coerce"
        )

        df["Invoice"] = df["Invoice"].astype(str).str.strip()

    print("\n========== DATASET VALIDATION ==========")

    record_check(
        "Raw dataset is not empty",
        len(raw) > 0,
        len(raw),
        "> 0"
    )

    record_check(
        "Cleaned dataset is not empty",
        len(clean) > 0,
        len(clean),
        "> 0"
    )

    record_check(
        "Required columns exist",
        set(REQUIRED_COLUMNS).issubset(clean.columns),
        sorted(set(REQUIRED_COLUMNS) - set(clean.columns)),
        "No missing required columns"
    )

    if not set(REQUIRED_COLUMNS).issubset(clean.columns):
        raise ValueError("Required columns missing from cleaned dataset.")

    print("\n========== CLEANING VALIDATION ==========")

    record_check(
        "No exact duplicate rows in cleaned dataset",
        clean.duplicated().sum() == 0,
        clean.duplicated().sum(),
        0
    )

    record_check(
        "No cancelled invoices",
        not clean["Invoice"].str.startswith("C", na=False).any(),
        clean["Invoice"].str.startswith("C", na=False).sum(),
        0
    )

    record_check(
        "All quantities are positive",
        (clean["Quantity"] > 0).all(),
        (clean["Quantity"] <= 0).sum(),
        0
    )

    record_check(
        "All prices are positive",
        (clean["Price"] > 0).all(),
        (clean["Price"] <= 0).sum(),
        0
    )

    record_check(
        "All invoice dates are valid",
        clean["InvoiceDate"].notna().all(),
        clean["InvoiceDate"].isna().sum(),
        0
    )

    # Verify revenue calculation.
    expected_revenue = clean["Quantity"] * clean["Price"]

    revenue_difference = (
        clean["TotalPrice"] - expected_revenue
    ).abs().max()

    record_check(
        "Revenue calculation is consistent",
        np.allclose(
            clean["TotalPrice"],
            expected_revenue,
            rtol=1e-9,
            atol=1e-6
        ),
        revenue_difference,
        "Maximum difference <= 0.000001"
    )

    print("\n========== CUSTOMER DATA VALIDATION ==========")

    record_check(
        "No missing Customer IDs in customer dataset",
        customers["Customer ID"].notna().all(),
        customers["Customer ID"].isna().sum(),
        0
    )

    expected_customer_rows = clean["Customer ID"].notna().sum()

    record_check(
        "Customer dataset row count matches filtered transactions",
        len(customers) == expected_customer_rows,
        len(customers),
        expected_customer_rows
    )

    record_check(
        "Customer IDs are consistent between datasets",
        set(customers["Customer ID"].dropna().unique())
        == set(clean["Customer ID"].dropna().unique()),
        customers["Customer ID"].nunique(),
        clean["Customer ID"].nunique()
    )

    print("\n========== CLEANING LOG VALIDATION ==========")

    required_log_columns = [
        "Step", "Rows_Before", "Rows_After", "Rows_Removed"
    ]

    log_columns_exist = set(required_log_columns).issubset(log.columns)

    record_check(
        "Cleaning log has required columns",
        log_columns_exist,
        list(log.columns),
        required_log_columns
    )

    if log_columns_exist and len(log) > 0:
        chain_valid = (
            log["Rows_Before"].iloc[1:].reset_index(drop=True)
            == log["Rows_After"].iloc[:-1].reset_index(drop=True)
        ).all()

        record_check(
            "Cleaning log row counts are continuous",
            chain_valid,
            chain_valid,
            True
        )

        removal_valid = (
            log["Rows_Before"] - log["Rows_After"]
            == log["Rows_Removed"]
        ).all()

        record_check(
            "Cleaning log removal counts are consistent",
            removal_valid,
            removal_valid,
            True
        )

        record_check(
            "Cleaning log final row count matches cleaned dataset",
            int(log["Rows_After"].iloc[-1]) == len(clean),
            int(log["Rows_After"].iloc[-1]),
            len(clean)
        )

        record_check(
            "Cleaning log starts with raw row count",
            int(log["Rows_Before"].iloc[0]) == len(raw),
            int(log["Rows_Before"].iloc[0]),
            len(raw)
        )

    print("\n========== SUMMARY VALIDATION ==========")

    summary_values = dict(zip(summary["Metric"], summary["Value"]))

    summary_checks = [
        ("Original rows", len(raw)),
        ("Cleaned transaction rows", len(clean)),
        ("Customer transaction rows", len(customers)),
        ("Unique customers", customers["Customer ID"].nunique()),
        ("Unique invoices", clean["Invoice"].nunique()),
        ("Unique products", clean["StockCode"].nunique()),
        ("Countries", clean["Country"].nunique())
    ]

    for metric, actual in summary_checks:
        recorded = summary_values.get(metric, np.nan)

        record_check(
            f"Summary matches: {metric}",
            pd.notna(recorded) and np.isclose(float(recorded), float(actual)),
            actual,
            recorded
        )

    recorded_revenue = summary_values.get("Total sales revenue", np.nan)
    actual_revenue = clean["TotalPrice"].sum()

    record_check(
        "Summary matches: Total sales revenue",
        pd.notna(recorded_revenue)
        and np.isclose(float(recorded_revenue), actual_revenue, atol=0.01),
        round(actual_revenue, 2),
        recorded_revenue
    )

    # Save machine-readable validation results.
    results_df = pd.DataFrame(results)
    results_df.to_csv(RESULTS_PATH, index=False)

    passed = int((results_df["Status"] == "PASS").sum())
    failed = int((results_df["Status"] == "FAIL").sum())

    report = f"""# Week 1 Independent Data Validation Report

## Project
Retail & E-commerce — Customer Segmentation and Churn Prediction

## Purpose
Independently validate the raw dataset, cleaned transactions,
customer-level dataset, cleaning log and cleaning summary.

## Dataset statistics

| Metric | Result |
|---|---:|
| Raw records | {len(raw):,} |
| Cleaned transactions | {len(clean):,} |
| Customer transactions | {len(customers):,} |
| Unique customers | {customers['Customer ID'].nunique():,} |
| Unique invoices | {clean['Invoice'].nunique():,} |
| Unique products | {clean['StockCode'].nunique():,} |
| Countries | {clean['Country'].nunique():,} |
| Total sales revenue | {actual_revenue:,.2f} |

## Validation results

- Total checks: {len(results_df)}
- Passed: {passed}
- Failed: {failed}

| Check | Status | Details |
|---|---|---|
"""

    for _, row in results_df.iterrows():
        report += (
            f"| {row['Check']} | {row['Status']} "
            f"| {row['Details']} |\n"
        )

    report += """
## Validation interpretation

PASS means the tested condition was satisfied by the available files.
FAIL means the condition requires investigation.

This validation checks consistency between the existing outputs.
It does not prove that every original cleaning decision is
business-correct or that the dataset is free of all possible errors.

## Limitations

- Customer-level data intentionally excludes records without Customer IDs.
- The transaction-level cleaned dataset retains those records.
- Negative quantities, cancellations and non-positive prices were
  excluded according to the existing cleaning pipeline.
- Duplicate removal is based on exact row matching.
"""

    REPORT_PATH.write_text(report, encoding="utf-8")

    print("\n========== FINAL VALIDATION SUMMARY ==========")
    print("Total checks:", len(results_df))
    print("Passed:", passed)
    print("Failed:", failed)
    print("\nReports saved:")
    print(RESULTS_PATH)
    print(REPORT_PATH)

    if failed:
        print("\nSome checks failed. Investigate before marking validation complete.")
        raise SystemExit(1)

    print("\nAll independent validation checks passed.")


if __name__ == "__main__":
    main()
