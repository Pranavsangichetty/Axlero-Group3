# Historical Churn Dataset Validation

## Time windows
- Feature window: 2011-01-02 to 2011-06-30
- Observation window: 2011-07-01 to 2011-09-28

## Dataset summary
- Customers: 2,724
- Churned customers (label 1): 1,315
- Active customers (label 0): 1,409
- Churn rate: 48.27%
- Duplicate customer IDs: 0
- Missing output values: 0

## Model usage
Use Recency, Frequency, Monetary, Total_Quantity, Unique_Products, and Average_Order_Value as candidate features.

**Do not use `Future_Orders_90d` as a model feature.** It is included only to audit how the target label was assigned.

Churn means no observed purchase during the 90-day observation window. It does not establish permanent customer loss.
