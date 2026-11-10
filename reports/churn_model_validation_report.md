# Independent Churn Model Validation

- Dataset rows: 2,724
- Training customers: 2,179
- Test customers: 545
- Saved model: `models/churn_model.pkl`
- Checks passed: 28
- Checks failed: 0

## Recomputed held-out test metrics

| Metric | Recomputed value |
|---|---:|
| Accuracy | 0.680734 |
| Precision | 0.652921 |
| Recall | 0.722433 |
| F1_Score | 0.685921 |
| ROC_AUC | 0.730807 |

## Confusion matrix

- Actual rows [Active, Churn], predicted columns [Active, Churn]
- Matrix: [[181, 101], [73, 190]]

## Validation checks

| Check                                             | Result   | Details                                                                            |
|:--------------------------------------------------|:---------|:-----------------------------------------------------------------------------------|
| Dataset exists                                    | PASS     |                                                                                    |
| Saved model exists                                | PASS     |                                                                                    |
| Metadata exists                                   | PASS     |                                                                                    |
| Evaluation report exists                          | PASS     |                                                                                    |
| Comparison CSV exists                             | PASS     |                                                                                    |
| Both evaluation figures exist                     | PASS     |                                                                                    |
| Required feature columns exist                    | PASS     | Recency, Frequency, Monetary, Total_Quantity, Unique_Products, Average_Order_Value |
| Target column exists                              | PASS     |                                                                                    |
| No missing values in model data                   | PASS     |                                                                                    |
| Customer IDs are unique                           | PASS     |                                                                                    |
| Target contains only 0 and 1                      | PASS     |                                                                                    |
| No negative model feature values                  | PASS     |                                                                                    |
| No infinite model feature values                  | PASS     |                                                                                    |
| Metadata feature list matches                     | PASS     |                                                                                    |
| Leakage/customer identifiers excluded in metadata | PASS     |                                                                                    |
| No forbidden columns in model feature list        | PASS     |                                                                                    |
| Recreated test split has expected size            | PASS     |                                                                                    |
| Recreated training split has expected size        | PASS     |                                                                                    |
| Model prediction output has correct length        | PASS     |                                                                                    |
| Predictions contain only 0 and 1                  | PASS     |                                                                                    |
| Predicted probabilities are valid                 | PASS     |                                                                                    |
| Accuracy matches saved metadata                   | PASS     | Recomputed=0.68073394; saved=0.6807339449541284                                    |
| Precision matches saved metadata                  | PASS     | Recomputed=0.65292096; saved=0.6529209621993127                                    |
| Recall matches saved metadata                     | PASS     | Recomputed=0.72243346; saved=0.7224334600760456                                    |
| F1_Score matches saved metadata                   | PASS     | Recomputed=0.68592058; saved=0.6859205776173285                                    |
| ROC_AUC matches saved metadata                    | PASS     | Recomputed=0.73080657; saved=0.7308065690478116                                    |
| Confusion matrix matches training report          | PASS     | Recomputed=[181, 101, 73, 190]; expected=[181, 101, 73, 190]                       |
| Model comparison contains both candidates         | PASS     |                                                                                    |

## Conclusion

All checks passed.
