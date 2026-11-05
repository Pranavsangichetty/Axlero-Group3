# Week 1 Progress Report
## Project: Retail & E-commerce — Customer Segmentation and Churn Prediction

**Contributor:** Lav Kumar  
**Branch:** `Lav-Kumar`  
**Week:** 1 — Data Understanding, Data Cleaning and Exploratory Data Analysis  
**Status:** Completed for the Python data preparation and EDA activities

---

## 1. Week 1 Objectives

The main objective of Week 1 was to understand the retail transaction dataset, examine its quality, perform appropriate data cleaning, and conduct exploratory data analysis.

The work included:

- Setting up the project repository and folder structure.
- Inspecting the original dataset.
- Identifying missing values and duplicate records.
- Investigating cancellations, returns and unusual prices.
- Preparing analytical datasets.
- Performing exploratory data analysis.
- Generating visualizations and summary reports.

## 2. Dataset Description

**Dataset:** `online_retail_II.csv`

**Original file size:** Approximately 90 MB.

**Original records:** 1,067,371  
**Number of columns:** 8

### Dataset columns

| Column | Description |
|---|---|
| Invoice | Invoice transaction identifier |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of products purchased |
| InvoiceDate | Date and time of transaction |
| Price | Unit price |
| Customer ID | Customer identifier |
| Country | Customer's country |

**Dataset coverage:** 1 December 2009 – 9 December 2011.

## 3. Initial Data Quality Audit

The initial audit identified the following issues:

| Data quality issue | Records |
|---|---:|
| Missing Customer IDs | 243,007 |
| Missing descriptions | 4,382 |
| Exact duplicate rows | 34,335 |
| Negative quantities | 22,950 |
| Zero prices | 6,202 |
| Negative prices | 5 |
| Cancelled invoice rows | 19,494 |

### Important observations

1. Approximately 22.77% of the original records had missing Customer IDs.
2. Negative quantities were investigated as possible returns or adjustments.
3. Cancelled invoices were identified using invoice numbers beginning with `C`.
4. All five negative-price records were associated with bad-debt adjustments.
5. Zero-price records included operational descriptions such as damages, lost, short and mixed.

## 4. Data Cleaning and Preprocessing

A Python cleaning pipeline was developed in `src/clean_data.py`.

The following operations were performed:

1. Removed exact duplicate rows.
2. Excluded cancelled invoices from completed-sales analysis.
3. Retained positive quantities.
4. Retained positive unit prices.
5. Converted invoice dates into datetime format.
6. Converted Customer IDs into nullable integer values.
7. Calculated transaction revenue using:

   `TotalPrice = Quantity × Price`

### Cleaning results

| Cleaning operation | Rows removed |
|---|---:|
| Exact duplicate removal | 34,335 |
| Cancelled invoice exclusion | 19,104 |
| Negative quantity exclusion | 3,393 |
| Non-positive price exclusion | 2,626 |
| Invalid date exclusion | 0 |
| **Total rows removed** | **59,458** |

The original dataset was preserved without modification.

### Final datasets

**Cleaned transaction dataset**

- Records: 1,007,913
- Includes transactions without Customer IDs.
- Used for overall transaction and revenue analysis.

**Customer transaction dataset**

- Records: 779,425
- Unique customers: 5,878
- Contains no missing Customer IDs.
- Prepared for customer-level analysis, RFM and churn modeling.

## 5. Exploratory Data Analysis

A Python EDA pipeline was developed in `src/eda.py`.

The following metrics were calculated:

| Metric | Result |
|---|---:|
| Cleaned transactions | 1,007,913 |
| Total revenue | 20,476,260.45 |
| Unique invoices | 40,077 |
| Unique customers | 5,878 |
| Unique products | 4,916 |
| Countries | 43 |

Revenue was calculated as the sum of `Quantity × Price` for the retained positive-sales records. The currency unit has not yet been independently documented.

### Visualizations generated

1. Monthly Revenue Trend
2. Monthly Order Volume
3. Top 10 Countries by Revenue
4. Top 10 Products by Quantity Sold
5. Top 10 Customers by Revenue
6. Order Value Distribution

All visualizations were saved in `reports/figures/`.

## 6. Project Files Created

```text
Axlero-Group3/
│
├── data/
│   ├── raw/
│   │   └── online_retail_II.csv
│   ├── interim/
│   │   └── cleaned_transactions.csv
│   └── processed/
│       └── customer_transactions.csv
│
├── src/
│   ├── dataset.py
│   ├── data_quality_audit.py
│   ├── investigate_transactions.py
│   ├── clean_data.py
│   ├── eda.py
│   └── features.py
│
├── reports/
│   ├── missing_values_report.csv
│   ├── data_quality_summary.csv
│   ├── cleaning_log.csv
│   ├── cleaning_summary.csv
│   ├── monthly_revenue.csv
│   ├── country_revenue_top10.csv
│   ├── customer_revenue_top10.csv
│   └── figures/
│       ├── monthly_revenue.png
│       ├── monthly_orders.png
│       ├── top_countries_revenue.png
│       ├── top_products_quantity.png
│       ├── top_customers_revenue.png
│       └── order_value_distribution.png
│
├── dashboard/
├── models/
├── notebooks/
├── requirements.txt
└── README.md
```

Additional investigation sample files were generated in `reports/`.

## 7. Limitations and Data Cleaning Decisions

- Transactions without Customer IDs were retained in the transaction dataset but excluded from customer-level modeling.
- Negative quantities were excluded from positive-sales calculations. They may represent returns or adjustments and require separate analysis.
- Cancelled invoices were excluded from completed-sales calculations.
- Zero and negative prices were excluded from the primary sales dataset.
- Exact duplicate records were removed. Identical invoice lines may sometimes represent legitimate repeated entries, so this assumption should be acknowledged.
- The dataset does not provide a unique invoice-line identifier to independently resolve every duplicate case.
- More than 5% of the original records were removed; the cleaning decisions and their limitations should be explicitly discussed in the final report.

## 8. Week 1 Deliverables

| Deliverable | Status |
|---|---|
| GitHub branch and repository setup | Completed |
| Project folder structure | Completed |
| Dataset inspection | Completed |
| Missing-value audit | Completed |
| Duplicate investigation | Completed |
| Cancellation and return investigation | Completed |
| Data cleaning pipeline | Completed |
| Cleaned analytical datasets | Completed |
| EDA pipeline | Completed |
| Six EDA visualizations | Generated |
| Week 1 progress documentation | Prepared |
| Tableau dashboard | Not started; planned for Week 4 |

## 9. Next Steps

The next stage is Week 2: Customer Segmentation using RFM analysis and K-Means clustering.

Planned activities:

1. Calculate Recency, Frequency and Monetary values.
2. Apply appropriate feature transformations and scaling.
3. Evaluate cluster counts using the Elbow Method and Silhouette Score.
4. Train and validate a K-Means clustering model.
5. Profile customer segments.
6. Develop actionable marketing recommendations.

---

**Conclusion**

Week 1 established the project's Python environment, repository structure, data-quality investigation, cleaning pipeline and exploratory analysis. The cleaned customer transaction dataset is ready for the next stage of customer-level analysis. The Tableau dashboard and predictive modeling will be completed in their respective project phases.

## 10. Business Insights and Recommendations

The EDA results provide the following business insights:

### 10.1 Geographical Revenue Analysis

- The United Kingdom generated approximately 17.41 million in recorded revenue.
- Total recorded revenue was approximately 20.48 million.
- The United Kingdom contributed approximately 85% of total recorded revenue.
- EIRE and the Netherlands were the second and third highest revenue-generating countries.

**Business recommendation:** The business should continue strengthening its UK customer base while exploring opportunities to grow sales in other countries. It should also monitor geographical revenue concentration.

### 10.2 Customer Revenue Analysis

The top customers by recorded revenue included:

| Customer ID | Revenue |
|---|---:|
| 18102 | 580,987.04 |
| 14646 | 528,602.52 |
| 14156 | 313,437.62 |
| 14911 | 291,420.81 |
| 17450 | 244,784.25 |

**Business recommendation:** High-revenue customers are potential candidates for loyalty programmes, personalized offers and retention campaigns. Customer segmentation can help identify different customer groups and design suitable marketing strategies.

### 10.3 Monthly Revenue Analysis

Monthly revenue varied during the dataset period. For example:

| Month | Revenue |
|---|---:|
| December 2009 | 822,483.95 |
| January 2010 | 651,155.11 |
| February 2010 | 551,504.73 |
| March 2010 | 830,915.26 |

**Business recommendation:** The business can use monthly revenue trends to support sales planning, inventory management and promotional decisions. A complete monthly trend should be examined before drawing conclusions about seasonality or long-term growth.

### 10.4 Overall Business Implications

The EDA indicates that:

1. Revenue is highly concentrated in the United Kingdom.
2. Some customers contribute substantially more revenue than others.
3. Monthly revenue fluctuates across the observation period.
4. Customer-level purchasing behaviour should be studied further to identify valuable, regular and inactive customers.

These findings support the next stages of the project:

- **Customer Segmentation:** RFM analysis and K-Means clustering to group customers according to purchasing behaviour.
- **Churn Prediction:** Classification models to identify customers who may stop purchasing.
- **Dashboard Development:** Interactive reporting of revenue, customer segments and churn risk.

**Note:** These findings describe historical transaction data. They do not independently establish customer churn, customer lifetime value or the causes of revenue changes.
