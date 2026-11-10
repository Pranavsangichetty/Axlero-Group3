# Week 2 Quality Assurance and Customer Segmentation Evaluation Report

## 1. Project Information

- Project: Retail & E-commerce – Customer Segmentation and Churn Prediction
- Review area: RFM Analysis, K-Means Clustering and Customer Segmentation
- QA documentation prepared in: Lav-Kumar branch
- Phase: Week 2
- Status: Completed based on available validation evidence

## 2. Purpose

The purpose of this report is to evaluate the customer segmentation
work completed during Week 2.

The review covers:
- RFM feature calculation.
- Data transformation and standardization.
- K-Means clustering evaluation.
- Selection of the final cluster count.
- Customer segment profiles.
- Business recommendations.
- Independent validation of the generated outputs.

## 3. RFM Analysis Review

RFM analysis was performed using the cleaned customer transaction
dataset containing 779,425 records and 5,878 unique customers.

The three RFM measures are:

| Feature | Meaning |
|---|---|
| Recency | Number of days since the customer's last purchase |
| Frequency | Number of distinct invoices/orders |
| Monetary | Total customer purchase value |

The reference date used for the RFM calculation was
10 December 2011.

The analysis used:
- Customer-level aggregation.
- Log1p transformation.
- StandardScaler normalization.
- K-Means clustering.

Generated files:
- data/processed/customer_rfm.csv
- data/processed/customer_rfm_scaled.csv
- data/processed/customer_segments.csv
- data/processed/customer_rfm_features.csv

## 4. K-Means Clustering Evaluation

The project evaluated cluster counts from k=2 to k=8.

| Number of clusters | Inertia | Silhouette score |
|---:|---:|---:|
| 2 | 8577.1061 | 0.4407 |
| 3 | 6336.7921 | 0.3499 |
| 4 | 4895.4134 | 0.3666 |
| 5 | 4069.6259 | 0.3455 |
| 6 | 3535.1145 | 0.3361 |
| 7 | 3170.9199 | 0.3034 |
| 8 | 2883.1159 | 0.2943 |

### Cluster selection review

The highest silhouette score was obtained at k=2 (approximately
0.4407).

However, the project selected k=4 to produce more detailed and
actionable customer groups.

This is a business-oriented selection rather than the
mathematically highest silhouette result. The trade-off should
be clearly explained during the project review.

The evaluation outputs are stored in:
- reports/cluster_evaluation.csv
- reports/elbow_method.png
- reports/silhouette_analysis.png

## 5. Customer Segment Evaluation

The final model produced four customer segments.

| Segment | Customers | Percentage | Avg. Recency | Avg. Frequency | Avg. Monetary |
|---|---:|---:|---:|---:|---:|
| Champions | 1,204 | 20.48% | 28.44 | 19.21 | 10,678.40 |
| Loyal High-Value | 1,455 | 24.75% | 231.20 | 5.03 | 1,945.08 |
| Recent Customers | 1,261 | 21.45% | 29.24 | 3.03 | 847.75 |
| At-Risk / Hibernating | 1,958 | 33.31% | 397.89 | 1.38 | 316.09 |

### Segment interpretation

#### 1. Champions

- 1,204 customers.
- High purchase frequency and monetary value.
- Low average recency indicates recent activity.
- Recommended strategy: loyalty rewards, VIP benefits and
  personalized offers.

#### 2. Loyal High-Value

- 1,455 customers.
- Higher average purchase value than recent customers.
- Average recency is relatively high.
- Recommended strategy: personalized re-engagement and
  loyalty campaigns.

#### 3. Recent Customers

- 1,261 customers.
- Recent purchase activity.
- Lower average frequency and monetary value.
- Recommended strategy: onboarding campaigns, product
  recommendations and repeat-purchase incentives.

#### 4. At-Risk / Hibernating

- 1,958 customers.
- Largest segment, representing 33.31% of customers.
- High average recency and low purchase frequency.
- Recommended strategy: win-back campaigns and targeted
  reactivation offers.

Segment profiles are stored in:
- reports/customer_segment_profile.csv
- reports/customer_segment_recommendations.csv

## 6. Independent Validation Results

The independent Week 2 validation script was executed to
check the RFM and clustering outputs.

Validation covered:
- RFM feature calculations.
- Customer identifiers and uniqueness.
- Reference date.
- Log transformation and standardization.
- K-Means reproducibility.
- Cluster assignments.
- Cluster evaluation metrics.
- Segment profile calculations.
- Integrated RFM feature dataset.
- Metadata consistency.

| Validation result | Count |
|---|---:|
| Total checks | 47 |
| Passed | 47 |
| Failed | 0 |

The results are stored in:
- reports/week2_validation_results.csv
- reports/week2_validation_report.md

The independent checks support the internal consistency
of the generated RFM and segmentation outputs.

## 7. Business Recommendations Review

The four segments can support different marketing strategies.

| Segment | Suggested action |
|---|---|
| Champions | VIP rewards and exclusive benefits |
| Loyal High-Value | Personalized loyalty and re-engagement |
| Recent Customers | Repeat-purchase incentives |
| At-Risk / Hibernating | Win-back campaigns |

Campaign performance should be measured using repeat-purchase
rate, revenue, customer retention and campaign conversion.

These are recommendations based on the segment profiles;
their effectiveness has not yet been experimentally verified.

## 8. Important Limitation: Churn Prediction Data Leakage

The RFM snapshot uses the complete available transaction
history with a reference date of 10 December 2011.

It is suitable for descriptive customer segmentation, but
should not be directly used as a historical churn-model
training dataset.

For churn prediction, customer features must be calculated
using only transactions available before a historical
prediction cutoff. Transactions after that cutoff should
only be used to define the future churn outcome.

This distinction is necessary to prevent future information
from leaking into model training.

## 9. Issues and Recommendations

1. The k=2 silhouette score is higher than the k=4 score.
   Document the business reason for choosing four clusters.

2. Validate segment stability on another time period before
   relying on the groups for long-term business decisions.

3. Monitor changes in segment size and customer behaviour.

4. Use time-based feature construction for churn prediction.

5. Do not treat the 90-day inactivity definition as proof
   of permanent customer loss.

6. Evaluate marketing recommendations using measurable
   campaign outcomes.

## 10. Final QA Conclusion

The Week 2 RFM and customer segmentation outputs passed
all 47 available independent validation checks.

The analysis covered 5,878 customers and generated four
business-oriented customer segments.

The k=4 selection provides more detailed customer groups,
although k=2 achieved the highest silhouette score.

The generated RFM datasets, cluster evaluation results,
segment profiles and recommendations provide a foundation
for the next phase of the project.

The full-history RFM dataset must remain separate from
historical churn training features to avoid temporal
data leakage.

---

End of Week 2 QA Report.
