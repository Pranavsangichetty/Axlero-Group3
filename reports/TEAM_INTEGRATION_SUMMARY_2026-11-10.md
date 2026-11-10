# Team Integration Summary — 10 November 2026

**Project:** Retail & E-commerce Customer Segmentation and Churn Prediction  
**Team Lead:** Pranav Sangichetty  
**Branch updated:** `main`  
**Integration method:** Selective integration of verified source files and saved evidence from member branches; stale branches were not merged wholesale.

## 1. Contributions integrated into main

| Member | Workstream | Integrated evidence | Current status |
|---|---|---|---|
| Pranav Kumar | Team coordination and integration | Updated README, integration checklist, execution flow, review outline and this summary | Integration coordination documented; release sign-off pending |
| Divya Akbari | Data engineering, customer modelling dataset and validation | Four notebooks copied to `notebooks/team_contributions/`; summary at `reports/divya_modelling_dataset_validation.md` | Notebook evidence preserved; multi-snapshot design needs modelling comparison |
| Lav Kumar | EDA/RFM handoff, customer scoring and dashboard | Existing RFM files on main; added `src/predict_customers.py`, sample scoring input/output, `dashboard/app.py`, Week 3/4 QA reports | Streamlit dashboard is supplementary; Power BI remains required |
| Nivesh243 | Churn prediction and model training | Main contains `src/churn_dataset.py`, `src/churn_prediction.py`, `src/validate_churn_model.py`, `models/churn_model.pkl`, metadata and evaluation files | Single-cohort model artifacts integrated; final temporal validation and team sign-off pending |
| Sirisha | Dashboard and visualization | Existing `Customer_Segmentation_Dashboard.pbix` and dashboard documentation remain in main; Streamlit view added as supplementary | Power BI churn page and final .pbix QA remain outstanding |
| Raj / raj4089 | Evaluation, QA and documentation | `reports/churn_model_evaluation.md`, `reports/week3_qa_report.md`, `reports/week4_qa_report.md`, validation scripts and project docs | QA reports are preserved; independent clean-clone rerun still required |

## 2. Churn model currently represented in main

The reproducible single-snapshot implementation uses:
- Feature window: 2 January 2011 to 30 June 2011 (180 days).
- Prediction/label window: 1 July 2011 to 28 September 2011 (90 days).
- Cohort: 2,724 customers.
- Churn label: no purchase during the 90-day future window.
- Churned: 1,315; active: 1,409.

Selected candidate: Logistic Regression, chosen by mean 3-fold training cross-validation ROC-AUC.

| Held-out test metric | Saved value |
|---|---:|
| Accuracy | 0.6807 |
| Precision | 0.6529 |
| Recall | 0.7224 |
| F1-score | 0.6859 |
| ROC-AUC | 0.7308 |

Training cross-validation ROC-AUC: 0.7639. The held-out ROC-AUC is below the stated 0.75 target. Do not report the target as achieved. The 90-day inactivity target is a proxy, not proof of permanent customer loss.

## 3. Divya's alternative multi-snapshot modelling design

Divya's notebooks report 16,495 customer-reference-date rows, 18 engineered features, three development reference dates and one out-of-time reference date. This design uses a 12-month feature lookback and a three-month future inactivity target, with 30-day minimum customer history. The validation notebook reports 83/83 checks passed and the customer ID/reference-date notebook reports 42/42 checks passed.

This is a different design from the single-snapshot six-feature model. It has been integrated as a separate notebook study, not merged into the trained model dataset. A controlled model comparison on the out-of-time split is required before replacing the current model pipeline.

## 4. Dashboard integration

- `dashboard/app.py` is an additional Streamlit dashboard with executive overview, RFM segments, historical churn analysis and customer details.
- Model performance chart values are read from `models/model_metadata.json`, not duplicated as hard-coded values.
- The committed prediction output contains only 10 sample customers. Blank scores for other customers mean no sample prediction is available.
- `Customer_Segmentation_Dashboard.pbix` remains the Power BI deliverable. Its churn page and final Power BI QA are still open. Streamlit does not silently replace the assigned Power BI deliverable.

Run the supplemental dashboard from the repository root:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## 5. Verification and release gates

The source notebooks and QA reports contain saved execution outputs from the member branches. Copying these artifacts into main does not mean they were freshly rerun in a clean clone during this integration.

Before final submission:
- [ ] Team confirms whether the final churn modelling design is the 180-day single snapshot or Divya's 12-month multi-snapshot approach.
- [ ] Nivesh and Raj run the current model validation on a clean clone and retain the generated results.
- [ ] Divya's notebooks are rerun using the documented raw dataset and local working directory.
- [ ] Run the customer scoring script and confirm its output matches the saved model pipeline.
- [ ] Sirisha completes the Power BI churn page, filters, KPI reconciliation and refresh testing, or the team explicitly approves a different final format.
- [ ] Raj reconciles QA counts, limitations, final report and README against actual generated outputs.
- [ ] Pranav completes final review and presentation rehearsal.

## 6. Integration decision

**Status: Core churn code, model artifacts, customer scoring workflow, supplemental Streamlit dashboard and Divya's validation notebooks are now present on main. The project is not yet release-ready.** Remaining blockers are the choice between the two feature-window/cohort designs, clean-clone independent QA, and completion of the required Power BI dashboard.
