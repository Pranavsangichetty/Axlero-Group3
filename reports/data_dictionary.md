# Data Dictionary

Prepared by raj4089 (Evaluation, QA & Documentation). All counts, types and ranges below were generated from the files produced by running the project scripts on 2026-11-10 (raw file SHA-256 `32569a66f3842a82b0d8c4d63b263c5d98a76bde5d1f65c6c01bf457e541d3a9`). Currency is not documented in the source data, so money values are in "the dataset's price unit".

## How the files connect

```text
data/raw/online_retail_II.csv            1,067,371 rows   (input, never modified)
      │  src/clean_data.py
      ▼
data/interim/cleaned_transactions.csv    1,007,913 rows   (sales lines, guests kept)
      │  keep rows that have a Customer ID
      ▼
data/processed/customer_transactions.csv   779,425 rows   (5,878 customers)
      │  src/rfm_analysis.py
      ▼
data/processed/customer_rfm.csv             5,878 rows    (one row per customer)
      ├─► customer_rfm_scaled.csv           5,878 rows    (model input, same row order)
      └─► customer_segments.csv             5,878 rows    (+ Cluster, Segment)
                │  src/features.py
                ▼
data/processed/customer_rfm_features.csv    5,878 rows    (final customer table)
```

**Type note.** `Invoice` and `StockCode` must be read as text (`dtype=str`). `Customer ID` is stored as a decimal (13085.0) in the raw and interim files and as a whole number in `customer_transactions.csv`; the RFM files call it `CustomerID`.

## 1. Raw data — `data/raw/online_retail_II.csv`
1,067,371 rows × 8 columns.

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `Invoice` | text | 1,067,371 | 0 | 53,628 | e.g. 489434 | Invoice (order) number: 6 digits. A leading `C` (19,494 rows) marks a cancellation; a leading `A` (6 rows) marks bad-debt accounting adjustments. Read as text: the column mixes numbers and codes. |
| `StockCode` | text | 1,067,371 | 0 | 5,305 | e.g. 85048 | Product code (5 digits, sometimes with a letter suffix). Non-product codes exist: POST, DOT, M, C2, B, AMAZONFEE and others. Read as text. |
| `Description` | text | 1,062,989 | 4,382 | 5,698 | e.g. 15CM CHRISTMAS GLASS BALL 20 | Product name. 4,382 rows are blank; all of them have a price of 0 and no Customer ID. |
| `Quantity` | integer | 1,067,371 | 0 | 1,057 | -80,995 to 80,995 | Units on the line. Negative for returns and cancellations. |
| `InvoiceDate` | text | 1,067,371 | 0 | 47,635 | e.g. 2009-12-01 07:45:00 | Date and time of the invoice (`YYYY-MM-DD HH:MM:SS`), from 1 Dec 2009 07:45 to 9 Dec 2011 12:50. |
| `Price` | decimal | 1,067,371 | 0 | 2,807 | -53,594.4 to 38,970 | Unit price in the recorded price unit (currency not verified). Includes 6,202 zero and 5 negative prices. |
| `Customer ID` | decimal | 824,364 | 243,007 | 5,942 | 12,346 to 18,287 | Customer number (5 digits). Blank for guest orders. 243,007 rows (22.77%) are blank; stored as a decimal (e.g. 13085.0) in the raw file. |
| `Country` | text | 1,067,371 | 0 | 43 | e.g. United Kingdom | Customer country (43 values). |

## 2. Cleaned transactions — `data/interim/cleaned_transactions.csv`
1,007,913 rows × 9 columns. Completed sales only; guest orders (no Customer ID) are kept. Rules are in `cleaning_documentation.md`.

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `Invoice` | text | 1,007,913 | 0 | 40,077 | e.g. 489434 | Invoice number of a completed sale (no cancellations). Read as text. |
| `StockCode` | text | 1,007,913 | 0 | 4,916 | e.g. 85048 | Product code (5 digits, sometimes with a letter suffix). Non-product codes exist: POST, DOT, M, C2, B, AMAZONFEE and others. Read as text. |
| `Description` | text | 1,007,913 | 0 | 5,399 | e.g. 15CM CHRISTMAS GLASS BALL 20 | Product name. No blanks remain after cleaning. |
| `Quantity` | integer | 1,007,913 | 0 | 520 | 1 to 80,995 | Units sold (always positive after cleaning). |
| `InvoiceDate` | text | 1,007,913 | 0 | 37,212 | e.g. 2009-12-01 07:45:00 | Date and time of the invoice (`YYYY-MM-DD HH:MM:SS`), from 1 Dec 2009 07:45 to 9 Dec 2011 12:50. |
| `Price` | decimal | 1,007,913 | 0 | 2,275 | 0.001 to 25,111.1 | Unit price (always above zero after cleaning). |
| `Customer ID` | decimal | 779,425 | 228,488 | 5,878 | 12,346 to 18,287 | Customer number; blank for guest orders (228,488 rows, 22.7%). Decimal in this file. |
| `Country` | text | 1,007,913 | 0 | 43 | e.g. United Kingdom | Customer country (43 values). |
| `TotalPrice` | decimal | 1,007,913 | 0 | 6,845 | 0.001 to 168,470 | Line revenue = `Quantity × Price`. Created in `clean_data.py`. Gross: cancellations and returns are not subtracted. |

## 3. Customer transactions — `data/processed/customer_transactions.csv`
779,425 rows × 9 columns. The cleaned transactions that have a Customer ID. Same columns as above.

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `Invoice` | integer | 779,425 | 0 | 36,969 | 489,434 to 581,587 | Invoice number of a completed sale. Pandas may read it as a whole number here because the `C` codes are gone; read it as text for consistency. |
| `StockCode` | text | 779,425 | 0 | 4,631 | e.g. 85048 | Product code (5 digits, sometimes with a letter suffix). Non-product codes exist: POST, DOT, M, C2, B, AMAZONFEE and others. Read as text. |
| `Description` | text | 779,425 | 0 | 5,283 | e.g. 15CM CHRISTMAS GLASS BALL 20 | Product name. No blanks remain after cleaning. |
| `Quantity` | integer | 779,425 | 0 | 437 | 1 to 80,995 | Units sold (always positive after cleaning). |
| `InvoiceDate` | text | 779,425 | 0 | 34,585 | e.g. 2009-12-01 07:45:00 | Date and time of the invoice (`YYYY-MM-DD HH:MM:SS`), from 1 Dec 2009 07:45 to 9 Dec 2011 12:50. |
| `Price` | decimal | 779,425 | 0 | 665 | 0.001 to 10,953.5 | Unit price (always above zero after cleaning). |
| `Customer ID` | integer | 779,425 | 0 | 5,878 | 12,346 to 18,287 | Customer number; no blanks (this is the customer-level table). Whole number in this file. |
| `Country` | text | 779,425 | 0 | 41 | e.g. United Kingdom | Customer country (41 values). |
| `TotalPrice` | decimal | 779,425 | 0 | 3,734 | 0.001 to 168,470 | Line revenue = `Quantity × Price`. Created in `clean_data.py`. Gross: cancellations and returns are not subtracted. |

## 4. RFM table — `data/processed/customer_rfm.csv`
5,878 rows × 4 columns. Reference date 2011-12-10.

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `CustomerID` | integer | 5,878 | 0 | 5,878 | 12,346 to 18,287 | Customer number. One row per customer. |
| `Recency` | integer | 5,878 | 0 | 593 | 1 to 739 | Days from the customer's last purchase date to the reference date (10 Dec 2011, the day after the last invoice). 1 = bought on the last day. |
| `Frequency` | integer | 5,878 | 0 | 90 | 1 to 398 | Number of distinct invoices. |
| `Monetary` | decimal | 5,878 | 0 | 5,776 | 2.95 to 580,987 | Total spend = sum of `TotalPrice` over all the customer's invoices. Gross revenue, in the dataset's price unit. |

## 5. Scaled features — `data/processed/customer_rfm_scaled.csv`
5,878 rows × 3 columns. The input of K-Means.

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `Recency` | decimal | 5,878 | 0 | 593 | -2.46986 to 1.3932 | `log1p(Recency)` then standardised (mean 0, standard deviation 1). Row order = `customer_rfm.csv`; no ID column. |
| `Frequency` | decimal | 5,878 | 0 | 90 | -1.05815 to 5.48492 | `log1p(Frequency)` then standardised. |
| `Monetary` | decimal | 5,878 | 0 | 5,775 | -3.92911 to 4.65978 | `log1p(Monetary)` then standardised. |

## 6. Customer segments — `data/processed/customer_segments.csv`
5,878 rows × 6 columns.

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `CustomerID` | integer | 5,878 | 0 | 5,878 | 12,346 to 18,287 | Customer number. One row per customer. |
| `Recency` | integer | 5,878 | 0 | 593 | 1 to 739 | Days from the customer's last purchase date to the reference date (10 Dec 2011, the day after the last invoice). 1 = bought on the last day. |
| `Frequency` | integer | 5,878 | 0 | 90 | 1 to 398 | Number of distinct invoices. |
| `Monetary` | decimal | 5,878 | 0 | 5,776 | 2.95 to 580,987 | Total spend = sum of `TotalPrice` over all the customer's invoices. Gross revenue, in the dataset's price unit. |
| `Cluster` | integer | 5,878 | 0 | 4 | 0 to 3 | K-Means cluster number (0 to 3). Numbers are arbitrary labels. |
| `Segment` | text | 5,878 | 0 | 4 | e.g. Champions | Business name given to the cluster (see segment table below). |

**`customer_rfm_features.csv`** has exactly the same 6 columns as this file (`CustomerID, Recency, Frequency, Monetary, Cluster, Segment`), sorted by `CustomerID`, and is the file to use for downstream work. Its metadata is in `customer_rfm_features_metadata.json` (row count, reference date, source files, and the churn-leakage warning).

### Segment names

| Cluster | Segment | Meaning |
|---:|---|---|
| 0 | Champions | Recent purchases; highest frequency and monetary value |
| 1 | Loyal High-Value | Higher historical spending and frequency but less recent purchasing |
| 2 | Recent Customers | Recent purchasing but lower frequency and monetary value |
| 3 | At-Risk / Hibernating | Longest recency; lowest frequency and monetary value |

Names come from the rule in `rfm_analysis.py`: each cluster average is compared with the median of the four cluster averages. They are descriptions, not fixed customer types.

## 7. Report tables

### `reports/cluster_evaluation.csv`
7 rows (k = 2 to 8).

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `k` | integer | 7 | 0 | 7 | 2 to 8 | Number of clusters tested. |
| `inertia` | decimal | 7 | 0 | 7 | 2,883.12 to 8,577.11 | Sum of squared distances to the nearest cluster centre; lower is tighter. |
| `silhouette_score` | decimal | 7 | 0 | 7 | 0.29432 to 0.440687 | Cluster separation from -1 to 1; higher is better. Estimated on a random sample of 5,000 customers. |

### `reports/customer_segment_profile.csv`
4 rows (one per cluster).

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `Cluster` | integer | 4 | 0 | 4 | 0 to 3 | Cluster number. |
| `Customers` | integer | 4 | 0 | 4 | 1,204 to 1,958 | Customers in the cluster. |
| `Avg_Recency` | decimal | 4 | 0 | 4 | 28.4352 to 397.892 | Mean Recency (days). |
| `Avg_Frequency` | decimal | 4 | 0 | 4 | 1.37692 to 19.2126 | Mean Frequency (invoices). |
| `Avg_Monetary` | decimal | 4 | 0 | 4 | 316.088 to 10,678.4 | Mean Monetary (spend). |
| `Total_Revenue` | decimal | 4 | 0 | 4 | 618,900 to 1.28568e+07 | Sum of Monetary in the cluster. |
| `Customer_Percentage` | decimal | 4 | 0 | 4 | 20.4832 to 33.3106 | Share of all 5,878 customers (%). |
| `Segment` | text | 4 | 0 | 4 | e.g. Champions | Business name of the cluster. |

### `reports/customer_segment_recommendations.csv`
4 rows (one per segment). Text columns written by the team; they are interpretations.

| Column | Type | Non-null | Missing | Distinct | Range / example | Description |
|---|---|---:|---:|---:|---|---|
| `Segment` | text | 4 | 0 | 4 | e.g. Champions | Segment name. |
| `Customer_Behaviour` | text | 4 | 0 | 4 | e.g. Recent purchases; highest fr | Typical behaviour in words. |
| `Marketing_Recommendation` | text | 4 | 0 | 4 | e.g. VIP rewards, exclusive offer | Suggested marketing action. |
| `Primary_Objective` | text | 4 | 0 | 4 | e.g. Retention and advocacy | Main business goal for the segment. |

### Cleaning and audit tables

| File | Columns | Content |
|---|---|---|
| `reports/cleaning_log.csv` | `Step, Rows_Before, Rows_After, Rows_Removed` | One row per cleaning step (5 rows). |
| `reports/cleaning_summary.csv` | `Metric, Value` | Original rows, cleaned rows, customer rows, customers, invoices, products, countries, total revenue. |
| `reports/data_quality_summary.csv` | `Metric, Value` | Audit of the raw data (rows, duplicates, negatives, missing values). |
| `reports/missing_values_report.csv` | (column name), `Missing_Count, Missing_Percentage` | Missing values per raw column. |
| `reports/monthly_revenue.csv` | `YearMonth, TotalPrice` | Revenue per month (Dec 2011 is a partial month, to 9 Dec). |
| `reports/country_revenue_top10.csv` | `Country, TotalPrice` | Top 10 countries by revenue. |
| `reports/customer_revenue_top10.csv` | `Customer ID, TotalPrice` | Top 10 customers by revenue. |
| `reports/*_samples.csv`, `negative_price_records.csv` | same 8 columns as the raw data | Up to 500 example rows of each issue type (duplicates, cancellations, negative quantities, zero prices); all 5 negative-price rows. |

### Feature definitions

| Feature | Formula |
|---|---|
| `TotalPrice` | `Quantity × Price` |
| `Recency` | `reference_date − date of last purchase` in days, with `reference_date = last InvoiceDate + 1 day` |
| `Frequency` | count of distinct `Invoice` per customer |
| `Monetary` | sum of `TotalPrice` per customer |
| Scaled feature | `StandardScaler(log1p(value))` |

## 8. Churn modelling tables (added 2026-11-11)

### `data/processed/historical_churn_dataset.csv`
2,724 rows × 9 columns. Built by `src/churn_dataset.py`. Features use only transactions from 2011-01-02 to 2011-06-30; the label uses only 2011-07-01 to 2011-09-28.

| Column | Type | Description |
|---|---|---|
| `CustomerID` | integer | Customer number; unique (one row per cohort customer) |
| `Recency` | integer | Days from the customer's last purchase in the feature window to the 2011-07-01 cutoff |
| `Frequency` | integer | Distinct invoices in the feature window |
| `Monetary` | decimal | Sum of `TotalPrice` in the feature window |
| `Total_Quantity` | integer | Units bought in the feature window |
| `Unique_Products` | integer | Distinct StockCodes in the feature window |
| `Average_Order_Value` | decimal | Mean invoice total in the feature window |
| `Future_Orders_90d` | integer | Invoices in the 90-day observation window. **Audit only — never a model feature** |
| `Churn` | integer | 1 = no purchase in the observation window; 0 = at least one purchase |

### `reports/customer_churn_predictions.csv`
10 rows × 4 columns. A demonstration output of `src/predict_customers.py`, **not** full-population scoring.

| Column | Type | Description |
|---|---|---|
| `CustomerID` | integer | Customer number |
| `Churn_Probability` | decimal | Model probability of churn (0 to 1) |
| `Predicted_Churn` | integer | 1 if probability ≥ 0.5 |
| `Risk_Category` | text | Low (< 0.40), Medium (0.40–0.70), High (> 0.70); illustrative thresholds, not validated business cut-offs |

### `models/model_metadata.json`
Selected model (Logistic Regression), parameters, feature list, excluded columns, split sizes and verified test metrics (see `metrics_documentation.md` §5).
