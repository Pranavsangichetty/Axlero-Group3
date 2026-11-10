# Week 4 QA Report – Dashboard and Project Integration

## 1. Objective
To test the integrated Streamlit dashboard, customer analytics,
churn analysis and customer data export functionality.

## 2. Dashboard Components
The dashboard contains four main sections:
1. Executive Overview
2. Customer Segmentation
3. Churn Analysis
4. Customer Details

## 3. Manual Dashboard Testing

| Test | Result |
|---|---|
| Executive Overview metrics and charts | PASS |
| Segment filter updates metrics and charts | PASS |
| Customer Segmentation charts and profile | PASS |
| Churn Analysis KPI values and charts | PASS |
| Model performance metrics | PASS |
| Customer ID search | PASS |
| CSV download | PASS |
| No missing-file or Python errors | PASS |

Total tests: 8
Passed: 8
Failed: 0

## 4. Churn Dashboard Data
- Historical cohort: 2,724 customers
- Churned customers: 1,315
- 90-day inactivity rate: 48.27%

Model performance values displayed in the dashboard
were checked against the saved evaluation results.

## 5. Customer Details and Export
Customer ID search was tested successfully.
CSV download was tested successfully.

Only 10 sample customer predictions are available
in the current sample scoring output. Missing scores
for other customers must not be interpreted as zero.

## 6. Technical Verification
- dashboard/app.py compiled successfully.
- src/predict_customers.py compiled successfully.
- Streamlit and Plotly dependencies were installed.
- Dashboard opened and all four sections were tested.

## 7. Limitations
The dashboard combines descriptive RFM data and a separate
historical churn cohort. These datasets represent different
time windows and must be interpreted separately.

The sample prediction file contains only 10 scored customers.
It is not a full-population prediction output.

## 8. QA Conclusion
All eight manual dashboard tests passed.
The dashboard's principal functionality was verified.
The Week 4 dashboard testing deliverable is complete
in the Lav-Kumar branch.
