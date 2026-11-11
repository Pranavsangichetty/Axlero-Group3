# Testing Evidence and Limitations

Prepared by raj4089 (Evaluation, QA & Documentation). Baseline tests were run on 2026-11-10; the churn deliverables added to `main` (commit `65a8029`) were verified on 2026-11-11. Tests ran on a Linux machine with Python 3.12.3, using the repository exactly as delivered in `Axlero-Group3-main.zip` and the raw file `online_retail_II.csv` (94,850,204 bytes, SHA-256 `32569a66f3842a82b0d8c4d63b263c5d98a76bde5d1f65c6c01bf457e541d3a9`). This follows the plan in `docs/CLEAN_RUN_TEST_PLAN.md`. Evidence files are in `reports/qa_evidence/`.

## 1. Summary

| Area | Result |
|---|---|
| Clean install from `requirements.txt` | **Pass** (63 s, no errors) |
| All 6 documented scripts run end to end | **Pass** (about 30 s in total) |
| Regenerated outputs equal the committed outputs | **Pass** (all 18 files identical) |
| Reported metrics equal actual outputs | **Pass** for cleaning, RFM, K-Means, segments and churn; 66 PASS, 3 FAIL (all real open issues), 3 INFO, 0 BLOCKED |
| Churn model evaluation | **Verified** (2026-11-11): cohort and all selected-model metrics reproduce exactly; test ROC-AUC 0.7308 is below the 0.75 target |
| PostgreSQL notebook | **Pass** (73 of 73 cells ran, 0 errors, 33/33 findings and 25/25 validation checks) |
| Dashboard | **Partly checked** (file structure only; not opened in Power BI) |

## 2. Execution tests (test plan section 4)

| ID | Test | Command | Result | Evidence |
|---|---|---|---|---|
| T1 | Fresh virtual environment and install | `python3 -m venv`, `pip install -r requirements.txt` | Pass | `pip_freeze_clean_env.txt` |
| T2 | Audit | `python src/data_quality_audit.py` | Pass (exit 0, 3 s) | `run_data_quality_audit.log` |
| T3 | Transaction investigation | `python src/investigate_transactions.py` | Pass (exit 0, 2 s) | `run_investigate_transactions.log` |
| T4 | Cleaning | `python src/clean_data.py` | Pass (exit 0, 8 s) | `run_clean_data.log` |
| T5 | EDA | `python src/eda.py` | Pass (exit 0, 6 s) | `run_eda.log` |
| T6 | RFM and K-Means | `python src/rfm_analysis.py` | Pass (exit 0, 6 s) | `run_rfm_analysis.log` |
| T7 | Feature integration | `python src/features.py` | Pass (exit 0, 1 s) | `run_features.log` |
| T8 | Dataset missing | `python src/data_quality_audit.py` with empty `data/raw/` | Fails with `FileNotFoundError: data/raw/online_retail_II.csv` (expected, now documented) | terminal output |
| T9 | Run from another folder | `cd /tmp && python <repo>/src/clean_data.py` | **Fails** with `FileNotFoundError` (4 scripts use paths relative to the current folder; `rfm_analysis.py` and `features.py` do not) | terminal output |
| T10 | RFM and features without raw data | `rfm_analysis.py`, `features.py` with `data/raw/` empty | Pass | terminal output |
| T11 | Package versions | newest releases installed | Pass: pandas 3.1.1, numpy 2.5.4, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2 produce the same results | `pip_freeze_clean_env.txt` |
| T12 | PostgreSQL notebook | `Online_Retail_II_Final_Complete_Fixed.ipynb`, all cells, PostgreSQL 16 | Pass in 46 s: 0 errors; the saved notebook in the repository still has 7 cells with no saved output | notebook run |
| T13 | Churn dataset rebuild (2026-11-11) | `python src/churn_dataset.py` | Pass: 2,724 customers, 1,315 churned, 48.27% — identical to the committed report | run output, `churn_metric_verification.csv` |
| T14 | Churn model retraining (2026-11-11) | `python src/churn_prediction.py` | Pass in 21 s. Selected Logistic Regression: all 6 metrics, best parameters and confusion matrix **identical** to the committed `churn_model_comparison.csv` and `model_metadata.json`. Random Forest within 0.004 (not selected) | `qa_evidence/churn_metric_verification.csv`, `qa_evidence/rerun_churn/` |
| T15 | Their validation suite (2026-11-11) | `python src/validate_churn_model.py` | Pass: 28 of 28 checks on the independently retrained model | `churn_model_validation_results.csv` |
| T16 | Raj's verification tool on real predictions (2026-11-11) | `python src/modeling/verify_churn_metrics.py --predictions qa_evidence/churn_test_predictions.csv --reported qa_evidence/churn_reported_metrics.csv` | 9 of 9 reported metrics PASS; PRD check ROC-AUC ≥ 0.75 **FAIL** (0.7308); no leakage or imbalance warnings | tool output |

## 3. Reproducibility of reported results

All regenerated files were compared with the committed files (`regeneration_comparison.csv`): the 9 report CSV files, 5 processed CSV files, `cleaned_transactions.csv`, both Markdown reports and the metadata JSON are identical in values. PNG charts were regenerated but not compared pixel by pixel.

## 4. Metric verification (`src/verify_reported_metrics.py`)

70 checks, saved in `metric_verification.csv`.

| Result | Count | Meaning |
|---|---:|---|
| PASS | 64 | Reported value equals the independently computed value |
| FAIL | 2 | A10: data loss 5.57% against the 5% target. F2: no churn page in the dashboard |
| BLOCKED | 2 | No churn model, so churn code, metrics and ROC-AUC ≥ 0.75 cannot be tested |
| INFO | 2 | k = 4 is not the highest-silhouette choice; dashboard has 2 of 4 planned pages |

What was re-computed from scratch: every row of the cleaning log and the README cleaning table; the audit counts of the raw file; Recency, Frequency and Monetary for all 5,878 customers; inertia and silhouette for k = 2 to 8; the k = 4 cluster labels (identical for all customers); every figure in the README segment table and in the Week 2 segment table (customers, percentage, three averages); reconciliation of segment totals with the transaction file.

## 5. Churn evaluation: verified (2026-11-11)

On 2026-11-10 nothing was available to verify (`models/` and `src/modeling/` contained only `.gitkeep`). The churn deliverables then landed on `main` (PR #12 and the team-lead integration). On 2026-11-11 I verified them end to end:

1. **Cohort reproduction.** `src/churn_dataset.py` re-run from the raw data: 2,724 customers, 1,315 churned, 1,409 active, 48.27% churn rate — identical to the committed evaluation report.
2. **Leakage review.** Features come only from 2011-01-02 to 2011-06-30; the label only from 2011-07-01 to 2011-09-28; `Future_Orders_90d` and `CustomerID` are excluded from training, and `predict_customers.py` refuses inputs that contain them. The design is leakage-safe. The RFM full-history table is (correctly) not used.
3. **Metric reproduction.** `src/churn_prediction.py` re-run (same seed): the selected Logistic Regression reproduces **exactly** — CV ROC-AUC 0.763876, test accuracy 0.680734, precision 0.652921, recall 0.722433, F1 0.685921, ROC-AUC 0.730807, confusion matrix [181, 101, 73, 190], parameters C=0.1. Random Forest differs by at most 0.004 (one test customer flips), consistent with environment-level nondeterminism; it was not selected. Evidence: `qa_evidence/churn_metric_verification.csv`.
4. **Their validation suite.** `src/validate_churn_model.py`: 28/28 checks pass on my independently retrained model against the committed metadata.
5. **My verification tool on real data.** I exported the 545 held-out test predictions with true labels (`qa_evidence/churn_test_predictions.csv`) and ran `src/modeling/verify_churn_metrics.py`: all 9 reported metrics PASS; the PRD check **ROC-AUC ≥ 0.75 FAILS at 0.7308**; no leakage warning (AUC far from 0.98) and no imbalance warning (48.3%).

**Conclusion:** the reported churn numbers are honest and fully reproducible, but the PRD performance target is not met on the held-out test set, and the committed prediction CSV covers only 10 demonstration customers.

## 6. Limitations of this testing

- Churn evaluation covers one historical cohort and one holdout split; out-of-time (temporal) validation has not been run. Random Forest results are environment-sensitive at the third decimal.
- Power BI Desktop was not available: dashboard values, filters, navigation and refresh were not tested, and there are no screenshots.
- Git history was not available (the zip has no `.git` folder), so the commit-day requirements in the handbook were not checked.
- The raw file was supplied separately as a CSV; the original UCI download is an Excel workbook, so the conversion step cannot be tested.
- Tests ran on Linux only; Windows paths and Power BI were not tried.
- Verification shows that the code reproduces the reported numbers; it does not prove that the cleaning and segmentation choices are the best ones (see `qa_checklist.md`, findings).
- The PostgreSQL notebook was tested against a local PostgreSQL 16 server with a test password.
