# Final Project Completion Report
## Retail & E-commerce Customer Segmentation and Churn Prediction

**Organization:** Axlero – Innovating Solutions  
**Dataset:** Online Retail II  
**Working Branch:** Lav-Kumar  
**Project Status:** Development and documented QA deliverables completed

---

## 1. Executive Summary

The project analyzes retail transaction data to understand customer purchasing behaviour, identify meaningful customer segments, and develop a customer churn prediction workflow.

The work covers data quality analysis, data cleaning, exploratory data analysis, RFM feature engineering, K-Means clustering, churn prediction, model validation, and an interactive Streamlit dashboard.

The completed workflow provides customer-level insights and demonstrates how transaction data can support customer retention and business decision-making.

## 2. Project Objectives

- Understand and clean the retail transaction dataset.
- Perform exploratory data analysis.
- Develop customer-level RFM features.
- Identify customer segments using K-Means.
- Build a historical churn prediction dataset.
- Train and evaluate machine learning models.
- Develop a customer scoring workflow.
- Build and manually test an interactive dashboard.
- Document project outputs, limitations, and validation results.

## 3. Week-wise Work Summary

### Week 1 – Data Cleaning and EDA

- Audited missing values, duplicate records, cancellations, and invalid transactions.
- Removed duplicate and invalid records through the documented cleaning pipeline.
- Created the TotalPrice feature.
- Prepared cleaned transaction and customer-level datasets.
- Generated EDA charts and reports.

Key results:

| Metric | Result |
|---|---:|
| Original records | 1,067,371 |
| Cleaned transactions | 1,007,913 |
| Customer-linked transactions | 779,425 |
| Identified customers | 5,878 |
| Products | 4,916 |
| Countries | 43 |
| EDA revenue | 20,476,260.45 |

Independent validation: 25 passed, 0 failed.

### Week 2 – RFM Analysis and Customer Segmentation

- Calculated Recency, Frequency, and Monetary values.
- Applied log transformation and StandardScaler.
- Evaluated K-Means cluster counts from 2 to 8.
- Selected four clusters for business interpretability.
- Generated segment profiles and marketing recommendations.

| Segment | Customers |
|---|---:|
| Champions | 1,204 |
| Loyal High-Value | 1,455 |
| Recent Customers | 1,261 |
| At-Risk / Hibernating | 1,958 |
| **Total** | **5,878** |

The k=2 solution had the highest Silhouette Score. The k=4 solution was selected as a business-oriented alternative offering four actionable customer groups.

Independent validation: 47 passed, 0 failed.

### Week 3 – Churn Prediction

- Created a historical customer cohort.
- Defined churn using a 90-day no-purchase observation period.
- Engineered six historical customer features.
- Excluded CustomerID and Future_Orders_90d from model training.
- Trained Logistic Regression and Random Forest.
- Selected Logistic Regression using cross-validation ROC-AUC.
- Saved the selected model and evaluation artifacts.
- Developed and tested a customer scoring script.

Historical churn cohort:

| Metric | Result |
|---|---:|
| Customers | 2,724 |
| Churned | 1,315 |
| Active | 1,409 |
| Inactivity-based churn rate | 48.27% |
| Test customers | 545 |

Selected model test results:

| Metric | Result |
|---|---:|
| Accuracy | 0.6807 |
| Precision | 0.6529 |
| Recall | 0.7224 |
| F1-score | 0.6859 |
| ROC-AUC | 0.7308 |

Independent model validation: 28 passed, 0 failed.

The prediction workflow was demonstrated using 10 sample customers. This is not a full-population scoring output.

### Week 4 – Dashboard and Final QA

Developed an interactive dashboard using Streamlit and Plotly.

Dashboard sections:
1. Executive Overview
2. Customer Segmentation
3. Churn Analysis
4. Customer Details

Dashboard features:
- Business KPI visualization.
- Customer segment filtering.
- Segment profiles and charts.
- Historical churn metrics.
- Model performance visualization.
- Customer ID search.
- CSV download.

Manual dashboard testing:

| Test | Result |
|---|---|
| Executive Overview | PASS |
| Segment filter | PASS |
| Segmentation charts and profiles | PASS |
| Churn Analysis | PASS |
| Model performance metrics | PASS |
| Customer ID search | PASS |
| CSV download | PASS |
| No missing-file or Python errors | PASS |

Total manual tests: 8 passed, 0 failed.

## 4. Overall QA Summary

| Validation Activity | Total | Passed | Failed |
|---|---:|---:|---:|
| Week 1 data validation | 25 | 25 | 0 |
| Week 2 RFM validation | 47 | 47 | 0 |
| Week 3 churn validation | 28 | 28 | 0 |
| **Automated validation total** | **100** | **100** | **0** |
| Week 4 dashboard manual tests | 8 | 8 | 0 |

Automated validations and manual dashboard tests are reported separately.

## 5. Major Project Deliverables

- Cleaned transaction dataset.
- Customer-level transaction dataset.
- EDA visualizations and reports.
- RFM customer features.
- K-Means customer segments.
- Segment profiles and recommendations.
- Historical churn dataset.
- Trained churn prediction model.
- Model comparison and evaluation reports.
- Independent validation reports.
- Sample customer scoring output.
- Interactive Streamlit dashboard.
- Week-wise QA reports.
- Updated README documentation.

## 6. Technical Implementation

Main technologies:
- Python
- Pandas and NumPy
- Scikit-learn
- Matplotlib and Seaborn
- Plotly
- Streamlit
- Git and GitHub

Important scripts:
- `src/clean_data.py`
- `src/eda.py`
- `src/rfm_analysis.py`
- `src/features.py`
- `src/churn_dataset.py`
- `src/churn_prediction.py`
- `src/predict_customers.py`
- `src/validate_week1.py`
- `src/validate_week2.py`
- `src/validate_churn_model.py`
- `dashboard/app.py`

## 7. Limitations and Risks

1. Customer IDs are missing from a portion of the original dataset.
2. The initial cancellation audit recorded 19,494 cancellation rows, whereas the cleaning log recorded 19,104 removed cancellation rows. This discrepancy remains unresolved.
3. Four customer clusters were selected for business usefulness, not because they achieved the highest Silhouette Score.
4. Churn is an inactivity-based proxy defined using a 90-day observation window.
5. Full-history RFM data and the historical churn cohort represent different time periods.
6. The current scoring demonstration contains only 10 customers.
7. Risk category thresholds are illustrative and have not been validated for operational decisions.
8. Model performance may change on future or independent customer populations.

## 8. Final Conclusion

The project has implemented the main data analytics, customer segmentation, churn prediction, validation, and dashboard workflows.

The completed work demonstrates how retail transaction records can be transformed into customer behaviour insights, actionable segments, and a machine learning-based churn prediction workflow.

The dashboard provides an integrated interface for exploring business metrics, customer segments, and historical churn analysis.

The documented validation activities recorded 100 successful automated checks and 8 successful manual dashboard tests.

The project is ready for final review of the completed deliverables in the Lav-Kumar branch, subject to the limitations and unresolved data discrepancy documented above.

