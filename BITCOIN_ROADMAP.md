# Bitcoin Research Roadmap — Phase 2 of Multi-Asset Program

**Status:** ACTIVE (initialization complete)
**Asset:** BTC-USD
**Framework:** Multi-Asset Quantitative Research Framework

---

## Program Context

| Phase | Asset | Status | Result |
|-------|-------|--------|--------|
| 1 | Gold (XAU/USD) | COMPLETE | No robust edge found |
| **2** | **Bitcoin (BTC)** | **ACTIVE** | **In progress** |
| 3 | Silver (XAG/USD) | PENDING | — |
| 4 | Oil (WTI Crude) | PENDING | — |

---

## Philosophy

Bitcoin presents a fundamentally different research target than gold:

- **Gold (1999–2026):** ~27 years, stable volatility (~18%), mean-reverting tendencies, mature derivatives market
- **Bitcoin (2014–2026):** ~12 years, extreme volatility (~70%+), structural regime changes (retail → institutional), evolving market microstructure

The same validation standards apply — but Bitcoin's shorter history and distinct microstructure mean different signal categories may be relevant.

---

## BTC Research Phases

### BTC-001: Price Structure Research (FIRST)
**Objective:** Determine whether Bitcoin contains robust alpha using the same validation standards as gold research.
**Dataset:** BTC-USD from Yahoo Finance, maximum available history.
**Validation:** Walk Forward, OOS, Monte Carlo (5,000), FDR, Bonferroni, Drift Neutralization, Monotonicity.

*Replicates the gold Phase 1-10 testing protocol on Bitcoin.*

### BTC-002: Volatility & Regime Analysis
**Objective:** Test Bitcoin-specific volatility dynamics (halving cycles, weekend effects, exchange flows).
**Dataset:** BTC-USD + blockchain data (if available).
**Signals:** Volatility regimes, halving cycle phases, weekend vs weekday, exchange order book imbalance.

### BTC-003: On-Chain & Flow Analysis
**Objective:** Test whether on-chain metrics (hash rate, active addresses, exchange reserves, miner flows) predict future Bitcoin returns.
**Dataset:** Blockchain data (Glassnode, CoinMetrics, or public APIs).
**Signals:** Hash ribbons, reserve risk, SOPR, MVRV Z-score, exchange net flows.

### BTC-004: Cross-Asset Analysis
**Objective:** Test Bitcoin's relationship with macro assets (DXY, Gold, S&P 500, US10Y, M2 Money Supply).
**Dataset:** BTC-USD + macro data from gold research.
**Signals:** Correlation regime shifts, lead-lag relationships, macro regime conditioning.

### BTC-005: Microstructure Analysis
**Objective:** Test intraday patterns, exchange-specific effects, and order book dynamics.
**Dataset:** BTC-USD H1 data from Yahoo Finance.
**Signals:** Session effects (Asia/Europe/US overlap), hour-of-day, volatility term structure.

---

## Validation Standards (Per Gold Protocol)

Every candidate signal must survive all applicable tests:

| Test | Standard | Description |
|------|----------|-------------|
| T1 | p<0.05, SR>1.0, PF>1.30, N>100 | Basic statistical significance |
| T2 | 3/4 WF periods positive | Walk-forward across temporal periods |
| T3 | Test SR > 0, PF > 1.0, decay < 30% | Out-of-sample validation |
| T4 | BH FDR q < 0.05 | Multiple testing correction |
| T5 | MC p < 0.05 (5,000 permutations) | Null distribution rejection |
| T6 | Alpha > 0 vs buy-and-hold | Drift neutralization |
| T7 | Spearman p < 0.05 (quintiles) | Directional consistency |

---

## Data Sources

| Source | Data | Coverage | Cost |
|--------|------|----------|------|
| Yahoo Finance (BTC-USD) | Daily OHLCV | 2014–present | Free |
| Yahoo Finance (BTC-USD) | H1 OHLCV | 2024–present | Free |
| CoinGecko/CoinMarketCap | Additional daily data | 2013–present | Free |
| Glassnode (on-chain) | Hash rate, active addresses, reserves | 2010–present | Free tier limited |
| FRED | M2, DXY, US10Y (existing) | As available | Free |

---

## Key Risks & Considerations

1. **Shorter history:** BTC-USD data from Yahoo starts ~2014 (11 years vs 26 for gold). Less statistical power, higher risk of false positives from limited samples.
2. **Regime shifts:** Bitcoin has undergone multiple structural transformations (retail 2014–2017, ICO bubble 2017–2018, institutional 2020–2022, post-FTX 2023+). Stationarity cannot be assumed.
3. **Weekend trading:** Bitcoin trades 24/7/365. Day-of-week and session effects differ from traditional markets.
4. **Data quality:** Yahoo Finance BTC-USD may have gaps or idiosyncrasies. Data audit (BTC-001A) is critical first step.
5. **Halving cycles:** ~4-year halving schedule creates structural return patterns that may confound shorter-term signal analysis.

---

## Success Criteria

Bitcoin research is considered complete when:

1. All planned phases (BTC-001 through BTC-005) have been executed
2. Each phase applies the full validation pipeline (T1–T7)
3. Results are documented in `reports/bitcoin/`
4. Any surviving signals are documented with full methodology for replication

If no edges survive: Bitcoin, like gold, is considered highly efficient under free data.

## Asset Comparison (Pre-Trade)

| Metric | Gold (GC=F) | Bitcoin (BTC-USD) |
|--------|-------------|-------------------|
| Data start | 2000 | ~2014 |
| Daily observations | ~6,466 | ~4,000 |
| Annualized volatility | ~18% | ~60-80% |
| Weekend trading | No | Yes (24/7) |
| Sharpe ratio (sample) | 0.69 | 0.8-1.5 (period-dependent) |
| Market structure | Futures/ETF/Physical | Spot/Futures/ETF |
| Dominant driver | Real rates, DXY | Liquidity, adoption, macro |
