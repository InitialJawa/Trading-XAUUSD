# Framework Audit — Script Classification

**Date:** 2026-06-08
**Goal:** ≥80% framework reuse across 30 gold research scripts.

## Classification

| Category | Count | Meaning |
|----------|-------|---------|
| **A** | 0 | Reusable without modification |
| **B** | 24 (80.0%) | Reusable with parameterization |
| **C** | 6 (20.0%) | Gold-specific, must isolate |

**Total reusable (A + B): 80.0%** — Target met.

---

## Full Audit

| Script | Cat | Description | Changes Required |
|--------|-----|-------------|------------------|
| `phase1_data_audit.py` | B | Data quality audit: missing values, gaps, duplicates | Parameterize file path, instrument name, `Close` column |
| `phase2_return_dist.py` | B | Return distribution: normality tests, skew/kurtosis | Parameterize file path, instrument name, `Close` column |
| `phase3_mean_reversion.py` | B | Z-score mean reversion across windows/thresholds | Parameterize file path, `Close` column |
| `phase4_trend_persistence.py` | B | Trend streak conditional probability analysis | Parameterize file path, `Close` column, date regimes |
| `phase5_volatility.py` | B | Volatility clustering: ATR, ACF, regime stability | Parameterize file path, column names |
| `phase7_dayofweek.py` | B | Day-of-week seasonal effects | Parameterize file path, instrument name, `Close` column |
| `phase8_macro_events.py` | B | Return/vol around NFP/CPI/FOMC | Parameterize file path, column names (event calendar rules are generic) |
| `phase9_driver_analysis.py` | B | Cross-asset driver analysis | Parameterize file paths, driver list, column names |
| `phase10_scorecard.py` | B | Edge compilation from all phases | Parameterize all file paths and parameters |
| `research_011_conditional_regime.py` | B | Conditional regime: quintile/decile analysis | Parameterize file paths, driver list, column names |
| `research_012_indicator_ensemble.py` | B | 6 technical indicator models + MC significance | Parameterize file path, column names (indicator logic is generic math) |
| `research_013_signal_persistence.py` | B | Holding period analysis (1-60d) | Parameterize file path, column names |
| `research_014_cot_analysis.py` | B | COT positioning edge discovery | Parameterize COT file, price file, COT column names, group names |
| `research_015_cot_reality_check.py` | B | COT validation (8 tests, WF, OOS, MC, FDR) | Parameterize COT file, price file, group/column names |
| `research_h1_001_intraday.py` | B | Intraday session analysis (Asia/London/NY) | Parameterize tickers, file paths, instrument name |
| `research_h1_002_validation.py` | B | H1 candidate validation | Parameterize file path, instrument name, column names |
| `download_data.py` | B | Download Yahoo Finance + Stooq data | Parameterize all ticker symbols, file names |
| `download_cot.py` | B | Download CFTC COT data | Parameterize commodity filter, year range, output file |
| `find_cot_urls.py` | B | Scrape CFTC for zip URLs | Parameterize search keywords |
| `test_cot.py` | B | Test cftc_cot library | Parameterize year, commodity filter |
| `test_cot2.py` | B | Download + process COT 2009-2026 | Parameterize date range, commodity filter, output file |
| `audit_overlap_bias.py` | B | Look-ahead bias detection | Parameterize file path, column names, ATR period |
| `check_data_v2.py` | B | Check Yahoo ticker data availability | Parameterize entire ticker list |
| `compare_futures_vs_spot.py` | B | Futures vs spot proxy comparison | Parameterize tickers, date range, file paths |
| `research_016_data_check.py` | C | Check gold-specific data infrastructure | Gold futures contract code scheme, GLD-specific fields. Cannot generalize. |
| `research_016_external_drivers.py` | C | Gold external driver analysis | Gold term structure (GC=F/(GLD×10)), individual GC contract tickers, GLD ETF domain. |
| `check_histdata.py` | C | Probe histdata.com for XAUUSD H1 | Gold-specific file path in URL |
| `get_spot_gold.py` | C | Download spot gold from FRED/OANDA | Gold-specific FRED series IDs, gold ETF tickers, XAUUSD ticker |
| `investigate_outliers.py` | C | Classify extreme gold price events | Hardcoded `known_events` dict of gold-specific historical events |
| `debug_016.py` | C | Debug RESEARCH-016 signal generation | Gold-specific column names, term structure calc, file paths |

---

## Refactoring Pattern (Category B → Reusable)

Every Category B script needs the same three changes:

```python
# BEFORE (hardcoded):
data = pd.read_csv('data/XAUUSD_cleaned.csv')
close = data['Close']
print("Instrument: XAU/USD (GC=F)")

# AFTER (parameterized):
def main(data_path='data/gold/XAUUSD_cleaned.csv', close_col='Close', instrument='XAU/USD'):
    data = pd.read_csv(data_path)
    close = data[close_col]
    print(f"Instrument: {instrument}")
```

### Specific Refactoring Needs by Subgroup

**Data I/O scripts** (`download_data.py`, `download_cot.py`, `check_data_v2.py`, `compare_futures_vs_spot.py`):
- Accept ticker list as parameter (CLI args or config dict)
- Accept output file paths as parameters

**Analysis scripts** (Phases 1-5, 7-13):
- Accept input file path and column mappings as parameters
- Accept instrument label string
- Accept date range boundaries as parameters

**COT scripts** (`research_014`, `research_015`):
- Accept COT column names and group names as parameters
- Accept price file path and price column name

**H1 scripts** (`research_h1_001`, `research_h1_002`):
- Accept ticker/asset symbol, data path, column names as parameters
- Session hour boundaries are generic UTC rules

### Category C Isolation

The 6 Category C scripts remain in `research/gold/scripts/` and are not moved to `framework/`. They contain gold-specific domain knowledge that has no analog for other assets.
