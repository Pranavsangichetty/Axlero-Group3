# Clean-Clone Integration Test Plan

**Owner:** Pranav Sangichetty  
**Purpose:** Verify that the project can be set up and its documented workflow can be followed from a fresh clone, without relying on files that exist only on one contributor's computer.

## Preconditions

- Repository is accessible to the tester.
- Required dataset is available through an approved source and placed at the documented path.
- Python version and dependencies are documented.
- No credentials or private data are required in committed files.

## Test procedure

### 1. Clone and inspect

```bash
git clone https://github.com/Pranavsangichetty/Axlero-Group3.git
cd Axlero-Group3
git branch -a
```

Expected: repository clones successfully and the expected branches are visible after fetching remote refs.

### 2. Create an isolated environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Expected: dependency installation completes without relying on globally installed packages.

### 3. Verify inputs and paths

- [ ] Confirm README identifies the required dataset and expected location.
- [ ] Confirm no required local-only file is missing from the repository or documented download process.
- [ ] Confirm scripts use repository-relative paths or clearly documented configuration.
- [ ] Confirm raw data is not modified in place.

### 4. Run the documented modules

Run only commands that correspond to files actually present in the current branch. The README currently documents these Week 1 and Week 2 commands:

```bash
python src/data_quality_audit.py
python src/investigate_transactions.py
python src/clean_data.py
python src/eda.py
python src/rfm_analysis.py
```

If a command fails because the file, dataset or dependency is absent, record the exact failure and assign it to the relevant module owner. Do not mark the test as passed.

### 5. Validate churn and dashboard when delivered

- [ ] Confirm churn target and feature cutoffs are documented.
- [ ] Run the training/evaluation pipeline using the documented command.
- [ ] Confirm saved model and prediction outputs are generated.
- [ ] Compare reported metrics with the generated evaluation output.
- [ ] Open the dashboard and verify source connections, filters and KPI totals.
- [ ] Record tool/version and any manual refresh steps.

### 6. Record results

| Test date | Commit/branch | Command or check | Result (Pass/Fail/Blocked) | Evidence or error | Owner |
|---|---|---|---|---|---|
| YYYY-MM-DD |  |  | Not run |  |  |

## Completion criteria

The clean-run test is complete only when the documented setup and applicable workflows have been run from a fresh clone, failures are resolved or explicitly recorded, and the evidence is linked in the project review record.

**Important:** This file is a test plan, not a claim that the project has already passed these tests.
