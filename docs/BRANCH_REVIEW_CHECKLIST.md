# Branch and Pull Request Review Checklist

**Maintainer:** Pranav Sangichetty  
**Stable branch:** `main`  
**Personal integration/worklog branch:** `Pranavsangichetty`

## Branch map

- `main` — shared project baseline.
- `Pranavsangichetty` — team-lead worklogs, coordination records and review documentation.
- `Divya-Akbari`, `Lav-Kumar`, `Nivesh243`, `Sirisha`, `raj4089` — member work branches.

A branch existing on GitHub does not prove that it contains current or reviewed work. Compare its head with the intended base and inspect the actual file diff.

## Before opening a pull request

- [ ] Update the feature branch from the latest intended base.
- [ ] Confirm the correct personal/feature branch is checked out.
- [ ] Keep the change focused on one logical task.
- [ ] Check that no unrelated or generated files are included.
- [ ] Run the relevant script, notebook or tests.
- [ ] Update documentation when paths, schemas or commands change.
- [ ] Use a descriptive commit message.
- [ ] Confirm no credentials, private data or local environment files are included.

## Reviewer checklist

- [ ] Does the change match the assigned task?
- [ ] Are files placed in the agreed repository location?
- [ ] Are existing files preserved unless a replacement was intended?
- [ ] Are assumptions and output schemas documented?
- [ ] Are results reproducible from documented inputs?
- [ ] Are metrics and figures traceable to actual outputs?
- [ ] Are tests or execution evidence included?
- [ ] Are downstream modules affected by this change?
- [ ] Is the README or relevant report updated?
- [ ] Are unresolved issues clearly recorded?

## Merge policy

1. Use pull requests to propose changes to `main`.
2. Review the diff and relevant execution evidence.
3. Request changes when important checks fail or evidence is missing.
4. Merge only after conflicts are resolved and required checks pass.
5. After merging, verify the resulting `main` branch and record the PR link.
6. If a stale PR is closed without merging, record that status accurately; do not describe it as merged.

## PR review record

| Date | PR | Source branch | Scope | Review decision | Follow-up |
|---|---|---|---|---|---|
| 2026-11-10 | [#13](https://github.com/Pranavsangichetty/Axlero-Group3/pull/13) | `Lav-Kumar` | Week 3/4 churn, scoring, dashboard and reports | Changes requested; not merged | Closed on 11 Nov 2026 after confirming stale/conflicting branch and selective integration of useful files into main |

## Current release gates

- [ ] Explicit team approval of churn definition and snapshot date.
- [ ] Controlled comparison of single-snapshot and multi-snapshot designs.
- [ ] Clean-environment rerun of churn model and independent metric reproduction.
- [ ] Rerun of contributed data-validation notebooks.
- [ ] Power BI churn page and final dashboard QA.
- [ ] End-to-end clean-clone run and final documentation reconciliation.
- [ ] Final team-lead sign-off after evidence is reviewed.

## Safety

Do not force-push shared branches or overwrite another member's work without coordination. Do not merge an untested model or dashboard artifact merely to meet a commit target.
