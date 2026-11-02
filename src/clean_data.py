import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/online_retail_II.csv")
INTERIM_DIR = Path("data/interim")
PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports")


def clean_data():

    print("Loading raw dataset...")

    df = pd.read_csv(RAW_PATH)

    initial_rows = len(df)

    # Normalize data types
    df["Invoice"] = df["Invoice"].astype(str).str.strip()
    df["StockCode"] = df["StockCode"].astype(str).str.strip()
    df["Country"] = df["Country"].astype(str).str.strip()

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    df["Customer ID"] = pd.to_numeric(
        df["Customer ID"], errors="coerce"
    ).astype("Int64")

    # Store cleaning statistics
    cleaning_log = []

    def log_step(step, before, after):
        cleaning_log.append({
            "Step": step,
            "Rows_Before": before,
            "Rows_After": after,
            "Rows_Removed": before - after
        })

        print(
            f"{step}: {before:,} -> {after:,} "
            f"(removed {before - after:,})"
        )

    # Step 1: Remove exact duplicate rows
    before = len(df)

    df = df.drop_duplicates().copy()

    log_step("Exact duplicate removal", before, len(df))

    # Step 2: Exclude cancelled invoices
    before = len(df)

    cancelled = df["Invoice"].str.startswith("C", na=False)
    df = df.loc[~cancelled].copy()

    log_step("Cancelled invoice exclusion", before, len(df))

    # Step 3: Keep positive quantities
    before = len(df)

    df = df.loc[df["Quantity"] > 0].copy()

    log_step("Positive quantity filter", before, len(df))

    # Step 4: Keep positive prices
    before = len(df)

    df = df.loc[df["Price"] > 0].copy()

    log_step("Positive price filter", before, len(df))

    # Step 5: Remove invalid dates
    before = len(df)

    df = df.dropna(subset=["InvoiceDate"]).copy()

    log_step("Valid invoice date filter", before, len(df))

    # Step 6: Calculate transaction revenue
    df["TotalPrice"] = df["Quantity"] * df["Price"]

    # Save transaction-level dataset.
    # Missing Customer IDs are retained here.
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    transaction_path = (
        INTERIM_DIR / "cleaned_transactions.csv"
    )

    df.to_csv(transaction_path, index=False)

    # Step 7: Create customer-level dataset
    customer_df = df.dropna(subset=["Customer ID"]).copy()

    customer_path = (
        PROCESSED_DIR / "customer_transactions.csv"
    )

    customer_df.to_csv(customer_path, index=False)

    # Save cleaning log
    cleaning_log_df = pd.DataFrame(cleaning_log)

    cleaning_log_df.to_csv(
        REPORT_DIR / "cleaning_log.csv",
        index=False
    )

    # Save final summary
    summary = pd.DataFrame({
        "Metric": [
            "Original rows",
            "Cleaned transaction rows",
            "Customer transaction rows",
            "Unique customers",
            "Unique invoices",
            "Unique products",
            "Countries",
            "Total sales revenue"
        ],
        "Value": [
            initial_rows,
            len(df),
            len(customer_df),
            customer_df["Customer ID"].nunique(),
            df["Invoice"].nunique(),
            df["StockCode"].nunique(),
            df["Country"].nunique(),
            round(df["TotalPrice"].sum(), 2)
        ]
    })

    summary.to_csv(
        REPORT_DIR / "cleaning_summary.csv",
        index=False
    )

    print("\n========== CLEANING COMPLETED ==========")
    print("Original rows:", f"{initial_rows:,}")
    print("Cleaned transactions:", f"{len(df):,}")
    print("Customer transactions:", f"{len(customer_df):,}")
    print(
        "Unique customers:",
        f"{customer_df['Customer ID'].nunique():,}"
    )
    print(
        "Total sales revenue:",
        round(df["TotalPrice"].sum(), 2)
    )

    print("\n========== OUTPUT FILES ==========")
    print(transaction_path)
    print(customer_path)
    print("reports/cleaning_log.csv")
    print("reports/cleaning_summary.csv")


if __name__ == "__main__":
    clean_data()
