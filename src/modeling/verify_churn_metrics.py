"""Independently re-compute churn-model metrics and compare them with the report.

Usage
-----
    python src/modeling/verify_churn_metrics.py \
        --predictions data/processed/churn_predictions.csv \
        --reported reports/churn_metrics.csv

    python src/modeling/verify_churn_metrics.py --self-test

Expected input (change the names with the --*-col options)
-----------------------------------------------------------
Predictions file, one row per scored customer:
    y_true   actual label, 1 = churn (positive class), 0 = not churn
    y_score  predicted churn probability
    y_pred   (optional) predicted class; if missing, y_score >= --threshold
    model    (optional) model name, e.g. LogisticRegression / RandomForest
    split    (optional) train / test; only --split rows (default 'test') are used

Reported metrics file, one row per model:
    model, precision, recall, f1, roc_auc  (optional: accuracy, tn, fp, fn, tp)

The tool checks that the reported numbers equal the numbers re-computed from
the saved predictions, prints the confusion matrix and class balance, and
tests the PRD target (ROC-AUC >= 0.75). It cannot prove that the predictions
themselves are free of data leakage; it only raises warnings.
"""

import argparse
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)

PRD_MIN_AUC = 0.75
SUSPICIOUS_AUC = 0.98
TOLERANCE = 0.005  # reports are usually rounded to 2-3 decimals


def recompute(frame, threshold):
    """Return the metrics, confusion matrix and class balance for one model."""
    y_true = frame["y_true"].astype(int)
    y_pred = (frame["y_pred"].astype(int) if "y_pred" in frame
              else (frame["y_score"] >= threshold).astype(int))
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    metrics = {
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "accuracy": accuracy_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, frame["y_score"]),
        "tn": tn, "fp": fp, "fn": fn, "tp": tp,
    }
    return metrics, y_true.mean(), len(frame)


def verify(predictions, reported, threshold=0.5, split="test", cols=None):
    cols = cols or {}
    predictions = predictions.rename(columns={v: k for k, v in cols.items()})
    needed = {"y_true", "y_score"} - set(predictions.columns)
    if needed:
        raise ValueError(f"Predictions file is missing columns: {sorted(needed)}")
    if "split" in predictions:
        predictions = predictions[predictions["split"] == split]
        if predictions.empty:
            raise ValueError(f"No rows with split == '{split}'")
    if "model" not in predictions:
        predictions = predictions.assign(model=reported["model"].iloc[0])

    rows, notes = [], []
    for model, frame in predictions.groupby("model"):
        actual, prevalence, n = recompute(frame, threshold)
        notes.append(f"{model}: n={n:,}, churn (positive) rate={prevalence:.1%}, "
                     f"TN={actual['tn']} FP={actual['fp']} FN={actual['fn']} "
                     f"TP={actual['tp']}")
        claimed = reported[reported["model"] == model]
        if claimed.empty:
            rows.append((model, "model missing from reported file", np.nan, np.nan, "FAIL"))
            continue
        claimed = claimed.iloc[0]
        for metric in ["precision", "recall", "f1", "roc_auc", "accuracy",
                       "tn", "fp", "fn", "tp"]:
            if metric not in claimed or pd.isna(claimed[metric]):
                continue
            tol = 0 if metric in ("tn", "fp", "fn", "tp") else TOLERANCE
            ok = abs(float(claimed[metric]) - float(actual[metric])) <= tol
            rows.append((model, metric, claimed[metric], actual[metric],
                         "PASS" if ok else "FAIL"))
        auc = actual["roc_auc"]
        rows.append((model, "PRD ROC-AUC >= 0.75", PRD_MIN_AUC, auc,
                     "PASS" if auc >= PRD_MIN_AUC else "FAIL"))
        if auc >= SUSPICIOUS_AUC:
            rows.append((model, "possible leakage (AUC too high)", SUSPICIOUS_AUC,
                         auc, "WARN"))
        if prevalence < 0.1 or prevalence > 0.9:
            rows.append((model, "severe class imbalance", "0.1-0.9", prevalence,
                         "WARN"))
    result = pd.DataFrame(rows, columns=["Model", "Metric", "Reported",
                                         "Recomputed", "Status"])
    return result, notes


def self_test():
    """Prove the tool works on synthetic data (these are NOT project results)."""
    rng = np.random.default_rng(0)
    n = 2000
    y_true = rng.binomial(1, 0.3, n)
    y_score = np.clip(0.3 + 0.35 * (y_true - 0.3) + rng.normal(0, 0.2, n), 0, 1)
    frame = pd.DataFrame({"y_true": y_true, "y_score": y_score,
                          "model": "SyntheticModel"})
    truth, _, _ = recompute(frame, 0.5)
    good = pd.DataFrame([{"model": "SyntheticModel",
                          **{k: round(truth[k], 3) for k in
                             ["precision", "recall", "f1", "roc_auc"]}}])
    bad = good.assign(precision=good["precision"] + 0.05)

    ok_result, _ = verify(frame, good)
    bad_result, _ = verify(frame, bad)
    print("SELF-TEST on synthetic data (not project results)")
    print(" correct report ->", sorted(ok_result["Status"].unique()))
    print(" tampered report ->", sorted(bad_result["Status"].unique()))
    passed = ("FAIL" not in set(ok_result["Status"])
              and "FAIL" in set(bad_result["Status"]))

    with tempfile.TemporaryDirectory() as folder:  # file round-trip
        path = Path(folder) / "p.csv"
        frame.to_csv(path, index=False)
        again, _ = verify(pd.read_csv(path), good)
        passed = passed and "FAIL" not in set(again["Status"])
    print("SELF-TEST", "PASSED" if passed else "FAILED")
    return 0 if passed else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--predictions")
    parser.add_argument("--reported")
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--split", default="test")
    parser.add_argument("--y-true-col", default="y_true")
    parser.add_argument("--y-score-col", default="y_score")
    parser.add_argument("--y-pred-col", default="y_pred")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not (args.predictions and args.reported):
        parser.error("--predictions and --reported are required (or use --self-test)")
    for path in (args.predictions, args.reported):
        if not Path(path).exists():
            print(f"BLOCKED: file not found: {path}")
            return 2

    cols = {"y_true": args.y_true_col, "y_score": args.y_score_col}
    predictions = pd.read_csv(args.predictions)
    if args.y_pred_col in predictions.columns:
        cols["y_pred"] = args.y_pred_col
    result, notes = verify(predictions, pd.read_csv(args.reported),
                           args.threshold, args.split, cols)
    print("\n".join(notes), "\n")
    print(result.to_string(index=False))
    return 1 if (result["Status"] == "FAIL").any() else 0


if __name__ == "__main__":
    sys.exit(main())
