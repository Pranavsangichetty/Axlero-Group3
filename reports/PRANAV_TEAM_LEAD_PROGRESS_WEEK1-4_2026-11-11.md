# Team Lead Progress Report — Weeks 1–4

**Prepared by:** Pranav Sangichetty  
**Role:** Team Leader — Group 3  
**Project:** Retail & E-commerce Customer Segmentation and Churn Prediction  
**Dataset:** Online Retail II  
**Repository:** https://github.com/Pranavsangichetty/Axlero-Group3  
**Personal branch:** `Pranavsangichetty`  
**Updated:** 11 November 2026

## 1. Overall responsibility

My responsibility as team leader was to coordinate the six-member team, keep work aligned with the project phases, monitor progress and blockers, review branch/PR changes, maintain shared project documentation, and coordinate integration into `main`. I also maintained a separate personal worklog so that leadership, review and integration activities are traceable. Team members remain the owners of their respective technical modules; this report distinguishes my coordination/review work from their implementation work.

## 2. Week 1 — Project setup, data understanding and coordination

I coordinated the initial division of responsibilities and consolidated the team's Week 1 progress update. I recorded the reported work covering dataset inspection, missing-value and duplicate review, cancellation/invalid-record handling, data cleaning, preprocessing and exploratory data analysis. I documented the handoff requirements for downstream work, particularly the need to agree on processed-data paths, customer identifiers and transaction-date fields before RFM and churn modelling depend on them.

The Week 1 contribution summary was based on updates supplied by team members. My worklog explicitly distinguishes that coordination record from independent rerunning or verification of every individual artifact.

**Evidence:** [Week 1 team contribution report](../reports/week1_team_contribution_update.md) · [My 5 November worklog](DAILY_WORKLOG_2026-11-05.md)

## 3. Week 2 — RFM/segmentation handoff and project alignment

I coordinated the transition from cleaned transaction data and EDA into customer-level analysis. The shared project baseline documents RFM feature generation using Recency, Frequency and Monetary value, followed by K-Means customer segmentation and segment profiling. My team-lead focus was to keep the customer-level data grain, reference date and output schema visible to downstream contributors, and to ensure the segmentation outputs could be connected to the later churn and dashboard work.

The RFM implementation and analytical outputs are owned by the relevant technical contributors; I did not claim authorship of their modelling code. The integration checklist records the remaining need to reconcile the RFM reference date with the churn cohort snapshot.

**Evidence:** [README on main](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/README.md) · [Project integration checklist](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/docs/PROJECT_INTEGRATION_CHECKLIST.md)

## 4. Week 3 — Churn definition, coordination and review criteria

I reviewed the churn-prediction requirements and prepared the proposed purchase-inactivity-based definition: a 180-day feature/observation window followed by a 90-day future label window. Under this proposal, an eligible customer with no valid purchase in the future 90-day period is labelled churned; a customer with at least one valid purchase is labelled active. I documented the need to keep future-period transactions out of the feature set to prevent target leakage, and to ensure the selected snapshot has a complete 90-day follow-up period.

I coordinated the related work allocation: Divya on transaction-date review and the modelling dataset; Lav on RFM scores and segment features; Nivesh on churn labels and prediction features; Sirisha on class balance and evaluation visuals; and Raj on metric definitions and QA. The 180-day/90-day definition was recorded as a proposal pending explicit team confirmation, not as a formally approved team decision.

**Evidence:** [Churn definition and prediction period](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/docs/WEEK3_CHURN_DEFINITION_AND_PREDICTION_PERIOD.md) · [My 7 November worklog](DAILY_WORKLOG_2026-11-07.md)

## 5. Week 4 — GitHub review, selective integration and documentation

I reviewed the member branches and their differences against `main`. Because some branches were materially behind the shared baseline, I did not merge entire branches blindly. I coordinated selective integration of relevant deliverables into `main`, preserving existing shared work and documenting provenance and verification status.

The current `main` contains the supplementary Streamlit dashboard, customer scoring script, sample scoring input and 10-customer demonstration output, Week 3/4 QA reports, and Divya's data verification/modelling/validation notebooks. I also updated shared project documentation, including the README, integration checklist, final project status, execution flow, presentation outline and team integration summary. The Streamlit app reads model metrics from the model metadata file rather than relying on duplicated hard-coded values.

I documented that the 10-row prediction CSV is a demonstration, not full-population scoring. I also kept the two churn dataset designs separate: the current single-snapshot pipeline uses a 180-day pre-cutoff feature window and 90-day future inactivity label; Divya's alternative multi-snapshot design uses a 12-month lookback, multiple reference dates and a different feature/dataset structure. These datasets and metrics must not be combined. A controlled comparison and team decision are still needed.

**Evidence:** [Team integration summary](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/reports/TEAM_INTEGRATION_SUMMARY_2026-11-10.md) · [Integration checklist](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/docs/PROJECT_INTEGRATION_CHECKLIST.md) · [Final project status](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/reports/FINAL_PROJECT_STATUS_2026-11-10.md) · [Execution flow](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/docs/FINAL_PROJECT_EXECUTION_FLOW.md) · [Presentation outline](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/docs/FINAL_REVIEW_PRESENTATION_OUTLINE.md)

## 6. Code review and PR decision

I reviewed [PR #13 — feat: complete week 3 and week 4 project deliverables](https://github.com/Pranavsangichetty/Axlero-Group3/pull/13), from `Lav-Kumar` into `main`. My review was submitted as **Changes requested** on 10 November 2026. The review identified that the branch was substantially behind `main`, the PR had merge conflicts, the dashboard scope did not match the Power BI deliverable requirement, the README/status claims needed reconciliation, and the reported QA results needed reproducible evidence.

After the review, relevant files were selectively integrated into `main` through the integration work. On 11 November 2026, I closed PR #13 **without merging it** because the branch was stale/conflicting and the useful deliverables were already present on `main`. Closing the PR did not delete the branch or its history. No claim is made that PR #13 was merged.

**Review evidence:** [PR #13](https://github.com/Pranavsangichetty/Axlero-Group3/pull/13) · [PR review record](https://github.com/Pranavsangichetty/Axlero-Group3/pull/13#pullrequestreview-)

## 7. Current technical status known from the shared repository

The current main-branch churn model metadata records Logistic Regression as the selected model, with held-out test metrics: Accuracy 0.6807, Precision 0.6529, Recall 0.7224, F1-score 0.6859 and ROC-AUC 0.7308. The stated ROC-AUC target is 0.75, so the target has not yet been met. The sample scoring output contains 10 demonstration customers only.

The Power BI `.pbix` remains a separate deliverable. Its documented current state is two pages (Sales Overview and RFM Segments); the churn page and final Power BI QA remain outstanding. The Streamlit dashboard is supplementary and does not replace Power BI.

## 8. Pending work and owners

| Pending item | Responsible follow-up |
|---|---|
| Confirm the churn definition, snapshot date and prediction horizon | Pranav to collect explicit team confirmation; Divya/Lav/Nivesh to validate feasibility and implementation |
| Compare single-snapshot and multi-snapshot modelling designs | Nivesh, Divya and Raj, with team decision coordinated by Pranav |
| Independently rerun churn model and reproduce metrics/QA | Nivesh and Raj |
| Rerun the contributed data-validation notebooks from a clean environment | Divya |
| Complete Power BI churn page and final dashboard checks | Sirisha |
| Verify the end-to-end clean-clone run and reconcile documentation | Raj and Pranav |
| Review any refreshed PR and record final acceptance | Pranav |

## 9. Final sign-off status

**Team-lead sign-off: pending.** I have completed the documented coordination, review, selective integration and project-status tracking described above. I am not marking the project as fully released or finally signed off yet because the churn design still needs explicit team confirmation, independent clean-run validation remains outstanding, the Power BI churn page and QA are incomplete, and the model ROC-AUC remains below the stated target. Final sign-off should be recorded only after these release gates are resolved or explicitly accepted by the project stakeholders.

## 10. Repository references

- [Repository](https://github.com/Pranavsangichetty/Axlero-Group3)
- [Personal team-lead branch](https://github.com/Pranavsangichetty/Axlero-Group3/tree/Pranavsangichetty)
- [Main README](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/README.md)
- [Team integration summary](https://github.com/Pranavsangichetty/Axlero-Group3/blob/main/reports/TEAM_INTEGRATION_SUMMARY_2026-11-10.md)
- [PR #13 — closed, not merged](https://github.com/Pranavsangichetty/Axlero-Group3/pull/13)
