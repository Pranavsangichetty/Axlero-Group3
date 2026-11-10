from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data/processed/historical_churn_dataset.csv"
MODEL_FILE = ROOT / "models/churn_model.pkl"
METADATA_FILE = ROOT / "models/model_metadata.json"
COMPARISON_FILE = ROOT / "reports/churn_model_comparison.csv"
REPORT_FILE = ROOT / "reports/churn_model_evaluation.md"
FIGURES = [
    ROOT / "reports/figures/churn_confusion_matrix.png",
    ROOT / "reports/figures/churn_roc_curve.png",
]

FEATURES = [
    "Recency", "Frequency", "Monetary",
    "Total_Quantity", "Unique_Products", "Average_Order_Value"
]
FORBIDDEN = ["CustomerID", "Future_Orders_90d"]

checks = []

def check(name, condition, detail=""):
    checks.append({
        "Check": name,
        "Result": "PASS" if condition else "FAIL",
        "Details": detail
    })

def close(a, b, tol=1e-8):
    return bool(np.isclose(float(a), float(b), atol=tol, rtol=tol))

print("Loading dataset, model and metadata...")

df = pd.read_csv(DATA_FILE)
model = joblib.load(MODEL_FILE)
metadata = json.loads(METADATA_FILE.read_text())

check("Dataset exists", DATA_FILE.exists())
check("Saved model exists", MODEL_FILE.exists())
check("Metadata exists", METADATA_FILE.exists())
check("Evaluation report exists", REPORT_FILE.exists())
check("Comparison CSV exists", COMPARISON_FILE.exists())
check("Both evaluation figures exist", all(p.exists() for p in FIGURES))

check(
    "Required feature columns exist",
    all(c in df.columns for c in FEATURES),
    ", ".join(FEATURES)
)
check("Target column exists", "Churn" in df.columns)
check("No missing values in model data",
      not df[FEATURES + ["Churn"]].isna().any().any())
check("Customer IDs are unique",
      "CustomerID" in df.columns and df["CustomerID"].is_unique)
check("Target contains only 0 and 1",
      set(df["Churn"].unique()).issubset({0, 1}))
check("No negative model feature values",
      bool((df[FEATURES] >= 0).all().all()))
check("No infinite model feature values",
      bool(np.isfinite(df[FEATURES].to_numpy(dtype=float)).all()))

metadata_features = metadata.get("features", [])
metadata_excluded = metadata.get("excluded_columns", [])

check("Metadata feature list matches",
      metadata_features == FEATURES)
check("Leakage/customer identifiers excluded in metadata",
      all(c in metadata_excluded for c in FORBIDDEN))
check("No forbidden columns in model feature list",
      not any(c in metadata_features for c in FORBIDDEN))

X = df[FEATURES]
y = df["Churn"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=metadata.get("test_size", 0.2),
    random_state=metadata.get("random_state", 42),
    stratify=y
)

check("Recreated test split has expected size",
      len(X_test) == metadata.get("test_customers"))
check("Recreated training split has expected size",
      len(X_train) == metadata.get("training_customers"))

print("Running predictions using the saved model...")
pred = model.predict(X_test)
prob = model.predict_proba(X_test)[:, 1]

check("Model prediction output has correct length",
      len(pred) == len(y_test))
check("Predictions contain only 0 and 1",
      set(np.unique(pred)).issubset({0, 1}))
check("Predicted probabilities are valid",
      bool(np.isfinite(prob).all() and
           (prob >= 0).all() and (prob <= 1).all()))

metrics = {
    "Accuracy": accuracy_score(y_test, pred),
    "Precision": precision_score(y_test, pred, zero_division=0),
    "Recall": recall_score(y_test, pred, zero_division=0),
    "F1_Score": f1_score(y_test, pred, zero_division=0),
    "ROC_AUC": roc_auc_score(y_test, prob),
}
saved_metrics = metadata.get("test_metrics", {})

for metric, value in metrics.items():
    check(
        f"{metric} matches saved metadata",
        metric in saved_metrics and close(value, saved_metrics[metric]),
        f"Recomputed={value:.8f}; saved={saved_metrics.get(metric)}"
    )

cm = confusion_matrix(y_test, pred, labels=[0, 1])
saved_cm = [181, 101, 73, 190]
check(
    "Confusion matrix matches training report",
    cm.ravel().tolist() == saved_cm,
    f"Recomputed={cm.ravel().tolist()}; expected={saved_cm}"
)

comparison = pd.read_csv(COMPARISON_FILE)
check("Model comparison contains both candidates",
      set(comparison["Model"]) == {"Logistic Regression", "Random Forest"})

results = pd.DataFrame(checks)
output_file = ROOT / "reports/churn_model_validation_results.csv"
results.to_csv(output_file, index=False)

passed = int((results["Result"] == "PASS").sum())
failed = int((results["Result"] == "FAIL").sum())

report = [
    "# Independent Churn Model Validation",
    "",
    f"- Dataset rows: {len(df):,}",
    f"- Training customers: {len(X_train):,}",
    f"- Test customers: {len(X_test):,}",
    f"- Saved model: `{MODEL_FILE.relative_to(ROOT)}`",
    f"- Checks passed: {passed}",
    f"- Checks failed: {failed}",
    "",
    "## Recomputed held-out test metrics",
    "",
    "| Metric | Recomputed value |",
    "|---|---:|",
]
for name, value in metrics.items():
    report.append(f"| {name} | {value:.6f} |")

report += [
    "",
    "## Confusion matrix",
    "",
    f"- Actual rows [Active, Churn], predicted columns [Active, Churn]",
    f"- Matrix: {cm.tolist()}",
    "",
    "## Validation checks",
    "",
    results.to_markdown(index=False),
    "",
    "## Conclusion",
    "",
    "All checks passed." if failed == 0 else
    "Some checks failed. Review the results before committing."
]

(ROOT / "reports/churn_model_validation_report.md").write_text(
    "\n".join(report) + "\n"
)

print("\n========== VALIDATION SUMMARY ==========")
print(results.to_string(index=False))
print(f"\nPassed: {passed}")
print(f"Failed: {failed}")
print(f"Results: {output_file}")
print("Report: reports/churn_model_validation_report.md")

if failed:
    raise SystemExit("Validation failed. Review the report.")
else:
    print("\nIndependent model validation completed successfully.")
