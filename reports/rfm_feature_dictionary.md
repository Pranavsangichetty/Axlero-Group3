# Customer RFM Feature Dictionary

## Purpose
This file documents the integrated customer-level RFM and segmentation dataset.

## Output
`data/processed/customer_rfm_features.csv`

| Column | Description |
|---|---|
| `CustomerID` | Unique customer identifier |
| `Recency` | Number of days since the customer's most recent purchase at the RFM reference date |
| `Frequency` | Number of distinct invoices/orders for the customer |
| `Monetary` | Sum of customer transaction value |
| `Cluster` | K-Means cluster identifier |
| `Segment` | Business-readable customer segment assigned to the cluster |

## Snapshot limitation
The current RFM snapshot uses the full available transaction history, with a reference date one day after the latest transaction. It is intended for descriptive customer segmentation. Do not use it directly to train a historical forward-looking churn model because that can introduce future-data leakage. Recalculate RFM at a historical cutoff for churn modelling.
