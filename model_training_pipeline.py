"""Reusable feature engineering and chronological model-development helpers.

Target: no purchase in the 60 days after an observation date.
Feature lookback: 90 days.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

LOOKBACK_DAYS = 90
PREDICTION_DAYS = 60
RANDOM_STATE = 42

FEATURES = [
    "recency_days", "order_frequency", "total_quantity", "monetary_value",
    "unique_products", "transaction_lines", "average_order_value",
    "customer_tenure_days",
]


def prepare_transactions(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate required columns and retain positive, identified sales rows."""
    required = {"Invoice", "InvoiceDate", "CustomerID", "StockCode", "Quantity", "Price"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    tx = frame.copy()
    tx["InvoiceDate"] = pd.to_datetime(tx["InvoiceDate"], errors="coerce")
    for col in ["CustomerID", "Quantity", "Price"]:
        tx[col] = pd.to_numeric(tx[col], errors="coerce")
    if "Revenue" not in tx.columns:
        tx["Revenue"] = tx["Quantity"] * tx["Price"]
    tx["Revenue"] = pd.to_numeric(tx["Revenue"], errors="coerce")
    tx = tx.dropna(subset=[
        "InvoiceDate", "CustomerID", "Invoice", "StockCode",
        "Quantity", "Price", "Revenue"
    ])
    tx = tx[
        (tx["CustomerID"] > 0) & (tx["Quantity"] > 0) &
        (tx["Price"] > 0) & (tx["Revenue"] > 0)
    ].copy()
    tx["CustomerID"] = tx["CustomerID"].astype("int64")
    tx["Invoice"] = tx["Invoice"].astype(str)
    return tx.sort_values("InvoiceDate").reset_index(drop=True)


def build_customer_snapshots(
    transactions: pd.DataFrame,
    lookback_days: int = LOOKBACK_DAYS,
    prediction_days: int = PREDICTION_DAYS,
) -> pd.DataFrame:
    """Build month-end customer features and the future no-purchase label."""
    tx = prepare_transactions(transactions)
    first_date = tx["InvoiceDate"].min().normalize()
    last_date = tx["InvoiceDate"].max().normalize()
    dates = pd.date_range(
        first_date + pd.offsets.MonthEnd(0),
        last_date - pd.Timedelta(days=prediction_days),
        freq="ME",
    )
    snapshots = []
    for date in dates:
        hist = tx[
            (tx["InvoiceDate"] > date - pd.Timedelta(days=lookback_days)) &
            (tx["InvoiceDate"] <= date)
        ]
        future = tx[
            (tx["InvoiceDate"] > date) &
            (tx["InvoiceDate"] <= date + pd.Timedelta(days=prediction_days))
        ]
        if hist.empty:
            continue
        future_buyers = set(future["CustomerID"].unique())
        frame = hist.groupby("CustomerID").agg(
            recency_days=("InvoiceDate", lambda x: (date - x.max()).days),
            order_frequency=("Invoice", "nunique"),
            total_quantity=("Quantity", "sum"),
            monetary_value=("Revenue", "sum"),
            unique_products=("StockCode", "nunique"),
            transaction_lines=("Invoice", "size"),
            first_purchase=("InvoiceDate", "min"),
            last_purchase=("InvoiceDate", "max"),
        ).reset_index()
        invoice_counts = hist.groupby("CustomerID")["Invoice"].nunique()
        frame["average_order_value"] = (
            frame.set_index("CustomerID")["monetary_value"] / invoice_counts
        ).reindex(frame["CustomerID"]).to_numpy()
        frame["customer_tenure_days"] = (
            frame["last_purchase"] - frame["first_purchase"]
        ).dt.days
        frame["observation_date"] = date
        frame["churn_risk"] = (~frame["CustomerID"].isin(future_buyers)).astype(int)
        snapshots.append(frame)
    if not snapshots:
        raise ValueError("No snapshots could be built. Check the dataset date range.")
    return pd.concat(snapshots, ignore_index=True)


def chronological_split(data: pd.DataFrame):
    """Return 60/20/20 chronological train, validation, and test frames."""
    dates = np.array(sorted(data["observation_date"].unique()))
    if len(dates) < 5:
        raise ValueError("At least five snapshot dates are recommended.")
    train_end = max(1, int(len(dates) * 0.60))
    valid_end = min(max(train_end + 1, int(len(dates) * 0.80)), len(dates) - 1)
    if train_end >= valid_end or valid_end >= len(dates):
        raise ValueError("Not enough dates for chronological split.")
    train_dates, valid_dates, test_dates = dates[:train_end], dates[train_end:valid_end], dates[valid_end:]
    return (
        data[data.observation_date.isin(train_dates)].copy(),
        data[data.observation_date.isin(valid_dates)].copy(),
        data[data.observation_date.isin(test_dates)].copy(),
    )


def candidate_models():
    """Return model pipelines to compare on validation data."""
    return {
        "Logistic Regression": Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(
                max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE
            )),
        ]),
        "Random Forest": Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", RandomForestClassifier(
                n_estimators=300, min_samples_leaf=3,
                class_weight="balanced_subsample", random_state=RANDOM_STATE,
                n_jobs=-1,
            )),
        ]),
        "Extra Trees": Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", ExtraTreesClassifier(
                n_estimators=300, min_samples_leaf=3,
                class_weight="balanced", random_state=RANDOM_STATE,
                n_jobs=-1,
            )),
        ]),
    }
