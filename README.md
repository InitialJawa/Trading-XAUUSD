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

trading_bot/                        Live trading bot pipeline
    collectors/         Fetch XAUUSD prices & calculate indicators
    signals/            RSI, MACD, MA crossover, Momentum signals
    trading/            MT5 connector, order executor, risk manager
    backtesting/        Archive snapshots & performance metrics
    dashboard/          HTML dashboard
    config/             Settings & signal weights
    utils/              Config loader & logger
    run_pipeline.py     Pipeline orchestrator

automation/
    run_bot.sh          Shell script for cron/systemd
```

## Gold Research Summary (v1.0 — Complete)

**26 years daily data | 2 years H1 data | 100+ hypotheses | 440+ signals | 0 edges**

After 19 phases of systematic testing across price-derived, indicator-derived, positioning-derived, and macro-driver domains, **no statistically robust, tradeable edge was discovered** in XAU/USD using publicly available free data.

## Framework

All validation components are designed to be instrument-agnostic. The same pipeline used for gold (walk-forward, OOS, Monte Carlo, FDR, drift neutralization, monotonicity) applies directly to any asset.

## Trading Bot (Live)

Pipeline otomatis untuk trading XAUUSD via MetaTrader 5:

```
python -m trading_bot.run_pipeline              # data + signals + dashboard
python -m trading_bot.run_pipeline --trade       # + eksekusi order
python -m trading_bot.run_pipeline --daemon      # loop setiap jam
```

### Konfigurasi

Edit `trading_bot/config/settings.json`:
- `mt5.login`, `mt5.password`, `mt5.server` — kredensial MT5
- `risk.max_risk_per_trade` — risiko per trade (%)

### Automation (cron)

```bash
crontab -e
# setiap jam
0 * * * * /path/to/automation/run_bot.sh --trade
```

## Requirements

- Python 3.10+
- pandas, numpy, scipy, matplotlib, yfinance, scikit-learn, requests
- MetaTrader5 (untuk live trading)

## License

MIT
