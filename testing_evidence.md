# Testing Evidence and Limitations

Prepared by raj4089 (Evaluation, QA & Documentation). Tests were run on 2026-11-10 on a Linux machine with Python 3.12.3, using the repository exactly as delivered in `Axlero-Group3-main.zip` and the raw file `online_retail_II.csv` (94,850,204 bytes, SHA-256 `32569a66f3842a82b0d8c4d63b263c5d98a76bde5d1f65c6c01bf457e541d3a9`). This follows the plan in `docs/CLEAN_RUN_TEST_PLAN.md`. Evidence files are in `reports/qa_evidence/`.

## 1. Summary

| Area | Result |
|---|---|
| Clean install from `requirements.txt` | **Pass** (63 s, no errors) |
| All 6 documented scripts run end to end | **Pass** (about 30 s in total) |
| Regenerated outputs equal the committed outputs | **Pass** (all 18 files identical) |
| Reported metrics equal actual outputs | **Pass** for cleaning, RFM, K-Means and segment numbers; 64 PASS, 2 FAIL, 2 BLOCKED, 2 INFO |
| Churn model evaluation | **Blocked** (nothing delivered) |
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

## 5. Churn evaluation (Nivesh243): blocked

The task asks to verify the evaluation results provided by Nivesh. Nothing was available to verify: `models/` and `src/modeling/` contain only `.gitkeep`, and no prediction file, metrics report or churn code exists. The churn definition document is still marked "Pending team confirmation". I therefore did **not** report any churn metric. What was prepared instead:

- `src/modeling/verify_churn_metrics.py`: re-computes the metrics from saved predictions and compares them with the report. Tested on synthetic data only: it passes a correct report, fails a tampered report (exit code 1), and stops with a clear message when files are missing. Synthetic results are not project results.
- Metric definitions and the project target in `metrics_documentation.md`.

## 6. Limitations of this testing

- The churn model, its evaluation and its leakage safety could not be tested.
- Power BI Desktop was not available: dashboard values, filters, navigation and refresh were not tested, and there are no screenshots.
- Git history was not available (the zip has no `.git` folder), so the commit-day requirements in the handbook were not checked.
- The raw file was supplied separately as a CSV; the original UCI download is an Excel workbook, so the conversion step cannot be tested.
- Tests ran on Linux only; Windows paths and Power BI were not tried.
- Verification shows that the code reproduces the reported numbers; it does not prove that the cleaning and segmentation choices are the best ones (see `qa_checklist.md`, findings).
- The PostgreSQL notebook was tested against a local PostgreSQL 16 server with a test password.
