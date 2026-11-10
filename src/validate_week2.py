
from pathlib import Path

import json
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

TRANSACTIONS_FILE = DATA / "customer_transactions.csv"
RFM_FILE = DATA / "customer_rfm.csv"
SCALED_FILE = DATA / "customer_rfm_scaled.csv"
SEGMENTS_FILE = DATA / "customer_segments.csv"
FEATURES_FILE = DATA / "customer_rfm_features.csv"
METADATA_FILE = DATA / "customer_rfm_features_metadata.json"
EVALUATION_FILE = REPORTS / "cluster_evaluation.csv"
PROFILE_FILE = REPORTS / "customer_segment_profile.csv"

RESULTS_FILE = REPORTS / "week2_validation_results.csv"
REPORT_FILE = REPORTS / "week2_validation_report.md"

RFM_COLUMNS = ["Recency", "Frequency", "Monetary"]
SEGMENT_COLUMNS = ["Cluster", "Segment"]

results = []


def check(name, passed, observed, expected, details=""):
    results.append({
        "Check": name,
        "Status": "PASS" if passed else "FAIL",
        "Observed": str(observed),
        "Expected": str(expected),
        "Details": details
    })

    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {details}")


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)

    required_files = [
        TRANSACTIONS_FILE,
        RFM_FILE,
        SCALED_FILE,
        SEGMENTS_FILE,
        FEATURES_FILE,
        METADATA_FILE,
        EVALUATION_FILE,
        PROFILE_FILE
    ]

    missing_files = [str(p) for p in required_files if not p.exists()]

    if missing_files:
        raise FileNotFoundError(
            "Missing required files: " + ", ".join(missing_files)
        )

    print("Loading Week 2 datasets...")

    transactions = pd.read_csv(
        TRANSACTIONS_FILE,
        parse_dates=["InvoiceDate"]
    )
    rfm = pd.read_csv(RFM_FILE)
    scaled = pd.read_csv(SCALED_FILE)
    segments = pd.read_csv(SEGMENTS_FILE)
    features = pd.read_csv(FEATURES_FILE)
    evaluation = pd.read_csv(EVALUATION_FILE)
    profile = pd.read_csv(PROFILE_FILE)

    with open(METADATA_FILE, encoding="utf-8") as file:
        metadata = json.load(file)

    # ---------------------------------------------------------
    # 1. Required columns and basic data checks
    # ---------------------------------------------------------

    print("\n========== DATASET STRUCTURE ==========")

    required_transaction_columns = {
        "Invoice", "InvoiceDate", "Customer ID", "TotalPrice"
    }
    required_rfm_columns = {"CustomerID", *RFM_COLUMNS}
    required_segment_columns = {
        "CustomerID", *RFM_COLUMNS, *SEGMENT_COLUMNS
    }
    required_feature_columns = {
        "CustomerID", *RFM_COLUMNS, *SEGMENT_COLUMNS
    }

    check(
        "Transaction columns exist",
        required_transaction_columns.issubset(transactions.columns),
        sorted(transactions.columns),
        sorted(required_transaction_columns)
    )

    check(
        "RFM columns exist",
        required_rfm_columns.issubset(rfm.columns),
        sorted(rfm.columns),
        sorted(required_rfm_columns)
    )

    check(
        "Segment columns exist",
        required_segment_columns.issubset(segments.columns),
        sorted(segments.columns),
        sorted(required_segment_columns)
    )

    check(
        "Integrated feature columns exist",
        required_feature_columns.issubset(features.columns),
        sorted(features.columns),
        sorted(required_feature_columns)
    )

    check(
        "All input datasets are non-empty",
        all(len(frame) > 0 for frame in [
            transactions, rfm, scaled, segments, features,
            evaluation, profile
        ]),
        "All datasets loaded",
        "All datasets non-empty"
    )

    # Stop if the required fields are unavailable.
    if not (
        required_transaction_columns.issubset(transactions.columns)
        and required_rfm_columns.issubset(rfm.columns)
        and required_segment_columns.issubset(segments.columns)
        and required_feature_columns.issubset(features.columns)
    ):
        raise ValueError("Required columns are missing. Cannot continue.")

    # ---------------------------------------------------------
    # 2. Customer uniqueness and population consistency
    # ---------------------------------------------------------

    print("\n========== CUSTOMER ID VALIDATION ==========")

    frames = {
        "RFM": rfm,
        "Segments": segments,
        "Integrated features": features
    }

    for name, frame in frames.items():
        check(
            f"{name} has unique CustomerID",
            not frame["CustomerID"].duplicated().any(),
            frame["CustomerID"].duplicated().sum(),
            0
        )

        check(
            f"{name} has no missing CustomerID",
            frame["CustomerID"].notna().all(),
            frame["CustomerID"].isna().sum(),
            0
        )

    rfm_ids = set(rfm["CustomerID"])
    segment_ids = set(segments["CustomerID"])
    feature_ids = set(features["CustomerID"])
    transaction_ids = set(transactions["Customer ID"].dropna())

    check(
        "RFM and segment customer populations match",
        rfm_ids == segment_ids,
        len(rfm_ids.symmetric_difference(segment_ids)),
        0
    )

    check(
        "RFM and integrated feature populations match",
        rfm_ids == feature_ids,
        len(rfm_ids.symmetric_difference(feature_ids)),
        0
    )

    check(
        "RFM and transaction customer populations match",
        rfm_ids == transaction_ids,
        len(rfm_ids.symmetric_difference(transaction_ids)),
        0
    )

    # ---------------------------------------------------------
    # 3. Independently recompute RFM values
    # ---------------------------------------------------------

    print("\n========== RFM RECALCULATION ==========")

    valid_transactions = transactions.dropna(
        subset=["Customer ID", "InvoiceDate", "TotalPrice"]
    ).copy()

    reference_date = (
        valid_transactions["InvoiceDate"].max().normalize()
        + pd.Timedelta(days=1)
    )

    recomputed = valid_transactions.groupby("Customer ID").agg(
        Recency=(
            "InvoiceDate",
            lambda x: (
                reference_date - x.max().normalize()
            ).days
        ),
        Frequency=("Invoice", "nunique"),
        Monetary=("TotalPrice", "sum")
    ).reset_index()

    recomputed = recomputed.rename(
        columns={"Customer ID": "CustomerID"}
    )

    recomputed = recomputed[
        (recomputed["Frequency"] > 0)
        & (recomputed["Monetary"] > 0)
    ].copy()

    comparison = rfm.merge(
        recomputed,
        on="CustomerID",
        how="outer",
        suffixes=("_saved", "_recomputed"),
        indicator=True
    )

    population_match = (comparison["_merge"] == "both").all()

    check(
        "Recomputed RFM customer population matches",
        population_match,
        comparison["_merge"].value_counts().to_dict(),
        "All records matched"
    )

    for column in RFM_COLUMNS:
        saved = comparison[f"{column}_saved"]
        recalculated = comparison[f"{column}_recomputed"]

        values_match = (
            comparison["_merge"].eq("both").all()
            and np.allclose(
                saved,
                recalculated,
                rtol=1e-8,
                atol=0.01
            )
        )

        max_difference = (
            (saved - recalculated).abs().max()
            if comparison["_merge"].eq("both").all()
            else "Customer population mismatch"
        )

        check(
            f"{column} independently recalculated",
            values_match,
            max_difference,
            "Maximum difference <= 0.01"
        )

    check(
        "RFM reference date matches expected date",
        reference_date.strftime("%Y-%m-%d") == "2011-12-10",
        reference_date.strftime("%Y-%m-%d"),
        "2011-12-10"
    )

    check(
        "RFM values are non-negative",
        (rfm[RFM_COLUMNS] >= 0).all().all(),
        rfm[RFM_COLUMNS].min().to_dict(),
        "All values >= 0"
    )

    check(
        "Frequency and Monetary are positive",
        (
            (rfm["Frequency"] > 0).all()
            and (rfm["Monetary"] > 0).all()
        ),
        {
            "minimum_frequency": rfm["Frequency"].min(),
            "minimum_monetary": rfm["Monetary"].min()
        },
        "Both values > 0"
    )

    # ---------------------------------------------------------
    # 4. Scaled feature validation
    # ---------------------------------------------------------

    print("\n========== SCALING VALIDATION ==========")

    scaled_match = False
    scaled_max_difference = np.nan

    if (
        len(scaled) == len(rfm)
        and set(RFM_COLUMNS).issubset(scaled.columns)
    ):
        expected_scaled = StandardScaler().fit_transform(
            np.log1p(rfm[RFM_COLUMNS])
        )

        scaled_match = np.allclose(
            scaled[RFM_COLUMNS].to_numpy(),
            expected_scaled,
            rtol=1e-6,
            atol=1e-6
        )

        scaled_max_difference = np.max(
            np.abs(
                scaled[RFM_COLUMNS].to_numpy() - expected_scaled
            )
        )

    check(
        "Scaled RFM values match log1p and StandardScaler",
        scaled_match,
        scaled_max_difference,
        "Maximum difference <= 0.000001"
    )

    check(
        "Scaled dataset row count matches RFM",
        len(scaled) == len(rfm),
        len(scaled),
        len(rfm)
    )

    # ---------------------------------------------------------
    # 5. Cluster and segment validation
    # ---------------------------------------------------------

    print("\n========== CLUSTER VALIDATION ==========")

    check(
        "Exactly four selected clusters exist",
        segments["Cluster"].nunique() == 4,
        sorted(segments["Cluster"].unique().tolist()),
        "Four clusters"
    )

    check(
        "No missing cluster or segment assignments",
        segments[SEGMENT_COLUMNS].notna().all().all(),
        segments[SEGMENT_COLUMNS].isna().sum().to_dict(),
        0
    )

    check(
        "Segment names match between segment and feature files",
        set(
            zip(segments["CustomerID"], segments["Segment"])
        ) == set(
            zip(features["CustomerID"], features["Segment"])
        ),
        "Compared customer-segment pairs",
        "Exact match"
    )

    check(
        "Cluster IDs match between segment and feature files",
        set(
            zip(segments["CustomerID"], segments["Cluster"])
        ) == set(
            zip(features["CustomerID"], features["Cluster"])
        ),
        "Compared customer-cluster pairs",
        "Exact match"
    )

    # Refit KMeans using the same parameters as the original script.
    X = StandardScaler().fit_transform(
        np.log1p(rfm[RFM_COLUMNS])
    )

    reproduced_model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    reproduced_labels = reproduced_model.fit_predict(X)

    label_comparison = rfm[["CustomerID"]].copy()
    label_comparison["ReproducedCluster"] = reproduced_labels

    label_comparison = label_comparison.merge(
        segments[["CustomerID", "Cluster"]],
        on="CustomerID",
        how="inner"
    )

    ari = adjusted_rand_score(
        label_comparison["Cluster"],
        label_comparison["ReproducedCluster"]
    )

    check(
        "Reproduced K-Means assignments match saved clusters",
        ari >= 0.99,
        round(ari, 6),
        "Adjusted Rand Index >= 0.99"
    )

    # ---------------------------------------------------------
    # 6. Cluster evaluation validation
    # ---------------------------------------------------------

    print("\n========== CLUSTER EVALUATION ==========")

    required_eval_columns = {
        "k", "inertia", "silhouette_score"
    }

    evaluation_columns_exist = required_eval_columns.issubset(
        evaluation.columns
    )

    check(
        "Cluster evaluation columns exist",
        evaluation_columns_exist,
        list(evaluation.columns),
        sorted(required_eval_columns)
    )

    if evaluation_columns_exist:
        check(
            "Cluster evaluation covers k=2 through k=8",
            set(evaluation["k"]) == set(range(2, 9)),
            sorted(evaluation["k"].tolist()),
            list(range(2, 9))
        )

        check(
            "Inertia values are positive",
            (evaluation["inertia"] > 0).all(),
            evaluation["inertia"].min(),
            "> 0"
        )

        check(
            "Inertia decreases as k increases",
            evaluation.sort_values("k")["inertia"].is_monotonic_decreasing,
            evaluation.sort_values("k")["inertia"].tolist(),
            "Monotonically decreasing"
        )

        check(
            "Silhouette scores are within valid range",
            evaluation["silhouette_score"].between(-1, 1).all(),
            evaluation["silhouette_score"].min(),
            "Between -1 and 1"
        )

        best_silhouette_k = int(
            evaluation.loc[
                evaluation["silhouette_score"].idxmax(), "k"
            ]
        )

        check(
            "Silhouette optimum is correctly identified as k=2",
            best_silhouette_k == 2,
            best_silhouette_k,
            2
        )

    # ---------------------------------------------------------
    # 7. Segment profile validation
    # ---------------------------------------------------------

    print("\n========== SEGMENT PROFILE VALIDATION ==========")

    actual_profile = segments.groupby("Cluster").agg(
        Customers=("CustomerID", "nunique"),
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Avg_Monetary=("Monetary", "mean"),
        Total_Revenue=("Monetary", "sum")
    ).reset_index()

    profile_comparison = profile.merge(
        actual_profile,
        on="Cluster",
        how="outer",
        suffixes=("_saved", "_actual"),
        indicator=True
    )

    check(
        "Saved profile contains all clusters",
        (profile_comparison["_merge"] == "both").all(),
        profile_comparison["_merge"].value_counts().to_dict(),
        "All clusters matched"
    )

    for column in [
        "Customers", "Avg_Recency", "Avg_Frequency",
        "Avg_Monetary", "Total_Revenue"
    ]:
        saved_column = f"{column}_saved"
        actual_column = f"{column}_actual"

        if (
            saved_column in profile_comparison.columns
            and actual_column in profile_comparison.columns
        ):
            matched = np.allclose(
                profile_comparison[saved_column],
                profile_comparison[actual_column],
                rtol=1e-6,
                atol=0.01
            )

            check(
                f"Segment profile {column} is consistent",
                matched,
                matched,
                "Saved and recomputed values match"
            )

    check(
        "Segment customer counts sum to RFM population",
        int(profile["Customers"].sum()) == len(rfm),
        int(profile["Customers"].sum()),
        len(rfm)
    )

    # ---------------------------------------------------------
    # 8. Integrated feature dataset and metadata
    # ---------------------------------------------------------

    print("\n========== FEATURE DATASET VALIDATION ==========")

    check(
        "Integrated features contain no missing values",
        not features.isna().any().any(),
        int(features.isna().sum().sum()),
        0
    )

    check(
        "Integrated features contain no duplicate rows",
        not features.duplicated().any(),
        int(features.duplicated().sum()),
        0
    )

    check(
        "Integrated feature RFM values match RFM dataset",
        features[["CustomerID"] + RFM_COLUMNS].sort_values(
            "CustomerID"
        ).reset_index(drop=True).equals(
            rfm[["CustomerID"] + RFM_COLUMNS].sort_values(
                "CustomerID"
            ).reset_index(drop=True)
        ),
        "Compared customer-level RFM records",
        "Exact match"
    )

    check(
        "Metadata row count matches feature dataset",
        metadata.get("row_count") == len(features),
        metadata.get("row_count"),
        len(features)
    )

    check(
        "Metadata unique customer count matches",
        metadata.get("unique_customers")
        == features["CustomerID"].nunique(),
        metadata.get("unique_customers"),
        features["CustomerID"].nunique()
    )

    check(
        "Metadata reference date is correct",
        metadata.get("reference_date")
        == reference_date.strftime("%Y-%m-%d"),
        metadata.get("reference_date"),
        reference_date.strftime("%Y-%m-%d")
    )

    # ---------------------------------------------------------
    # 9. Save validation results and report
    # ---------------------------------------------------------

    results_df = pd.DataFrame(results)
    results_df.to_csv(RESULTS_FILE, index=False)

    passed = int((results_df["Status"] == "PASS").sum())
    failed = int((results_df["Status"] == "FAIL").sum())

    report = [
        "# Week 2 Independent RFM and Segmentation Validation",
        "",
        "## Project",
        "Retail & E-commerce – Customer Segmentation and Churn Prediction",
        "",
        "## Validation summary",
        f"- Total checks: {len(results_df)}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        "",
        "## Dataset summary",
        f"- Customers: {len(rfm):,}",
        f"- RFM reference date: {reference_date:%Y-%m-%d}",
        f"- Selected clusters: {segments['Cluster'].nunique()}",
        f"- Integrated feature records: {len(features):,}",
        f"- K-Means reproduction ARI: {ari:.6f}",
        "",
        "## Detailed validation results",
        "",
        "| Check | Status | Details |",
        "|---|---|---|"
    ]

    for _, row in results_df.iterrows():
        report.append(
            f"| {row['Check']} | {row['Status']} | {row['Details']} |"
        )

    report.extend([
        "",
        "## Model selection interpretation",
        "",
        "The k=2 model has the highest silhouette score in the saved "
        "evaluation. The project selected k=4 as a business-oriented "
        "candidate to provide four actionable customer groups. "
        "Therefore, k=4 is not claimed to be the mathematical optimum.",
        "",
        "## Churn modelling limitation",
        "",
        "The RFM snapshot uses the full available transaction history "
        "and is suitable for descriptive segmentation. It must not be "
        "used directly as a historical churn-training snapshot because "
        "this can introduce future-data leakage. Historical churn "
        "features must be recomputed using only data available before "
        "each prediction cutoff.",
        "",
        "## Conclusion",
        "",
        (
            "All independent validation checks passed."
            if failed == 0
            else "One or more validation checks failed and require investigation."
        ),
        ""
    ])

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("\n========== FINAL VALIDATION SUMMARY ==========")
    print("Total checks:", len(results_df))
    print("Passed:", passed)
    print("Failed:", failed)
    print("\nGenerated files:")
    print(RESULTS_FILE.relative_to(ROOT))
    print(REPORT_FILE.relative_to(ROOT))

    if failed:
        raise SystemExit(
            "Week 2 validation found failures. Investigate before committing."
        )

    print("\nAll independent Week 2 validation checks passed.")


if __name__ == "__main__":
    main()
