# Model Selection Report Template

**Project:** Axlero Group 3 — Online Retail II  
**Target:** No purchase in the next 60 days  
**Feature lookback:** 90 days

> Complete this report only after running the model-development notebook. Replace placeholders with actual outputs.

## 1. Candidate algorithms
- Dummy Classifier baseline
- Logistic Regression
- Random Forest
- Extra Trees

## 2. Data split
Chronological split by observation date:
- Training: earliest 60%
- Validation: next 20%
- Test: latest 20%

## 3. Selection method
Models are compared using validation F1. The test set is not used for model selection. The selected model is refitted on training plus validation data and evaluated once on the final test period.

## 4. Validation results
Paste `ml_validation_model_comparison.csv` here.

Selected model: [actual model name]

## 5. Hyperparameter experiment
Paste `random_forest_tuning_results.csv` here. Explain which tested Random Forest settings performed best on validation F1.

## 6. Final test results
Paste `ml_final_test_metrics.csv` here. Discuss precision, recall, F1, balanced accuracy, ROC-AUC, and PR-AUC.

## 7. Interpretation
Use the actual confusion matrix and feature-importance output. Feature importance indicates model reliance, not causality.

## 8. Limitations
- A 60-day no-purchase period is an inactivity-risk proxy, not proof of permanent churn.
- The latest 60 days cannot be labelled without future transactions.
- Dataset coverage may omit customer interactions or purchases outside the source.
- Monitor performance on later unseen periods.

## 9. Conclusion
[Write a conclusion supported by actual test results.]
