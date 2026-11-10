# Metric Documentation

Prepared by raj4089 (Evaluation, QA & Documentation). "Verified" means the value was re-computed independently from the saved data on 2026-11-10 and matched the reported value (`src/verify_reported_metrics.py`).

## 1. Data-quality metrics

| Metric | Definition | Value | Meaning | Verified |
|---|---|---:|---|---|
| Rows removed | Original rows − cleaned rows | 59,458 | Rows dropped by the cleaning pipeline | Yes |
| Share removed | Rows removed ÷ original rows | 5.57% | Project target: at most 5% | Yes, **target missed** |
| Missing Customer ID | Rows with no customer number | 243,007 (22.77%) | Guest orders; cannot be used for customer analysis | Yes |
| Customer coverage | Customer revenue ÷ total revenue | 84.9% | Part of sales that the RFM and segments describe | Yes |

## 2. RFM metrics (one value per customer)

| Metric | Formula | Range | Meaning |
|---|---|---|---|
| Recency | Reference date (10 Dec 2011) − date of last purchase, in days | 1 to 739 | Low = bought recently (good) |
| Frequency | Number of distinct invoices | 1 to 398 | High = buys often (good) |
| Monetary | Sum of `Quantity × Price` over all the customer's invoices | 2.95 to 580,987 | High = spends a lot (good); gross, cancellations not subtracted |

All three were independently re-computed for all 5,878 customers: maximum difference 0 (Monetary: 4e-12).

## 3. Clustering metrics (K-Means, k = 2 to 8)

Input: `log1p` of Recency, Frequency and Monetary, then `StandardScaler`; `random_state=42`, `n_init=10`.

| Metric | Meaning | How to read it |
|---|---|---|
| Inertia | Sum of squared distances from each customer to its cluster centre | Always falls as k grows; look for the "elbow" where the fall slows down |
| Silhouette score | Average of (nearest-other-cluster distance − own-cluster distance) ÷ the larger of the two, from −1 to 1 | Above 0.5 = clear clusters; 0.25 to 0.5 = some overlap; below 0.25 = weak. Higher is better |

| k | Inertia | Silhouette (reported, 5,000-customer sample) | Silhouette (all 5,878 customers) |
|---:|---:|---:|---:|
| 2 | 8,577.11 | 0.4407 | 0.4385 |
| 3 | 6,336.79 | 0.3499 | 0.3479 |
| **4** | **4,895.41** | **0.3666** | **0.3664** |
| 5 | 4,069.63 | 0.3455 | 0.3440 |
| 6 | 3,535.11 | 0.3361 | 0.3348 |
| 7 | 3,170.92 | 0.3034 | 0.3029 |
| 8 | 2,883.12 | 0.2943 | 0.2957 |

- Inertia matches exactly; reported silhouette matches exactly when the same 5,000-customer sample is used.
- The reported silhouette is a sample estimate; the all-customer value differs by at most 0.0021. The ranking of k does not change (k = 2 is best, then k = 4).
- k = 4 has a silhouette of 0.37: moderate overlap between groups, normal for behaviour data. It was chosen for business usefulness (the project needs at least 4 segments), not because it scores highest.
- Re-running with the same seed reproduces all 5,878 cluster labels exactly.

## 4. Segment metrics (`customer_segment_profile.csv`)

| Metric | Definition |
|---|---|
| Customers | Customers in the cluster |
| Customer_Percentage | Customers ÷ 5,878 × 100 |
| Avg_Recency / Avg_Frequency / Avg_Monetary | Mean of the RFM value in the cluster |
| Total_Revenue | Sum of Monetary in the cluster |

| Segment | Customers | % customers | Avg Recency | Avg Frequency | Avg Monetary | % of customer revenue |
|---|---:|---:|---:|---:|---:|---:|
| Champions | 1,204 | 20.48% | 28.4 | 19.2 | 10,678.40 | 74.0% |
| Loyal High-Value | 1,455 | 24.75% | 231.2 | 5.0 | 1,945.08 | 16.3% |
| Recent Customers | 1,261 | 21.45% | 29.2 | 3.0 | 847.75 | 6.2% |
| At-Risk / Hibernating | 1,958 | 33.31% | 397.9 | 1.4 | 316.09 | 3.6% |

Segment totals reconcile: 5,878 customers, £17,374,804.27 revenue, equal to `customer_transactions.csv`.

## 5. Churn-model metrics (not yet measurable)

No churn model, prediction file or metrics report exists in the repository, so none of these values can be verified yet. They are defined here so the report and dashboard use them consistently. **Positive class = churned customer (1).**

| Metric | Formula | Meaning for this project |
|---|---|---|
| Confusion matrix | TP, FP, FN, TN counts | TP = churners found; FN = churners missed; FP = loyal customers flagged by mistake |
| Precision | TP ÷ (TP + FP) | Of the customers flagged as churn, how many really churn. Low precision wastes retention budget |
| Recall | TP ÷ (TP + FN) | Of all real churners, how many are found. Usually the priority: a missed churner is a lost customer |
| F1-score | 2 × Precision × Recall ÷ (Precision + Recall) | One number balancing precision and recall |
| ROC-AUC | Area under the true-positive vs false-positive curve | Chance that a random churner gets a higher score than a random non-churner; 0.5 = guessing, 1 = perfect. **Project target: at least 0.75** |
| Accuracy | (TP + TN) ÷ all | Misleading when churners are a minority; report it only with the others |

Also required with any churn result: class balance, how the train/test split was made (time-based preferred), the threshold used (0.5 by default) and the reason for it, and proof that no feature uses data after the cutoff date.

**Checking tool.** When the model arrives, run `python src/modeling/verify_churn_metrics.py --predictions <file> --reported <file>`. It re-computes precision, recall, F1, ROC-AUC and the confusion matrix from the saved predictions, compares them with the report, tests ROC-AUC ≥ 0.75, and warns about a suspiciously high AUC (≥ 0.98, a sign of data leakage) or severe class imbalance. Its self-test passes on synthetic data and it correctly fails a tampered report; no project result has been checked with it yet.

## 6. Dashboard KPIs

| KPI | Definition | Reference value |
|---|---|---:|
| Total revenue | Sum of `TotalPrice` over cleaned sales | 20,476,260.45 |
| Total orders | Distinct invoices | 40,077 |
| Average order value | Total revenue ÷ total orders | 510.92 |
| Customers | Distinct Customer IDs | 5,878 |
| Repeat customers | Customers with Frequency above 1 | 4,255 (72.4%) |
| UK share of revenue | UK revenue ÷ total revenue | 85.0% |

These are the `src/` pipeline values. The notebook pipeline gives different totals (see `cleaning_documentation.md`, section 7).
