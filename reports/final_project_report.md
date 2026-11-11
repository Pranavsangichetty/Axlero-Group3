# Final Project Report
## Retail & E-commerce: Customer Segmentation and Churn Prediction

**Team:** Group 3, Axlero – Innovating Solutions  
**Dataset:** Online Retail II (1 Dec 2009 – 9 Dec 2011)  
**Prepared by:** raj4089 (Evaluation, QA & Documentation)  
**Report date:** 11 November 2026 (v2, after churn model delivery)  
**Basis:** repository re-run and checked on 2026-11-10; churn deliverables on `main` (commit `65a8029`) independently re-run and verified on 2026-11-11

## 1. Executive summary

The team cleaned 1,067,371 transaction rows, analysed sales, and divided 5,878 identified customers into four segments with RFM analysis and K-Means. Every reported number for these parts was re-computed independently and matches, and the whole pipeline reproduces exactly from the raw file.

The churn model is now delivered and was **verified end to end**: the historical cohort, the training pipeline and every reported metric of the selected Logistic Regression model were reproduced exactly from the raw data (see section 5.4). Two project targets remain unmet: the held-out churn ROC-AUC is 0.7308 against the 0.75 target, and the cleaning removes 5.57% of rows against a 5% target. The Power BI dashboard still has 2 of 4 planned pages and no churn page; a supplementary Streamlit dashboard was added by the team.

| Project target (PRD) | Result | Status |
|---|---|---|
| Missing values and outliers handled, no more than 5% of data dropped | 5.57% dropped | **Not met** |
| Churn model ROC-AUC of at least 0.75 | Test ROC-AUC 0.7308 (training CV 0.7639), verified | **Not met** on the held-out test set |
| Dashboard with at least 4 segments and an action for each | 4 segments and recommendations exist; recommendations are not on the Power BI dashboard | **Partly met** |

Key business finding: **20% of customers (Champions) bring 74% of customer revenue**, while the 33% in the At-Risk / Hibernating group bring 3.6%.

## 2. Business problem

D2C retailers pay high acquisition costs and have unpredictable retention. The project asks which customer groups are valuable, which are at risk of leaving, and what marketing to apply to each group.

## 3. Data

| Item | Value |
|---|---|
| Source | Online Retail II, UK online gift retailer |
| Raw rows / columns | 1,067,371 / 8 |
| Period | 1 Dec 2009 – 9 Dec 2011 |
| Customers with an ID | 5,942 raw → 5,878 after cleaning |
| Rows without Customer ID | 243,007 (22.77%) |
| Countries | 43 |

Columns are described in `data_dictionary.md`.

## 4. Method

### 4.1 Cleaning (`src/clean_data.py`)
Five ordered steps (details in `cleaning_documentation.md`):

| Step | Rows removed |
|---|---:|
| Exact duplicates | 34,335 |
| Cancelled invoices | 19,104 |
| Non-positive quantity | 3,393 |
| Non-positive price | 2,626 |
| Invalid dates | 0 |
| **Total** | **59,458 (5.57%)** |

Result: 1,007,913 sales rows (£20,476,260.45), of which 779,425 rows belong to 5,878 identified customers (£17,374,804.27, 84.9% of revenue).

### 4.2 Exploratory analysis (`src/eda.py`)
Six charts in `reports/figures/`: monthly revenue, monthly orders, top countries, top products, top customers, order-value distribution.

Main observations (from the saved report tables):
- The United Kingdom brings 85.0% of revenue; EIRE, the Netherlands, Germany and France follow.
- The best month is November 2011 (£1.50M), then November 2010 (£1.46M); sales peak in the autumn before Christmas. December 2011 is incomplete.
- The top customer, 18102, spent £580,987; the top 10 customers are in `customer_revenue_top10.csv`.
- Customers have 40,077 orders in total; the average order value is £510.92 (dataset price unit).

### 4.3 RFM (`src/rfm_analysis.py`)
Recency (days since the last purchase on the reference date 10 Dec 2011), Frequency (distinct invoices) and Monetary (total spend) for each of the 5,878 customers. 72.4% of customers (4,255) bought more than once.

### 4.4 Clustering
`log1p` and `StandardScaler` were applied because the three measures are very skewed and have different units. K-Means (`random_state=42`, `n_init=10`) was tested for k = 2 to 8 with inertia and silhouette score (`metrics_documentation.md` §3). k = 4 was selected.

## 5. Results

### 5.1 Choice of k
k = 2 has the highest silhouette (0.4407) but only splits customers into "good" and "bad". k = 4 scores 0.3666, the next best, and gives the four actionable groups the project requires. This is a business decision, not the statistical optimum. Silhouette values are sample estimates; scores on all customers differ by at most 0.0021.

### 5.2 Customer segments

| Segment | Customers | % | Avg Recency (days) | Avg Frequency | Avg Monetary | % of revenue |
|---|---:|---:|---:|---:|---:|---:|
| Champions | 1,204 | 20.5% | 28 | 19.2 | 10,678 | 74.0% |
| Loyal High-Value | 1,455 | 24.8% | 231 | 5.0 | 1,945 | 16.3% |
| Recent Customers | 1,261 | 21.5% | 29 | 3.0 | 848 | 6.2% |
| At-Risk / Hibernating | 1,958 | 33.3% | 398 | 1.4 | 316 | 3.6% |

### 5.3 Recommended actions
These are interpretations of the profiles, not model guarantees.

| Segment | Recommended action | Goal |
|---|---|---|
| Champions | VIP rewards, early access, referral campaigns | Retention and advocacy |
| Loyal High-Value | Personalised win-back emails, loyalty reminders, relevant offers | Reactivation (they buy often but have been quiet about 8 months) |
| Recent Customers | Welcome journey, second-purchase offers, product recommendations | Repeat purchases |
| At-Risk / Hibernating | Low-cost re-engagement, feedback survey, carefully targeted discounts | Reactivation without heavy spend |

Priority: protect Champions first (74% of revenue), then win back Loyal High-Value customers, who have the best return on a campaign.

### 5.4 Churn prediction
**Delivered and verified (2026-11-11).** The pipeline (`src/churn_dataset.py`, `src/churn_prediction.py`) builds a leakage-safe historical cohort: six features from a 180-day window (2 Jan–30 Jun 2011), label = no purchase in the following 90 days (1 Jul–28 Sep 2011). `Future_Orders_90d` and `CustomerID` are excluded from training. Cohort: 2,724 customers, 1,315 churned (48.27%). Stratified 80/20 split, 3-fold CV grid search, selection by training CV ROC-AUC only.

| Model | CV ROC-AUC | Test accuracy | Precision | Recall | F1 | Test ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| **Logistic Regression (selected)** | 0.7639 | 0.6807 | 0.6529 | 0.7224 | 0.6859 | **0.7308** |
| Random Forest | 0.7360 | 0.6385 | 0.6071 | 0.7110 | 0.6550 | 0.7115 |

Confusion matrix on 545 test customers (TN, FP, FN, TP): 181, 101, 73, 190. The model finds 72% of churners; about one in three churn flags is a false alarm.

**Independent verification (raj4089):** the cohort (2,724 / 1,315 / 1,409 / 48.27%) and every reported metric of the selected model were reproduced **exactly** by re-running the pipeline from the raw data; `src/modeling/verify_churn_metrics.py` passed all 9 metric checks on the real test predictions; the 28-check `src/validate_churn_model.py` suite passed. Random Forest metrics differed by at most 0.004 on re-run (environment-level nondeterminism; it was not the selected model). **The held-out test ROC-AUC (0.7308) is below the 0.75 target** — the 0.75 is met only by the training CV estimate. The 90-day horizon matches the team proposal but still awaits formal confirmation against the PRD's 30/60-day example. The committed `customer_churn_predictions.csv` is a 10-customer demonstration, not full-population scoring.

### 5.5 Dashboard
The Power BI file has a sales page (6 visuals) and a segment page (5 charts). KPI cards, slicers, a Customer Behaviour page, a Churn page and the High-Risk list are missing. A supplementary Streamlit dashboard (`dashboard/app.py`, 4 sections including churn analysis) was added by the team; it does not replace the required Power BI deliverable. Details: `dashboard_guide.md`.

## 6. Quality assurance

| Test | Result |
|---|---|
| Clean install and run of all 6 scripts | Pass |
| Regenerated files equal committed files | 18 of 18 identical |
| Automated metric checks (2026-11-11) | 66 PASS, 3 FAIL, 3 INFO, 0 BLOCKED |
| Independent RFM recalculation for 5,878 customers | Exact match |
| k = 4 clusters reproduced | Exact match |
| Churn cohort rebuilt from raw data | Exact match (2,724 / 1,315 / 48.27%) |
| Churn model retrained and metrics recomputed | Selected model: exact match on all 6 metrics and the confusion matrix |
| `verify_churn_metrics.py` on real test predictions | 9 of 9 metric checks pass; PRD AUC check fails (0.7308 < 0.75) |
| `validate_churn_model.py` (28 checks) | 28 of 28 pass |
| PostgreSQL notebook | 73 of 73 cells run, 0 errors, 33/33 findings and 25/25 validation checks |

The three automated FAILs are real open issues, not script errors: data loss 5.57% (target 5%), test ROC-AUC 0.7308 (target 0.75), and no churn page in the Power BI file.

Evidence: `testing_evidence.md` and `reports/qa_evidence/`.

## 7. Limitations

1. 5.57% of rows removed (target 5%); duplicates are the largest part (3.22%) and rest on the assumption that identical rows are errors.
2. 22.77% of rows have no Customer ID, so customer analysis covers 84.9% of revenue.
3. Two cancelled orders (£245,653) still count as sales; 10 customers change segment if they are removed.
4. Revenue is gross: cancellations (−£1.53M in the raw data) and returns are not subtracted; non-product codes are 4.07% of revenue.
5. Silhouette values are estimated on a 5,000-customer sample; k = 4 is a business choice.
6. The RFM table is a full-history snapshot, valid for description only.
7. Two cleaning pipelines (scripts and notebook) give different totals; the dashboard probably mixes them.
8. Currency is not documented.
9. The churn test ROC-AUC (0.7308) is below the 0.75 target; the target is met only by the training CV estimate (0.7639). Evaluation uses one historical cohort and one holdout split; temporal generalization is untested.
10. The committed churn prediction file scores only 10 demonstration customers; full-population scoring is pending.
11. Power BI dashboard behaviour and Git history could not be tested from this environment.

## 8. Recommendations and next steps

| Priority | Action | Owner |
|---|---|---|
| 1 | Record formal team confirmation of the implemented churn definition (180-day features + 90-day horizon) against the PRD's 30/60-day example | Pranav / team |
| 2 | Decide how to treat the missed ROC-AUC target (0.7308 vs 0.75): accept and document the deviation, or improve the model (more features, out-of-time validation, threshold tuning); compare with Divya's multi-snapshot design in a controlled test | Nivesh243 / Divya / raj4089 |
| 2b | Score the full customer base with `src/predict_customers.py` and publish the High-Risk list (current CSV is a 10-row demo) | Nivesh243 / Sirisha |
| 3 | Decide how to handle the 5% target and the two cancelled outlier orders; choose one cleaning pipeline and regenerate everything from it | Pranav / Divya |
| 4 | Finish the dashboard: churn page, High-Risk list, KPI cards, slicers, titles, segment recommendations; add screenshots | Sirisha |
| 5 | Allow model files in `.gitignore`; store large CSV files with Git LFS or regenerate them | Pranav |
| 6 | Make the 4 relative-path scripts runnable from any folder | Divya / Lav |

## 9. Reproducing this report

```bash
pip install -r requirements.txt
# put online_retail_II.csv in data/raw/
python src/data_quality_audit.py && python src/investigate_transactions.py
python src/clean_data.py && python src/eda.py
python src/rfm_analysis.py && python src/features.py
python src/verify_reported_metrics.py
```

## 10. Related documents

`README.md` · `metrics_documentation.md` · `data_dictionary.md` · `cleaning_documentation.md` · `dashboard_guide.md` · `testing_evidence.md` · `qa_checklist.md`
