# Stage 03 — Profile summary

## Overview
45,000 rows × 41 columns, 2024-04-01 → 2025-03-31, 63 MB. Weekly target (Sale rows, qty>0, store & article known): 7,067 series-weeks over 145 series × 53 weeks; mean 12.1 units, median 10, max 77; 8% of the full grid has no sales.

## Issues, ranked by impact on the forecast
| # | Issue | Size | Proposed fix |
|---|---|---|---|
| 1 | **Last week (2025-03-31) is one day** — 294 units vs median 1,626/week. Also inflates stage-01 baselines | 1 week | Drop it; test = Jan 6 – Mar 24 2025 (12 weeks) |
| 2 | Returns with conflicting sign: 9,878 of 11,460 Returns have positive NET; 2,312 Sales have negative NET | 27% of rows | Trust BILL_TYPE only; demand = Sale rows; do not use amounts |
| 3 | Sale rows with quantity 0 | 2,773 | Drop |
| 4 | ARTICLE missing | 3,588 (8%) | Drop from article-level model (cannot be recovered; DIVISION is also missing 5,293 but is derivable from ARTICLE, 1:1) |
| 5 | SITE has junk codes (TBD, UNKNOWN, STORE_X, LOC99, BRANCH-01, missing) | 7,277 (16%) | Use SITE_NAME (complete, 5 clean values) |
| 6 | SALES_CHANNEL inconsistent labels (ECOM/Online Grocery/online, In-Store/offline, 'Null', 'Walk-In', B2B) | 8 values | Map to In-Store / Online / B2B / Unknown if used as a feature |
| 7 | Duplicate BILL_NO + ARTICLE pairs | 2,288 | Keep: repeat lines can be legitimate; quantify impact in stage 05 |
| 8 | TAXABLEAMT contains text 'ERR' | 727 | Not used for the target; drop the column |
| 9 | Amount mismatch: NET ≠ RATE_TOTAL+TAX (>1) | 3,267 of 30,767 Sales | Not used |
| 10 | Constant columns (IGST*, RETURN_AMOUNT) | 3 | Drop |

## Leakage and label hints
- `_quality_tier` (HIGH 22,500 / MEDIUM 13,500 / LOW 9,000) and `_generated_at` are generator metadata: **never features**. Useful only to explain issues: LOW rows have 51% junk SITE codes and 40% missing ARTICLE; HIGH rows have neither.
- `BILL_QUANTITY` on Sale rows is the target itself; RATE_TOTAL, NET_AMOUNT, TAX* are derived from it → leak if used same-week.
- EXPIRY_DATE and SHELF_LIFE_DAYS are per article; usable as static features (SHELF_LIFE_DAYS has 10 values).

## Drift and shape
- Total weekly units are flat (~1,600) across the year: no trend, no seasonality visible; monthly mean RATE 67–69.5. Store totals are within 6% (16.5k–17.5k units). Real seasonality is unlikely to be learnable; this is synthetic.
- Rate varies little within an article (median CV 5.8%), so price elasticity is not a viable objective.

## Questions for you
1. Dropping rows with missing ARTICLE (8%) understates demand and hits LOW-tier rows hardest. OK?
2. Use SITE_NAME as the store, ignoring SITE?
3. Should `_quality_tier` be excluded from modelling (recommended)?

Files: reports/tables/data_dictionary.csv, reports/03_profile.html, figures/03_target.png, figures/03_missing.png.
