from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]

SEGMENTS_FILE = ROOT / "data/processed/customer_rfm_features.csv"
SEGMENT_PROFILE_FILE = ROOT / "reports/business_insights_metrics.csv"
CHURN_FILE = ROOT / "data/processed/historical_churn_dataset.csv"
PREDICTIONS_FILE = ROOT / "reports/customer_churn_predictions.csv"
MODEL_METADATA_FILE = ROOT / "models/model_metadata.json"

st.set_page_config(
    page_title="Retail Customer Analytics",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_csv(path):
    if not path.exists():
        return None
    return pd.read_csv(path)


segments = load_csv(SEGMENTS_FILE)
profile = load_csv(SEGMENT_PROFILE_FILE)
churn = load_csv(CHURN_FILE)
predictions = load_csv(PREDICTIONS_FILE)

if MODEL_METADATA_FILE.exists():
    model_metadata = json.loads(MODEL_METADATA_FILE.read_text(encoding="utf-8"))
    test_metrics = model_metadata.get("test_metrics", {})
else:
    model_metadata = {}
    test_metrics = {}


def money(value):
    return f"{value:,.2f}"


st.title("Retail & E-commerce Customer Analytics")
st.caption(
    "Customer segmentation, historical churn analysis and model predictions"
)

if segments is None or profile is None:
    st.error("Required segmentation files are missing. Run the RFM and business-insights scripts first.")
    st.stop()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

segment_options = sorted(segments["Segment"].dropna().unique().tolist())
selected_segments = st.sidebar.multiselect(
    "Customer segments",
    segment_options,
    default=segment_options,
)

filtered_segments = segments[
    segments["Segment"].isin(selected_segments)
].copy()

tabs = st.tabs([
    "Executive Overview",
    "Customer Segmentation",
    "Churn Analysis",
    "Customer Details",
])

# --------------------------------------------------
# 1. Executive Overview
# --------------------------------------------------
with tabs[0]:
    st.header("Executive Overview")

    total_customers = segments["CustomerID"].nunique()
    total_revenue = segments["Monetary"].sum()
    total_orders = int(profile["Unique_Orders"].sum())
    avg_customer_value = total_revenue / total_customers

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Identified customers", f"{total_customers:,}")
    c2.metric("RFM customer monetary value", money(total_revenue))
    c3.metric("Unique orders", f"{total_orders:,}")
    c4.metric("Average customer monetary value", money(avg_customer_value))

    st.info(
        "Revenue and monetary values use the cleaned customer-linked transaction "
        "data. Currency units have not been independently verified."
    )

    left, right = st.columns(2)

    with left:
        fig = px.pie(
            profile,
            names="Segment",
            values="Customers",
            title="Customer Distribution by Segment",
            hole=0.35,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            profile,
            x="Segment",
            y="Total_Revenue",
            title="Revenue Contribution by Segment",
            text_auto=".2s",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Segment Performance")
    display_columns = [
        "Segment",
        "Customers",
        "Customer_Percentage",
        "Total_Revenue",
        "Revenue_Share_Percentage",
        "Avg_Recency",
        "Avg_Frequency",
        "Avg_Monetary",
    ]
    st.dataframe(
        profile[display_columns].round(2),
        use_container_width=True,
        hide_index=True,
    )

# --------------------------------------------------
# 2. Customer Segmentation
# --------------------------------------------------
with tabs[1]:
    st.header("Customer Segmentation")

    if filtered_segments.empty:
        st.warning("Select at least one segment from the sidebar.")
    else:
        count = filtered_segments["CustomerID"].nunique()
        revenue = filtered_segments["Monetary"].sum()

        c1, c2, c3 = st.columns(3)
        c1.metric("Filtered customers", f"{count:,}")
        c2.metric("Filtered monetary value", money(revenue))
        c3.metric(
            "Average recency",
            f"{filtered_segments['Recency'].mean():.1f} days",
        )

        left, right = st.columns(2)

        with left:
            fig = px.box(
                filtered_segments,
                x="Segment",
                y="Recency",
                color="Segment",
                title="Recency Distribution",
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.scatter(
                filtered_segments,
                x="Frequency",
                y="Monetary",
                color="Segment",
                hover_data=["CustomerID", "Recency"],
                title="Customer Frequency vs Monetary Value",
                log_y=True,
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Segment Profile")
        st.dataframe(
            profile[profile["Segment"].isin(selected_segments)].round(2),
            use_container_width=True,
            hide_index=True,
        )

        recommendations = {
            "Champions": "Protect loyalty with VIP rewards, early access and referral benefits.",
            "Loyal High-Value": "Test personalized win-back campaigns and relevant product recommendations.",
            "Recent Customers": "Encourage second purchases through welcome campaigns and targeted recommendations.",
            "At-Risk / Hibernating": "Test cost-effective re-engagement and feedback campaigns.",
        }

        st.subheader("Recommended Actions")
        for segment in selected_segments:
            st.markdown(f"**{segment}:** {recommendations.get(segment, 'Review segment behaviour.')}")

# --------------------------------------------------
# 3. Churn Analysis
# --------------------------------------------------
with tabs[2]:
    st.header("Historical Churn Analysis")

    if churn is None:
        st.warning("Historical churn dataset is not available.")
    else:
        churn_rate = churn["Churn"].mean() * 100
        churned = int(churn["Churn"].sum())
        active = int((churn["Churn"] == 0).sum())

        c1, c2, c3 = st.columns(3)
        c1.metric("Historical cohort", f"{len(churn):,}")
        c2.metric("Churned customers", f"{churned:,}")
        c3.metric("90-day inactivity rate", f"{churn_rate:.2f}%")

        st.caption(
            "Churn means no purchase during the defined 90-day observation window. "
            "It is an inactivity proxy, not proof of permanent customer loss."
        )

        churn_summary = pd.DataFrame({
            "Status": ["Active", "Churned"],
            "Customers": [active, churned],
        })

        left, right = st.columns(2)

        with left:
            fig = px.pie(
                churn_summary,
                names="Status",
                values="Customers",
                title="Historical Churn Distribution",
                hole=0.35,
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            fig = px.histogram(
                churn,
                x="Recency",
                color="Churn",
                barmode="overlay",
                nbins=30,
                title="Recency Distribution by Churn Label",
                labels={"Churn": "Churn label"},
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Churn Model Test Performance")
        st.write(
            "Selected model: Logistic Regression. "
            "The held-out test metrics are reported below."
        )

        metric_labels = [
            ("Accuracy", "Accuracy"),
            ("Precision", "Precision"),
            ("Recall", "Recall"),
            ("F1-score", "F1_Score"),
            ("ROC-AUC", "ROC_AUC"),
        ]
        metric_data = pd.DataFrame([
            {"Metric": label, "Score": test_metrics[key]}
            for label, key in metric_labels
            if key in test_metrics
        ])

        if metric_data.empty:
            st.warning("Saved model test metrics are unavailable. Run the churn training workflow.")
        else:
            fig = px.bar(
                metric_data,
                x="Metric",
                y="Score",
                title="Selected Model – Test Metrics",
                text_auto=".3f",
                range_y=[0, 1],
            )
            st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Metrics are from the saved model evaluation report, not calculated "
            "from the sample prediction CSV."
        )

# --------------------------------------------------
# 4. Customer Details
# --------------------------------------------------
with tabs[3]:
    st.header("Customer Details")

    detail = filtered_segments.copy()

    if predictions is not None:
        detail = detail.merge(
            predictions,
            on="CustomerID",
            how="left",
            validate="one_to_one",
        )
        st.caption(
            "Churn scores appear only for customers in the current sample "
            "prediction file. Blank scores mean no prediction is available."
        )
    else:
        detail["Churn_Probability"] = pd.NA
        detail["Risk_Category"] = pd.NA

    search_id = st.text_input("Search Customer ID")

    if search_id.strip():
        try:
            customer_id = int(search_id)
            detail = detail[detail["CustomerID"] == customer_id]
        except ValueError:
            st.warning("Enter a valid numeric Customer ID.")

    detail_columns = [
        "CustomerID",
        "Segment",
        "Recency",
        "Frequency",
        "Monetary",
        "Churn_Probability",
        "Risk_Category",
    ]

    st.dataframe(
        detail[detail_columns].round(3),
        use_container_width=True,
        hide_index=True,
    )

    csv = detail[detail_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download filtered customer data",
        data=csv,
        file_name="filtered_customer_analytics.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "Retail & E-commerce Customer Segmentation and Churn Prediction | "
    "Axlero Group 3 | Academic project"
)
