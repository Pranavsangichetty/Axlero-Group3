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


## 7. Team-lead integration review — 10 November 2026

This section records the repository state inspected by the team lead. It is a review snapshot, not a declaration that every module is accepted.

### Current evidence from the shared `main` branch

- Week 1 data audit, cleaning and EDA are documented as complete and reproducible.
- Week 2 RFM and K-Means segmentation are documented as complete and reproducible, with 64 verification checks recorded in the current README.
- Churn prediction is still recorded as not delivered on `main`.
- The Power BI dashboard is recorded as partial on `main`; the README describes two existing pages.
- The proposed churn rule remains pending team confirmation in `docs/WEEK3_CHURN_DEFINITION_AND_PREDICTION_PERIOD.md`.

### Pull request review

| Item | Finding | Team-lead action |
|---|---|---|
| PR #13 | Open PR with churn prediction, customer scoring, Streamlit dashboard and Week 3/4 reports | Requested changes; not merged |
| Branch freshness | `Lav-Kumar` is 38 commits behind `main` and 1 commit ahead at review time | Update/rebase before final review |
| PR review history | No prior submitted reviews were returned | Formal review submitted by team lead |
| Churn windows | PR code documents 180 days of features and 90 days for the inactivity label | Consistent with proposal; team approval still required |
| Dashboard format | PR adds Streamlit; assigned deliverable specifies Power BI `.pbix` | Confirm scope with team and provide agreed artifact |
| Test evidence | PR reports 28 churn checks and 8 manual dashboard tests | Require reproducible logs/results before acceptance |

### Release gates — do not mark complete until verified

- [ ] Team members confirm the churn definition, snapshot date and 90-day label horizon.
- [ ] Divya confirms cleaned data date coverage, customer-key uniqueness and data-quality evidence.
- [ ] Lav confirms segment labels and the RFM reference-date relationship to the churn cohort.
- [ ] Nivesh supplies the training pipeline, saved preprocessing/model artifact, predictions and reproducible metric output.
- [ ] Raj independently reproduces the reported metrics and records QA results.
- [ ] Sirisha confirms whether the accepted dashboard is Power BI or an explicitly approved Streamlit alternative; the requested `.pbix` is present if Power BI remains in scope.
- [ ] PR branch is current with `main`; refreshed diff is reviewed and checks pass.
- [ ] README, final report, execution commands and dashboard instructions match the actual merged files.
- [ ] Clean-clone execution and final presentation rehearsal are recorded.

### Integration decision

**Status: Integration in progress — PR #13 is not approved for merge.** The churn implementation and dashboard work are present on the PR branch, but branch freshness, team approval, dashboard-format alignment and reproducible test evidence must be resolved first.

