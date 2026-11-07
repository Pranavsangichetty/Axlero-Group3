# Week 3 Day 1 — Churn Definition and Prediction Period

**Project:** Retail & E-commerce Customer Segmentation and Churn Prediction  
**Prepared by:** Pranav Sangichetty (Team Leader)  
**Date:** 7 November 2026  
**Status:** Proposed for team confirmation — not yet finalized

## 1. Purpose

Agree on a consistent, measurable churn definition and prediction period before the team creates churn labels, builds features or trains models.

The project uses Online Retail II transaction history. It does not contain an explicit subscription cancellation or account-closure event. Therefore, the team should describe the target as **purchase-inactivity-based (proxy) churn**, not confirmed customer cancellation.

## 2. Recommended definition for team approval

A customer is labelled **churn-risk / churned for the modelling target** when:

- The customer made at least one valid purchase during the observation window; and
- The customer made **no valid purchase during the following 90-day prediction window**.

A customer with one or more valid purchases during the prediction window is labelled **not churned** for this target.

This is a modelling proxy based on observed purchasing inactivity. It does not prove that a customer has permanently left the business.

## 3. Proposed time windows

| Component | Proposal |
|---|---|
| Observation / feature window | 180 days immediately before the snapshot date |
| Snapshot / prediction date | The cutoff date at which features are calculated |
| Prediction / label window | 90 days immediately after the snapshot date |
| Eligibility | At least one valid purchase in the 180-day observation window |
| Positive churn label | Zero valid purchases in the following 90 days |
| Negative churn label | One or more valid purchases in the following 90 days |

**Timeline:**

```text
180-day observation window              90-day prediction window
(features only)                         (label only)
|--------------------------------------|--------------------------|
                                  Snapshot date
                                  Model predicts here
```

## 4. Rules to prevent data leakage

1. Calculate every feature using transactions dated on or before the snapshot date and within the agreed observation window.
2. Do not use any transaction from the 90-day prediction window as a model feature.
3. Use the prediction window only to generate the target label.
4. Calculate RFM values as of the same snapshot date. Do not use RFM values calculated using the full dataset if they include transactions after that date.
5. Select snapshot dates only where the dataset contains the complete 90-day follow-up period. Otherwise, churn labels cannot be reliably assigned.
6. Use chronological/time-based validation where possible; do not randomly mix future information into training features.

## 5. Dataset-specific feasibility check

Before confirming the dates, Divya and Nivesh should check the minimum and maximum valid InvoiceDate values after cleaning. The latest usable snapshot date must be at least 90 days before the last date with observable transactions, so the full label window is available.

If the team uses multiple snapshots, ensure a customer's feature and label windows are constructed consistently and that overlapping windows are considered when splitting data for validation.

## 6. Responsibilities and handoff

| Member | Confirmation / action needed |
|---|---|
| Pranav | Coordinate approval of the churn definition, observation window and prediction horizon |
| Divya | Confirm valid transaction date range and whether the proposed 180 + 90 day windows are feasible |
| Lav Kumar | Confirm RFM features can be recalculated as of each agreed snapshot date |
| Nivesh243 | Implement labels only after the team approves the definition and cutoff rules |
| Sirisha | Plan visuals using the agreed churn label and class distribution |
| Raj | Align metric reporting with the positive churn class and agreed validation strategy |

## 7. Team decision record

The following fields must be completed after the team discusses and approves the proposal.

| Decision item | Proposed value | Team status |
|---|---|---|
| Churn concept | No purchase in the next 90 days | Pending confirmation |
| Observation window | Previous 180 days | Pending confirmation |
| Prediction horizon | Next 90 days | Pending confirmation |
| Customer eligibility | At least one purchase in observation window | Pending confirmation |
| Snapshot date(s) | Based on valid data coverage | Pending Divya/Nivesh check |
| RFM reference date | Same as snapshot date | Pending Lav confirmation |

**Approval record**

| Team member | Approved / changes requested | Date | Notes |
|---|---|---|---|
| Divya | Pending |  |  |
| Lav Kumar | Pending |  |  |
| Nivesh243 | Pending |  |  |
| Sirisha | Pending |  |  |
| Raj | Pending |  |  |
| Pranav | Coordinator; awaiting team responses |  |  |

## 8. Finalization rule

This is a recommendation prepared for discussion, not a confirmed team decision. Update the status to **Approved** only after the relevant members confirm the windows and Divya verifies that the dataset supports a complete 90-day label period. Nivesh should then use this approved definition for churn-label implementation.
