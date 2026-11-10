# Week 1 Independent Data Validation Report

## Project
Retail & E-commerce — Customer Segmentation and Churn Prediction

## Purpose
Independently validate the raw dataset, cleaned transactions,
customer-level dataset, cleaning log and cleaning summary.

## Dataset statistics

| Metric | Result |
|---|---:|
| Raw records | 1,067,371 |
| Cleaned transactions | 1,007,913 |
| Customer transactions | 779,425 |
| Unique customers | 5,878 |
| Unique invoices | 40,077 |
| Unique products | 4,916 |
| Countries | 43 |
| Total sales revenue | 20,476,260.45 |

## Validation results

- Total checks: 25
- Passed: 25
- Failed: 0

| Check | Status | Details |
|---|---|---|
| Raw dataset is not empty | PASS |  |
| Cleaned dataset is not empty | PASS |  |
| Required columns exist | PASS |  |
| No exact duplicate rows in cleaned dataset | PASS |  |
| No cancelled invoices | PASS |  |
| All quantities are positive | PASS |  |
| All prices are positive | PASS |  |
| All invoice dates are valid | PASS |  |
| Revenue calculation is consistent | PASS |  |
| No missing Customer IDs in customer dataset | PASS |  |
| Customer dataset row count matches filtered transactions | PASS |  |
| Customer IDs are consistent between datasets | PASS |  |
| Cleaning log has required columns | PASS |  |
| Cleaning log row counts are continuous | PASS |  |
| Cleaning log removal counts are consistent | PASS |  |
| Cleaning log final row count matches cleaned dataset | PASS |  |
| Cleaning log starts with raw row count | PASS |  |
| Summary matches: Original rows | PASS |  |
| Summary matches: Cleaned transaction rows | PASS |  |
| Summary matches: Customer transaction rows | PASS |  |
| Summary matches: Unique customers | PASS |  |
| Summary matches: Unique invoices | PASS |  |
| Summary matches: Unique products | PASS |  |
| Summary matches: Countries | PASS |  |
| Summary matches: Total sales revenue | PASS |  |

## Validation interpretation

PASS means the tested condition was satisfied by the available files.
FAIL means the condition requires investigation.

This validation checks consistency between the existing outputs.
It does not prove that every original cleaning decision is
business-correct or that the dataset is free of all possible errors.

## Limitations

- Customer-level data intentionally excludes records without Customer IDs.
- The transaction-level cleaned dataset retains those records.
- Negative quantities, cancellations and non-positive prices were
  excluded according to the existing cleaning pipeline.
- Duplicate removal is based on exact row matching.
