# Final Project Report
## Retail & E-commerce: Customer Segmentation and Churn Prediction

**Team:** Group 3, Axlero – Innovating Solutions  
**Dataset:** Online Retail II (1 Dec 2009 – 9 Dec 2011)  
**Prepared by:** raj4089 (Evaluation, QA & Documentation)  
**Report date:** 10 November 2026  
**Basis:** repository `Axlero-Group3-main.zip`, re-run and checked on 2026-11-10

## 1. Executive summary

The team cleaned 1,067,371 transaction rows, analysed sales, and divided 5,878 identified customers into four segments with RFM analysis and K-Means. Every reported number for these parts was re-computed independently and matches, and the whole pipeline reproduces exactly from the raw file.

Three things are **not complete**: the churn prediction model is not in the repository, the dashboard has 2 of the 4 planned pages and no churn view, and the cleaning removes 5.57% of rows against a 5% target. This report states results only for what was delivered and verified.

| Project target (PRD) | Result | Status |
|---|---|---|
| Missing values and outliers handled, no more than 5% of data dropped | 5.57% dropped | **Not met** |
| Churn model ROC-AUC of at least 0.75 | No model delivered | **Not met / not measurable** |
| Dashboard with at least 4 segments and an action for each | 4 segments and recommendations exist; recommendations are not on the dashboard | **Partly met** |

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
**Not delivered.** There is no model, prediction file or metrics report, so no churn result is reported here. The team's churn proposal (180-day observation window, 90-day prediction window, proxy label "no purchase") is still pending confirmation, and differs from the 30 or 60 days in the project requirements. The current RFM table uses the full history and **must not** be used to train the churn model, because that leaks future information; features must be recomputed at a historical cutoff date.

### 5.5 Dashboard
The Power BI file has a sales page (6 visuals) and a segment page (5 charts). KPI cards, slicers, a Customer Behaviour page, a Churn page and the High-Risk list are missing. Details: `dashboard_guide.md`.

## 6. Quality assurance

| Test | Result |
|---|---|
| Clean install and run of all 6 scripts | Pass |
| Regenerated files equal committed files | 18 of 18 identical |
| Automated metric checks | 64 PASS, 2 FAIL, 2 BLOCKED, 2 INFO |
| Independent RFM recalculation for 5,878 customers | Exact match |
| k = 4 clusters reproduced | Exact match |
| PostgreSQL notebook | 73 of 73 cells run, 0 errors, 33/33 findings and 25/25 validation checks |

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
9. Churn modelling and the complete dashboard are missing; dashboard behaviour and Git history could not be tested.

## 8. Recommendations and next steps

| Priority | Action | Owner |
|---|---|---|
| 1 | Agree the churn definition and horizon, then build features at a historical cutoff and train Logistic Regression and Random Forest; use class weights if churn is a minority; report precision, recall, F1, ROC-AUC and the confusion matrix on a time-based test set | Nivesh243 / Pranav |
| 2 | Run `src/modeling/verify_churn_metrics.py` on the results; require ROC-AUC of at least 0.75 and investigate any value above 0.98 for leakage | raj4089 |
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
