# Divya's Data Engineering Deliverables — Integration Notes

**Contributor:** Divya Akbari  
**Source branch:** `Divya-Akbari`  
**Integrated into:** `main/notebooks/team_contributions/`  
**Review date:** 10 November 2026

## Integrated notebooks

1. `01_Data_Verification.ipynb` — verifies the cleaned transaction dataset, cancellation rows, key fields, date range and cleaning outputs.
2. `02_Modelling_and_Feature_Dataset.ipynb` — constructs a customer-level modelling dataset and feature-only dataset across multiple historical reference dates.
3. `03_Data_Validation.ipynb` — independently recalculates the modelling rows/features/labels and checks dataset consistency and leakage.
4. `04_Customer_ID_and_Reference_Date_Check.ipynb` — checks five-digit customer IDs, eligibility at each reference date, complete time windows and row-level dates.

These notebooks are preserved as contributed analytical evidence. They are not silently substituted for the current `src/` pipeline.

## Reported notebook evidence

The executed notebook outputs on `Divya-Akbari` report:

- Raw source: 1,067,371 rows, 8 columns.
- Clean transaction output: 1,003,338 rows.
- Cancellation output: 17,914 rows.
- Known customers: 5,852; 226,761 transaction rows without a customer ID are excluded from customer-level modelling.
- Customer-level modelling dataset: 16,495 rows × 22 columns.
- Feature-only dataset: 16,495 rows × 21 columns.
- Feature set: 18 engineered features.
- Four reference dates: 1 Dec 2010, 1 Mar 2011, 1 Jun 2011 and 1 Sep 2011.
- Development rows: 3,921 + 4,132 + 4,214; out-of-time test rows: 4,228.
- Churn label: no order in the three months after the reference date.
- The validation notebook reports 83/83 checks passed; the customer ID/reference-date notebook reports 42/42 checks passed.

These are the saved notebook outputs from Divya's branch. They have not been re-executed from a clean clone as part of this integration.

## Important modelling design difference

The currently integrated churn model in `src/churn_dataset.py` uses one historical cohort with a 180-day feature window and a 90-day label window. Divya's notebook design uses a 12-month feature window, four quarterly reference dates, an eligibility rule requiring at least 30 days of customer history, and a three-month target window.

Both designs use a three-month inactivity label, but their feature lookback, reference dates, cohort construction and row grain differ. Therefore:

- Keep the current six-feature, single-cutoff pipeline as the reproducible model that produced the metrics in `reports/churn_model_evaluation.md`.
- Treat Divya's multi-snapshot, 18-feature dataset as a separate temporal-validation / expanded-feature design for evaluation.
- Do not concatenate the two datasets or reuse model metrics across them.
- Before adopting Divya's design as the final modelling approach, run a documented model comparison using the multi-snapshot dataset and an out-of-time split, then have Nivesh and Raj review the results.

## Execution note

The notebooks were authored to read `online_retail_II.csv` and intermediate files from a local `Working_Data/` directory. The raw dataset is intentionally not committed. Follow each notebook's setup notes and keep generated data local or in approved ignored paths.
