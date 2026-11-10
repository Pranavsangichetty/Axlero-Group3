# RFM Feature Integration and Validation Report

## Validation results
- Integrated customer records: 5,878
- Unique customers: 5,878
- Duplicate customer IDs: 0
- Missing cells: 0
- RFM reference date: 2011-12-10
- RFM and segment customer IDs: exact match
- Transaction and RFM customer IDs: exact match
- Frequency and Monetary values: positive for all records

## Segment counts and average RFM values
| Segment | Customers | Avg Recency | Avg Frequency | Avg Monetary |
|---|---:|---:|---:|---:|
| At-Risk / Hibernating | 1958 | 397.89 | 1.38 | 316.09 |
| Loyal High-Value | 1455 | 231.20 | 5.03 | 1945.08 |
| Recent Customers | 1261 | 29.24 | 3.03 | 847.75 |
| Champions | 1204 | 28.44 | 19.21 | 10678.40 |

## Churn modelling caution
This RFM snapshot uses the full available transaction history. It is suitable for descriptive segmentation, but must not be used directly as a historical churn-training snapshot. For churn prediction, recompute features at each historical cutoff and use only transactions available on or before that cutoff.
