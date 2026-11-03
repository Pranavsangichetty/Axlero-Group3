# Week 2 Progress Report: Customer Segmentation

## 1. Objective
The objective of Week 2 is to segment customers according to purchasing
behaviour using Recency, Frequency and Monetary (RFM) analysis and K-Means
clustering.

## 2. Dataset
Input: data/processed/customer_transactions.csv

Customers included: 5,878

RFM features:
- Recency: Days since the customer's most recent purchase.
- Frequency: Number of distinct invoices/orders.
- Monetary: Total customer spending based on TotalPrice.

The reference date is one day after the latest transaction date.

## 3. Preprocessing
- Removed records without Customer ID, InvoiceDate or TotalPrice for RFM.
- Retained customers with positive frequency and monetary value.
- Applied log1p transformation to RFM features.
- Applied StandardScaler before K-Means clustering.

## 4. Model evaluation

K-Means was evaluated for k values from 2 to 8.

| k | Inertia | Silhouette Score |
|---|---:|---:|
| 2 | 8577.11 | 0.4407 |
| 3 | 6336.79 | 0.3499 |
| 4 | 4895.41 | 0.3666 |
| 5 | 4069.63 | 0.3455 |
| 6 | 3535.11 | 0.3361 |
| 7 | 3170.92 | 0.3034 |
| 8 | 2883.12 | 0.2943 |

The two-cluster model has the highest silhouette score. Four clusters
were selected as a business-oriented candidate to provide more actionable
customer groups. This is a trade-off between cluster separation and
business usefulness, not a claim that k=4 is mathematically optimal.

## 5. Customer segment profile

| Segment | Customers | Percentage | Avg Recency | Avg Frequency | Avg Monetary |
|---|---:|---:|---:|---:|---:|
| Champions | 1204 | 20.48% | 28.44 | 19.21 | 10678.40 |
| Loyal High-Value | 1455 | 24.75% | 231.20 | 5.03 | 1945.08 |
| Recent Customers | 1261 | 21.45% | 29.24 | 3.03 | 847.75 |
| At-Risk / Hibernating | 1958 | 33.31% | 397.89 | 1.38 | 316.09 |

Segment names are descriptive, based on relative RFM cluster profiles.

## 6. Marketing recommendations

- Champions: VIP rewards, exclusive offers and referral campaigns.
- Loyal High-Value: Personalized win-back campaigns and loyalty reminders.
- Recent Customers: Second-purchase incentives and product recommendations.
- At-Risk / Hibernating: Re-engagement campaigns and targeted offers.

## 7. Generated deliverables

- data/processed/customer_rfm.csv
- data/processed/customer_rfm_scaled.csv
- data/processed/customer_segments.csv
- reports/cluster_evaluation.csv
- reports/customer_segment_profile.csv
- reports/customer_segment_recommendations.csv
- reports/elbow_method.png
- reports/silhouette_analysis.png
- reports/rfm_distribution.png

## 8. Limitations and next steps

- Four clusters provide more actionable groups, but the two-cluster
  model has a higher silhouette score.
- Segment names and marketing strategies are initial interpretations.
- Monetary values are in the dataset's recorded price units; currency
  has not been independently verified.
- Week 3 will focus on churn definition, feature engineering,
  classification, and model evaluation.
