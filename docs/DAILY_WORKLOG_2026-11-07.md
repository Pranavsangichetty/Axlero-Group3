# Daily Work Update — Week 3 Day 1

**Date:** 7 November 2026  
**Owner:** Pranav Sangichetty  
**Role:** Team Leader  
**Task:** Finalize the churn definition and prediction period with the team.

## Work completed today

- Reviewed the repository's project overview and Week 3 churn-prediction plan.
- Identified that Online Retail II contains transaction history rather than an explicit subscription cancellation event.
- Prepared a proposed purchase-inactivity-based churn definition for team discussion.
- Proposed a 180-day observation/feature window and a 90-day prediction/label window.
- Specified customer eligibility, label rules, snapshot-date alignment and leakage-prevention requirements.
- Listed the dataset date-range check required from Divya and the RFM snapshot-date confirmation required from Lav.
- Prepared a team decision table so approval or requested changes can be recorded before Nivesh implements labels.

## Decision status

**Pending team confirmation.** The proposed definition has not been represented as a finalized team decision. The 90-day label period must be supported by a complete follow-up period in the cleaned dataset.

## Next actions

1. Share the proposal with all members and collect feedback.
2. Ask Divya to confirm the cleaned dataset's valid InvoiceDate range and feasible snapshot date(s).
3. Ask Lav to confirm that RFM values can be calculated as of the same snapshot date.
4. Once agreed, communicate the approved definition and date rules to Nivesh and Raj.
5. Update the shared decision record with actual approvals.

## GitHub evidence

- Shared proposal: `docs/WEEK3_CHURN_DEFINITION_AND_PREDICTION_PERIOD.md` on `main`.
- This daily record: `docs/DAILY_WORKLOG_2026-11-07.md` on `Pranavsangichetty`.
