import pandas as pd
from pathlib import Path

DATA_PATH = "data/raw/online_retail_II.csv"
REPORT_DIR = Path("reports")

def run_audit():

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # Convert columns for analysis
    df["Invoice"] = df["Invoice"].astype(str)
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    # Basic dataset information
    total_rows = len(df)

    print("\n========== DATASET OVERVIEW ==========")
    print("Total rows:", total_rows)
    print("Total columns:", len(df.columns))
    print("Date range:", df["InvoiceDate"].min(),
          "to", df["InvoiceDate"].max())

    print("\n========== UNIQUE COUNTS ==========")
    print("Unique invoices:", df["Invoice"].nunique())
    print("Unique customers:", df["Customer ID"].nunique())
    print("Unique products:", df["StockCode"].nunique())
    print("Unique countries:", df["Country"].nunique())

    # Missing values
    print("\n========== MISSING VALUES ==========")
    missing = df.isnull().sum()

    missing_report = pd.DataFrame({
        "Missing_Count": missing,
        "Missing_Percentage": (missing / total_rows * 100).round(2)
    })

    print(missing_report)

    # Duplicate records
    print("\n========== DUPLICATE ANALYSIS ==========")
    duplicate_count = df.duplicated().sum()
    print("Exact duplicate rows:", duplicate_count)
    print("Duplicate percentage:",
          round(duplicate_count / total_rows * 100, 2), "%")

    # Negative and zero quantities
    print("\n========== QUANTITY ANALYSIS ==========")
    print("Negative quantities:", (df["Quantity"] < 0).sum())
    print("Zero quantities:", (df["Quantity"] == 0).sum())
    print("Positive quantities:", (df["Quantity"] > 0).sum())

    # Price analysis
    print("\n========== PRICE ANALYSIS ==========")
    print("Negative prices:", (df["Price"] < 0).sum())
    print("Zero prices:", (df["Price"] == 0).sum())
    print("Positive prices:", (df["Price"] > 0).sum())

    # Cancelled invoices
    print("\n========== CANCELLATION ANALYSIS ==========")
    cancelled = df["Invoice"].str.startswith("C", na=False)

    print("Cancelled invoice rows:", cancelled.sum())
    print("Normal invoice rows:", (~cancelled).sum())
    print("Unique cancelled invoices:",
          df.loc[cancelled, "Invoice"].nunique())

    # Missing customer ID investigation
    print("\n========== CUSTOMER ID ANALYSIS ==========")
    missing_customer = df["Customer ID"].isna()

    print("Rows without Customer ID:", missing_customer.sum())
    print("Rows with Customer ID:", (~missing_customer).sum())

    print("Missing Customer ID with negative quantity:",
          (missing_customer & (df["Quantity"] < 0)).sum())

    print("Missing Customer ID with cancelled invoice:",
          (missing_customer & cancelled).sum())

    # Missing description investigation
    print("\n========== DESCRIPTION ANALYSIS ==========")
    print("Missing descriptions:", df["Description"].isna().sum())

    # Save audit reports
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    missing_report.to_csv(
        REPORT_DIR / "missing_values_report.csv"
    )

    summary = pd.DataFrame({
        "Metric": [
            "Total Rows",
            "Total Columns",
            "Unique Invoices",
            "Unique Customers",
            "Unique Products",
            "Unique Countries",
            "Exact Duplicates",
            "Negative Quantities",
            "Zero Quantities",
            "Negative Prices",
            "Zero Prices",
            "Cancelled Invoice Rows",
            "Missing Customer IDs",
            "Missing Descriptions"
        ],
        "Value": [
            total_rows,
            len(df.columns),
            df["Invoice"].nunique(),
            df["Customer ID"].nunique(),
            df["StockCode"].nunique(),
            df["Country"].nunique(),
            duplicate_count,
            (df["Quantity"] < 0).sum(),
            (df["Quantity"] == 0).sum(),
            (df["Price"] < 0).sum(),
            (df["Price"] == 0).sum(),
            cancelled.sum(),
            missing_customer.sum(),
            df["Description"].isna().sum()
        ]
    })

    summary.to_csv(
        REPORT_DIR / "data_quality_summary.csv",
        index=False
    )

    print("\n========== REPORTS SAVED ==========")
    print("reports/missing_values_report.csv")
    print("reports/data_quality_summary.csv")


if __name__ == "__main__":
    run_audit()
