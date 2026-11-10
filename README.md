# Retail & E-commerce Customer Segmentation and Churn Prediction

## 1. Project Overview

This project analyzes retail transaction data to understand customer purchasing behaviour, identify valuable customer segments, and predict customer churn.

The project uses data cleaning, exploratory data analysis (EDA), RFM analysis, K-Means clustering, machine learning, and an interactive dashboard to support customer retention and data-driven business decisions.

**Project Domain:** Retail & E-commerce  
**Organization:** Axlero – Innovating Solutions  
**Project:** Customer Segmentation and Churn Prediction  
**Dataset:** Online Retail II  
**Working Branch:** `Lav-Kumar`

## 2. Project Objectives

- Analyze customer purchasing behaviour.
- Identify and handle missing values, duplicates, cancellations, and invalid transactions.
- Perform exploratory data analysis.
- Calculate Recency, Frequency, and Monetary (RFM) metrics.
- Apply K-Means clustering to identify customer segments.
- Develop and evaluate customer churn prediction models.
- Build an interactive business dashboard.
- Generate customer retention recommendations.

## 3. Dataset Description

The project uses the Online Retail II transaction dataset.

The original dataset contains 1,067,371 records and eight columns.

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

A `TotalPrice` feature was created:

`TotalPrice = Quantity × Price`

## 4. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn |
| Clustering | K-Means |
| Dashboard | Streamlit |
| Model Storage | Joblib / Pickle |
| Version Control | Git and GitHub |

## 5. Project Progress and Deliverables

### Week 1 – Data Cleaning and Exploratory Data Analysis

**Status: Completed**

Activities:
1. Dataset exploration and understanding.
2. Data quality audit.
3. Missing-value analysis.
4. Duplicate transaction identification.
5. Cancellation transaction investigation.
6. Removal of invalid quantity and price records.
7. Creation of the `TotalPrice` feature.
8. Customer-level transaction dataset preparation.
9. Exploratory data analysis and visualization.

#### Data cleaning results

| Description | Records |
|---|---:|
| Original transactions | 1,067,371 |
| After exact duplicate removal | 1,033,036 |
| After cancellation exclusion | 1,013,932 |
| After positive quantity filtering | 1,010,539 |
| Final cleaned transactions | 1,007,913 |
| Customer-linked transactions | 779,425 |
| Identified customers | 5,878 |

Approximately 5.57% of original records were removed during the documented cleaning pipeline.

#### EDA summary

| Metric | Result |
|---|---:|
| Cleaned transactions | 1,007,913 |
| Total revenue | 20,476,260.45 |
| Orders | 40,077 |
| Customers | 5,878 |
| Products | 4,916 |
| Countries | 43 |

Visualizations include:
- Monthly orders.
- Monthly revenue.
- Order value distribution.
- Top countries by revenue.
- Top customers by revenue.
- Top products by quantity.

Main outputs:
- `data/interim/cleaned_transactions.csv`
- `data/processed/customer_transactions.csv`
- `reports/cleaning_log.csv`
- `reports/cleaning_summary.csv`
- `reports/week1_progress_report.md`
- `reports/figures/`

### Week 2 – RFM Analysis and Customer Segmentation

**Status: Completed**

RFM analysis was performed using:

- **Recency:** Days since the customer's most recent purchase.
- **Frequency:** Number of distinct invoices.
- **Monetary:** Total customer spending.

Log transformation and StandardScaler were applied before K-Means clustering.

K-Means was evaluated for cluster counts from 2 to 8.

#### Cluster evaluation

| Clusters (k) | Silhouette Score |
|---:|---:|
| 2 | 0.4407 |
| 3 | 0.3499 |
| 4 | 0.3666 |
| 5 | 0.3455 |
| 6 | 0.3361 |
| 7 | 0.3034 |
| 8 | 0.2943 |

Four clusters were selected as a business-oriented solution. Although k=2 achieved the highest Silhouette Score, k=4 provided four more actionable customer groups.

#### Identified customer segments

| Customer Segment | Customers | Percentage |
|---|---:|---:|
| Champions | 1,204 | 20.48% |
| Loyal High-Value | 1,455 | 24.75% |
| Recent Customers | 1,261 | 21.45% |
| At-Risk / Hibernating | 1,958 | 33.31% |
| **Total** | **5,878** | **100%** |

#### Business recommendations

- **Champions:** VIP rewards, exclusive offers, and referral campaigns.
- **Loyal High-Value:** Personalized loyalty campaigns and engagement reminders.
- **Recent Customers:** Second-purchase incentives and product recommendations.
- **At-Risk / Hibernating:** Re-engagement campaigns and targeted offers.

Main outputs:
- `data/processed/customer_rfm.csv`
- `data/processed/customer_rfm_scaled.csv`
- `data/processed/customer_segments.csv`
- `data/processed/customer_rfm_features.csv`
- `reports/cluster_evaluation.csv`
- `reports/customer_segment_profile.csv`
- `reports/customer_segment_recommendations.csv`
- `reports/week2_progress_report.md`

### Week 3 – Customer Churn Prediction

**Status: Completed**

A historical customer cohort was prepared to develop a leakage-safe churn prediction model.

#### Churn definition

- Feature window: 180 days.
- Observation window: 90 days.
- Historical cohort: 2,724 customers.
- Churned customers: 1,315.
- Active customers: 1,409.
- Inactivity-based churn rate: 48.27%.

A customer was labelled as churned if they made no purchase during the 90-day observation period.

This is an inactivity-based proxy, not proof of permanent customer loss.

#### Feature engineering and leakage prevention

Six historical features were used:
- Recency
- Frequency
- Monetary
- Total_Quantity
- Unique_Products
- Average_Order_Value

`CustomerID` and `Future_Orders_90d` were excluded from model training to prevent leakage.

#### Models evaluated

1. Logistic Regression
2. Random Forest

Logistic Regression was selected based on its higher mean cross-validation ROC-AUC score.

#### Selected model performance

| Metric | Test Result |
|---|---:|
| Accuracy | 0.6807 |
| Precision | 0.6529 |
| Recall | 0.7224 |
| F1-score | 0.6859 |
| ROC-AUC | 0.7308 |

The held-out test set contained 545 customers.

#### Prediction workflow

The script `src/predict_customers.py` loads the saved model, validates input features, generates churn probabilities, and assigns illustrative risk categories.

A 10-customer sample scoring workflow was tested. This is a demonstration and not a full-population production scoring output.

Main outputs:
- `data/processed/historical_churn_dataset.csv`
- `data/processed/historical_churn_dataset_metadata.json`
- `models/churn_model.pkl`
- `models/model_metadata.json`
- `reports/churn_model_comparison.csv`
- `reports/churn_model_evaluation.md`
- `reports/churn_model_validation_report.md`
- `reports/customer_churn_predictions.csv`
- `reports/figures/churn_confusion_matrix.png`
- `reports/figures/churn_roc_curve.png`

### Week 4 – Interactive Dashboard and Final QA

**Status: Completed**

An interactive dashboard was developed using Streamlit and Plotly.

#### Dashboard sections

1. **Executive Overview**
   - Customer and transaction KPIs.
   - Revenue and business overview charts.

2. **Customer Segmentation**
   - Customer segment distribution.
   - Segment-level metrics and profiles.
   - Segment filtering.

3. **Churn Analysis**
   - Historical churn cohort metrics.
   - Churn rate.
   - Model evaluation metrics.
   - Churn-related visualizations.

4. **Customer Details**
   - Customer ID search.
   - Customer-level information.
   - Available sample churn predictions.
   - CSV download functionality.

#### Run the dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard was manually tested for:
- Executive Overview metrics and charts.
- Segment filter behaviour.
- Customer Segmentation charts and profiles.
- Churn Analysis metrics and charts.
- Model performance metrics.
- Customer ID search.
- CSV download.
- Missing-file and Python error checks.

**Manual dashboard testing result: 8 passed, 0 failed.**

Main dashboard file: `dashboard/app.py`

## 6. Independent Validation and QA

Independent validation scripts were developed to verify data quality, RFM outputs, clustering, and churn model results.

| Validation | Checks | Passed | Failed |
|---|---:|---:|---:|
| Week 1 data validation | 25 | 25 | 0 |
| Week 2 RFM validation | 47 | 47 | 0 |
| Week 3 churn model validation | 28 | 28 | 0 |
| **Automated total** | **100** | **100** | **0** |
| Week 4 dashboard manual tests | 8 | 8 | 0 |

The 100 automated checks and 8 manual dashboard tests are separate validation activities.

Validation scripts:
- `src/validate_week1.py`
- `src/validate_week2.py`
- `src/validate_churn_model.py`

QA reports:
- `reports/week1_qa_report.md`
- `reports/week2_qa_report.md`
- `reports/week3_qa_report.md`
- `reports/week4_qa_report.md`

## 7. Installation and Setup

### Clone the repository

```bash
git clone https://github.com/Pranavsangichetty/Axlero-Group3.git
cd Axlero-Group3
```

### Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Dataset setup

Place the Online Retail II dataset in the location expected by the data-loading scripts. The raw dataset may be excluded from Git because of its size and licensing/distribution considerations.

### Run the analysis

```bash
python src/data_quality_audit.py
python src/investigate_transactions.py
python src/clean_data.py
python src/eda.py
python src/rfm_analysis.py
python src/features.py
python src/churn_dataset.py
python src/churn_prediction.py
```

Run the validation scripts:

```bash
python src/validate_week1.py
python src/validate_week2.py
python src/validate_churn_model.py
```

Run the prediction workflow:

```bash
python src/predict_customers.py \
  --input data/processed/sample_customer_scoring_input.csv \
  --output reports/customer_churn_predictions.csv
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

Run only the scripts required for the outputs you want to regenerate. Some later-stage scripts depend on files generated by earlier stages.

## 8. Repository Structure

```text
Axlero-Group3/
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── models/
│   ├── churn_model.pkl
│   └── model_metadata.json
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
│   ├── churn_dataset.py
│   ├── churn_prediction.py
│   ├── predict_customers.py
│   ├── validate_week1.py
│   ├── validate_week2.py
│   └── validate_churn_model.py
│
├── dashboard/
│   └── app.py
│
├── reports/
│   ├── figures/
│   ├── week1_progress_report.md
│   ├── week2_progress_report.md
│   ├── week1_qa_report.md
│   ├── week2_qa_report.md
│   ├── week3_qa_report.md
│   ├── week4_qa_report.md
│   ├── churn_model_evaluation.md
│   └── customer_segment_profile.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 9. Limitations and Considerations

- Customer IDs are missing from a portion of the original transaction dataset.
- The documented cleaning pipeline removed approximately 5.57% of original records.
- The initial cancellation audit reported 19,494 cancellation rows, while the cleaning log recorded 19,104 removed cancellation rows. This difference remains to be reconciled.
- The RFM segmentation uses full-history customer behaviour, whereas churn modelling uses a separate historical snapshot and observation window.
- The four-cluster solution prioritizes business usefulness rather than the highest Silhouette Score.
- Churn is defined using a 90-day inactivity proxy and does not establish permanent customer loss.
- Model performance may change when applied to future customers or different time periods.
- Only 10 sample customers are included in the current prediction demonstration.
- Risk category thresholds are illustrative and have not been validated as business decision thresholds.
- Monetary values are reported in the dataset's recorded price units; currency interpretation should be verified before financial use.

## 10. Future Scope

- Validate churn predictions on newer and independent customer cohorts.
- Improve model performance and probability calibration.
- Generate predictions for a larger eligible customer population.
- Validate business risk thresholds.
- Add campaign response and customer lifetime value analysis.
- Improve dashboard interactivity and deployment.
- Integrate automated data pipelines and scheduled model monitoring.

## 11. GitHub Repository

Repository: https://github.com/Pranavsangichetty/Axlero-Group3

Working branch: `Lav-Kumar`

## 12. Acknowledgement

This project was developed as part of the Retail & E-commerce Customer Segmentation and Churn Prediction project with Axlero – Innovating Solutions.

**Project objective:** Transform retail transaction data into meaningful customer insights and actionable customer retention strategies.

