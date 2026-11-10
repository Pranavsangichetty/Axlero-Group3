# Final Project Status — 10 November 2026

**Project:** Retail & E-commerce Customer Segmentation and Churn Prediction  
**Team:** Group 3  
**Prepared by:** Pranav Sangichetty — Team Leader  
**Repository:** `Pranavsangichetty/Axlero-Group3`  
**Status:** Integration in progress; final merge and review are not yet complete.

## Executive status

The shared `main` branch contains reproducible Week 1 data preparation and Week 2 RFM/segmentation work. Churn prediction and dashboard deliverables are proposed in open PR #13 from `Lav-Kumar`, but they have not yet been integrated into `main`.

The team-lead review has requested changes on PR #13. No code from that PR is being represented as merged or accepted.

## Module status at review time

| Workstream | Current repository evidence | Status | Owner / next action |
|---|---|---|---|
| Data cleaning and validation | Main README and Week 1 scripts/reports; README records reproducible checks | Documented complete on main | Divya: reconfirm final dataset, date range, IDs and validation notebook |
| EDA and RFM segmentation | Main README, RFM outputs and segment reports | Documented complete on main | Lav: confirm four segment labels, counts and snapshot compatibility |
| Churn definition | `docs/WEEK3_CHURN_DEFINITION_AND_PREDICTION_PERIOD.md` | Proposed; team confirmation pending | Pranav: collect member approvals; Divya/Lav validate dates and RFM cutoff |
| Churn modelling | PR #13 adds historical cohort, model training, evaluation and scoring artifacts on `Lav-Kumar` | Present on PR branch; not merged | Nivesh: confirm approved label rule, supply reproducible run evidence |
| Model QA | PR #13 reports 28 validation checks | Claimed on PR branch; evidence needs reproduction | Raj: independently rerun and reconcile metrics |
| Dashboard | Main README records Power BI as partial; PR #13 adds a Streamlit dashboard | Format/scope mismatch to resolve | Sirisha: confirm required Power BI `.pbix` or obtain explicit approval for Streamlit |
| Final report and README | Main has existing documentation; PR #13 adds a completion report and rewrites README | Pending review and reconciliation | Raj: align status, limitations, commands and evidence with merged artifacts |
| Integration and release | PR #13 open; branch comparison shows `Lav-Kumar` 38 commits behind `main`, 1 commit ahead | Blocked pending PR revision | Pranav: review refreshed diff, clean run, merge and prepare review |

## PR #13 — team-lead review

**Title:** `feat: complete week 3 and week 4 project deliverables`  
**Link:** https://github.com/Pranavsangichetty/Axlero-Group3/pull/13

The PR changes nine files, including README, Streamlit dashboard, prediction script, sample scoring data, completion report and Week 3/4 QA reports. It reports a historical cohort of 2,724 customers and Logistic Regression test metrics of Accuracy 0.6807, Precision 0.6529, Recall 0.7224, F1-score 0.6859 and ROC-AUC 0.7308. These are PR-reported values, not independently reproduced by this team-lead review.

**Review outcome:** Changes requested; not merged.

Required before merge:
1. Update the PR branch against current `main` and review the refreshed diff.
2. Record team approval for the churn definition and selected snapshot dates.
3. Resolve the dashboard scope mismatch: the task asks for a Power BI `.pbix`, while the PR adds Streamlit.
4. Reproduce the reported churn checks and dashboard tests; retain logs/evidence.
5. Reconcile README and report status with the actual repository state and execution paths.

## Churn definition alignment

The current shared proposal recommends a 180-day feature/observation window before a snapshot and a 90-day future label window. The PR's churn dataset script uses a 180-day feature period (2 January–30 June 2011) and a 90-day inactivity period (1 July–28 September 2011). This is consistent with the proposed window lengths, but it does not itself prove that the team approved the definition or the selected historical dates.

The target is purchase-inactivity-based proxy churn, not proof of permanent customer loss. Features must use only transactions before the cutoff; future transactions are for label construction only.

## Final project execution flow for review

1. Obtain the permitted Online Retail II source file and place it in the documented raw-data location.
2. Run the data audit and transaction investigation.
3. Run cleaning and generate the processed transaction tables and cleaning evidence.
4. Run EDA and generate the Week 1 visualizations and reports.
5. Run RFM feature generation, scaling and K-Means segmentation.
6. Verify segment labels, profiles, counts and business recommendations.
7. Confirm the churn definition, snapshot dates and complete future label coverage.
8. Build the historical customer-level churn dataset using pre-cutoff features and post-cutoff labels.
9. Train Logistic Regression and Random Forest using a leakage-safe pipeline; compare using the agreed validation method.
10. Save the selected model and preprocessing pipeline; reproduce held-out metrics and confusion matrix/ROC curve.
11. Generate customer-level predictions using the saved model and documented feature schema.
12. Connect validated segmentation and churn outputs to the agreed dashboard format; test filters, visuals and refresh.
13. Run independent QA, update README/final report/data dictionary and record limitations.
14. Perform a clean-clone run, review/merge approved PRs, and rehearse the final presentation.

**Important:** This is the proposed end-to-end flow. Commands and artifact paths must be confirmed against the final merged repository before the presentation.

## Immediate team-lead actions

- Collect explicit churn-definition and snapshot-date confirmation from Divya, Lav and Nivesh; circulate the decision to Sirisha and Raj.
- Ask Divya for the final customer modelling dataset and validation evidence.
- Ask Lav for final RFM outputs, segment profiles and reference date.
- Ask Nivesh for the reproducible model pipeline, saved model, prediction output and evaluation artifacts.
- Ask Sirisha to confirm and submit the agreed dashboard file and refresh guide.
- Ask Raj to reproduce model metrics, test execution instructions and finalize the QA/report package.
- Re-review PR #13 only after its branch is current and all acceptance gates are evidenced.

## Release decision

**Do not mark the project fully integrated or ready for final submission yet.** Week 1 and Week 2 are documented complete on `main`; Week 3 and Week 4 have substantial work on PR #13 but remain pending review, branch synchronization, scope confirmation and evidence-based acceptance.

# Integration update — 10 November 2026

This addendum supersedes the earlier snapshot in this report.

## Selective member integration into main

The main branch now contains:
- Divya's four data verification, modelling dataset and validation notebooks in `notebooks/team_contributions/`.
- Lav's Streamlit dashboard, customer scoring script, sample scoring input/output and Week 3/4 QA reports.
- The single-snapshot churn dataset builder, model training script, validation script, saved model, model metadata and evaluation outputs.
- The existing Power BI `.pbix` remains in the repository as the requested dashboard artifact.

The branches were not merged wholesale because several member branches were materially behind main. Individual files and reports were copied selectively to avoid overwriting newer shared work.

## Updated status

| Workstream | Current main status | Remaining action |
|---|---|---|
| Week 1 cleaning and EDA | Existing main pipeline and reports | Re-run clean clone and retain current evidence |
| Week 2 RFM segmentation | Existing main data and four segment profiles | Reconcile RFM snapshot with churn cohort |
| Divya data engineering | Four notebooks integrated; saved notebook evidence reports 83/83 and 42/42 validation checks | Re-run notebooks from clean setup; compare alternative modelling design |
| Nivesh churn model | Single-cohort dataset, Logistic Regression/Random Forest training, validation code, saved model and metadata present | Team approval and independent rerun |
| Lav customer scoring | Scoring script and 10-row sample input/output integrated | Generate full eligible-population scoring only after approved feature pipeline |
| Lav dashboard | Streamlit app integrated and model metrics read from metadata | Run locally and test clean clone |
| Sirisha Power BI | Existing two-page PBIX remains | Add churn page and verify interactions/refresh |
| Raj QA/documentation | Churn evaluation and Week 3/4 QA reports present | Independently reproduce metrics and tests |
| Pranav integration | README, checklist, execution flow, review outline and integration summary updated | Confirm final modelling design and release readiness |

## Model design reconciliation

The current saved model is based on one historical cohort, 180 days of pre-cutoff features and a 90-day future inactivity label. Saved held-out test results are Accuracy 0.6807, Precision 0.6529, Recall 0.7224, F1-score 0.6859 and ROC-AUC 0.7308. ROC-AUC is below the stated 0.75 target.

Divya's notebook study constructs 16,495 customer-reference-date rows across four reference dates, with 12-month feature lookback and 18 features. It reports 83/83 checks and 42/42 checks passing in saved notebook outputs. This is an alternative multi-snapshot dataset design, not the dataset used to train the currently saved model. No metrics from one design should be attributed to the other.

## Dashboard decision

The Streamlit dashboard is an additional interactive view and includes segmentation, historical churn and a sample customer table. It does not replace the assigned Power BI deliverable. The Power BI file still needs a churn page and final QA.

## Release decision

**Core Week 3 code and supporting member artifacts are now present on main, but final release is not yet approved.** Required next steps are team confirmation of the modelling design, clean-clone reruns by Nivesh/Raj, notebook reruns by Divya, Power BI completion by Sirisha and final integration sign-off by Pranav.
