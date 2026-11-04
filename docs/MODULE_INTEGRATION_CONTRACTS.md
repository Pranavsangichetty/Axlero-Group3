# Module Integration Contracts

This document defines the hand-off information required between Group 3 modules. The proposed names below are examples; module owners should confirm actual paths and column names before connecting code.

## 1. Data engineering and cleaning — Divya

**Handoff:** reproducible cleaned transaction data plus a data-quality summary.

Minimum documentation:
- Input file name and permitted access method.
- Cleaning rules and order of operations.
- Treatment of missing Customer IDs, cancellations, duplicates and invalid quantities/prices.
- Output file path, row count and date range.
- Column names, data types and revenue calculation.

**Acceptance checks:** output can be regenerated; row counts are recorded; no raw data is silently overwritten.

## 2. EDA and customer segmentation — Lav

**Handoff:** EDA summary, customer-level RFM table, cluster assignments and segment profile.

Minimum documentation:
- Snapshot/observation date.
- Recency, Frequency and Monetary definitions.
- Customer eligibility and exclusions.
- Transformations/scaling and K-Means settings.
- Cluster evaluation results and rationale for selected k.
- Segment profile and business interpretation.

**Acceptance checks:** one row per eligible customer; cluster IDs map to labels consistently; customer totals reconcile with the profile.

## 3. Churn prediction and model training — Nivesh243

**Handoff:** reproducible training pipeline, candidate model artifacts and customer-level prediction output.

Minimum documentation:
- Operational churn definition and prediction horizon.
- Observation cutoff and label window.
- Feature list and feature availability dates.
- Leakage prevention and train/test strategy.
- Class distribution and any imbalance handling.
- Logistic Regression and Random Forest settings.
- Saved preprocessing/model pipeline and output schema.

**Acceptance checks:** no future information enters features; preprocessing is fitted on training data only; test data is not used for tuning; predictions can be regenerated.

## 4. Visualization and dashboard — Sirisha

**Handoff:** dashboard file plus a short guide to data sources, refresh and interactions.

Minimum documentation:
- Tool and version.
- Source tables/files and refresh steps.
- KPI formulas and filter definitions.
- Dashboard pages and intended audience.
- Screenshots and test notes.

**Acceptance checks:** displayed values reconcile with validated source outputs; filters behave correctly; no placeholder or fabricated metrics remain.

## 5. Model evaluation and documentation — raj4089

**Handoff:** model comparison, evaluation report, test evidence and final documentation.

Minimum documentation:
- Confusion matrix and precision, recall, F1-score and ROC-AUC where appropriate.
- Positive-class definition and class balance.
- Validation method and threshold rationale.
- Limitations and potential operational impact.
- Reproduction commands and dependency versions.

**Acceptance checks:** metrics correspond to the saved model and stated test split; the report distinguishes measured results from recommendations.

## 6. Team leadership and integration — Pranav

**Handoff:** reviewed module interfaces, integration checklist, branch/PR review record and release coordination.

Minimum documentation:
- Current status and owner for each module.
- Open blockers and decisions.
- Accepted artifact paths and versions.
- Integration and clean-run results.
- Pull requests reviewed and merged.

**Acceptance checks:** no module is marked complete without inspected evidence; changes are integrated without overwriting another member's work.

## Change protocol

1. Module owner announces a proposed output/schema change.
2. Affected owners review the change before implementation.
3. Update this contract and the relevant README instructions.
4. Make the change on the owner's branch and open a pull request.
5. Run affected validation checks before merging.
