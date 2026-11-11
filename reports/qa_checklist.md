# QA Checklist and Findings

Reviewer: raj4089 (Evaluation, QA & Documentation). Review dates: 2026-11-10 (baseline) and 2026-11-11 (churn model verification against `main`, commit `65a8029`). A box is ticked only when the file or output was inspected and, where applicable, run (rule from `docs/PROJECT_INTEGRATION_CHECKLIST.md`).

## 1. My tasks

| # | Task | Status | Evidence |
|---|---|---|---|
| 1 | Verify model evaluation results provided by Nivesh | **Done** (2026-11-11): churn pipeline on `main` re-run from raw data; every reported metric of the selected model reproduced exactly | `testing_evidence.md` §5, `qa_evidence/churn_metric_verification.csv` |
| 2 | Check reported metrics match actual model output | **Done** for cleaning, RFM, K-Means, segments and churn (66 PASS, 3 FAIL = real open issues) | `qa_evidence/metric_verification.csv` |
| 3 | Test the project execution steps | **Done** (clean venv, 6 scripts, notebook) | `testing_evidence.md` §2 |
| 4 | Update the final project report | **Done** | `final_project_report.md` |
| 5 | Update README with installation and execution instructions | **Done** | `README.md` |
| 6 | Complete data dictionary and cleaning documentation | **Done** | `data_dictionary.md`, `cleaning_documentation.md` |
| 7 | Document model metrics and their meanings | **Done** (churn values pending) | `metrics_documentation.md` |
| 8 | Document dashboard usage and refresh instructions | **Done** from file inspection; not tested in Power BI | `dashboard_guide.md` |
| 9 | Prepare final testing evidence and limitations | **Done** | `testing_evidence.md` |

## 2. Checklist by area

### Data preparation
- [x] Source dataset location and access documented (README, with row count and checksum)
- [x] Cleaning reproducible from documented inputs (regenerated files identical)
- [x] Row counts, filters and output paths recorded (`cleaning_documentation.md`)
- [x] Same customer ID and date fields used downstream (`Customer ID` / `CustomerID`, `InvoiceDate`)
- [ ] Data-integrity target (at most 5% rows dropped): **5.57%, not met** (finding F-02)

### EDA and RFM segmentation
- [x] EDA outputs regenerate from the current processed data
- [x] RFM definitions, reference date (2011-12-10) and customer inclusion rules documented
- [x] Cluster count explained with metrics and business reasoning (k = 4 vs highest silhouette at k = 2)
- [x] Segment labels and customer counts match generated outputs
- [x] Recommendations recorded as interpretations
- [x] At least 4 segments with a recommendation each

### Churn prediction (verified 2026-11-11)
- [ ] Churn definition and horizon **formally** agreed: implemented as 180-day features + 90-day label, matching the team proposal, but still marked pending confirmation vs the PRD's 30/60-day example (F-06)
- [x] Target built without future information: features end 2011-06-30, label from 2011-07-01 to 2011-09-28; `Future_Orders_90d` and `CustomerID` excluded; `predict_customers.py` rejects inputs containing them
- [x] Logistic Regression and Random Forest trained and compared (3-fold CV grid search; selection by training CV ROC-AUC)
- [x] Precision, recall, F1, ROC-AUC, confusion matrix, class balance reported (48.27% churn rate — near-balanced)
- [ ] ROC-AUC at least 0.75: **measured 0.7308 on the held-out test set — target not met** (training CV 0.7639) (F-15)
- [x] Model saved in `models/` (`churn_model.pkl` + `model_metadata.json` committed; F-07 resolved)
- [x] Reported metrics independently reproduced: cohort exact (2,724/1,315/48.27%), all 6 selected-model metrics and the confusion matrix exact; `validate_churn_model.py` 28/28; `verify_churn_metrics.py` 9/9 metric checks on real test predictions
- [ ] Full-population scoring: committed predictions file is a 10-customer demo (F-16)

### Dashboard
- [x] .pbix file present and structurally valid (2 pages, 11 visuals)
- [ ] KPI cards, slicers, Customer Behaviour page, Churn page, High-Risk list: not in the file (F-03)
- [ ] Values, filters and refresh tested in Power BI Desktop: not possible here
- [ ] Screenshots and tool version recorded: missing

### Repository and reproducibility
- [x] Relative paths work from a fresh clone when run from the repository root
- [ ] Scripts work from any folder: 4 of 6 do not (F-08)
- [x] Dependencies install in a clean environment; tested versions recorded (`requirements-tested.txt`)
- [x] No credentials committed (the notebook reads `PG_PASSWORD`; see F-10)
- [ ] Large files within GitHub limits: `cleaned_transactions.csv` is 95.4 MB, close to the 100 MB limit (F-09)
- [ ] Git commit history checked: not available in the zip

### Final delivery
- [x] README reflects completed, partial and missing work
- [x] Final report has method, results, limitations, recommendations
- [ ] Team contributions verified against git history: not possible here
- [ ] Churn model and complete dashboard present: no

## 3. Findings

Severity: **High** blocks the project goals; **Medium** can give wrong or inconsistent numbers; **Low** is a quality or convenience issue.

| ID | Severity | Finding | Owner | Suggested action |
|---|---|---|---|---|
| F-01 | ~~High~~ **Resolved 2026-11-11** | Churn model, code, metadata and evaluation report are now on `main` and were independently verified (exact metric reproduction). | Nivesh243 / Lav | Done; see F-15 and F-16 for the remaining gaps |
| F-15 | High | **Churn test ROC-AUC 0.7308 is below the 0.75 PRD target.** Only the training CV estimate (0.7639) meets it. One cohort, one holdout; no out-of-time validation. | Nivesh243 / Pranav | Accept and document the deviation, or improve (features, threshold, out-of-time test); compare with Divya's multi-snapshot design |
| F-16 | Medium | **`customer_churn_predictions.csv` scores only 10 demonstration customers.** No full-population scoring or High-Risk list exists; dashboard churn views depend on it. | Nivesh243 / Sirisha | Run `predict_customers.py` on the full cohort features and commit the output |
| F-17 | Low | **Random Forest metrics shift slightly on re-run** (≤ 0.004; confusion matrix differs by one customer) across environments. The selected Logistic Regression reproduces exactly. | Lav | Note in the report; pin versions via `requirements-tested.txt` |
| F-02 | High | **5.57% of rows are dropped** (PRD: at most 5%). Duplicates are 3.22% alone. The notebook pipeline drops 6.00%. | Divya / Pranav | Choose an option in `cleaning_documentation.md` §6 and record the decision |
| F-03 | High | **Dashboard lacks the planned and required content**: no churn page, High-Risk list, KPI cards or slicers; only 3 of 11 visuals have titles. | Sirisha | Complete after the churn output exists; add titles and KPI cards |
| F-04 | Medium | **Two pipelines, different numbers** (5,878 vs 5,852 customers; £20.48M vs £19.40M revenue; different segment names). Dashboard page 1 probably uses the notebook export (`Revenue` column) and page 2 the `src/` output. | Pranav | Declare one source of truth; rebuild the dashboard from it |
| F-05 | Medium | **Cancelled orders keep the original sale.** Two orders (74,215 and 80,995 units, £245,653) were cancelled within 20 minutes but still count. Customers 12346 and 16446 appear as Champions; 16446 really bought £2.90. Effect: 10 of 5,878 segments change. | Divya / Lav | Remove cancelled originals, or add an outlier rule as the notebook does |
| F-06 | Medium | **Churn horizon implemented but not formally approved.** The delivered model uses 180 + 90 days as proposed; the PRD example is 30/60 days; the definition doc still says "pending team confirmation". | Pranav / team | Record approval in `docs/WEEK3_CHURN_DEFINITION_AND_PREDICTION_PERIOD.md` |
| F-07 | ~~Medium~~ **Resolved** | `models/churn_model.pkl` and `model_metadata.json` are committed on `main`. | Pranav | Done |
| F-08 | Low | `data_quality_audit.py`, `investigate_transactions.py`, `clean_data.py`, `eda.py` (and `dataset.py`) use relative paths and fail outside the repository root. `rfm_analysis.py` and `features.py` are safe. | Divya / Lav | Use `Path(__file__).resolve().parents[1]` as in `rfm_analysis.py`. README now says to run from the root |
| F-09 | Low | `data/interim/cleaned_transactions.csv` is 95.4 MB and `customer_transactions.csv` 74.9 MB: close to GitHub's 100 MB file limit and not reproducible-only artifacts. | Pranav | Consider Git LFS, or ignore and regenerate |
| F-10 | Low | `online_retail_ii_data_cleaning_eda_validation.py` falls back to the database password `postgres`; the notebook correctly requires `PG_PASSWORD`. | Divya | Make the .py raise an error like the notebook |
| F-11 | Low | Silhouette scores use a 5,000-customer sample. Differences are at most 0.0021, ranking unchanged. | Lav | Documented in README and `metrics_documentation.md`; optionally use all customers |
| F-12 | Low | The notebook in the repository has 7 code cells with no saved output (stale). It runs cleanly when executed. | Divya | Re-run and save it |
| F-13 | Low | Non-product codes (POST, DOT, M, AMAZONFEE…) are 4.07% of revenue; one bad-debt row (£11,062) remains. | Divya | Remove or document as an accepted limitation |
| F-14 | Info | The original README referenced `assets/axlero-logo.png`, which does not exist, listed a folder layout that was out of date, and gave no dataset instructions. Fixed in the updated README. | raj4089 | Done |

## 4. Sign-off

| Gate | Decision |
|---|---|
| Segmentation deliverables (Week 1 and 2) | **Accept**: reproducible and the reported numbers are correct |
| Churn modelling (Week 3) | **Verified, conditional accept**: pipeline is leakage-safe and every reported number reproduces exactly, but the 0.75 ROC-AUC target is not met on the test set (0.7308) and full-population scoring is missing — stakeholders must explicitly accept or reject the deviation (F-15, F-16, F-06) |
| Dashboard (Week 4) | **Not accepted**: Power BI still partial (no churn page); Streamlit app is supplementary only |
| Documentation | **Accept** for delivered work; updated 2026-11-11 for the churn delivery |
