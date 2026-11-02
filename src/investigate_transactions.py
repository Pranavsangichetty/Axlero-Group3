import pandas as pd
from pathlib import Path

DATA_PATH = "data/raw/online_retail_II.csv"
REPORT_DIR = Path("reports")

def investigate():

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # Normalize fields for investigation
    df["Invoice"] = df["Invoice"].astype(str).str.strip()
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    cancelled = df["Invoice"].str.startswith("C", na=False)
    negative_qty = df["Quantity"] < 0
    zero_price = df["Price"] == 0
    negative_price = df["Price"] < 0
    missing_customer = df["Customer ID"].isna()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Relationship between cancellations and negative quantities
    print("\n========== CANCELLATION VS QUANTITY ==========")

    print(pd.crosstab(
        cancelled,
        negative_qty,
        rownames=["Cancelled invoice"],
        colnames=["Negative quantity"]
    ))

    print("\nNegative quantity on cancelled invoices:",
          (cancelled & negative_qty).sum())

    print("Negative quantity on non-cancelled invoices:",
          (~cancelled & negative_qty).sum())

    # 2. Duplicate investigation
    print("\n========== DUPLICATE INVESTIGATION ==========")

    exact_duplicates = df.duplicated(keep=False)

    print("Rows belonging to exact duplicate groups:",
          exact_duplicates.sum())

    print("Repeated Invoice + StockCode + InvoiceDate groups:",
          df.duplicated(
              subset=["Invoice", "StockCode", "InvoiceDate"],
              keep=False
          ).sum())

    df.loc[exact_duplicates].head(500).to_csv(
        REPORT_DIR / "duplicate_samples.csv",
        index=False
    )

    # 3. Negative quantity examples
    print("\n========== NEGATIVE QUANTITY EXAMPLES ==========")

    print(df.loc[
        negative_qty,
        ["Invoice", "StockCode", "Description",
         "Quantity", "InvoiceDate", "Price", "Customer ID"]
    ].head(15).to_string(index=False))

    df.loc[negative_qty].head(500).to_csv(
        REPORT_DIR / "negative_quantity_samples.csv",
        index=False
    )

    # 4. Zero-price investigation
    print("\n========== ZERO PRICE EXAMPLES ==========")

    print(df.loc[
        zero_price,
        ["Invoice", "StockCode", "Description",
         "Quantity", "InvoiceDate", "Customer ID"]
    ].head(15).to_string(index=False))

    df.loc[zero_price].head(500).to_csv(
        REPORT_DIR / "zero_price_samples.csv",
        index=False
    )

    # 5. Negative-price investigation
    print("\n========== NEGATIVE PRICE RECORDS ==========")

    print(df.loc[
        negative_price,
        ["Invoice", "StockCode", "Description",
         "Quantity", "InvoiceDate", "Customer ID"]
    ].to_string(index=False))

    df.loc[negative_price].to_csv(
        REPORT_DIR / "negative_price_records.csv",
        index=False
    )

    # 6. Missing customer ID investigation
    print("\n========== MISSING CUSTOMER ID ==========")

    print("Missing customer rows:", missing_customer.sum())
    print("Missing customer + negative quantity:",
          (missing_customer & negative_qty).sum())
    print("Missing customer + cancellation:",
          (missing_customer & cancelled).sum())

    # 7. Missing descriptions
    print("\n========== MISSING DESCRIPTION EXAMPLES ==========")

    print(df.loc[
        df["Description"].isna(),
        ["Invoice", "StockCode", "Quantity",
         "Price", "Customer ID", "Country"]
    ].head(15).to_string(index=False))

    # 8. Save cancellation and negative quantity samples
    df.loc[cancelled].head(500).to_csv(
        REPORT_DIR / "cancelled_invoice_samples.csv",
        index=False
    )

    print("\nInvestigation reports saved in reports/")


if __name__ == "__main__":
    investigate()
