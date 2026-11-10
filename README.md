# Retail & E-commerce Customer Segmentation and Churn Prediction

## Project Overview

This project analyzes retail and e-commerce transaction data to understand customer purchasing behaviour, identify valuable customer groups, and prepare a customer churn prediction system.

The project uses data analytics and machine learning techniques to support customer retention, targeted marketing campaigns, and data-driven business decisions.

**Project Domain:** Retail & E-commerce  
**Organization:** Axlero – Innovating Solutions  
**Project:** Customer Segmentation and Churn Prediction  
**Dataset:** Online Retail II  
**Technology:** Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, K-Means, Power BI

---

## Project Status at a Glance

Status was checked by re-running the code on 2026-11-10 (see [`reports/testing_evidence.md`](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/testing_evidence.md)).

| Area | Status | Evidence |
|---|---|---|
| Data audit, cleaning, EDA (Week 1) | Complete and reproducible | All outputs regenerate identically from the raw CSV |
| RFM and K-Means segmentation (Week 2) | Complete and reproducible | 64 automated checks pass (`src/verify_reported_metrics.py`) |
| Churn prediction (Week 3) | **Not in this repository** | No churn code, model file, predictions or metrics found |
| Power BI dashboard (Week 4) | Partial | 2 pages (sales overview, RFM segments); no churn page |
| Final documentation | Complete for delivered work | `reports/final_project_report.md` |

Open issues are listed in [`reports/qa_checklist.md`](reports/qa_checklist.md).

---

## Project Objectives

- Analyze customer purchasing behaviour using transaction data.
- Identify and handle missing values, duplicates, cancellations, and invalid transactions.
- Perform Exploratory Data Analysis (EDA).
- Calculate Recency, Frequency, and Monetary (RFM) metrics.
- Apply K-Means clustering to identify customer segments.
- Develop customer churn prediction models (target ROC-AUC of at least 0.75).
- Create an interactive business dashboard.
- Provide actionable marketing and customer retention recommendations.

---

## Dataset

The project uses the **Online Retail II** dataset (UCI Machine Learning Repository), a UK online gift retailer's transactions from 1 December 2009 to 9 December 2011.

The raw data is **not stored in this repository** (it is git-ignored). Before running anything, place the single CSV file at:

```text
data/raw/online_retail_II.csv
```

The UCI download is an Excel workbook with two yearly sheets. Combine both sheets into one CSV with the 8 columns below, or use a CSV copy of the same dataset. Check the file before use:

| Check | Expected value |
|---|---|
| Rows | 1,067,371 |
| Columns | 8 |
| File size used in testing | 94,850,204 bytes |
| SHA-256 of the file used in testing | `32569a66f3842a82b0d8c4d63b263c5d98a76bde5d1f65c6c01bf457e541d3a9` |

| Attribute | Description |
|---|---|
| Invoice | Invoice/order identifier (starts with `C` for a cancellation) |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of products purchased |
| InvoiceDate | Transaction date and time |
| Price | Unit price |
| Customer ID | Customer identifier (missing for guest orders) |
| Country | Customer's country |

A `TotalPrice` feature is created: `TotalPrice = Quantity × Price`.

The full column-by-column description of every file is in [`reports/data_dictionary.md`](reports/data_dictionary.md).

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python 3.9 or newer (tested with 3.12.3) |
| Data Manipulation | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn, Power BI Desktop |
| Machine Learning | Scikit-learn |
| Clustering | K-Means |
| Database (optional notebook route) | PostgreSQL, SQLAlchemy, psycopg2 |
| Version Control | Git and GitHub |
| Development Environment | Jupyter Notebook, VS Code |

---

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Pranavsangichetty/Axlero-Group3.git
cd Axlero-Group3
```

### 2. Create and activate a virtual environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` has no version numbers, so pip installs the newest releases. To install the exact versions used in testing, use `pip install -r requirements-tested.txt` instead (it pins every package in `requirements.txt` to the version used in testing).

### 4. Add the dataset

Place `online_retail_II.csv` in `data/raw/` (see the Dataset section).

### 5. Run the pipeline

**Run every command from the repository root folder.** `data_quality_audit.py`, `investigate_transactions.py`, `clean_data.py` and `eda.py` use paths relative to the current folder and fail if started from another folder.

```bash
python src/data_quality_audit.py        # Week 1: audit of the raw data
python src/investigate_transactions.py  # Week 1: cancellations, duplicates, zero prices
python src/clean_data.py                # Week 1: cleaning -> data/interim and data/processed
python src/eda.py                       # Week 1: six charts in reports/figures/
python src/rfm_analysis.py              # Week 2: RFM, K-Means, segments
python src/features.py                  # Week 2: integrated customer_rfm_features.csv
```

Order matters: each step uses the files created by the step before. Together they take about 30 seconds.

| Script | Main outputs |
|---|---|
| `data_quality_audit.py` | `reports/data_quality_summary.csv`, `reports/missing_values_report.csv` |
| `investigate_transactions.py` | sample files in `reports/` (duplicates, negative quantities, zero prices, cancellations) |
| `clean_data.py` | `data/interim/cleaned_transactions.csv`, `data/processed/customer_transactions.csv`, `reports/cleaning_log.csv`, `reports/cleaning_summary.csv` |
| `eda.py` | `reports/figures/*.png`, `reports/monthly_revenue.csv`, `reports/country_revenue_top10.csv`, `reports/customer_revenue_top10.csv` |
| `rfm_analysis.py` | `data/processed/customer_rfm.csv`, `customer_rfm_scaled.csv`, `customer_segments.csv`, `reports/cluster_evaluation.csv`, `reports/customer_segment_profile.csv`, three PNG charts |
| `features.py` | `data/processed/customer_rfm_features.csv` and its metadata, `reports/rfm_feature_dictionary.md`, `reports/rfm_validation_report.md` |

If the dataset is missing, the first script stops with `FileNotFoundError: data/raw/online_retail_II.csv`. `rfm_analysis.py` and `features.py` only need the files in `data/processed/` and can be run without the raw dataset.

### 6. Verify the results

```bash
python src/verify_reported_metrics.py
```

This re-computes the key numbers and compares them with the reports and with this README. It prints every check that is not a plain PASS and saves all results to `reports/qa_evidence/metric_verification.csv`. The last run gave PASS = 64, FAIL = 2, WARN = 0, INFO = 2, BLOCKED = 2. The two FAIL results are real open issues (the 5% data-loss target and the missing churn dashboard page), not script errors. The script exits with code 1 while a FAIL remains.

### 7. Churn model verification (when delivered)

When the churn model is delivered, check its reported metrics against its saved predictions:

```bash
python src/modeling/verify_churn_metrics.py \
    --predictions data/processed/churn_predictions.csv \
    --reported reports/churn_metrics.csv
python src/modeling/verify_churn_metrics.py --self-test    # tool test on synthetic data
```

The expected file formats are described at the top of `src/modeling/verify_churn_metrics.py`.

### Optional: PostgreSQL notebook route

`Online_Retail_II_Final_Complete_Fixed.ipynb` repeats the cleaning, EDA, RFM and K-Means steps with PostgreSQL. It uses stricter cleaning, so its numbers differ from the `src/` scripts (see [`reports/cleaning_documentation.md`](reports/cleaning_documentation.md)). To run it:

1. Install and start PostgreSQL, and keep `online_retail_II.csv` in the same folder as the notebook.
2. Set the database password as an environment variable (never write it into a file):
   - macOS / Linux: `export PG_PASSWORD="your-password"`
   - Windows PowerShell: `$env:PG_PASSWORD="your-password"`
3. Open the notebook and use **Restart & Run All**. The notebook stops with an error if any of its validation checks fails.

The stand-alone export `online_retail_ii_data_cleaning_eda_validation.py` falls back to the password `postgres` when `PG_PASSWORD` is not set; always set the variable.

---

## Project Progress

### Week 1 – Data Understanding, Cleaning and EDA

**Status: Completed and verified**

Activities performed:

1. Dataset exploration and understanding.
2. Data quality audit.
3. Missing-value analysis.
4. Duplicate transaction identification.
5. Cancellation transaction investigation.
6. Removal of invalid quantity and price records.
7. Creation of the `TotalPrice` feature.
8. Customer-level transaction dataset preparation.
9. Exploratory Data Analysis.

**Cleaning results:**

| Description | Records |
|---|---:|
| Original transactions | 1,067,371 |
| After exact duplicate removal | 1,033,036 |
| After cancellation exclusion | 1,013,932 |
| After positive quantity filtering | 1,010,539 |
| Final cleaned transactions | 1,007,913 |
| Customer-linked transactions | 779,425 |
| Identified customers | 5,878 |

In total 59,458 rows (5.57%) were removed. The project requirement is to drop no more than 5%, so this target is **not met** (see Limitations).

**EDA visualizations generated:**

- Monthly orders analysis.
- Monthly revenue analysis.
- Order value distribution.
- Top countries by revenue.
- Top customers by revenue.
- Top products by quantity.

### Week 2 – RFM Analysis and Customer Segmentation

**Status: Completed and verified**

RFM analysis was performed using three customer behaviour metrics:

- **Recency:** Number of days since the customer's most recent purchase.
- **Frequency:** Number of distinct invoices/orders.
- **Monetary:** Total customer spending.

Log transformation and StandardScaler were applied before K-Means clustering.

K-Means was evaluated for cluster counts from 2 to 8 using inertia and Silhouette Score. The silhouette scores below are estimates calculated on a random sample of 5,000 of the 5,878 customers (`sample_size=5000` in `rfm_analysis.py`). Scores on all customers differ by at most 0.0021 and give the same ranking of k.

**Model evaluation:**

| Clusters (k) | Silhouette Score |
|---:|---:|
| 2 | 0.4407 |
| 3 | 0.3499 |
| 4 | 0.3666 |
| 5 | 0.3455 |
| 6 | 0.3361 |
| 7 | 0.3034 |
| 8 | 0.2943 |

Four clusters were selected as a business-oriented solution to provide more actionable customer groups. The two-cluster solution achieved the highest Silhouette Score, so the four-cluster selection represents a trade-off between cluster separation and business usefulness.

**Identified customer segments:**

| Customer Segment | Customers | Percentage |
|---|---:|---:|
| Champions | 1,204 | 20.48% |
| Loyal High-Value | 1,455 | 24.75% |
| Recent Customers | 1,261 | 21.45% |
| At-Risk / Hibernating | 1,958 | 33.31% |
| **Total** | **5,878** | **100%** |

**Marketing recommendations:**

- Champions: VIP rewards, exclusive offers, and referral campaigns.
- Loyal High-Value: Personalized win-back campaigns and loyalty reminders.
- Recent Customers: Second-purchase incentives and product recommendations.
- At-Risk / Hibernating: Re-engagement campaigns and targeted offers.

These recommendations are interpretations of the segment profiles, not model guarantees.

### Week 3 – Customer Churn Prediction

**Status: Not delivered in this repository**

`models/` and `src/modeling/` contain no model, code, predictions or metrics. The churn definition (no purchase in the next 90 days after a 180-day observation window) is still marked *pending team confirmation* in `docs/WEEK3_CHURN_DEFINITION_AND_PREDICTION_PERIOD.md`. The Project Requirements Document example uses 30 or 60 days, so the team must confirm the final horizon.

Planned activities:

- Define a leakage-safe customer churn target.
- Prepare features for churn prediction at a historical cutoff date.
- Handle class imbalance where necessary.
- Train Logistic Regression and Random Forest models.
- Evaluate models using Precision, Recall, F1-score, and ROC-AUC (target: ROC-AUC of at least 0.75).
- Save the selected model and evaluation results.

### Week 4 – Dashboard and Final Documentation

**Status: Partial**

- `Customer_Segmentation_Dashboard.pbix` has 2 pages: `Page 1` (sales overview) and `RFM & Customer Segments`.
- No churn page, KPI cards or slicers exist yet, although `reports/Dashboard_Documentation.docx` plans them.
- Final report, metric documentation, data dictionary, cleaning documentation, dashboard guide and QA checklist are in `reports/`.

---

## Dashboard Usage and Refresh

Open `Customer_Segmentation_Dashboard.pbix` with Power BI Desktop (Windows). To refresh it after re-running the pipeline:

1. Re-run steps 5 and 6 above.
2. In Power BI Desktop, check **Transform data → Data source settings** that each table points to the regenerated file.
3. Click **Home → Refresh**.
4. Compare the values with the reference table in [`reports/dashboard_guide.md`](reports/dashboard_guide.md).

Full usage notes, the page and visual inventory, and the known gaps are in [`reports/dashboard_guide.md`](reports/dashboard_guide.md).

---

## Repository Structure

```text
Axlero-Group3/
│
├── data/
│   ├── raw/                     (place online_retail_II.csv here; git-ignored)
│   ├── interim/
│   │   └── cleaned_transactions.csv
│   └── processed/
│       ├── customer_transactions.csv
│       ├── customer_rfm.csv
│       ├── customer_rfm_scaled.csv
│       ├── customer_segments.csv
│       ├── customer_rfm_features.csv
│       └── customer_rfm_features_metadata.json
│
├── notebooks/
│
├── src/
│   ├── dataset.py
│   ├── data_quality_audit.py
│   ├── investigate_transactions.py
│   ├── clean_data.py
│   ├── eda.py
│   ├── rfm_analysis.py
│   ├── features.py
│   ├── verify_reported_metrics.py
│   └── modeling/
│       └── verify_churn_metrics.py
│
├── models/                      (empty: no churn model delivered yet)
├── dashboard/                   (empty; the .pbix is in the repository root)
│
├── reports/
│   ├── figures/
│   ├── qa_evidence/             (verification results and run logs)
│   ├── final_project_report.md
│   ├── qa_checklist.md
│   ├── metrics_documentation.md
│   ├── testing_evidence.md
│   ├── data_dictionary.md
│   ├── cleaning_documentation.md
│   ├── dashboard_guide.md
│   ├── week1_progress_report.md
│   ├── week2_progress_report.md
│   ├── cluster_evaluation.csv
│   ├── customer_segment_profile.csv
│   └── customer_segment_recommendations.csv
│
├── docs/                        (architecture, contracts, checklists, work logs)
├── Customer_Segmentation_Dashboard.pbix
├── Online_Retail_II_Final_Complete_Fixed.ipynb
├── requirements.txt
├── requirements-tested.txt
├── .gitignore
└── README.md
```

---

## Documentation Index

| Document | Purpose |
|---|---|
| [`reports/final_project_report.md`](reports/final_project_report.md) | Final report: method, results, status, limitations, recommendations |
| [`reports/metrics_documentation.md`](reports/metrics_documentation.md) | Every metric: definition, meaning, current value, verification status |
| [`reports/data_dictionary.md`](reports/data_dictionary.md) | Columns and types of every dataset |
| [`reports/cleaning_documentation.md`](reports/cleaning_documentation.md) | Cleaning rules, order, row counts and open data issues |
| [`reports/dashboard_guide.md`](reports/dashboard_guide.md) | Dashboard contents, usage, refresh steps and reference KPI values |
| [`reports/testing_evidence.md`](reports/testing_evidence.md) | Test commands, results and evidence files |
| [`reports/qa_checklist.md`](reports/qa_checklist.md) | QA checklist and list of open findings |
| [`docs/`](docs/) | Architecture, module contracts, branch review and clean-run test plan |

---

## Limitations

- **Data loss above the target.** 5.57% of the original rows are removed by the `src/` pipeline (6.00% by the notebook pipeline); the project requirement is a maximum of 5%.
- **Customer IDs.** 22.77% of the original rows have no Customer ID. They stay in the sales figures but are excluded from customer-level analysis, so RFM covers 5,878 customers and £17.37M of the £20.48M total revenue (84.9%).
- **Cancelled orders.** The `src/` cleaning drops cancellation rows but keeps the original orders they cancelled. Two orders (74,215 and 80,995 units, cancelled minutes later) are still counted and make customers 12346 and 16446 appear as Champions. Excluding them changes the segment of 10 of 5,878 customers.
- **Revenue is gross.** Revenue is the sum of `Quantity × Price` for completed sales; cancellations and returns are not subtracted. It also includes postage, manual and fee codes (4.07% of revenue).
- **Silhouette scores are sample estimates** (5,000 of 5,878 customers).
- **k = 4 is a business choice.** k = 2 has the highest silhouette score.
- **RFM is a full-history snapshot.** It is for descriptive segmentation only and must not be used to train a churn model (data leakage). Recompute features at a historical cutoff for churn modelling.
- **Two pipelines give different numbers.** The `src/` scripts (5,878 customers) and the PostgreSQL notebook (5,852 customers) apply different cleaning rules and name the clusters differently. The dashboard and this README use the `src/` results.
- Monetary values use the dataset's recorded price units; the currency has not been independently verified.
- Churn prediction is not delivered, and the dashboard has no churn view.

---

## Future Scope

- Complete and validate the churn prediction models.
- Add a churn-risk page and a High-Risk customer list to the dashboard.
- Agree one cleaning pipeline and bring data loss within the 5% target.
- Improve customer segmentation using additional behavioural features.
- Develop personalized retention strategies.

---

## GitHub Repository

Repository: https://github.com/Pranavsangichetty/Axlero-Group3

Working branch: `Lav-Kumar, Rishuraj`

---

## Acknowledgement

This project is developed as part of the Retail & E-commerce Customer Segmentation and Churn Prediction project with Axlero – Innovating Solutions.

**Project objective:** Transform retail transaction data into meaningful customer insights and actionable business strategies.
