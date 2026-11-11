"""Verify that the metrics reported in the documentation match the real outputs.

Run from anywhere:  python src/verify_reported_metrics.py

It re-computes the key numbers from the saved data (and from the raw dataset
when it is available) and compares them with:
  * the generated report files (reports/*.csv, data/processed/*.csv)
  * the numbers written in README.md and reports/week2_progress_report.md
  * the project success criteria in the Project Requirements Document (PRD)

Status values: PASS, FAIL, WARN (works, but needs attention), INFO (context),
SKIP (input not available), BLOCKED (nothing to verify yet, e.g. churn model).
The result table is saved to reports/qa_evidence/metric_verification.csv.
The exit code is 1 when at least one check is FAIL.
"""

import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "online_retail_II.csv"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
EVIDENCE = REPORTS / "qa_evidence"

README = (ROOT / "README.md").read_text(encoding="utf-8")
WEEK2 = (REPORTS / "week2_progress_report.md").read_text(encoding="utf-8")

results = []


def record(check_id, area, description, status, reported="", actual="", note=""):
    results.append({
        "ID": check_id, "Area": area, "Check": description, "Status": status,
        "Reported": reported, "Actual": actual, "Note": note,
    })


def compare(check_id, area, description, reported, actual, tol=0.0, note=""):
    """PASS when reported and actual agree within tol."""
    ok = abs(float(reported) - float(actual)) <= tol + 1e-12
    record(check_id, area, description, "PASS" if ok else "FAIL",
           reported, actual, note)


def number(text):
    return float(text.replace(",", "").replace("%", "").strip())


def table_rows(text, start, end):
    """Return the markdown table rows (as cell lists) between two markers."""
    block = text.split(start, 1)[1].split(end, 1)[0]
    rows = []
    for line in block.splitlines():
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
            rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows[1:]  # drop the header row


# --------------------------------------------------------------------------
# A. Data cleaning
# --------------------------------------------------------------------------
log = pd.read_csv(REPORTS / "cleaning_log.csv")
summary = pd.read_csv(REPORTS / "cleaning_summary.csv").set_index("Metric")["Value"]

readme_clean = {
    r[0]: number(r[1]) for r in table_rows(
        README, "**Cleaning results:**", "**EDA visualizations")
}
expected = {
    "Original transactions": log["Rows_Before"].iloc[0],
    "After exact duplicate removal": log["Rows_After"].iloc[0],
    "After cancellation exclusion": log["Rows_After"].iloc[1],
    "After positive quantity filtering": log["Rows_After"].iloc[2],
    "Final cleaned transactions": log["Rows_After"].iloc[-1],
    "Customer-linked transactions": summary["Customer transaction rows"],
    "Identified customers": summary["Unique customers"],
}
for i, (label, actual) in enumerate(expected.items(), start=1):
    compare(f"A{i}", "Cleaning", f"README '{label}' = cleaning output",
            readme_clean[label], actual)

arithmetic_ok = (
    (log["Rows_Before"] - log["Rows_After"] == log["Rows_Removed"]).all()
    and (log["Rows_After"].iloc[:-1].to_numpy()
         == log["Rows_Before"].iloc[1:].to_numpy()).all()
)
record("A8", "Cleaning", "Cleaning log is arithmetically consistent",
       "PASS" if arithmetic_ok else "FAIL")

original_rows = int(log["Rows_Before"].iloc[0])
removed = original_rows - int(log["Rows_After"].iloc[-1])
removed_pct = removed / original_rows * 100
compare("A9", "Cleaning", "README states ~5.57% of rows removed",
        5.57, round(removed_pct, 2), tol=0.005)
record("A10", "PRD criterion", "Data Integrity: no more than 5% of rows dropped",
       "PASS" if removed_pct <= 5 else "FAIL", "<= 5%", f"{removed_pct:.2f}%",
       f"{removed:,} of {original_rows:,} rows removed")

cleaned = pd.read_csv(
    ROOT / "data" / "interim" / "cleaned_transactions.csv",
    dtype={"Invoice": str, "StockCode": str}, low_memory=False,
    usecols=["Invoice", "StockCode", "Quantity", "Price", "TotalPrice",
             "Customer ID", "Country"],
)
compare("A11", "Cleaning", "cleaned_transactions.csv row count",
        summary["Cleaned transaction rows"], len(cleaned))
compare("A12", "Cleaning", "Total sales revenue in cleaning_summary.csv",
        summary["Total sales revenue"], round(cleaned["TotalPrice"].sum(), 2),
        tol=0.01)
compare("A13", "Cleaning", "TotalPrice = Quantity x Price on every row",
        0, int((~np.isclose(cleaned["TotalPrice"],
                            cleaned["Quantity"] * cleaned["Price"])).sum()))

if RAW.exists():
    raw = pd.read_csv(RAW, dtype={"Invoice": str, "StockCode": str})
    audit = pd.read_csv(REPORTS / "data_quality_summary.csv").set_index("Metric")["Value"]
    raw_facts = {
        "Total Rows": len(raw),
        "Exact Duplicates": int(raw.duplicated().sum()),
        "Negative Quantities": int((raw["Quantity"] < 0).sum()),
        "Zero Prices": int((raw["Price"] == 0).sum()),
        "Negative Prices": int((raw["Price"] < 0).sum()),
        "Cancelled Invoice Rows": int(raw["Invoice"].str.startswith("C").sum()),
        "Missing Customer IDs": int(raw["Customer ID"].isna().sum()),
        "Missing Descriptions": int(raw["Description"].isna().sum()),
        "Unique Customers": int(raw["Customer ID"].nunique()),
    }
    for i, (label, actual) in enumerate(raw_facts.items(), start=14):
        compare(f"A{i}", "Data audit", f"Raw data: {label}",
                audit[label], actual)
else:
    record("A14", "Data audit", "Raw-data audit figures re-computed", "SKIP",
           note="data/raw/online_retail_II.csv not found")

# --------------------------------------------------------------------------
# B. RFM
# --------------------------------------------------------------------------
transactions = pd.read_csv(
    PROCESSED / "customer_transactions.csv", parse_dates=["InvoiceDate"],
    dtype={"Invoice": str},
)
rfm = pd.read_csv(PROCESSED / "customer_rfm.csv")

reference_date = transactions["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)
grouped = transactions.groupby("Customer ID")
independent = pd.DataFrame({
    "Recency": (reference_date - grouped["InvoiceDate"].max().dt.normalize()).dt.days,
    "Frequency": grouped["Invoice"].nunique(),
    "Monetary": grouped["TotalPrice"].sum(),
}).reset_index().rename(columns={"Customer ID": "CustomerID"})
merged = independent.merge(rfm, on="CustomerID", suffixes=("_new", "_saved"))

compare("B1", "RFM", "Customers in customer_rfm.csv = customers in transactions",
        len(independent), len(rfm))
compare("B2", "RFM", "Customer IDs match one-to-one", len(rfm), len(merged))
for i, col in enumerate(["Recency", "Frequency", "Monetary"], start=3):
    diff = float(np.abs(merged[f"{col}_new"] - merged[f"{col}_saved"]).max())
    compare(f"B{i}", "RFM", f"Independent {col} recalculation (max abs diff)",
            0, diff, tol=1e-6)
metadata = json.loads(
    (PROCESSED / "customer_rfm_features_metadata.json").read_text(encoding="utf-8"))
record("B6", "RFM", "RFM reference date matches metadata",
       "PASS" if metadata["reference_date"] == f"{reference_date:%Y-%m-%d}" else "FAIL",
       metadata["reference_date"], f"{reference_date:%Y-%m-%d}")
record("B7", "RFM", "No duplicate IDs; Frequency and Monetary > 0",
       "PASS" if (not rfm["CustomerID"].duplicated().any()
                  and (rfm["Frequency"] > 0).all()
                  and (rfm["Monetary"] > 0).all()) else "FAIL")

# --------------------------------------------------------------------------
# C. K-Means evaluation
# --------------------------------------------------------------------------
evaluation = pd.read_csv(REPORTS / "cluster_evaluation.csv").set_index("k")
readme_sil = {
    int(r[0]): number(r[1]) for r in table_rows(
        README, "**Model evaluation:**", "Four clusters were selected")
}
for k in evaluation.index:
    compare(f"C{k - 1}", "K-Means", f"README silhouette for k={k} = saved value",
            readme_sil[k], round(evaluation.loc[k, "silhouette_score"], 4),
            tol=0.00006)

scaled = pd.read_csv(PROCESSED / "customer_rfm_scaled.csv").to_numpy()
models, inertia_gap, sampled_gap, full_gap = {}, 0.0, 0.0, 0.0
for k in evaluation.index:
    model = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled)
    models[k] = model
    sampled = silhouette_score(scaled, model.labels_,
                               sample_size=min(5000, len(scaled)), random_state=42)
    full = silhouette_score(scaled, model.labels_)
    inertia_gap = max(inertia_gap, abs(model.inertia_ - evaluation.loc[k, "inertia"]))
    sampled_gap = max(sampled_gap, abs(sampled - evaluation.loc[k, "silhouette_score"]))
    full_gap = max(full_gap, abs(full - evaluation.loc[k, "silhouette_score"]))

compare("C8", "K-Means", "Inertia re-computed for k=2..8 (max abs diff)",
        0, inertia_gap, tol=1e-4)
compare("C9", "K-Means", "Sampled silhouette re-computed (same settings as script)",
        0, sampled_gap, tol=1e-6)
disclosed = "sample" in README.lower() and "5,000" in README
record("C10", "K-Means", "Silhouette scores are sample estimates and README says so",
       "PASS" if disclosed else "WARN", "5,000-customer sample estimate",
       f"full-data gap up to {full_gap:.4f}",
       "rfm_analysis.py uses sample_size=5000 of 5,878 customers; full-data "
       "scores differ slightly but the ranking of k is unchanged")
selected_labels = models[4].labels_
segments = pd.read_csv(PROCESSED / "customer_segments.csv")
record("C11", "K-Means", "k=4 cluster labels re-produced exactly (random_state=42)",
       "PASS" if (selected_labels == segments["Cluster"].to_numpy()).all() else "FAIL")
best_k = int(evaluation["silhouette_score"].idxmax())
record("C12", "K-Means", "Selected k vs highest-silhouette k", "INFO",
       "k=4 selected", f"highest silhouette at k={best_k}",
       "k=4 is a documented business choice, not the statistical optimum")

# --------------------------------------------------------------------------
# D. Segments
# --------------------------------------------------------------------------
profile = pd.read_csv(REPORTS / "customer_segment_profile.csv").set_index("Segment")
readme_seg = {r[0]: r for r in table_rows(
    README, "**Identified customer segments:**", "**Marketing recommendations:**")}
week2_seg = {r[0]: r for r in table_rows(
    WEEK2, "## 5. Customer segment profile", "Segment names are descriptive")}

for i, (name, row) in enumerate(profile.iterrows(), start=1):
    compare(f"D{i}a", "Segments", f"README customers for '{name}'",
            number(readme_seg[name][1]), row["Customers"])
    compare(f"D{i}b", "Segments", f"README % for '{name}'",
            number(readme_seg[name][2]), round(row["Customer_Percentage"], 2),
            tol=0.005)
    w = week2_seg[name]
    for col, idx, key in (("Recency", 3, "Avg_Recency"),
                          ("Frequency", 4, "Avg_Frequency"),
                          ("Monetary", 5, "Avg_Monetary")):
        compare(f"D{i}{'cde'[idx - 3]}", "Segments",
                f"Week 2 report avg {col} for '{name}'",
                number(w[idx]), round(row[key], 2), tol=0.005)

by_cluster = segments.groupby("Segment").agg(
    Customers=("CustomerID", "size"), Revenue=("Monetary", "sum"))
compare("D5", "Segments", "Profile customers reconcile with customer_segments.csv",
        0, int((by_cluster["Customers"] - profile["Customers"]).abs().sum()))
compare("D6", "Segments", "Profile revenue reconciles with customer_segments.csv",
        0, float((by_cluster["Revenue"] - profile["Total_Revenue"]).abs().max()),
        tol=0.01)
compare("D7", "Segments", "Segment customers add up to all customers",
        len(rfm), int(profile["Customers"].sum()))
compare("D8", "Segments", "Segment revenue = customer-level revenue",
        round(transactions["TotalPrice"].sum(), 2),
        round(profile["Total_Revenue"].sum(), 2), tol=0.01)
recommendations = pd.read_csv(REPORTS / "customer_segment_recommendations.csv")
record("D9", "PRD criterion",
       "Actionability: >= 4 segments, each with a recommendation",
       "PASS" if (profile.shape[0] >= 4 and
                  set(profile.index) <= set(recommendations["Segment"])) else "FAIL",
       ">= 4", f"{profile.shape[0]} segments, "
       f"{recommendations['Segment'].nunique()} recommendations")

# --------------------------------------------------------------------------
# E. Churn model (Nivesh243)
# --------------------------------------------------------------------------
model_files = [p for pattern in ("*.joblib", "*.pkl") for p in (ROOT / "models").glob(pattern)]
churn_code = [p for p in (ROOT / "src").glob("churn_*.py")]
metadata_file = ROOT / "models" / "model_metadata.json"
found = len(model_files) + len(churn_code)
record("E1", "Churn model", "Churn model, code and metrics are present",
       "PASS" if (found and metadata_file.exists()) else "BLOCKED",
       "model + code + metadata", f"{found} files + metadata",
       "" if found else "No model file or churn code exists. "
       "Use src/modeling/verify_churn_metrics.py once delivered.")
if metadata_file.exists():
    churn_meta = json.loads(metadata_file.read_text(encoding="utf-8"))
    test_auc = float(churn_meta["test_metrics"]["ROC_AUC"])
    record("E2", "PRD criterion", "Model Performance: churn ROC-AUC >= 0.75 (held-out test)",
           "PASS" if test_auc >= 0.75 else "FAIL", ">= 0.75", round(test_auc, 4),
           f"CV ROC-AUC {churn_meta.get('cross_validation_roc_auc', float('nan')):.4f}; "
           "selection used training CV only")
    comparison_file = REPORTS / "churn_model_comparison.csv"
    if comparison_file.exists():
        comp = pd.read_csv(comparison_file).set_index("Model")
        selected = churn_meta["selected_model"]
        gaps = [abs(float(churn_meta["test_metrics"][m]) - float(comp.loc[selected, m]))
                for m in ["Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"]]
        compare("E3", "Churn model",
                "Metadata test metrics equal churn_model_comparison.csv (max abs diff)",
                0, max(gaps), tol=1e-9)
    predictions_file = REPORTS / "customer_churn_predictions.csv"
    if predictions_file.exists():
        n_scored = len(pd.read_csv(predictions_file))
        record("E4", "Churn model", "Committed prediction CSV is a demonstration sample",
               "INFO", "full-population scoring pending", f"{n_scored} customers scored",
               "Scores for the remaining cohort must not be read as zero risk")
else:
    record("E2", "PRD criterion", "Model Performance: churn ROC-AUC >= 0.75",
           "BLOCKED", ">= 0.75", "not measured",
           "No churn evaluation available to verify")

# --------------------------------------------------------------------------
# F. Dashboard file
# --------------------------------------------------------------------------
pbix = ROOT / "Customer_Segmentation_Dashboard.pbix"
if pbix.exists():
    with zipfile.ZipFile(pbix) as archive:
        pages = [n for n in archive.namelist() if n.endswith("/page.json")]
        names = [json.loads(archive.read(n)).get("displayName") for n in pages]
    record("F1", "Dashboard", "Dashboard pages found in .pbix", "INFO",
           "4 planned pages (Dashboard_Documentation.docx)",
           f"{len(names)} pages: {', '.join(names)}")
    has_churn = any("churn" in (n or "").lower() for n in names)
    record("F2", "PRD criterion", "Dashboard shows a High-Risk Churn list",
           "PASS" if has_churn else "FAIL", "required", "no churn page",
           "" if has_churn else "Depends on the churn model (see E1)")
else:
    record("F1", "Dashboard", ".pbix file present", "SKIP")

# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------
table = pd.DataFrame(results)
EVIDENCE.mkdir(parents=True, exist_ok=True)
table.to_csv(EVIDENCE / "metric_verification.csv", index=False)

counts = table["Status"].value_counts()
print(table[table["Status"] != "PASS"].to_string(index=False, max_colwidth=60))
print("\nSummary:", ", ".join(f"{s}={counts.get(s, 0)}" for s in
                              ["PASS", "FAIL", "WARN", "INFO", "SKIP", "BLOCKED"]))
print(f"Saved: {(EVIDENCE / 'metric_verification.csv').relative_to(ROOT)}")
sys.exit(1 if (table["Status"] == "FAIL").any() else 0)
