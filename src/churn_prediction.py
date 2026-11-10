from pathlib import Path
import json
import warnings

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data/processed/historical_churn_dataset.csv"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

FEATURES = [
    "Recency",
    "Frequency",
    "Monetary",
    "Total_Quantity",
    "Unique_Products",
    "Average_Order_Value",
]
TARGET = "Churn"
RANDOM_STATE = 42


def evaluate_model(name, estimator, X_test, y_test):
    predictions = estimator.predict(X_test)
    probabilities = estimator.predict_proba(X_test)[:, 1]

    return {
        "Model": name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions, zero_division=0),
        "Recall": recall_score(y_test, predictions, zero_division=0),
        "F1_Score": f1_score(y_test, predictions, zero_division=0),
        "ROC_AUC": roc_auc_score(y_test, probabilities),
        "Confusion_Matrix_TN_FP_FN_TP": confusion_matrix(
            y_test, predictions
        ).ravel().tolist(),
    }


def main():
    warnings.filterwarnings("ignore", category=UserWarning)

    for folder in [MODEL_DIR, REPORT_DIR, FIGURE_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Historical churn dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    required = FEATURES + [TARGET, "CustomerID", "Future_Orders_90d"]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df["CustomerID"].duplicated().any():
        raise ValueError("Duplicate CustomerID values found.")

    if df[FEATURES + [TARGET]].isna().any().any():
        raise ValueError("Missing values found in features or target.")

    if not df[TARGET].isin([0, 1]).all():
        raise ValueError("Churn target must contain only 0 and 1.")

    if (df[FEATURES] < 0).any().any():
        raise ValueError("Negative values found in non-negative features.")

    if not np.isfinite(df[FEATURES].to_numpy(dtype=float)).all():
        raise ValueError("Infinite or non-finite feature values found.")

    # Future_Orders_90d is deliberately excluded to prevent target leakage.
    X = df[FEATURES].astype(float)
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    # Logistic Regression: log transformation reduces feature skew.
    logistic_pipeline = Pipeline([
        (
            "log_transform",
            FunctionTransformer(
                np.log1p,
                validate=False,
                feature_names_out="one-to-one",
            ),
        ),
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                max_iter=3000,
                random_state=RANDOM_STATE,
            ),
        ),
    ])

    logistic_search = GridSearchCV(
        estimator=logistic_pipeline,
        param_grid={
            "classifier__C": [0.1, 1.0, 10.0],
            "classifier__class_weight": [None, "balanced"],
        },
        scoring="roc_auc",
        cv=cv,
        n_jobs=-1,
        refit=True,
    )

    # Random Forest: tree models do not require feature scaling.
    forest_pipeline = Pipeline([
        (
            "classifier",
            RandomForestClassifier(
                random_state=RANDOM_STATE,
                n_jobs=1,
            ),
        )
    ])

    forest_search = GridSearchCV(
        estimator=forest_pipeline,
        param_grid={
            "classifier__n_estimators": [300, 500],
            "classifier__max_depth": [None, 12],
            "classifier__min_samples_leaf": [1, 3],
            "classifier__class_weight": [None, "balanced"],
        },
        scoring="roc_auc",
        cv=cv,
        n_jobs=-1,
        refit=True,
    )

    searches = {
        "Logistic Regression": logistic_search,
        "Random Forest": forest_search,
    }

    results = []
    fitted_models = {}

    print("\nTraining and tuning candidate models...")
    print(f"Training customers: {len(X_train):,}")
    print(f"Test customers: {len(X_test):,}")

    for name, search in searches.items():
        print(f"\nRunning {name}...")
        search.fit(X_train, y_train)

        fitted_models[name] = search.best_estimator_

        result = evaluate_model(
            name,
            search.best_estimator_,
            X_test,
            y_test,
        )
        result["CV_ROC_AUC_Mean"] = search.best_score_
        result["Best_Parameters"] = json.dumps(
            search.best_params_,
            default=str,
        )
        results.append(result)

        print(f"Best CV ROC-AUC: {search.best_score_:.4f}")
        print(f"Test ROC-AUC: {result['ROC_AUC']:.4f}")
        print(f"Test F1-score: {result['F1_Score']:.4f}")

    # Select using training cross-validation only, not test performance.
    best_name = max(
        searches,
        key=lambda name: searches[name].best_score_,
    )
    best_search = searches[best_name]
    best_model = best_search.best_estimator_

    comparison = pd.DataFrame(results).sort_values(
        "CV_ROC_AUC_Mean",
        ascending=False,
    )

    comparison_file = REPORT_DIR / "churn_model_comparison.csv"
    comparison.to_csv(comparison_file, index=False)

    model_file = MODEL_DIR / "churn_model.pkl"
    joblib.dump(best_model, model_file)

    best_result = next(
        row for row in results if row["Model"] == best_name
    )

    metadata = {
        "project": "Retail & E-commerce Customer Churn Prediction",
        "selected_model": best_name,
        "selection_metric": "Mean 3-fold training cross-validation ROC-AUC",
        "cross_validation_roc_auc": float(best_search.best_score_),
        "best_parameters": best_search.best_params_,
        "features": FEATURES,
        "target": TARGET,
        "excluded_columns": [
            "CustomerID",
            "Future_Orders_90d",
        ],
        "random_state": RANDOM_STATE,
        "test_size": 0.20,
        "training_customers": int(len(X_train)),
        "test_customers": int(len(X_test)),
        "test_metrics": {
            key: float(best_result[key])
            for key in [
                "Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"
            ]
        },
        "target_definition": (
            "No purchase during the 90-day observation window"
        ),
        "warning": (
            "Churn is a 90-day inactivity proxy, not permanent customer loss. "
            "Evaluation is based on one historical time cohort and does not "
            "guarantee future performance."
        ),
    }

    metadata_file = MODEL_DIR / "model_metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=4, default=str))

    # Final selected model test-set predictions.
    predictions = best_model.predict(X_test)
    probabilities = best_model.predict_proba(X_test)[:, 1]

    cm = confusion_matrix(y_test, predictions, labels=[0, 1])

    fig, ax = plt.subplots(figsize=(6, 5))
    image = ax.imshow(cm)
    ax.set_title(f"Confusion Matrix - {best_name}")
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Actual label")
    ax.set_xticks([0, 1], ["Active (0)", "Churn (1)"])
    ax.set_yticks([0, 1], ["Active (0)", "Churn (1)"])

    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")

    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "churn_confusion_matrix.png", dpi=160)
    plt.close(fig)

    fpr, tpr, _ = roc_curve(y_test, probabilities)
    auc_value = roc_auc_score(y_test, probabilities)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, label=f"{best_name} (AUC = {auc_value:.3f})")
    ax.plot([0, 1], [0, 1], linestyle="--", label="Random baseline")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Churn Model ROC Curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "churn_roc_curve.png", dpi=160)
    plt.close(fig)

    report = [
        "# Churn Model Training and Evaluation",
        "",
        "## 1. Dataset",
        f"- Customer records: {len(df):,}",
        f"- Training records: {len(X_train):,}",
        f"- Test records: {len(X_test):,}",
        f"- Churned customers: {int(y.sum()):,}",
        f"- Active customers: {int((y == 0).sum()):,}",
        f"- Churn rate: {y.mean() * 100:.2f}%",
        "",
        "## 2. Features",
        *[f"- {feature}" for feature in FEATURES],
        "",
        "`Future_Orders_90d` and `CustomerID` were excluded from model inputs.",
        "",
        "## 3. Modelling methodology",
        "- Stratified 80/20 train-test split.",
        "- Random state: 42.",
        "- Three-fold stratified cross-validation on training data.",
        "- Hyperparameter tuning using training data only.",
        "- Candidate models: Logistic Regression and Random Forest.",
        "- Selection metric: mean cross-validation ROC-AUC.",
        "",
        "## 4. Model comparison",
        comparison[
            ["Model", "CV_ROC_AUC_Mean", "Accuracy", "Precision",
             "Recall", "F1_Score", "ROC_AUC"]
        ].to_markdown(index=False),
        "",
        "## 5. Selected model",
        f"- Model: {best_name}",
        f"- Training CV ROC-AUC: {best_search.best_score_:.4f}",
        f"- Test ROC-AUC: {auc_value:.4f}",
        f"- Test accuracy: {accuracy_score(y_test, predictions):.4f}",
        f"- Test precision: {precision_score(y_test, predictions, zero_division=0):.4f}",
        f"- Test recall: {recall_score(y_test, predictions, zero_division=0):.4f}",
        f"- Test F1-score: {f1_score(y_test, predictions, zero_division=0):.4f}",
        "",
        "### Classification report",
        "```text",
        classification_report(
            y_test,
            predictions,
            target_names=["Active", "Churn"],
            zero_division=0,
        ),
        "```",
        "",
        "### Confusion matrix",
        "Rows are actual classes [Active, Churn]; columns are predicted classes.",
        f"- Matrix: {cm.tolist()}",
        "- Figure: reports/figures/churn_confusion_matrix.png",
        "- ROC figure: reports/figures/churn_roc_curve.png",
        "",
        "## 6. Saved model files",
        "- models/churn_model.pkl",
        "- models/model_metadata.json",
        "- reports/churn_model_comparison.csv",
        "",
        "## 7. Limitations",
        "- Churn is defined as 90-day inactivity, not permanent churn.",
        "- Results are based on one historical cohort and one holdout split.",
        "- Performance may change for other time periods or customer populations.",
        "- The holdout evaluation does not establish causal effects of marketing actions.",
        "",
        "## 8. Conclusion",
        f"The selected candidate was {best_name}, chosen using training "
        "cross-validation ROC-AUC. Its final metrics were measured on the "
        "held-out test set. Further temporal validation is recommended "
        "before production use.",
    ]

    report_file = REPORT_DIR / "churn_model_evaluation.md"
    report_file.write_text("\n".join(report) + "\n")

    print("\n========== MODEL COMPARISON ==========")
    print(comparison[
        ["Model", "CV_ROC_AUC_Mean", "Accuracy", "Precision",
         "Recall", "F1_Score", "ROC_AUC"]
    ].to_string(index=False))

    print(f"\nSelected model: {best_name}")
    print(f"Saved model: {model_file}")
    print(f"Metadata: {metadata_file}")
    print(f"Comparison: {comparison_file}")
    print(f"Evaluation report: {report_file}")
    print("\nTraining completed.")


if __name__ == "__main__":
    main()
