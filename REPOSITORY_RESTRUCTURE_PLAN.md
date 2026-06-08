# Repository Restructure Plan

**Objective:** Convert XAU/USD-specific repository into a reusable multi-asset quantitative research framework.

**Status:** Phase 1 (Gold Freeze) + Phase 2 (Architecture) complete.

---

## Current Structure (Post-Migration)

```
repository/
├── data/
│   ├── gold/                  # Gold-specific datasets
│   │   ├── XAUUSD_yahoo_raw.csv
│   │   ├── XAUUSD_cleaned.csv
│   │   ├── XAUUSD_H1.csv
│   │   ├── gold_cot.csv
│   │   └── gcf.csv
│   ├── bitcoin/               # (empty — ready for BTC data)
│   ├── silver/                # (empty — ready for SI data)
│   ├── oil/                   # (empty — ready for CL data)
│   ├── DXY_H1.csv             # Cross-asset (Dollar Index H1)
│   ├── related_instruments.csv
│   ├── drivers_additional.csv
│   ├── edge_scorecard.csv
│   ├── gld.csv
│   ├── ief.csv
│   ├── irx.csv
│   ├── tip.csv
│   ├── tnx.csv
│   └── tyx.csv
│
├── research/
│   ├── gold/
│   │   ├── scripts/           # 30 gold research scripts
│   │   └── charts/            # 15 visualization PNGs
│   ├── bitcoin/               # (empty — BTC-001.md init)
│   ├── silver/                # (empty)
│   └── oil/                   # (empty)
│
├── framework/
│   ├── __init__.py
│   ├── validasi.py            # Legacy validation entry point
│   ├── validation/
│   │   └── __init__.py
│   ├── monte_carlo/
│   │   └── __init__.py
│   ├── walk_forward/
│   │   └── __init__.py
│   ├── drift_neutralization/
│   │   └── __init__.py
│   ├── statistics/
│   │   └── __init__.py
│   └── reporting/
│       └── __init__.py
│
├── reports/
│   ├── gold/                  # 27 gold research reports
│   ├── bitcoin/               # (empty)
│   ├── silver/                # (empty)
│   └── oil/                   # (empty)
│
├── master_chronicle/
│   └── GOLD_MASTER_CHRONICLE.md
│
├── FRAMEWORK_AUDIT.md
├── REPOSITORY_RESTRUCTURE_PLAN.md
├── BITCOIN_ROADMAP.md
├── .gitignore
└── README.md
```

---

## Phase 1 — Gold Freeze ✅ DONE

All gold research artifacts moved to isolated directories:

| Original Location | New Location |
|-------------------|--------------|
| `scripts/*.py` | `research/gold/scripts/` |
| `reports/*.md` | `reports/gold/` |
| `charts/*.png` | `research/gold/charts/` |
| `data/XAUUSD_*.csv`, `data/gold_cot.csv`, `data/gcf.csv` | `data/gold/` |
| `MASTER_CHRONICLE.md` | `master_chronicle/GOLD_MASTER_CHRONICLE.md` |
| `validasi.py` | `framework/validasi.py` |

**No content modified. No historical results changed. All artifacts preserved.**

---

## Phase 2 — Multi-Asset Architecture ✅ DONE

Created instrument-agnostic directory tree:

```
data/{gold,bitcoin,silver,oil}/
research/{gold,bitcoin,silver,oil}/
framework/{validation,monte_carlo,walk_forward,drift_neutralization,statistics,reporting}/
reports/{gold,bitcoin,silver,oil}/
```

Framework module stubs created with `__init__.py` files.

---

## Phase 3 — Framework Extraction (NEXT)

### 3a. Extract Framework Core

The following components currently embedded in gold scripts should be extracted into `framework/` modules:

| Framework Module | Source Script | Key Functions to Extract |
|-----------------|---------------|--------------------------|
| `framework/statistics/` | `research/gold/scripts/phase2_return_dist.py` | `compute_summary_stats()`, `normality_tests()` |
| `framework/statistics/` | `research/gold/scripts/phase3_mean_reversion.py` | `zscore_test()`, `mean_reversion_stats()` |
| `framework/validation/` | `research/gold/scripts/research_015_cot_reality_check.py` | `t1_screening()`, `walk_forward()`, `oos_test()` |
| `framework/monte_carlo/` | `research/gold/scripts/research_015_cot_reality_check.py` | `monte_carlo_permutation()` |
| `framework/monte_carlo/` | `research/gold/scripts/research_012_indicator_ensemble.py` | `monte_carlo_sharpe()` |
| `framework/drift_neutralization/` | `research/gold/scripts/research_015_cot_reality_check.py` | `drift_neutralize()`, `alpha_vs_bh()` |
| `framework/walk_forward/` | `research/gold/scripts/research_015_cot_reality_check.py` | `walk_forward_periods()`, `period_return()` |
| `framework/reporting/` | `research/gold/scripts/phase10_scorecard.py` | `generate_report()`, `scorecard_table()` |

### 3b. Refactor Category B Scripts

Apply the standard parameterization pattern to 24 Category B scripts:

```
Category B Refactoring Template:
  1. Add CLI args: --data-path, --close-col, --instrument-name
  2. Wrap logic in main() function
  3. Move reusable utilities to framework/
```

### 3c. Cross-Asset Data

Move shared macro data to `data/` root or create `data/shared/`:

- `data/related_instruments.csv` — cross-asset price data
- `data/drivers_additional.csv` — macro driver data
- `data/tnx.csv` — 10Y yield
- `data/tip.csv` — TIPS ETF
- `data/ief.csv` — Treasury ETF
- `data/tyx.csv` — 30Y yield
- `data/irx.csv` — 13wk T-Bill

---

## Phase 4 — Future Asset Onboarding

### Onboarding Checklist

To add a new asset (e.g., Bitcoin):

1. Create `data/{asset}/` directory
2. Create `research/{asset}/` directory
3. Create `reports/{asset}/` directory
4. Download source data → `data/{asset}/`
5. Parameterize a Category B script: `python research/gold/scripts/phase2_return_dist.py --data-path data/{asset}/prices.csv --instrument {asset}`
6. Or use framework modules directly: `from framework.statistics import compute_summary_stats`

### Framework Invocation Pattern (Future)

```python
from framework.validation import t1_screening, walk_forward, oos_test
from framework.monte_carlo import monte_carlo_permutation
from framework.drift_neutralization import alpha_vs_bh

results = t1_screening(returns, signal_col='Signal', ret_col='Ret_1d')
wf = walk_forward(returns, mask, periods=PERIODS)
mc = monte_carlo_permutation(actual_returns, population_returns, n=5000)
drift = alpha_vs_bh(signal_returns, bh_returns)
```
