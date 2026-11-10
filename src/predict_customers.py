from pathlib import Path
import argparse
import json

import joblib
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL_FILE = ROOT / "models" / "churn_model.pkl"
METADATA_FILE = ROOT / "models" / "model_metadata.json"

FEATURES = [
    "Recency",
    "Frequency",
    "Monetary",
    "Total_Quantity",
    "Unique_Products",
    "Average_Order_Value",
]


def load_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_FILE}")

    if not METADATA_FILE.exists():
        raise FileNotFoundError(f"Metadata not found: {METADATA_FILE}")

    with open(METADATA_FILE, "r") as file:
        metadata = json.load(file)

    if metadata.get("features") != FEATURES:
        raise ValueError("Model metadata features do not match expected features.")

    model = joblib.load(MODEL_FILE)
    return model, metadata


def prepare_input(input_file):
    input_path = Path(input_file)

    if not input_path.is_absolute():
        input_path = ROOT / input_path

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    data = pd.read_csv(input_path)

    required = ["CustomerID"] + FEATURES
    missing = sorted(set(required) - set(data.columns))

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    leakage_columns = {"Churn", "Future_Orders_90d"}
    present_leakage = leakage_columns.intersection(data.columns)

    if present_leakage:
        raise ValueError(
            f"Remove target/future-information columns from input: "
            f"{sorted(present_leakage)}"
        )

    data = data[required].copy()

    if data["CustomerID"].isna().any():
        raise ValueError("CustomerID contains missing values.")

    if data["CustomerID"].duplicated().any():
        raise ValueError("Duplicate CustomerID values found.")

    for column in required:
        data[column] = pd.to_numeric(data[column], errors="raise")

    if not np.isfinite(data[required].to_numpy(dtype=float)).all():
        raise ValueError("Input contains non-finite numeric values.")

    if (data[FEATURES] < 0).any().any():
        raise ValueError("Model features must be non-negative.")

    return data


def predict(input_file, output_file):
    model, metadata = load_model()
    data = prepare_input(input_file)

    probabilities = model.predict_proba(data[FEATURES])[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    results = pd.DataFrame({
        "CustomerID": data["CustomerID"],
        "Churn_Probability": probabilities,
        "Predicted_Churn": predictions,
    })

    # Operational bands for prioritization, not calibrated business thresholds.
    results["Risk_Category"] = pd.cut(
        results["Churn_Probability"],
        bins=[-0.001, 0.40, 0.70, 1.001],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    ).astype(str)

    output_path = Path(output_file)

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    print("Customer churn prediction completed.")
    print(f"Model: {metadata['selected_model']}")
    print(f"Customers scored: {len(results)}")
    print(f"Output: {output_path}")
    print("\nRisk category counts:")
    print(results["Risk_Category"].value_counts().to_string())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Score customers using the saved churn prediction model."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input CSV containing CustomerID and the six model features.",
    )
    parser.add_argument(
        "--output",
        default="reports/customer_churn_predictions.csv",
        help="Output CSV path.",
    )

    args = parser.parse_args()
    predict(args.input, args.output)
