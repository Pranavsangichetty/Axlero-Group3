# Branch and Pull Request Review Checklist

**Maintainer:** Pranav Sangichetty  
**Stable branch:** `main`  
**Personal integration branch:** `Pranavsangichetty`

## Branch map

The repository branch search currently shows:
- `main`
- `Pranavsangichetty`
- `Divya-Akbari`
- `Lav-Kumar`
- `Nivesh243`
- `Sirisha`
- `raj4089`

A branch existing on GitHub does not by itself prove that it contains current or reviewed work. Check its latest commits and file changes.

## Before opening a pull request

- [ ] Pull the latest changes from the intended base branch.
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

## PR review record

| Date | PR | Source branch | Scope | Review decision | Follow-up |
|---|---|---|---|---|---|
| YYYY-MM-DD |  |  |  | Pending |  |

## Safety

Do not force-push shared branches or overwrite another member's work without coordination. Do not merge an untested model or dashboard artifact merely to meet a commit target.
