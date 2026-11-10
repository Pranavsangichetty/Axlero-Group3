# Week 3 QA Report – Churn Prediction

## 1. Objective
To independently validate the historical churn dataset, feature engineering,
model training, model evaluation and prediction workflow.

## 2. Dataset Validation
- Historical customer cohort: 2,724
- Churned customers: 1,315
- Active customers: 1,409
- Churn rate: 48.27%
- Feature observation window: 180 days
- Churn observation window: 90 days
- Missing values: 0
- Duplicate Customer IDs: 0

Churn represents no purchase during the 90-day observation window.
It is an inactivity-based proxy and does not prove permanent customer loss.

## 3. Model Development
Two models were evaluated:
- Logistic Regression
- Random Forest

Logistic Regression was selected based on the higher mean
cross-validation ROC-AUC score.

Selected model: Logistic Regression

## 4. Model Test Results

| Metric | Result |
|---|---:|
| Accuracy | 0.6807 |
| Precision | 0.6529 |
| Recall | 0.7224 |
| F1-score | 0.6859 |
| ROC-AUC | 0.7308 |

The model was evaluated on a held-out test set of 545 customers.

## 5. Leakage Prevention
The following fields were excluded from model training:
- CustomerID
- Future_Orders_90d

Only the six approved historical customer features were used.

## 6. Independent Validation
Validation script: src/validate_churn_model.py

Total checks: 28
Passed: 28
Failed: 0

The validation confirmed model loading, feature selection,
prediction outputs, probability validity, evaluation metrics
and confusion matrix consistency.

## 7. Prediction Workflow
The script src/predict_customers.py was created and tested.
It loads the saved model, validates customer input and generates
churn probabilities and risk categories.

A sample of 10 customers was successfully scored.

The sample scoring output is a workflow demonstration,
not an independent model evaluation.

Risk categories use initial illustrative thresholds and
have not been validated as business decision thresholds.

## 8. Limitations
- Historical cohort and observation period are limited.
- Churn is defined using a 90-day inactivity proxy.
- Model performance may change on future customer data.
- The 10-row scoring sample is not a production scoring population.

## 9. QA Conclusion
All 28 independent churn-model validation checks passed.
The Week 3 churn prediction development and validation
deliverables are complete in the Lav-Kumar branch.
