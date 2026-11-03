# Retail & E-commerce Customer Segmentation and Churn Prediction

## Project Overview

This project focuses on analyzing retail and e-commerce transaction data to understand customer purchasing behaviour, identify valuable customer groups, and develop a customer churn prediction system.

The project uses data analytics and machine learning techniques to support customer retention, targeted marketing campaigns, and data-driven business decisions.

**Project Domain:** Retail & E-commerce  
**Organization:** Axlero – Innovating Solutions  
**Project:** Customer Segmentation and Churn Prediction  
**Dataset:** Online Retail II  
**Technology:** Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, K-Means

---

## Project Objectives

- Analyze customer purchasing behaviour using transaction data.
- Identify and handle missing values, duplicates, cancellations, and invalid transactions.
- Perform Exploratory Data Analysis (EDA).
- Calculate Recency, Frequency, and Monetary (RFM) metrics.
- Apply K-Means clustering to identify customer segments.
- Develop customer churn prediction models.
- Create an interactive business dashboard.
- Provide actionable marketing and customer retention recommendations.

---

## Dataset Description

The project uses the Online Retail II dataset.

The original dataset contains:

| Attribute | Description |
|---|---|
| Invoice | Invoice/order identifier |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of products purchased |
| InvoiceDate | Transaction date and time |
| Price | Unit price |
| Customer ID | Customer identifier |
| Country | Customer's country |

The dataset originally contained **1,067,371 transaction records** and 8 columns.

A `TotalPrice` feature was created using:

`TotalPrice = Quantity × Price`

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Manipulation | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Clustering | K-Means |
| Data Processing | Python scripts |
| Version Control | Git and GitHub |
| Development Environment | Jupyter Notebook, VS Code |

---

## Project Progress

### Week 1 – Data Understanding, Cleaning and EDA

**Status: Completed**

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

**EDA visualizations generated:**

- Monthly orders analysis.
- Monthly revenue analysis.
- Order value distribution.
- Top countries by revenue.
- Top customers by revenue.
- Top products by quantity.

### Week 2 – RFM Analysis and Customer Segmentation

**Status: Completed**

RFM analysis was performed using three customer behaviour metrics:

- **Recency:** Number of days since the customer's most recent purchase.
- **Frequency:** Number of distinct invoices/orders.
- **Monetary:** Total customer spending.

Log transformation and StandardScaler were applied before K-Means clustering.

K-Means was evaluated for cluster counts from 2 to 8 using inertia and Silhouette Score.

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

### Week 3 – Customer Churn Prediction

**Status: Planned / In Progress**

Planned activities:

- Define a leakage-safe customer churn target.
- Prepare features for churn prediction.
- Handle class imbalance where necessary.
- Train Logistic Regression and Random Forest models.
- Evaluate models using Precision, Recall, F1-score, and ROC-AUC.
- Save the selected model and evaluation results.

### Week 4 – Dashboard and Final Documentation

**Status: Planned / In Progress**

Planned activities:

- Develop a Tableau or Power BI dashboard.
- Build an executive overview of business KPIs.
- Visualize customer segments.
- Present churn risk distribution and customer details.
- Prepare final technical documentation and project report.

---

## Repository Structure

```text
Axlero-Group3/
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│       ├── customer_transactions.csv
│       ├── customer_rfm.csv
│       ├── customer_rfm_scaled.csv
│       └── customer_segments.csv
│
├── notebooks/
│
├── src/
│   ├── dataset.py
│   ├── features.py
│   ├── data_quality_audit.py
│   ├── investigate_transactions.py
│   ├── clean_data.py
│   ├── eda.py
│   └── rfm_analysis.py
│
├── models/
│
├── dashboard/
│
├── reports/
│   ├── figures/
│   ├── week1_progress_report.md
│   ├── week2_progress_report.md
│   ├── cluster_evaluation.csv
│   ├── customer_segment_profile.csv
│   └── customer_segment_recommendations.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Pranavsangichetty/Axlero-Group3.git
cd Axlero-Group3
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

For macOS/Linux:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Week 1 scripts

```bash
python src/data_quality_audit.py
python src/investigate_transactions.py
python src/clean_data.py
python src/eda.py
```

### 6. Run Week 2 analysis

```bash
python src/rfm_analysis.py
```

Ensure the required dataset is available in the expected `data/` directory before running the scripts.

---

## Key Deliverables

| Deliverable | Location |
|---|---|
| Data quality analysis | `reports/` |
| Cleaned transaction data | `data/interim/` |
| Customer transaction data | `data/processed/` |
| EDA visualizations | `reports/figures/` |
| RFM analysis | `src/rfm_analysis.py` |
| Customer segments | `data/processed/customer_segments.csv` |
| Cluster evaluation | `reports/cluster_evaluation.csv` |
| Segment recommendations | `reports/customer_segment_recommendations.csv` |
| Week 1 report | `reports/week1_progress_report.md` |
| Week 2 report | `reports/week2_progress_report.md` |

---

## Limitations

- Customer IDs are missing in a portion of the original transaction dataset.
- Approximately 5.57% of original records were removed during the documented cleaning process.
- RFM segmentation includes 5,878 customers with identifiable customer information.
- The four-cluster solution is a business-oriented selection rather than the highest Silhouette Score solution.
- Monetary values use the recorded dataset price units; the currency has not been independently verified.
- Churn prediction and dashboard development remain future project activities until implemented and validated.

---

## Future Scope

- Improve customer segmentation using additional behavioural features.
- Develop and validate churn prediction models.
- Identify customers with high churn risk.
- Build interactive dashboards for business users.
- Develop personalized retention strategies.
- Support data-driven marketing decisions.

---

## GitHub Repository

Repository: https://github.com/Pranavsangichetty/Axlero-Group3

Working branch: `Lav-Kumar`

---

## Acknowledgement

This project is developed as part of the Retail & E-commerce Customer Segmentation and Churn Prediction project with Axlero – Innovating Solutions.

**Project objective:** Transform retail transaction data into meaningful customer insights and actionable business strategies.

<p align="center">
  <img src="assets/axlero-logo.png"
       alt="Axlero Logo"
       width="350"/>
</p>
