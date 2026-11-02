import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = "data/interim/cleaned_transactions.csv"

FIGURE_DIR = Path("reports/figures")
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def run_eda():

    print("Loading cleaned transaction dataset...")

    df = pd.read_csv(
        DATA_PATH,
        dtype={"Invoice": "string"},
        low_memory=False
    )

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Time-based features
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month

    print("\n========== EDA OVERVIEW ==========")
    print("Rows:", len(df))
    print("Revenue:", round(df["TotalPrice"].sum(), 2))
    print("Orders:", df["Invoice"].nunique())
    print("Customers:", df["Customer ID"].nunique())
    print("Products:", df["StockCode"].nunique())
    print("Countries:", df["Country"].nunique())

    # 1. Monthly revenue
    monthly_revenue = (
        df.groupby("YearMonth")["TotalPrice"]
        .sum()
        .sort_index()
    )

    plt.figure(figsize=(14, 6))
    monthly_revenue.plot(marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "monthly_revenue.png", dpi=300)
    plt.close()

    # 2. Monthly orders
    monthly_orders = (
        df.groupby("YearMonth")["Invoice"]
        .nunique()
        .sort_index()
    )

    plt.figure(figsize=(14, 6))
    monthly_orders.plot(marker="o")
    plt.title("Monthly Order Volume")
    plt.xlabel("Month")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "monthly_orders.png", dpi=300)
    plt.close()

    # 3. Top 10 countries by revenue
    country_revenue = (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x=country_revenue.values,
        y=country_revenue.index
    )
    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "top_countries_revenue.png", dpi=300)
    plt.close()

    # 4. Top 10 products by quantity
    product_quantity = (
        df.groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x=product_quantity.values,
        y=product_quantity.index
    )
    plt.title("Top 10 Products by Quantity Sold")
    plt.xlabel("Quantity Sold")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "top_products_quantity.png", dpi=300)
    plt.close()

    # 5. Top 10 customers by revenue
    customer_revenue = (
        df.dropna(subset=["Customer ID"])
        .groupby("Customer ID")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x=customer_revenue.values,
        y=customer_revenue.index.astype(str)
    )
    plt.title("Top 10 Customers by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Customer ID")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "top_customers_revenue.png", dpi=300)
    plt.close()

    # 6. Transaction value distribution
    invoice_revenue = (
        df.groupby("Invoice")["TotalPrice"].sum()
    )

    plt.figure(figsize=(12, 6))
    sns.histplot(
        invoice_revenue,
        bins=50,
        kde=True
    )
    plt.title("Order Value Distribution")
    plt.xlabel("Order Value")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "order_value_distribution.png", dpi=300)
    plt.close()

    # Save analytical summaries
    monthly_revenue.to_csv(
        "reports/monthly_revenue.csv"
    )

    country_revenue.to_csv(
        "reports/country_revenue_top10.csv"
    )

    customer_revenue.to_csv(
        "reports/customer_revenue_top10.csv"
    )

    print("\n========== EDA COMPLETED ==========")
    print("Charts saved in reports/figures/")
    print("Summary CSV files saved in reports/")


if __name__ == "__main__":
    run_eda()
