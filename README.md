# Churn Modelling and Model Evaluation

**Project:** Retail & Ecommerce Customer Segmentation & Churn Prediction  
**Team:** Axlero Group 3  
**Contributor:** Nivesh  
**Assigned responsibility:** Churn Modelling and Model Evaluation

## Churn definition

The team leader confirmed a **60-day** churn-risk definition:

- `1` = the customer makes no purchase during the 60 days after the observation date.
- `0` = the customer makes at least one purchase during the 60 days after the observation date.

The notebook uses the previous 90 days of transactions to calculate customer features. This is a future inactivity-risk label, not proof of permanent customer cancellation.

## Files

- `Churn_Modelling_Model_Evaluation_60_Day.ipynb` — modelling, validation-based model selection, held-out test evaluation, charts, and output generation.
- `churn_model_report_template.md` — fill in after the notebook has run successfully.
- `requirements.txt` — Python packages used by the notebook.
- `.gitignore` — prevents accidental commits of datasets and generated model files.

## Input data

The notebook expects `online_retail_II_cleaned.csv` in its working directory, with these columns:

`Invoice`, `InvoiceDate`, `CustomerID`, `StockCode`, `Quantity`, `Price`

`Revenue` is optional; the notebook calculates it from `Quantity * Price` if absent.

**Do not commit the raw or cleaned customer transaction CSV to this public/shared repository unless the team lead has explicitly approved it.** Upload the dataset to Colab separately when running the notebook.

## How to run in Google Colab

1. Open Google Colab and upload `Churn_Modelling_Model_Evaluation_60_Day.ipynb`.
2. Upload `online_retail_II_cleaned.csv` to the Colab session.
3. Run all cells from top to bottom.
4. Confirm that every cell finishes without errors.
5. Review the validation comparison and final test metrics.
6. Complete `churn_model_report_template.md` using the actual generated results.
7. Download and add the approved output files to this folder before committing.

## Model-selection and evaluation approach

The notebook uses chronological observation dates:

- Earliest 60% of snapshot dates: training
- Next 20%: validation and model selection
- Latest 20%: final held-out test

Candidate models: Dummy Classifier, Logistic Regression, and Random Forest. The best model is selected using validation F1. The selected model is refitted on training plus validation data, then evaluated once on the held-out test data.

## Expected generated outputs

After a successful run, the notebook generates:

- `churn_validation_model_comparison.csv`
- `churn_test_evaluation.csv`
- `churn_test_predictions.csv`
- `churn_feature_importance.csv`
- `churn_model.joblib`
- `churn_evaluation_summary.txt`
- `confusion_matrix.png`
- `roc_curve.png`
- `precision_recall_curve.png`
- `churn_feature_importance.png`

Only commit generated results after confirming they exist and contain real outputs. Do not invent or manually estimate evaluation metrics.
