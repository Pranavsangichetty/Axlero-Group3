# Churn Model Training and Evaluation

## 1. Dataset
- Customer records: 2,724
- Training records: 2,179
- Test records: 545
- Churned customers: 1,315
- Active customers: 1,409
- Churn rate: 48.27%

## 2. Features
- Recency
- Frequency
- Monetary
- Total_Quantity
- Unique_Products
- Average_Order_Value

`Future_Orders_90d` and `CustomerID` were excluded from model inputs.

## 3. Modelling methodology
- Stratified 80/20 train-test split.
- Random state: 42.
- Three-fold stratified cross-validation on training data.
- Hyperparameter tuning using training data only.
- Candidate models: Logistic Regression and Random Forest.
- Selection metric: mean cross-validation ROC-AUC.

## 4. Model comparison
| Model               |   CV_ROC_AUC_Mean |   Accuracy |   Precision |   Recall |   F1_Score |   ROC_AUC |
|:--------------------|------------------:|-----------:|------------:|---------:|-----------:|----------:|
| Logistic Regression |          0.763876 |   0.680734 |    0.652921 | 0.722433 |   0.685921 |  0.730807 |
| Random Forest       |          0.735978 |   0.638532 |    0.607143 | 0.711027 |   0.654991 |  0.711485 |

## 5. Selected model
- Model: Logistic Regression
- Training CV ROC-AUC: 0.7639
- Test ROC-AUC: 0.7308
- Test accuracy: 0.6807
- Test precision: 0.6529
- Test recall: 0.7224
- Test F1-score: 0.6859

### Classification report
```text
              precision    recall  f1-score   support

      Active       0.71      0.64      0.68       282
       Churn       0.65      0.72      0.69       263

    accuracy                           0.68       545
   macro avg       0.68      0.68      0.68       545
weighted avg       0.68      0.68      0.68       545

```

### Confusion matrix
Rows are actual classes [Active, Churn]; columns are predicted classes.
- Matrix: [[181, 101], [73, 190]]
- Figure: reports/figures/churn_confusion_matrix.png
- ROC figure: reports/figures/churn_roc_curve.png

## 6. Saved model files
- models/churn_model.pkl
- models/model_metadata.json
- reports/churn_model_comparison.csv

## 7. Limitations
- Churn is defined as 90-day inactivity, not permanent churn.
- Results are based on one historical cohort and one holdout split.
- Performance may change for other time periods or customer populations.
- The holdout evaluation does not establish causal effects of marketing actions.

## 8. Conclusion
The selected candidate was Logistic Regression, chosen using training cross-validation ROC-AUC. Its final metrics were measured on the held-out test set. Further temporal validation is recommended before production use.
