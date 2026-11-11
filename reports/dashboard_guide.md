# Dashboard Guide

Prepared by raj4089 (Evaluation, QA & Documentation). File: `Customer_Segmentation_Dashboard.pbix` (Power BI Desktop, built by Sirisha). **Update 2026-11-11:** the team also added a supplementary Streamlit dashboard (`dashboard/app.py`: executive overview, segmentation, churn analysis and customer details; run with `streamlit run dashboard/app.py`). It reads model metrics from `models/model_metadata.json` and shows the 10-customer demo predictions only — missing scores are not zero risk. It does not replace this Power BI deliverable; the Power BI gaps below are unchanged. This guide describes what the file **actually contains**, which was read from its internal report definition on 2026-11-10. The file was not opened in Power BI Desktop, so the screenshots, visual appearance and live refresh were not tested (see section 6).

## 1. What the dashboard contains

| Page | Visuals found |
|---|---|
| **Page 1** (sales overview) | Monthly Revenue (line), monthly order count (line), top countries by revenue (bar, Top-N filter), top products by revenue (bar, Top-N filter), Top 10 Customers by Revenue (bar), Order Value Distribution (column chart of revenue bins) |
| **RFM & Customer Segments** | Five column charts by segment: customers, total revenue, average recency, average frequency, average monetary |

Source tables named in the file: `online_retail_II` (page 1) and `customer_segment_profile` (page 2).

## 2. Gaps against the plan and the project requirements

`Dashboard_Documentation.docx` plans four pages, five KPI cards and slicers for date, country and customer group. The project requirements also ask for a "High-Risk Churn" list and a clear recommendation for each segment.

| Planned or required | Found in the .pbix |
|---|---|
| Customer Behaviour page | No |
| Churn Analysis page and High-Risk Churn list | No (churn model not delivered) |
| KPI cards (revenue, orders, customers, average order value, repeat customers) | No card visuals |
| Slicers (date, country, customer group) | No slicers |
| Marketing recommendation per segment | Not on the dashboard (only in `reports/customer_segment_recommendations.csv`) |
| Visual titles | Only 3 of 11 visuals have a title; the five segment charts are untitled |

Also note: `Page 1` is not renamed, and the segment charts show averages per segment, so "Sum of Avg_Recency" in the field list is only correct because each segment has exactly one row.

## 3. Likely data mismatch (needs Sirisha's confirmation)

Page 1 uses a column named `Revenue`. The `src/` pipeline names that column `TotalPrice`; the PostgreSQL notebook names it `Revenue`. Page 1 was therefore probably built from the notebook's export (1,003,338 rows, revenue 19,398,208.42), while page 2 uses the `src/` segment profile (5,878 customers). If so, the two pages use different cleaning rules and their totals will not agree. This is an inference from column names; the data model inside the file is compressed and was not inspected.

## 4. How to use it

1. Open `Customer_Segmentation_Dashboard.pbix` in Power BI Desktop (Windows only; Power BI Service needs the file to be published).
2. Use the page tabs at the bottom to switch between **Page 1** and **RFM & Customer Segments**.
3. Click a bar or column to cross-filter the other visuals on the same page. Click again on the same item to clear it.
4. Hover over a bar or point to see its exact value.
5. Use **Export data** from a visual's "…" menu to take its numbers.

## 5. How to refresh

1. Regenerate the data from the repository root: `python src/clean_data.py`, `python src/eda.py`, `python src/rfm_analysis.py`, `python src/features.py`.
2. Open the .pbix. Go to **Home → Transform data → Data source settings** and check that every source points to the regenerated file. File paths are stored inside the .pbix and may still point to the author's own computer.
   - Segment page: `reports/customer_segment_profile.csv`
   - Sales page: the cleaned transactions file (`data/interim/cleaned_transactions.csv`, which has `TotalPrice`) — or the notebook export if that pipeline is chosen. The `Revenue` field must be re-pointed to `TotalPrice`, or the column renamed in Power Query.
3. Click **Home → Refresh**.
4. Compare the values with section 7.
5. Save the file and commit it.

## 6. What was and was not verified

| Check | Result |
|---|---|
| File is a valid Power BI package, 2 pages, 11 visuals | Verified (read from file) |
| Fields used by the visuals exist in the repository outputs (`Segment`, `Customers`, `Total_Revenue`, `Avg_*`) | Verified against `customer_segment_profile.csv` |
| Values shown on screen, filters, navigation, layout | **Not tested** (no Power BI Desktop available) |
| Data source paths and refresh | **Not tested** |
| Screenshots | **Not available**; Sirisha should add them to `reports/figures/` |

## 7. Reference values to check the dashboard against

| Item | Expected value |
|---|---:|
| Total revenue (`src/` pipeline) | 20,476,260.45 |
| Distinct invoices | 40,077 |
| Average order value | 510.92 |
| Top country | United Kingdom, 17,410,196.12 (85.0%) |
| Best month | 2011-11, 1,503,866.78 |
| Top customer | 18102, 580,987.04 |
| Customers by segment | Champions 1,204; Loyal High-Value 1,455; Recent Customers 1,261; At-Risk / Hibernating 1,958 |
| Revenue by segment | 12,856,793.52; 2,830,096.17; 1,069,014.65; 618,899.93 |
| Average Recency by segment | 28.44; 231.20; 29.24; 397.89 |
| Average Frequency by segment | 19.21; 5.03; 3.03; 1.38 |
| Average Monetary by segment | 10,678.40; 1,945.08; 847.75; 316.09 |

Note: December 2011 is a partial month (data ends 9 Dec), so the last point of the monthly lines is low by design.
