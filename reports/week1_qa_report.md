# Week 1 Quality Assurance and Evaluation Report

## 1. Project Information

- Project: Retail & E-commerce – Customer Segmentation and Churn Prediction
- Review area: Data Quality, Cleaning Verification and Exploratory Data Analysis
- QA documentation prepared in: Lav-Kumar branch
- Phase: Week 1
- Status: Completed based on available validation evidence

## 2. Purpose

The purpose of this QA review is to evaluate the quality of the
original retail transaction dataset, review the data cleaning
pipeline, verify the prepared analytical datasets and assess
the available exploratory data analysis outputs.

The review uses the existing data quality audit, cleaning log,
cleaning summary, Week 1 progress report and independent
validation results.

## 3. Dataset Quality Assessment

Original dataset: online_retail_II.csv

| Metric | Initial audit result |
|---|---:|
| Total rows | 1,067,371 |
| Total columns | 8 |
| Unique invoices | 53,628 |
| Unique customers | 5,942 |
| Unique products | 5,305 |
| Unique countries | 43 |
| Exact duplicate rows | 34,335 |
| Missing Customer IDs | 243,007 |
| Missing descriptions | 4,382 |
| Negative quantities | 22,950 |
| Zero quantities | 0 |
| Negative prices | 5 |
| Zero prices | 6,202 |
| Cancelled invoice rows | 19,494 |

The initial audit identified missing customer identifiers,
duplicate records, cancellation entries, negative quantities
and non-positive prices.

These issues were considered during data preparation.

## 4. Data Cleaning Pipeline Review

The cleaning pipeline was implemented in src/clean_data.py.

| Cleaning operation | Rows before | Rows after | Rows removed |
|---|---:|---:|---:|
| Exact duplicate removal | 1,067,371 | 1,033,036 | 34,335 |
| Cancelled invoice exclusion | 1,033,036 | 1,013,932 | 19,104 |
| Positive quantity filter | 1,013,932 | 1,010,539 | 3,393 |
| Positive price filter | 1,010,539 | 1,007,913 | 2,626 |
| Valid invoice date filter | 1,007,913 | 1,007,913 | 0 |

Total rows removed: 59,458.

Final cleaned transaction records: 1,007,913.

The cleaning log was checked for continuous row counts and
consistent removal totals.

### Cleaning observations

- Exact duplicate records were removed.
- Cancelled invoices were excluded from completed-sales analysis.
- Non-positive quantities and prices were excluded.
- Invoice dates were validated.
- TotalPrice was calculated using Quantity multiplied by Price.
- The original dataset was preserved.

The initial audit recorded 19,494 cancelled invoice rows,
while the subsequent cancellation filter removed 19,104.
The difference is 390 rows. The available aggregate reports
do not independently establish the exact record-level reason
for this difference.

## 5. Prepared Analytical Datasets

### Cleaned transaction dataset

- Records: 1,007,913
- Includes records without Customer IDs.
- Used for transaction-level analysis.

### Customer transaction dataset

- Records: 779,425
- Unique customers: 5,878
- Missing Customer IDs: 0.
- Prepared for customer-level analysis.

The distinction between the transaction-level and
customer-level datasets is important because records
without Customer IDs cannot be assigned to individual
customers for RFM or customer-level churn analysis.

## 6. Independent Validation Results

The independent validation script src/validate_week1.py
was executed against the available datasets and reports.

| Validation category | Result |
|---|---|
| Dataset availability and structure | PASS |
| Duplicate and cancellation checks | PASS |
| Positive quantity and price checks | PASS |
| Invoice date validation | PASS |
| Revenue calculation consistency | PASS |
| Customer ID completeness | PASS |
| Customer population consistency | PASS |
| Cleaning log verification | PASS |
| Cleaning summary verification | PASS |

Total checks: 25

Passed: 25

Failed: 0

The results are recorded in:

- reports/week1_validation_results.csv
- reports/week1_data_validation_report.md

These checks establish consistency of the available outputs.
They do not prove that every original cleaning decision is
business-correct or that all possible data-quality issues
have been identified.

## 7. Exploratory Data Analysis Review

The EDA outputs report the following:

| Metric | Result |
|---|---:|
| Cleaned transactions | 1,007,913 |
| Total sales revenue | 20,476,260.45 |
| Unique invoices | 40,077 |
| Unique customers | 5,878 |
| Unique products | 4,916 |
| Countries | 43 |

The following six visualizations were generated:

1. Monthly revenue trend
2. Monthly order volume
3. Order value distribution
4. Top countries by revenue
5. Top customers by revenue
6. Top products by quantity sold

The images are stored in reports/figures/.

The existence of these files was verified. This review does
not independently reproduce every chart value or assess
every visual design element.

## 8. Issues and Limitations

1. Missing Customer IDs: 243,007 original rows had no
   customer identifier. These records are excluded from
   customer-level analysis.

2. Returns and negative quantities: Negative quantities
   may represent returns or adjustments. They were excluded
   from the positive-sales dataset.

3. Cancelled invoices: Cancelled invoice rows were excluded.
   The aggregate cancellation counts differ by 390 between
   the initial audit and the later cleaning filter.

4. Duplicate records: Exact duplicate rows were removed.
   Identical invoice lines may sometimes represent legitimate
   repeated entries.

5. Non-positive prices: Zero and negative prices were
   excluded from the primary positive-sales analysis.

6. Currency: The recorded monetary unit has not been
   independently verified in the available reports.

7. Validation scope: The 25 checks validate consistency
   between existing outputs, not every possible business
   assumption or source-data issue.

## 9. QA Recommendations

- Preserve the original dataset for reproducibility.
- Keep the cleaning log and validation results with the project.
- Investigate the 390-row cancellation count difference
  at record level before making a definitive claim.
- Document the treatment of returns and missing customer IDs.
- Review unusual high-value transactions before excluding
  or modifying them.
- Revalidate datasets after changes to the cleaning pipeline.
- Clearly document the currency unit before final business
  reporting.

## 10. Final QA Conclusion

The Week 1 data preparation outputs passed all 25 available
independent validation checks.

The cleaning log is continuous, the cleaned transaction
dataset contains 1,007,913 records, and the customer-level
dataset contains 779,425 records for 5,878 customers.

The EDA deliverables include six generated visualizations
and supporting CSV reports.

Based on the available evidence, the Week 1 data preparation
outputs are internally consistent and suitable for proceeding
to customer-level RFM analysis, subject to the documented
limitations and follow-up recommendations.

---

End of Week 1 QA Report.
