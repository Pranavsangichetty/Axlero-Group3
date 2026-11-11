# Team Lead Worklog — Pranav Sangichetty

**Repository:** Pranavsangichetty/Axlero-Group3  
**Working branch:** `Pranavsangichetty`  
**Purpose:** Evidence-based record of team coordination, review, integration decisions and release tracking.

## Team responsibilities

| Member | Area | Evidence to request |
|---|---|---|
| Divya | Data engineering and cleaning | Cleaning script/notebook, processed-data description and quality checks |
| Lav Kumar | EDA and customer segmentation | EDA outputs, RFM calculations, cluster results and recommendations |
| Nivesh243 | Churn prediction and model training | Target definition, feature pipeline, model artifacts and predictions |
| Sirisha | Visualization and dashboard | Dashboard file, source mapping, screenshots and test notes |
| raj4089 | Model evaluation and documentation | Metrics, validation report, README and final report |
| Pranav Sangichetty | Leadership and integration | Task coordination, decisions, PR reviews, integration and final checks |

## Week 1–4 leadership summary

- **Week 1:** Coordinated role allocation and consolidated the team-supplied data cleaning/EDA progress update. Recorded shared-data handoff requirements and follow-up checks.
- **Week 2:** Coordinated the transition into RFM and K-Means segmentation, keeping customer grain, reference-date alignment and downstream data dependencies visible.
- **Week 3:** Prepared and documented the proposed 180-day feature/observation plus 90-day future inactivity-label definition; coordinated module handoffs and leakage-prevention requirements. Team approval of the definition/snapshot remains to be collected.
- **Week 4:** Reviewed member branches, selectively integrated relevant notebooks, scripts, reports, sample scoring files and the supplementary Streamlit dashboard into `main`; updated shared project documentation and recorded differences between the two churn dataset designs.
- **Review:** Submitted Changes requested on PR #13 on 10 November. Closed it without merging on 11 November after confirming merge conflicts/stale branch status and that the useful deliverables were already selectively present on `main`.
- **Sign-off:** Final sign-off remains pending because clean-run verification, churn design confirmation, Power BI churn-page completion/QA and final end-to-end review remain outstanding.

## Daily coordination routine

### Start of day
- Confirm the active phase and expected deliverables.
- Check each owner's progress and blockers.
- Confirm branch names and latest base branch.
- Identify shared files that must not be edited concurrently.

### During development
- Keep tasks small and specific.
- Ask owners to record assumptions and output paths.
- Coordinate schema changes before downstream work depends on them.
- Review actual diffs rather than commit counts alone.

### End of day
- Check pushed commits and pull requests.
- Verify changed files are relevant and non-duplicative.
- Record completed work, blockers and next actions.
- Do not mark a deliverable complete without evidence.

## Decision log

| Date | Decision | Reason | Affected modules | Follow-up |
|---|---|---|---|---|
| 2026-11-10 | PR #13 — Lav-Kumar | Stale branch, merge conflicts, dashboard scope mismatch and missing reproducible evidence | Changes requested; not merged | Review refreshed work only if a new/current PR is submitted |
| 2026-11-11 | PR #13 closed | Useful deliverables had already been selectively integrated into main; stale/conflicting PR was not safe to merge wholesale | PR closed without merge; source branch/history retained | Use a fresh PR from an updated branch for any genuinely new changes |
| 2026-11-11 | Personal branch synchronized | Personal branch had no unique commits and was 73 commits behind main | Fast-forwarded `Pranavsangichetty` to current main; no force push | Keep personal worklogs on this branch |

## Daily work log

| Date | Member/module | Work reviewed | Evidence | Status / next action |
|---|---|---|---|---|
| 2026-11-05 | Team coordination / Week 1 | Consolidated six members' supplied Week 1 contributions and documented handoff requirements | `docs/DAILY_WORKLOG_2026-11-05.md`; `reports/week1_team_contribution_update.md` | Recorded; independently verify member artifacts where required |
| 2026-11-07 | Churn definition / Week 3 | Drafted 180-day feature and 90-day future inactivity-label proposal; documented leakage and date checks | `docs/DAILY_WORKLOG_2026-11-07.md`; `docs/WEEK3_CHURN_DEFINITION_AND_PREDICTION_PERIOD.md` | Proposal pending explicit team approval |
| 2026-11-10 | PR review / integration | Reviewed PR #13, requested changes, updated shared status/integration documentation and selectively integrated member artifacts into main | [PR #13](https://github.com/Pranavsangichetty/Axlero-Group3/pull/13); [Team integration summary](../reports/TEAM_INTEGRATION_SUMMARY_2026-11-10.md) | Relevant deliverables present on main; final QA/release gates remain |
| 2026-11-11 | PR closure / personal progress record | Confirmed PR #13 remained unmerged and closed it; synchronized personal branch and prepared Week 1–4 report | [PR #13](https://github.com/Pranavsangichetty/Axlero-Group3/pull/13); `reports/PRANAV_TEAM_LEAD_PROGRESS_WEEK1-4_2026-11-11.md` | PR closed without merge; final sign-off pending |

## Integration and release notes

- Main branch is the shared project baseline.
- `Pranavsangichetty` is the personal team-lead worklog branch.
- Member work is selectively integrated only after reviewing file-level differences and preserving newer shared work.
- Streamlit is supplementary and does not replace the Power BI deliverable.
- The 10-row customer scoring CSV is a demonstration, not full-population scoring.
- Reported notebook/QA outputs are not described as independently rerun unless a fresh execution has been performed.

## Reporting principles

- Record only work that has actually been completed and reviewed.
- Distinguish planned, in-progress, blocked and completed work.
- Do not create artificial commits or duplicate files to inflate activity.
- Never store passwords, tokens, private customer data or other secrets in this worklog.
