# Week 2 Independent RFM and Segmentation Validation

## Project
Retail & E-commerce – Customer Segmentation and Churn Prediction

## Validation summary
- Total checks: 47
- Passed: 47
- Failed: 0

## Dataset summary
- Customers: 5,878
- RFM reference date: 2011-12-10
- Selected clusters: 4
- Integrated feature records: 5,878
- K-Means reproduction ARI: 1.000000

## Detailed validation results

| Check | Status | Details |
|---|---|---|
| Transaction columns exist | PASS |  |
| RFM columns exist | PASS |  |
| Segment columns exist | PASS |  |
| Integrated feature columns exist | PASS |  |
| All input datasets are non-empty | PASS |  |
| RFM has unique CustomerID | PASS |  |
| RFM has no missing CustomerID | PASS |  |
| Segments has unique CustomerID | PASS |  |
| Segments has no missing CustomerID | PASS |  |
| Integrated features has unique CustomerID | PASS |  |
| Integrated features has no missing CustomerID | PASS |  |
| RFM and segment customer populations match | PASS |  |
| RFM and integrated feature populations match | PASS |  |
| RFM and transaction customer populations match | PASS |  |
| Recomputed RFM customer population matches | PASS |  |
| Recency independently recalculated | PASS |  |
| Frequency independently recalculated | PASS |  |
| Monetary independently recalculated | PASS |  |
| RFM reference date matches expected date | PASS |  |
| RFM values are non-negative | PASS |  |
| Frequency and Monetary are positive | PASS |  |
| Scaled RFM values match log1p and StandardScaler | PASS |  |
| Scaled dataset row count matches RFM | PASS |  |
| Exactly four selected clusters exist | PASS |  |
| No missing cluster or segment assignments | PASS |  |
| Segment names match between segment and feature files | PASS |  |
| Cluster IDs match between segment and feature files | PASS |  |
| Reproduced K-Means assignments match saved clusters | PASS |  |
| Cluster evaluation columns exist | PASS |  |
| Cluster evaluation covers k=2 through k=8 | PASS |  |
| Inertia values are positive | PASS |  |
| Inertia decreases as k increases | PASS |  |
| Silhouette scores are within valid range | PASS |  |
| Silhouette optimum is correctly identified as k=2 | PASS |  |
| Saved profile contains all clusters | PASS |  |
| Segment profile Customers is consistent | PASS |  |
| Segment profile Avg_Recency is consistent | PASS |  |
| Segment profile Avg_Frequency is consistent | PASS |  |
| Segment profile Avg_Monetary is consistent | PASS |  |
| Segment profile Total_Revenue is consistent | PASS |  |
| Segment customer counts sum to RFM population | PASS |  |
| Integrated features contain no missing values | PASS |  |
| Integrated features contain no duplicate rows | PASS |  |
| Integrated feature RFM values match RFM dataset | PASS |  |
| Metadata row count matches feature dataset | PASS |  |
| Metadata unique customer count matches | PASS |  |
| Metadata reference date is correct | PASS |  |

## Model selection interpretation

The k=2 model has the highest silhouette score in the saved evaluation. The project selected k=4 as a business-oriented candidate to provide four actionable customer groups. Therefore, k=4 is not claimed to be the mathematical optimum.

## Churn modelling limitation

The RFM snapshot uses the full available transaction history and is suitable for descriptive segmentation. It must not be used directly as a historical churn-training snapshot because this can introduce future-data leakage. Historical churn features must be recomputed using only data available before each prediction cutoff.

## Conclusion

All independent validation checks passed.
