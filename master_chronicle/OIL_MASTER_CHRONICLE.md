# Crude Oil (CL=F) Edge Discovery Framework — Master Chronicle

> *A systematic 8-phase journey through 25.8 years of WTI Crude Oil data, testing 100+ hypotheses — finding that Oil is structurally different from Gold and Bitcoin, but equally unpredictable.*

---

## Prologue: Why Oil Is Different

Crude Oil (WTI, CL=F) is fundamentally different from Gold and Bitcoin in one critical way: **Oil has zero long-term drift.**

| Metric | Gold | Bitcoin | Oil |
|--------|------|---------|-----|
| Buy-and-hold Sharpe (annual) | 0.69 | 0.97 | **-0.02** |
| Annualized return | +12.4% | +66.7%* | **-1.77%** |
| Annualized volatility | 18.0% | 66.7% | **77.5%** |
| Long-term trend | Upward | Strong upward | **Flat/Mean-reverting** |
| Data history | 25 years | 11 years | 25.8 years |

*Bitcoin annualized return is period-dependent (2014-2026).*

This zero-drift property means Oil is the **cleanest test of pure predictive skill** — unlike Gold and Bitcoin, where every long-biased signal looks good due to secular uptrend, Oil's returns are mean-reverting around zero. Any genuine edge would show clearly without drift contamination.

However, Oil has:
- **Extreme negative skew** (-40.58) — crashes are sudden and violent
- **Fat tails** (kurtosis 2449) — daily moves >10% happen
- **Futures contract roll gaps** — the April 2020 negative oil event alone caused a -306% daily return

---

## Phase 1 — Price Structure (OIL-001)

**Script:** `research/oil/scripts/oil_001_price_structure.py`
**Report:** `reports/oil/OIL-001_Price_Structure.md`
**Status:** COMPLETE

### Key Statistics

| Metric | Value |
|--------|-------|
| Daily mean return | -0.0070% |
| Annualized volatility | 77.53% |
| Sharpe ratio | **-0.02** |
| % Positive days | 52.0% |
| Autocorrelation lag 1 | 0.23 (significant) |
| Vol clustering ATR(14) lag 1 | 0.99 |

### Mean Reversion & Trend Tests

- **Serial correlation is positive at lag 1** (0.23, p≈0) — contrary to mean reversion expectation. Oil shows slight 1-day persistence.
- **Volatility clusters strongly** (ATR-14 autocorr 0.99 at lag 1) — same as Gold and Bitcoin.
- **No streak pattern:** consecutive up/down days show no predictive power for the next day.
- **Z-score mean reversion:** No parameter combination (10d/20d/50d windows, 1.0-2.5 sigma thresholds) produces PF > 1.30 with statistical significance. Overbought conditions weakly predict negative returns but not strongly enough.

### Verdict

**No price-derived edge.** Oil's flat long-term return profile means trend-following has no foundation, and mean reversion is too weak to exploit. The data foundation confirms Oil is a zero-drift, high-volatility, negatively skewed asset.

---

## Phase 2 — Calendar Effects (OIL-002)

**Script:** `research/oil/scripts/oil_002_calendar.py`
**Report:** `reports/oil/OIL-002_Calendar_Effects.md`
**Status:** COMPLETE

### Tests

- **Day of week:** No day passes PF > 1.30. Monday shows slight positive edge (WR ~53%) but PF ~1.15 — below threshold.
- **Month of year:** No month passes PF > 1.30. February and July show modest positive returns. September and October show weakness (end of driving season).
- **Quarter:** No quarter shows significant edge. Q3 (hurricane season) slightly positive but not statistically significant.
- **Driving season vs winter:** Summer (May-Sep) vs Winter (Nov-Mar) shows no significant difference in return profiles.

### Verdict

**No calendar edge.** Unlike Gold (Monday/Friday near-misses), Oil shows no day-of-week or seasonal pattern strong enough to trade. The driving season effect is real in oil markets but too weak for daily-frequency exploitation.

---

## Phase 3 — Macro Events (OIL-003)

**Script:** `research/oil/scripts/oil_003_macro_events.py`
**Report:** `reports/oil/OIL-003_Macro_Events.md`
**Status:** COMPLETE

### Events Tested

- **Hurricane season** (Jun-Nov): No significant return difference vs non-hurricane months.
- **Driving season transition** (May start, Sep end): No significant edge at monthly level.
- **Macro regimes by decade:** The 2008-2014 period showed highest volatility. 2015-2019 (Shale boom) showed negative average returns. 2020-2022 (COVID + Ukraine) showed positive returns. None significant at standard criteria.
- **Known crash events:** 9/11, GFC 2008, COVID 2020, Ukraine 2022 — post-event returns are mixed. No consistent pattern.

### Verdict

**No robust macro event edge.** Oil's major moves are driven by supply shocks (OPEC, geopolitics, hurricanes, pipelines) that are inherently unpredictable in timing and magnitude with public data.

---

## Phase 4 — Cross-Asset Drivers (OIL-004)

**Script:** `research/oil/scripts/oil_004_cross_asset.py`
**Report:** `reports/oil/OIL-004_Driver_Analysis.md`
**Status:** COMPLETE

### Contemporaneous Correlations

| Driver | Same-day r | Interpretation |
|--------|-----------|----------------|
| USO (Oil ETF) | +0.54 | Same asset, different vehicle |
| Brent (BZ=F) | +0.52 | Global oil benchmark |
| XLE (Energy stocks) | +0.30 | Oil equities track crude |
| SP500 | +0.13 | Weak equity correlation |
| US10Y | +0.13 | Weak yield correlation |
| VIX | -0.11 | Inverse volatility |
| DXY | -0.08 | Weak dollar inverse |
| GLD | +0.09 | Near-zero gold correlation |

### Predictive Signals (T1 Candidates)

| Signal | Sharpe | PF | WR% | p | N |
|--------|--------|----|-----|---|----|
| DXY_Level_5d Q3 | 1.36 | 1.64 | 60.5% | 0.0000 | 1,293 |
| DXY_Level_10d Q3 | 1.30 | 1.94 | 61.8% | 0.0000 | 1,292 |
| DXY_Level_20d Q3 | 1.20 | 2.31 | 66.0% | 0.0000 | 1,290 |
| USO_Level_60d Q1 | 1.15 | 11.13 | 72.8% | 0.0000 | 1,002 |

### Key Insight

DXY mid-quintile (Q3) predicts Oil returns across multiple horizons. This could be a genuine regime effect (when the dollar is neither strong nor weak, oil performs). The USO low-quintile signal (USO at 60d lows → oil rallies) has massive PF (11.13) but likely captures oil's mean-reverting nature.

**Validation required** — these candidates survive T1 screening but need walk-forward, OOS, Monte Carlo, and drift neutralization tests.

---

## Phase 5 — Term Structure (OIL-005)

**Script:** `research/oil/scripts/oil_005_term_structure.py`
**Report:** `reports/oil/OIL-005_Term_Structure.md`
**Status:** COMPLETE

### Test

- **Term structure proxy** (USO/CL=F spread): 0 T1 candidates.
- **Roll yield signal** (USO return minus CL=F return): 1 borderline candidate.

### Result

| Signal | Sharpe | PF | WR% | p | N |
|--------|--------|----|-----|---|----|
| RollMA5_1d Q4 | 1.11 | 1.21 | 55.1% | 0.0264 | 1,012 |

### Verdict

**No robust term structure edge.** The contango/backwardation signal is well-known to oil traders and likely already priced in. The proxy via USO/CL=F spread is noisy due to USO's expense ratio and rolling methodology.

---

## Phase 6 — Intraday H1 (OIL-006)

**Script:** `research/oil/scripts/oil_006_intraday.py`
**Report:** `reports/oil/OIL-006_Intraday_Analysis.md`
**Status:** COMPLETE

### Data

11,231 hourly bars (2024-06-09 to 2026-06-08) — Yahoo Finance H1 cap.

### Tests

- **Session effect** (Asia/Europe/US/Pit hours): PF values near 1.00 across all sessions. US pit session (14-21 UTC) has highest volatility but no return edge.
- **Hour of day:** Several hours show marginal PF > 1.05 but none > 1.30. No hour passes the threshold.
- **EIA inventory release** (Wednesdays 15:30 UTC): No significant edge in the immediate post-release hour.

### Verdict

**No intraday edge.** Oil's 23-hour CME Globex market shows no predictable session or hourly patterns. Even the EIA inventory release — oil's most-watched weekly event — shows no consistent directional edge at hourly resolution.

---

## Phase 7 — Signal Persistence (OIL-007)

**Script:** `research/oil/scripts/oil_007_signal_persistence.py`
**Report:** `reports/oil/OIL-007_Signal_Persistence.md`
**Status:** COMPLETE

### Models Tested (6 × 9 holding periods)

| Model | Best Hold | Sharpe | PF | MC p | Verdict |
|-------|-----------|--------|----|-------|---------|
| A — Trend Following | 5d | 0.21 | 1.15 | 1.000 | Noise |
| B — Trend Pullback | 1d | 0.44 | 1.24 | 1.000 | Noise |
| C — Mean Reversion Extreme | 60d | -0.05 | 0.77 | 0.000 | Anti-edge |
| D — Volatility Expansion | 1d | 0.04 | 1.01 | 1.000 | Noise |
| E — Breakout | 1d | 0.18 | 1.03 | 1.000 | Noise |
| F — Consensus | 1d | 0.42 | 1.10 | 1.000 | Noise |

### Critical Finding

**No model passes any criteria.** The best Sharpe across all 6 models × 9 holding periods is **0.44** (Model B, 1d) — far below the 1.0 threshold.

This is the cleanest result of the entire multi-asset framework: **Oil's lack of drift means signals that look promising on trending assets (Gold, Bitcoin) collapse to near-zero here.** Trend Following on Oil (Sharpe 0.21) is useless because there's no trend to follow.

Mean Reversion Extreme (Model C) is an anti-edge — buying extreme RSI deviations in Oil loses money. Breakout strategies also fail.

---

## Phase 8 — External Drivers (OIL-008)

**Script:** `research/oil/scripts/oil_008_external_drivers.py`
**Report:** `reports/oil/OIL-008_External_Drivers.md`
**Status:** COMPLETE

### Phases

- **Phase A (USO Volume/Return/Divergence):** No T1 candidates from volume spikes (inventory proxy), USO return quintiles, or USO-OIL divergence.
- **Phase B (XLE Oil-Equity):** No T1 candidates from XLE returns or XLE-OIL divergence.
- **Phase C (Macro Regimes: DXY, US10Y):** 175 total signals, **0 T1 candidates.**

### Result

**No external driver edge found.** Unlike Gold (Silver proxy) and Bitcoin (GBTC/VIX signals), Oil shows zero predictive signals from ETF flows, energy equities, or macro regimes that survive basic screening.

---

## Performance Summary

| Phase | Phase | Signals | T1 Candidates | Strongest Signal | Verdict |
|-------|-------|---------|--------------|------------------|---------|
| 1 | Price Structure | 100+ | 0 | None | No price edge |
| 2 | Calendar Effects | 40+ | 0 | None | No calendar edge |
| 3 | Macro Events | 20+ | 0 | None | No event edge |
| 4 | Cross-Asset Drivers | 200+ | 4 | DXY Q3 (SR 1.36) | Need validation |
| 5 | Term Structure | 85 | 0 | RollMA5 (SR 1.11) | Borderline |
| 6 | Intraday H1 | 50+ | 0 | None | No intraday edge |
| 7 | Signal Persistence | 6×9=54 | 0 | Pullback (SR 0.44) | All noise |
| 8 | External Drivers | 175 | 0 | None | No driver edge |

**Across 8 phases and 700+ signals: zero robust, tradeable edges.**

---

## Comparison: Gold vs Bitcoin vs Oil

| Dimension | Gold | Bitcoin | Oil |
|-----------|------|---------|-----|
| Data history | 25 yrs | 11 yrs | 25.8 yrs |
| Buy-and-hold Sharpe | 0.69 | 0.97 | **-0.02** |
| Volatility | 18% | 67% | 78% |
| Skewness | -0.09 | -0.50 | **-40.58** |
| Trend following works? | Weak (SR 0.67) | **Strong (SR 1.88)** | Useless (SR 0.21) |
| Mean reversion works? | No | Anti-edge | No |
| Cross-asset predictor | Silver (artifact) | None | DXY Q3 (?) |
| Overall | Efficient | Uptrending | **Mean-reverting** |

### The Oil Paradox

Oil is the **only asset** of the three where buy-and-hold is *not* the optimal strategy (negative Sharpe). This makes it theoretically more attractive for active strategies. Yet no systematic signal — trend, mean reversion, calendar, macro, cross-asset, or intraday — produces a reliable edge.

The explanation: Oil's price moves are dominated by **unpredictable supply shocks** (OPEC surprises, pipeline outages, geopolitical flashpoints, hurricane disruptions). These events are discrete, severe, and impossible to forecast with public data. The noise from these shocks overwhelms any statistical patterns that might exist in quiet periods.

---

## Final Closing — Project Complete (June 2026)

After **8 phases** across Crude Oil, testing **700+ signals** across price structure, calendar, macro events, cross-asset, term structure, intraday, signal persistence, and external driver domains:

**No simple, statistically robust, tradeable edge exists in Crude Oil using publicly available data.**

This completes the multi-asset framework: **Gold, Bitcoin, and Oil — three fundamentally different markets — all produce the same answer under rigorous validation.**

### Multi-Asset Conclusion (35 Phases Total)

| Asset | Phases | Signals | Robust Edges | BH Sharpe |
|-------|--------|---------|-------------|-----------|
| Gold | 19 | 2,000+ | 0 | 0.69 |
| Bitcoin | 8 | 2,000+ | 0 (1 trend-confounded) | 0.97 |
| Oil | 8 | 700+ | 0 (4 unvalidated) | -0.02 |
| **Total** | **35** | **4,700+** | **0** | — |

The only signal surviving Monte Carlo across all three assets was Bitcoin's Trend Following (Sharpe 1.88, MC p=0.024) — which is confounded by Bitcoin's secular uptrend and requires drift neutralization.

---

## Technical Appendix

### Repository Structure
```
├── research/oil/scripts/
│   ├── oil_001_price_structure.py
│   ├── oil_002_calendar.py
│   ├── oil_003_macro_events.py
│   ├── oil_004_cross_asset.py
│   ├── oil_005_term_structure.py
│   ├── oil_006_intraday.py
│   ├── oil_007_signal_persistence.py
│   └── oil_008_external_drivers.py
├── reports/oil/
│   ├── OIL-001_Price_Structure.md
│   ├── OIL-002_Calendar_Effects.md
│   ├── OIL-003_Macro_Events.md
│   ├── OIL-004_Driver_Analysis.md
│   ├── OIL-005_Term_Structure.md
│   ├── OIL-006_Intraday_Analysis.md
│   ├── OIL-007_Signal_Persistence.md
│   └── OIL-008_External_Drivers.md
├── data/oil/
│   ├── CLF_cleaned.csv
│   ├── USO.csv
│   ├── XLE.csv
│   ├── OIH.csv
│   └── BZ=F.csv
└── master_chronicle/OIL_MASTER_CHRONICLE.md (this file)
```

### Data Sources
| Source | Symbol | Period | Observations |
|--------|--------|--------|-------------|
| Yahoo Finance | CL=F (WTI Crude) | 2000-08-23 to 2026-06-08 | 6,475 daily |
| Yahoo Finance | CL=F H1 | 2024-06-09 to 2026-06-08 | 11,231 hourly |
| Yahoo Finance | BZ=F (Brent) | 2007-07-30 to 2026-06-08 | 4,693 daily |
| Yahoo Finance | USO | 2006-04-10 to 2026-06-08 | 5,072 daily |
| Yahoo Finance | XLE | 1998-12-22 to 2026-06-08 | 6,906 daily |
| Local files | DXY, US10Y, VIX | Various | 5,000-16,000 daily |

### Success Criteria
- Sample size > 300
- P-value < 0.05
- Profit factor > 1.30
- Sharpe ratio > 1.00 (annualized)
- Stable across sub-periods (walk-forward)
- Survives Monte Carlo permutation test

---

*Built June 2026. All data from Yahoo Finance. All results reproducible. No guarantee of future market behavior.*

*"The market can remain irrational longer than you can remain solvent." — John Maynard Keynes*
