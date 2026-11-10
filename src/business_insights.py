
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Paths and configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

FEATURES_FILE = ROOT / "data/processed/customer_rfm_features.csv"
TRANSACTIONS_FILE = ROOT / "data/processed/customer_transactions.csv"

REPORT_DIR = ROOT / "reports"
CHART_DIR = REPORT_DIR / "business_insights"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

SEGMENT_ORDER = [
    "Champions",
    "Loyal High-Value",
    "Recent Customers",
    "At-Risk / Hibernating",
]

RECOMMENDATIONS = {
    "Champions": {
        "behaviour": "Recent purchasing, highest average frequency and monetary value.",
        "strategy": "Offer VIP rewards, early product access, referral benefits and exclusive loyalty perks.",
        "objective": "Retain high-value customers and encourage advocacy.",
    },
    "Loyal High-Value": {
        "behaviour": "Historically valuable customers with lower recent purchasing activity.",
        "strategy": "Send personalized win-back emails, loyalty reminders and relevant product recommendations.",
        "objective": "Reactivate valuable customers.",
    },
    "Recent Customers": {
        "behaviour": "Recently active customers with comparatively lower purchase frequency and spending.",
        "strategy": "Use welcome campaigns, second-purchase incentives and product recommendations.",
        "objective": "Convert recent buyers into repeat customers.",
    },
    "At-Risk / Hibernating": {
        "behaviour": "Longest time since purchase and lowest average frequency and monetary value.",
        "strategy": "Test targeted re-engagement campaigns, feedback surveys and carefully controlled discounts.",
        "objective": "Reactivate customers where commercially worthwhile.",
    },
}


def load_data():
    """Load and validate customer and transaction datasets."""

    if not FEATURES_FILE.exists():
        raise FileNotFoundError(f"Missing file: {FEATURES_FILE}")

    if not TRANSACTIONS_FILE.exists():
        raise FileNotFoundError(f"Missing file: {TRANSACTIONS_FILE}")

    customers = pd.read_csv(FEATURES_FILE)
    transactions = pd.read_csv(TRANSACTIONS_FILE)

    required_customer_columns = {
        "CustomerID", "Recency", "Frequency",
        "Monetary", "Cluster", "Segment"
    }
    required_transaction_columns = {
        "Invoice", "Customer ID", "InvoiceDate",
        "Quantity", "TotalPrice"
    }

    if not required_customer_columns.issubset(customers.columns):
        raise ValueError("Customer RFM feature file is missing required columns.")

    if not required_transaction_columns.issubset(transactions.columns):
        raise ValueError("Transaction file is missing required columns.")

    if customers["CustomerID"].duplicated().any():
        raise ValueError("Duplicate CustomerID values found.")

    if customers[list(required_customer_columns)].isna().any().any():
        raise ValueError("Missing values found in customer RFM features.")

    customers["CustomerID"] = pd.to_numeric(
        customers["CustomerID"], errors="raise"
    ).astype("int64")

    transactions["Customer ID"] = pd.to_numeric(
        transactions["Customer ID"], errors="raise"
    ).astype("int64")

    transactions["InvoiceDate"] = pd.to_datetime(
        transactions["InvoiceDate"], errors="raise"
    )

    if not set(customers["CustomerID"]).issubset(
        set(transactions["Customer ID"])
    ):
        raise ValueError("Some RFM customers are absent from transaction data.")

    return customers, transactions


def calculate_insights(customers, transactions):
    """Calculate segment-level customer and transaction metrics."""

    customer_metrics = (
        customers.groupby("Segment")
        .agg(
            Customers=("CustomerID", "nunique"),
            Avg_Recency=("Recency", "mean"),
            Median_Recency=("Recency", "median"),
            Avg_Frequency=("Frequency", "mean"),
            Median_Frequency=("Frequency", "median"),
            Avg_Monetary=("Monetary", "mean"),
            Median_Monetary=("Monetary", "median"),
            Total_Revenue=("Monetary", "sum"),
        )
    )

    total_customers = customers["CustomerID"].nunique()
    total_revenue = customers["Monetary"].sum()

    customer_metrics["Customer_Percentage"] = (
        customer_metrics["Customers"] / total_customers * 100
    )

    customer_metrics["Revenue_Share_Percentage"] = (
        customer_metrics["Total_Revenue"] / total_revenue * 100
    )

    customer_metrics["Revenue_Per_Customer"] = (
        customer_metrics["Total_Revenue"] /
        customer_metrics["Customers"]
    )

    # Join transactions to the customer segment assignment.
    segment_lookup = customers[["CustomerID", "Segment"]].rename(
        columns={"CustomerID": "Customer ID"}
    )

    transaction_data = transactions.merge(
        segment_lookup,
        on="Customer ID",
        how="inner",
        validate="many_to_one",
    )

    transaction_metrics = (
        transaction_data.groupby("Segment")
        .agg(
            Transaction_Lines=("Invoice", "size"),
            Unique_Orders=("Invoice", "nunique"),
            Units_Sold=("Quantity", "sum"),
            Transaction_Revenue=("TotalPrice", "sum"),
            Active_Customers=("Customer ID", "nunique"),
        )
    )

    result = customer_metrics.join(transaction_metrics, how="left")

    result["Average_Order_Value"] = (
        result["Transaction_Revenue"] / result["Unique_Orders"]
    )

    result = result.reindex(SEGMENT_ORDER)
    result.index.name = "Segment"

    return result, transaction_data


def create_charts(metrics):
    """Save business insight charts."""

    chart_data = metrics.dropna()

    # Chart 1: Customer distribution
    plt.figure(figsize=(10, 6))
    plt.bar(
        chart_data.index,
        chart_data["Customers"],
    )
    plt.title("Customer Distribution by Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "customer_distribution.png", dpi=300)
    plt.close()

    # Chart 2: Revenue contribution
    plt.figure(figsize=(10, 6))
    plt.bar(
        chart_data.index,
        chart_data["Revenue_Share_Percentage"],
    )
    plt.title("Revenue Contribution by Customer Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Revenue Share (%)")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "revenue_contribution.png", dpi=300)
    plt.close()

    # Chart 3: Average customer monetary value
    plt.figure(figsize=(10, 6))
    plt.bar(
        chart_data.index,
        chart_data["Avg_Monetary"],
    )
    plt.title("Average Monetary Value by Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Average Monetary Value")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "average_customer_value.png", dpi=300)
    plt.close()


def write_report(metrics, customers, transactions):
    """Generate the business insights Markdown report."""

    total_customers = customers["CustomerID"].nunique()
    total_revenue = customers["Monetary"].sum()
    total_orders = transactions["Invoice"].nunique()

    lines = [
        "# Customer Segmentation – Business Insights",
        "",
        "## 1. Executive Summary",
        "",
        f"The analysis covers **{total_customers:,} customers**, "
        f"with customer-level RFM monetary value totaling "
        f"**{total_revenue:,.2f}**.",
        "",
        f"The transaction dataset contains **{total_orders:,} unique orders**.",
        "",
        "The objective is to translate the four RFM customer segments "
        "into practical retention, engagement and revenue-growth actions.",
        "",
        "## 2. Segment-Level Business Metrics",
        "",
        "| Segment | Customers | Customer Share | Revenue | Revenue Share | "
        "Avg. Recency | Avg. Frequency | Avg. Monetary |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for segment, row in metrics.iterrows():
        if pd.isna(row["Customers"]):
            continue

        lines.append(
            f"| {segment} "
            f"| {row['Customers']:,.0f} "
            f"| {row['Customer_Percentage']:.2f}% "
            f"| {row['Total_Revenue']:,.2f} "
            f"| {row['Revenue_Share_Percentage']:.2f}% "
            f"| {row['Avg_Recency']:.2f} days "
            f"| {row['Avg_Frequency']:.2f} "
            f"| {row['Avg_Monetary']:,.2f} |"
        )

    lines.extend([
        "",
        "## 3. Segment-Wise Business Insights",
        "",
    ])

    for segment in SEGMENT_ORDER:
        if segment not in metrics.index:
            continue

        row = metrics.loc[segment]
        recommendation = RECOMMENDATIONS[segment]

        lines.extend([
            f"### {segment}",
            "",
            f"- Customers: {row['Customers']:,.0f} "
            f"({row['Customer_Percentage']:.2f}% of customers)",
            f"- Revenue contribution: {row['Total_Revenue']:,.2f}",
            f"- Revenue share: {row['Revenue_Share_Percentage']:.2f}%",
            f"- Average recency: {row['Avg_Recency']:.2f} days",
            f"- Average frequency: {row['Avg_Frequency']:.2f} orders",
            f"- Average monetary value: {row['Avg_Monetary']:,.2f}",
            f"- Customer behaviour: {recommendation['behaviour']}",
            f"- Recommended strategy: {recommendation['strategy']}",
            f"- Primary objective: {recommendation['objective']}",
            "",
        ])

    lines.extend([
        "## 4. Overall Business Recommendations",
        "",
        "1. Protect Champions through loyalty benefits and personalized experiences.",
        "2. Prioritize high-value customer reactivation campaigns for Loyal High-Value customers.",
        "3. Encourage Recent Customers to make a second and third purchase.",
        "4. Test cost-effective re-engagement campaigns for At-Risk / Hibernating customers.",
        "5. Monitor segment size, revenue share and purchasing behaviour over time.",
        "6. Measure campaign performance using repeat purchase rate, reactivation rate "
        "and incremental revenue.",
        "",
        "## 5. Important Interpretation Notes",
        "",
        "- Monetary values are based on the existing cleaned customer transaction data.",
        "- Revenue share is calculated from the sum of customer-level Monetary values.",
        "- Frequency represents the number of distinct invoices in the RFM dataset.",
        "- Average Order Value is calculated using transaction revenue divided by "
        "unique invoices in each segment.",
        "- These are descriptive historical findings, not proof that a marketing "
        "campaign will cause a particular outcome.",
        "- The RFM snapshot uses the complete available transaction history, with "
        "reference date 2011-12-10. It is suitable for descriptive segmentation.",
        "- Do not use this full-history RFM snapshot as historical input for "
        "forward-looking churn prediction because it can introduce future-data leakage.",
        "- A churn model requires cutoff-based historical features and a separate "
        "future observation window for its target label.",
        "",
        "## 6. Visualizations",
        "",
        "![Customer Distribution](business_insights/customer_distribution.png)",
        "",
        "![Revenue Contribution](business_insights/revenue_contribution.png)",
        "",
        "![Average Customer Value](business_insights/average_customer_value.png)",
        "",
        "## 7. Conclusion",
        "",
        "The RFM analysis identifies distinct customer groups with different "
        "purchasing patterns and business value. Segment-specific retention and "
        "engagement strategies can help the business prioritize its marketing "
        "efforts. Their effectiveness should be assessed using measured campaign "
        "results rather than assumed outcomes.",
        "",
    ])

    output = REPORT_DIR / "business_insights.md"
    output.write_text("\n".join(lines), encoding="utf-8")


def write_retention_strategy(metrics):
    """Generate a separate actionable retention strategy document."""

    lines = [
        "# Customer Retention Strategy",
        "",
        "## Objective",
        "",
        "Define segment-specific actions using the existing RFM segmentation.",
        "",
        "| Segment | Business Objective | Recommended Actions | Suggested KPI |",
        "|---|---|---|---|",
    ]

    kpis = {
        "Champions": "Repeat purchase rate, referral participation, revenue per customer",
        "Loyal High-Value": "Reactivation rate, repeat purchase rate, recovered revenue",
        "Recent Customers": "Second-purchase rate, time to second purchase",
        "At-Risk / Hibernating": "Reactivation rate, campaign conversion, campaign ROI",
    }

    for segment in SEGMENT_ORDER:
        recommendation = RECOMMENDATIONS[segment]
        lines.append(
            f"| {segment} "
            f"| {recommendation['objective']} "
            f"| {recommendation['strategy']} "
            f"| {kpis[segment]} |"
        )

    lines.extend([
        "",
        "## Campaign Measurement",
        "",
        "- Establish a baseline before each campaign.",
        "- Compare campaign outcomes with an appropriate control group where possible.",
        "- Track incremental revenue, conversion and campaign costs.",
        "- Avoid excessive discounts where they reduce profitability.",
        "- Review segment movement regularly using consistently defined RFM snapshots.",
        "",
        "## Limitations",
        "",
        "These recommendations are proposed strategies, not experimentally proven "
        "results. Test campaigns and measure their actual performance before "
        "scaling them.",
        "",
    ])

    output = REPORT_DIR / "customer_retention_strategy.md"
    output.write_text("\n".join(lines), encoding="utf-8")


def main():
    print("Loading project datasets...")
    customers, transactions = load_data()

    print("Calculating segment-level business metrics...")
    metrics, transaction_data = calculate_insights(customers, transactions)

    metrics.to_csv(
        REPORT_DIR / "business_insights_metrics.csv",
        index=True,
    )

    transaction_data.groupby("Segment").agg(
        Transaction_Lines=("Invoice", "size"),
        Unique_Orders=("Invoice", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Revenue=("TotalPrice", "sum"),
    ).reindex(SEGMENT_ORDER).to_csv(
        REPORT_DIR / "business_insights_transaction_summary.csv"
    )

    print("Creating charts...")
    create_charts(metrics)

    print("Writing business insights report...")
    write_report(metrics, customers, transactions)

    print("Writing customer retention strategy...")
    write_retention_strategy(metrics)

    print("\nBUSINESS INSIGHTS COMPLETED")
    print("-" * 60)
    print("Customers:", customers["CustomerID"].nunique())
    print("Transactions:", len(transactions))
    print("Unique orders:", transactions["Invoice"].nunique())
    print("\nSegment metrics:")
    print(metrics.round(2).to_string())

    print("\nGenerated files:")
    print("reports/business_insights.md")
    print("reports/business_insights_metrics.csv")
    print("reports/business_insights_transaction_summary.csv")
    print("reports/customer_retention_strategy.md")
    print("reports/business_insights/")


if __name__ == "__main__":
    main()
