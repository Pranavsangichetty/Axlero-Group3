# Data Cleaning Documentation

Prepared by raj4089 (Evaluation, QA & Documentation). Every number in this file was produced by running `src/data_quality_audit.py` and `src/clean_data.py` on the raw file (SHA-256 `32569a66…41d3a9`) on 2026-11-10 and was compared with the committed reports (identical). Related files: `reports/cleaning_log.csv`, `reports/cleaning_summary.csv`, `reports/data_quality_summary.csv`, `reports/missing_values_report.csv`.

## 1. What goes in and what comes out

| Stage | File | Rows |
|---|---|---:|
| Raw data (never modified) | `data/raw/online_retail_II.csv` | 1,067,371 |
| Cleaned sales, guests kept | `data/interim/cleaned_transactions.csv` | 1,007,913 |
| Cleaned sales with a Customer ID | `data/processed/customer_transactions.csv` | 779,425 |

Date range: 1 Dec 2009 07:45 to 9 Dec 2011 12:50 (no row has an invalid date).

## 2. Problems found in the raw data (audit)

| Issue | Rows | % of raw | How it is handled |
|---|---:|---:|---|
| Exact duplicate rows | 34,335 | 3.22% | Removed (step 1) |
| Cancelled invoices (Invoice starts with `C`) | 19,494 | 1.83% | Removed (step 2); 19,104 remain after step 1 |
| Negative quantities | 22,950 | 2.15% | 19,493 are on cancelled invoices (step 2); 3,457 are not and are removed by step 3 |
| Zero prices | 6,202 | 0.58% | Removed (step 4); none is on a cancelled invoice |
| Negative prices | 5 | 0.00% | Removed (step 4); all are "Adjust bad debt" entries |
| Missing Customer ID | 243,007 | 22.77% | Kept in the sales data, left out of the customer table |
| Missing Description | 4,382 | 0.41% | Removed by step 4: all have price 0 and no Customer ID |

## 3. Cleaning steps in the order they run

The order matters: duplicates are removed first, so later counts are counted without them.

| # | Step (code rule) | Rows removed | % of raw | Rows left | Reason |
|---|---|---:|---:|---:|---|
| 0 | Raw data | | | 1,067,371 | Starting point |
| 1 | Exact duplicate removal (`drop_duplicates()`) | 34,335 | 3.22% | 1,033,036 | The same line recorded twice would count a sale twice |
| 2 | Cancelled invoice exclusion (`Invoice` starts with `C`) | 19,104 | 1.79% | 1,013,932 | A cancellation is not a completed sale |
| 3 | Positive quantity filter (`Quantity > 0`) | 3,393 | 0.32% | 1,010,539 | Negative quantities that are not on a `C` invoice are stock adjustments or returns |
| 4 | Positive price filter (`Price > 0`) | 2,626 | 0.25% | 1,007,913 | Zero prices are free items, damages or write-offs; negative prices are bad-debt entries |
| 5 | Valid invoice date filter | 0 | 0.00% | 1,007,913 | All dates are valid |
| | **Total removed** | **59,458** | **5.57%** | **1,007,913** | |

After step 5:
- `TotalPrice = Quantity × Price` is added and the data is saved to `data/interim/cleaned_transactions.csv`.
- Rows with a Customer ID (779,425 rows, 5,878 customers) are saved to `data/processed/customer_transactions.csv`.
- Text columns `Invoice`, `StockCode` and `Country` have leading and trailing spaces removed; `Customer ID` becomes a nullable whole number; `InvoiceDate` becomes a date-time.

### Headline figures after cleaning (`cleaning_summary.csv`)

| Metric | Value |
|---|---:|
| Cleaned transaction rows | 1,007,913 |
| Customer transaction rows | 779,425 |
| Unique customers | 5,878 |
| Unique invoices | 40,077 |
| Unique products (StockCodes) | 4,916 |
| Countries | 43 |
| Total sales revenue | 20,476,260.45 |
| Revenue from rows with a Customer ID | 17,374,804.27 (84.9%) |

### Reconciliation of customers
The raw data has 5,942 distinct Customer IDs and the customer table has 5,878. The 64 missing customers have only cancellation rows (129 rows) or zero/negative-price rows (3 rows), so no completed sale remains for them.

## 4. Decisions and assumptions

1. **Raw data is never modified.** All outputs are new files.
2. **Guest orders are kept in the sales figures** (22.7% of cleaned rows) because they are real sales, but they cannot be used for customer-level analysis such as RFM.
3. **Exact duplicates are treated as errors.** The data has no unique line identifier, so a genuine repeated line cannot be told apart from a double entry. This assumption affects 3.22% of the raw rows (the largest single step).
4. **Cancellations are excluded, not netted.** Revenue is gross sales; refunds are not subtracted (see section 5).
5. **Missing descriptions need no separate rule** because every blank description is also a zero-price row removed in step 4.
6. **No outlier rule exists** in the `src/` pipeline (see section 5).

## 5. Open data issues (not handled by `src/clean_data.py`)

| # | Issue | Size | Effect |
|---|---|---|---|
| 1 | **The data-integrity target is missed.** The project requirement is to drop no more than 5% of the data; 5.57% is removed. | 59,458 rows | Needs a team decision (section 6) |
| 2 | **Cancelled orders keep their original sale.** The `C` row is dropped but the order it cancelled stays in. The two largest cases are invoice 541431 (74,215 units, £77,183.60, customer 12346, cancelled 16 minutes later) and invoice 581483 (80,995 units, £168,469.60, customer 16446, cancelled 12 minutes later). | 2 orders, £245,653.20 (1.4% of customer revenue) | Both customers are labelled "Champions"; customer 16446 has 1 genuine purchase worth £2.90. Excluding the two orders changes the segment of 10 of 5,878 customers (0.17%). |
| 3 | **Cancellations are not subtracted from revenue.** The cancelled rows are worth −£1,526,667.86 in the raw data (−£1,095,136.79 with a Customer ID). | | Revenue and Monetary are gross figures |
| 4 | **Non-product codes count as revenue** (POST, DOT, M, AMAZONFEE, C2, B and others: postage, fees, manual entries). | 4,573 rows, £832,398.83 (4.07% of revenue) | Monetary is slightly inflated for the customers who paid these |
| 5 | **One bad-debt adjustment stays in** (invoice A563185, StockCode `B`, +£11,062.06, no Customer ID). | 1 row | Counted as sales revenue (0.05%) |
| 6 | **Currency is unknown.** | | All money is in "the recorded price unit" |

## 6. The 5% target: options for the team

The rows removed are of different kinds:

| Kind of rows | Rows | % of raw |
|---|---:|---:|
| Non-sales records (cancellations, zero or negative prices, negative quantities) | 25,123 | 2.35% |
| Exact duplicates | 34,335 | 3.22% |
| **Total** | **59,458** | **5.57%** |

QA does not choose between the options; the team lead should record the decision in the integration checklist.

- **Option A – accept and document the deviation.** The non-sales records are not "lost data", and the duplicate rule is a stated assumption. The report would state that the 5% target is exceeded by 0.57 percentage points and why.
- **Option B – change the duplicate rule.** Keep exact duplicates that belong to an invoice with other distinct lines, or only remove duplicates that are adjacent. This needs evidence from the data and a new run of the whole pipeline.
- **Option C – agree a different definition** of "dropped" with the mentor (for example, count only rows that were real sales).

Any change to the cleaning rules changes every downstream number, so the README, reports and dashboard must be regenerated together.

## 7. The two pipelines

The repository has two cleaning pipelines. Their results differ, so numbers must never be mixed.

| | `src/` scripts (**used by README, reports and dashboard segments**) | PostgreSQL notebook `Online_Retail_II_Final_Complete_Fixed.ipynb` |
|---|---|---|
| Duplicates removed | 34,335 | 34,335 |
| Cancelled orders removed | 19,104 | 19,104 |
| Invalid quantity or price removed | 6,019 | 5,653 |
| Missing-description rows removed | (inside the price filter) | 361 |
| Bad-debt adjustments removed | no | 6 |
| Non-product codes removed | no | 4,572 |
| Outlier orders removed (80,995 and 74,215 units) | no | 2 |
| **Total removed** | **59,458 (5.57%)** | **64,033 (6.00%)** |
| Clean rows | 1,007,913 | 1,003,338 |
| Customers | 5,878 | 5,852 |
| Segment names | Champions, Loyal High-Value, Recent Customers, At-Risk / Hibernating | Profile-based names such as "Recent / High Frequency / High Value (C3)" |

The notebook fixes issues 2, 4 and 5 of section 5 but removes even more data (6.00%). The notebook passes its own 33 findings checks and 25 validation checks.

**Recommendation.** Pick one pipeline as the single source of truth before the final submission, update `docs/MODULE_INTEGRATION_CONTRACTS.md` with the choice, and regenerate the dashboard from it.

## 8. How to reproduce

```bash
python src/data_quality_audit.py
python src/clean_data.py
python src/verify_reported_metrics.py     # checks 14 to 28 of the cleaning section
```

Expected: `reports/cleaning_log.csv` shows 59,458 rows removed and 1,007,913 rows left.
