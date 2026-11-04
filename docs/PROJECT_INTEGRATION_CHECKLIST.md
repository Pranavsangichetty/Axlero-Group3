# Project Integration Checklist

**Project:** Retail & E-commerce Customer Segmentation and Churn Prediction  
**Team:** Group 3  
**Coordinator:** Pranav Sangichetty  
**Purpose:** Track integration readiness across data preparation, customer segmentation, churn modelling, dashboard development and final delivery.

## Current baseline

The repository README records Week 1 data understanding, cleaning and EDA as completed, and Week 2 RFM analysis and customer segmentation as completed. It describes Week 3 churn prediction and Week 4 dashboard/final documentation as planned or in progress. Treat those statuses as the README's recorded status; update them only after checking the latest branch artifacts and successful runs.

## Integration checklist

### 1. Data preparation
- [ ] Confirm the source dataset location and access instructions are documented; do not commit private or licensed raw data unless permitted.
- [ ] Confirm the cleaning workflow can be reproduced from the documented inputs.
- [ ] Record row counts, key filters, missing-value handling and output paths.
- [ ] Confirm downstream modules use the same customer identifier and transaction date fields.

### 2. EDA and RFM segmentation
- [ ] Confirm EDA outputs are generated from the current processed dataset.
- [ ] Confirm RFM definitions, observation date and customer inclusion rules are documented.
- [ ] Confirm the selected cluster count is explained using both evaluation metrics and business interpretation.
- [ ] Verify segment labels and customer counts against generated outputs.
- [ ] Record business recommendations as interpretations, not model guarantees.

### 3. Churn prediction
- [ ] Agree and document the operational churn definition and prediction horizon before interpreting model results.
- [ ] Verify that target construction does not use information from after the prediction cutoff.
- [ ] Check customer-level feature aggregation and train/test split strategy.
- [ ] Train and compare the planned Logistic Regression and Random Forest baselines.
- [ ] Report precision, recall, F1-score and ROC-AUC where appropriate; include the confusion matrix and class distribution.
- [ ] Save the fitted model and preprocessing objects only after validating the pipeline.
- [ ] Document limitations and avoid describing a proxy churn label as observed contractual churn.

### 4. Dashboard
- [ ] Confirm dashboard input files and refresh procedure.
- [ ] Validate KPI calculations against source tables.
- [ ] Include sales overview, customer segments and churn-risk views only when corresponding validated data is available.
- [ ] Test filters, drill-throughs, labels and date ranges.
- [ ] Capture final screenshots and document the dashboard tool/version.

### 5. Repository and reproducibility
- [ ] Check that each deliverable has one clear canonical location.
- [ ] Check relative paths work from a fresh clone.
- [ ] Update dependencies in requirements.txt when necessary.
- [ ] Confirm large datasets, credentials, local environments and generated caches are excluded where appropriate.
- [ ] Run the documented workflow from a clean environment and record the result.
- [ ] Review each pull request before merging to main.

### 6. Final delivery
- [ ] README accurately reflects completed, in-progress and pending work.
- [ ] Final report includes methodology, results, limitations and recommendations.
- [ ] Team contributions are accurately recorded.
- [ ] Dashboard, model artifacts and reports are present or have clear access instructions.
- [ ] Final demonstration has been rehearsed.

## Daily review record

| Date | Module reviewed | Reviewer | Result / blocker | Follow-up owner |
|---|---|---|---|---|
| YYYY-MM-DD |  |  |  |  |

## Review rule

A checkbox should be marked complete only after the relevant file or output has been inspected and, where applicable, executed successfully. This checklist is a coordination aid, not evidence that a task has already been completed.
