# Multi-Asset Quantitative Research Framework

A systematic, reproducible research framework for detecting statistically robust trading edges across multiple asset classes. Originally developed for XAU/USD (Gold), now extended to Bitcoin, Silver, Oil, and beyond.

## Program Status

| Phase | Asset | Status | Result |
|-------|-------|--------|--------|
| 1 | Gold (XAU/USD) | COMPLETE | No robust edge found |
| 2 | Bitcoin | ACTIVE | In progress |
| 3 | Silver | PENDING | — |
| 4 | Oil | PENDING | — |

## Repository Structure

```
data/
    gold/               Gold-specific datasets
    bitcoin/            Bitcoin datasets
    silver/             Silver datasets
    oil/                Oil datasets

research/
    gold/               Gold research scripts, charts, artifacts
        scripts/        Python research scripts
        charts/         Visualization PNGs
    bitcoin/            Bitcoin research
    silver/             Silver research
    oil/                Oil research

framework/              Instrument-agnostic validation engine
    validation/         Test 1 screening pipeline
    monte_carlo/        Permutation testing
    walk_forward/       Walk-forward analysis
    drift_neutralization/  Alpha vs buy-and-hold
    statistics/         Statistical helpers
    reporting/          Report generation
    validasi.py         Legacy validation entry point

reports/
    gold/               Gold research reports
    bitcoin/            Bitcoin research reports
    silver/             Silver research reports
    oil/                Oil research reports

master_chronicle/
    GOLD_MASTER_CHRONICLE.md   Gold research narrative (19 phases)
```

## Gold Research Summary (v1.0 — Complete)

**26 years daily data | 2 years H1 data | 100+ hypotheses | 440+ signals | 0 edges**

After 19 phases of systematic testing across price-derived, indicator-derived, positioning-derived, and macro-driver domains, **no statistically robust, tradeable edge was discovered** in XAU/USD using publicly available free data.

## Framework

All validation components are designed to be instrument-agnostic. The same pipeline used for gold (walk-forward, OOS, Monte Carlo, FDR, drift neutralization, monotonicity) applies directly to any asset.

## Requirements

- Python 3.14+
- pandas, numpy, scipy, matplotlib, yfinance, scikit-learn, requests

## License

MIT
