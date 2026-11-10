# Final Review Presentation — Slide Outline

**Project:** Retail & E-commerce Customer Segmentation and Churn Prediction  
**Team:** Group 3 | **Coordinator:** Pranav Sangichetty  
**Prepared:** 10 November 2026

> Use this as the review structure. Replace pending items with verified evidence after the final PR is merged and the team confirms the outstanding decisions.

## Slide 1 — Title and team
- Project title, Axlero – Innovating Solutions, Group 3.
- Team members and responsibilities.
- One-sentence objective: turn retail transactions into customer insights, segments and churn-risk evidence.

## Slide 2 — Problem statement and objectives
- Understand purchasing behaviour.
- Clean and validate transaction data.
- Segment customers using RFM and K-Means.
- Build a leakage-safe inactivity-based churn prediction workflow.
- Present validated results in the agreed dashboard.

## Slide 3 — Dataset and preparation (Week 1)
- Online Retail II dataset and key fields.
- Cleaning sequence: audit, duplicates, cancellations, invalid quantity/price, customer IDs.
- Show verified row counts, missing-value evidence and data-quality limitations.
- Evidence: Week 1 progress report, cleaning log and validation outputs.

## Slide 4 — EDA findings (Week 1)
- Monthly orders and revenue.
- Order value distribution.
- Top countries, customers and products.
- Highlight business observations only where supported by saved charts/reports.

## Slide 5 — RFM segmentation (Week 2)
- Define Recency, Frequency and Monetary.
- Explain scaling and K-Means.
- Explain why four business-oriented segments were selected even though k=2 has the higher silhouette score.
- Show segment counts and profiles.

## Slide 6 — Four customer segments and actions
- Champions: VIP benefits and referral opportunities.
- Loyal High-Value: personalized loyalty and engagement.
- Recent Customers: second-purchase encouragement.
- At-Risk / Hibernating: cost-effective re-engagement.
- Present recommendations as hypotheses to test, not guaranteed outcomes.

## Slide 7 — Churn definition and dataset
- State that churn is a 90-day purchase-inactivity proxy, not permanent cancellation.
- Show the 180-day pre-snapshot feature window and 90-day post-snapshot label window.
- Explain cohort eligibility, snapshot date and leakage prevention.
- Include the final team-approved date range only after confirmation.

## Slide 8 — Model development and evaluation
- Compare Logistic Regression and Random Forest.
- Explain the training-only cross-validation selection process.
- Present Accuracy, Precision, Recall, F1-score and ROC-AUC.
- Include confusion matrix and ROC curve.
- Distinguish training CV performance from held-out test performance.
- Include independently reproduced metrics only.

## Slide 9 — Dashboard demonstration
- Show the agreed final dashboard artifact.
- Executive overview and customer segments.
- Churn distribution and model performance.
- Customer details, filters and export.
- Demonstrate refresh and interaction behaviour.
- If Power BI remains the required format, show the final `.pbix`; do not substitute Streamlit without approval.

## Slide 10 — QA, limitations and next steps
- Data/model/dashboard test totals with evidence.
- Data loss, missing customer IDs, cancellation discrepancies, historical cohort limits and sample scoring limitations.
- Remaining integration items and practical next steps.

## Slide 11 — Conclusion and Q&A
- Summarize the project flow from transaction data to business recommendations.
- Explain what has been verified and what remains limited.
- Invite questions.

## Evidence checklist before presenting
- [ ] Final cleaned dataset and data validation evidence.
- [ ] Final RFM outputs, segment profile and recommendations.
- [ ] Approved churn definition and snapshot date(s).
- [ ] Saved model and preprocessing pipeline.
- [ ] Reproduced model metrics, confusion matrix and ROC curve.
- [ ] Final prediction output and its population coverage.
- [ ] Agreed dashboard file, refresh guide and test evidence.
- [ ] README, final report and clean-clone execution results.
- [ ] PRs merged only after review; no pending blockers represented as complete.
