# Machine Learning & Model Development

**Project:** Axlero Group 3 — Online Retail II Customer Segmentation & Churn Prediction  
**Churn horizon:** 60 days  
**Feature lookback:** 90 days

## Scope
This workstream develops reusable machine-learning components for the project's customer inactivity-risk prediction task.

## Contents
- `Machine_Learning_Model_Development.ipynb` — end-to-end feature preparation, candidate model training, validation-based selection, final held-out test evaluation, and artifact generation.
- `model_training_pipeline.py` — reusable functions for transaction preparation, customer snapshot creation, chronological splitting, and candidate model construction.
- `model_selection_report_template.md` — report template to complete with actual run outputs.
- `requirements.txt` — dependencies.

## Target definition
`churn_risk = 1` when a customer makes no purchase during the 60 days after the observation date; otherwise `0`. Features use the preceding 90 days. This target is an inactivity-risk proxy, not confirmed permanent churn.

## How to run
1. Upload `online_retail_II_cleaned.csv` to Google Colab.
2. Open and run `Machine_Learning_Model_Development.ipynb` from top to bottom.
3. Review validation model comparison and Random Forest tuning outputs.
4. Confirm final test metrics are generated from the latest chronological holdout.
5. Complete the report template using actual outputs.

## Model development approach
Candidate models include Logistic Regression, Random Forest, and Extra Trees, with a Dummy baseline in the notebook. The notebook selects the candidate by validation F1. The final test period is held out from model selection. A small Random Forest parameter experiment is also compared using validation data only.

## Expected outputs after successful execution
- `ml_validation_model_comparison.csv`
- `random_forest_tuning_results.csv`
- `ml_final_test_metrics.csv`
- `ml_confusion_matrix.png`
- `ml_feature_importance.csv` and `.png` (when a tree model is selected)
- `ml_churn_model_artifact.joblib`
- `ml_model_development_summary.txt`

Do not commit raw or cleaned transaction data, customer-level predictions, or generated artifacts unless the team lead approves. Do not report metrics until the notebook has been run successfully.
