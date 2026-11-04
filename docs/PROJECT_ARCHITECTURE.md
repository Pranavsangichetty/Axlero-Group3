# Project Architecture and Workflow

## Project purpose

The project analyzes Online Retail II transaction data to understand purchasing behaviour, segment customers using RFM and K-Means, develop a customer churn prediction workflow, and present validated business indicators in a dashboard.

## High-level workflow

```text
Online Retail II source data
          |
          v
Data understanding and quality audit
          |
          v
Cleaning and transaction preparation
          |
          +--------------------------+
          |                          |
          v                          v
Exploratory data analysis       Customer-level aggregation
                                     |
                                     v
                              RFM feature generation
                                     |
                                     v
                              Scaling and K-Means
                                     |
                                     v
                              Customer segments
                                     |
                                     +----------------------+
                                                            |
Prepared customer history and leakage-safe features       |
          |                                                 |
          v                                                 |
Churn target definition and feature engineering             |
          |                                                 |
          v                                                 |
Train/test evaluation                                       |
          |                                                 |
          v                                                 |
Logistic Regression / Random Forest                         |
          |                                                 |
          v                                                 |
Validated churn scores and model metrics                    |
          |                                                 |
          +--------------------------+----------------------+
                                     |
                                     v
                         Dashboard and business insights
                                     |
                                     v
                         Final report and recommendations
```

## Team ownership

| Team member | Primary responsibility | Integration output |
|---|---|---|
| Pranav Sangichetty | Team leadership and integration | Approved interfaces, branch review, integration status and final coordination |
| Divya | Data engineering and cleaning | Reproducible cleaned data and data-quality evidence |
| Lav Kumar | EDA and customer segmentation | EDA results, RFM analysis, cluster outputs and business interpretation |
| Nivesh243 | Churn prediction and model training | Churn target/features, trained candidate models and prediction outputs |
| Sirisha | Visualization and dashboard | Dashboard pages, visuals and dashboard test evidence |
| raj4089 | Model evaluation and documentation | Metrics, validation evidence, README and final report |

## Integration boundaries

1. **Data preparation → analytics:** downstream modules should consume documented, reproducible processed data rather than independently re-cleaning the raw source.
2. **Segmentation → churn analysis:** customer identifiers and snapshot dates must be consistent. Segment labels may be used as features only when they are available at the prediction cutoff and do not leak future information.
3. **Churn model → dashboard:** publish a documented customer-level output containing the identifier, prediction score or risk category, model/version context and prediction date. Do not expose sensitive customer details unnecessarily.
4. **Analytics → dashboard:** every KPI should have a written definition and be traceable to a source table or output.
5. **Documentation → execution:** README commands and paths must match the actual repository files.

## Suggested output contracts

These are proposed interfaces; confirm the actual column names and paths with module owners before implementation.

| Artifact | Suggested grain | Required content |
|---|---|---|
| Clean transaction table | One row per valid transaction line | Invoice, date, customer ID, product, quantity, unit price and calculated revenue |
| Customer RFM table | One row per identified customer at a stated snapshot | Customer ID, recency, frequency, monetary |
| Segmentation output | One row per customer at the same snapshot | Customer ID, RFM fields, cluster ID and readable segment label |
| Churn modelling table | One row per customer at prediction cutoff | Customer ID, eligible features, churn target and cutoff metadata |
| Churn prediction output | One row per scored customer | Customer ID, score, predicted class/risk band, model version and scoring date |
| Evaluation report | One record per model/run or metric | Split strategy, target definition, class balance and evaluation metrics |
| Dashboard source | Defined by dashboard page | Validated KPI tables and documented refresh process |

## Technical and governance rules

- Keep raw data unchanged and separate from processed outputs.
- Never commit credentials, access tokens or personal secrets.
- Do not invent churn labels: document the proxy definition and horizon.
- Use time-aware validation when the business question is future churn prediction.
- Fit preprocessing only on training data and apply the fitted transformation to validation/test data.
- Keep model artifacts, reports and dashboards versioned with clear provenance.
- Record assumptions, exclusions and known limitations.

## Status

This document describes the intended integration architecture. It does not assert that all modules or outputs have already been implemented. Update it as the team verifies actual artifacts.
