# Final Project Execution Flow — Team Review

**Owner:** Pranav Sangichetty (Team Leader)  
**Date:** 10 November 2026  
**Status:** Proposed execution sequence; verify final paths after PR integration.

## End-to-end flow

```text
Online Retail II source data
        |
        v
Data audit and transaction investigation
        |
        v
Cleaning, customer-ID checks and data validation
        |
        +------------------------------+
        |                              |
        v                              v
Week 1 EDA and business charts     Customer-level transactions
                                       |
                                       v
                                RFM feature generation
                                       |
                                       v
                                Scaling and K-Means
                                       |
                                       v
                                Four customer segments
                                       |
                                       +---------------------------+
                                                                   |
Historical cutoff + approved churn definition                     |
        |                                                          |
        v                                                          |
180-day pre-cutoff feature aggregation                             |
        |                                                          |
        v                                                          |
90-day future inactivity label                                     |
        |                                                          |
        v                                                          |
Leakage-safe train/test preparation                                |
        |                                                          |
        v                                                          |
Logistic Regression + Random Forest                                |
        |                                                          |
        v                                                          |
Model comparison and independent QA                               |
        |                                                          |
        v                                                          |
Saved model + prediction output                                    |
        |                                                          |
        +-----------------------------+----------------------------+
                                      |
                                      v
                        Agreed dashboard implementation
                                      |
                                      v
                    Final report, README and QA evidence
                                      |
                                      v
                   Clean-clone test, PR review and merge
                                      |
                                      v
                         Final project presentation
```

## Integration contracts

| Handoff | Required checks |
|---|---|
| Divya → Lav/Nivesh | Customer ID and InvoiceDate fields, row counts, date coverage, cleaning rules and no duplicate customer-level keys |
| Lav → Nivesh | RFM snapshot date, one row per customer, segment labels and reproducible profile/counts |
| Divya/Lav → Nivesh | Feature values computed only before the agreed snapshot; consistent eligible customer cohort |
| Nivesh → Raj | Target definition, train/test split, feature list, saved pipeline/model, predictions, metrics, confusion matrix and ROC curve |
| Nivesh → Sirisha | Customer-level prediction schema, score meaning, prediction date and model metadata |
| Lav/Nivesh → Sirisha | Segment and churn tables with documented grain and date context; do not imply the full-history RFM snapshot is the same cohort as the historical churn sample |
| Sirisha → Pranav/Raj | Accepted dashboard artifact, source mapping, KPI definitions, refresh guide, screenshots and interaction test results |
| Raj → Pranav | Reproduced metrics, QA evidence, final report, data dictionary, limitations and clean-run results |

## Release controls

- Do not merge a branch that is materially behind `main` without updating and reviewing the complete diff.
- Do not mark the churn definition final until the team confirms the 180-day feature window, 90-day label window and snapshot date(s).
- Do not accept hard-coded dashboard metrics unless they are traceable to validated report outputs.
- Confirm whether the final dashboard must be Power BI `.pbix` or whether Streamlit is an approved replacement.
- Run the documented commands from a clean clone and record any blocked steps caused by the unavailable raw dataset.
- Keep raw data, credentials and private information out of Git.
