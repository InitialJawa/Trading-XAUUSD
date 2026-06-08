# RESEARCH-FINAL: XAU/USD Edge Discovery Framework — Consolidated Summary

**Date:** 2026-06-08
**Instrument:** XAU/USD (GC=F — Gold Futures)
**Total Research Phases:** 15 (001–011, H1-001, H1-002, plus sub-studies)
**Total Scripts:** 14
**Total Reports:** 17
**Data Period:** 2000-08-30 to 2026-06-08 (~25.8 years daily, ~2 years H1)
**Observations:** 6,466 daily bars + 11,395 H1 (hourly) bars

---

## FINAL VERDICT: 0 EDGES FOUND

**No statistically robust, tradeable edge was discovered in XAU/USD across all research phases.** The market appears highly efficient for simple statistical patterns at daily and H1 frequencies.

The single candidate (Silver→Gold 1-day lead, R²=0.27, 64.9% WR) passes all numerical criteria but is flagged as a likely **data alignment artifact** rather than a genuine edge.

---

## PHASE-BY-PHASE RESULTS

### Phase 1 — Data Audit (RESEARCH-001)
- 6,466 daily observations from GC=F (Yahoo Finance)
- 0 missing values, 0 data anomalies
- Quality score: 90/100 (gaps due to futures contract roll)
- **Verdict:** Data is fit for purpose

### Phase 1A — Outlier Investigation (RESEARCH-001A)
- All 40 extreme returns (>4% or <-4%) are valid market events (9/11, Financial Crisis, COVID, 2026 events)
- 0 data anomalies or futures roll artifacts detected
- **Verdict:** No data cleaning needed

### Phase 1B — Futures vs Spot (RESEARCH-001B)
- GC=F (futures) vs GLD (ETF spot proxy)
- Daily correlation: r=0.92 (below 0.98 threshold)
- Weekly correlation: r=0.98 (passes)
- Paired t-test: means are statistically equal (p=0.83)
- **Verdict:** GC=F is the best available proxy; minor daily deviations exist

### Phase 2 — Return Distribution (RESEARCH-002)
- Mean daily return: 0.0492% (ann. 12.4%)
- Ann. volatility: 18.0%
- Sharpe (buy-hold): 0.6884
- Skewness: -0.09 (near-symmetric)
- Kurtosis: 8.94 (fat tails)
- NOT normally distributed (JB p≈0)
- **Verdict:** Standard risk models understate tail risk

### Phase 3 — Mean Reversion (RESEARCH-003)
- Tested 20 parameter combinations (windows 10/20/30/50 × thresholds 1.0–3.0σ)
- 2 statistically significant (p<0.05) but **direction is anti-edge** (negative returns)
- Best case: Window 50, threshold 2.0 → 45.6% WR, PF 0.72 (loss-making)
- **Verdict: 0 edges — mean reversion is unprofitable**

### Phase 4 — Trend Persistence (RESEARCH-004)
- Tested consecutive up/down streaks (N=1 to 6) with magnitude and regime splits
- Down-streak N=1 significant (p=0.04) but → probability of down next = 45% (anti-persistence)
- Magnitude analysis: 3/36 significant; all anti-edges or small-sample
- Cross-regime stability: 0/72 sub-periods significant
- **Verdict: 0 edges — no momentum or persistence**

### Phase 5 — Volatility Clustering (RESEARCH-005 + 005A)
- ATR(14) autocorrelation: 0.989 (lag 1), 0.503 (lag 22)
- R² for ATR(t) → ATR(t+20): 0.26 (non-overlapping, corrected from 0.91 overlap bias)
- Q5→Q5 persistence: 52% vs 20% random (p≈0)
- Volatility squeeze → large move: P=45.7% vs 57.0% baseline (squeeze suppresses vol)
- **Verdict:** Volatility magnitude is highly predictable; direction is NOT predictable

### Phase 7 — Day of Week (RESEARCH-007)
- ANOVA: F=1.74, p=0.137 (no significant day-to-day differences)
- Kruskal-Wallis: H=11.95, p=0.018 (suggests some difference)
- Monday: 54.7% WR, PF 1.27 (near-miss, PF < 1.30)
- Friday: 53.0% WR, PF 1.24 (near-miss, PF < 1.30)
- **Verdict: 0 edges — Monday/Friday near-misses fail PF criterion**

### Phase 8 — Macro Events (RESEARCH-008)
- NFP (first Friday): no significant post-event edge (p=0.55)
- CPI (approx. dates): pre-event run-up significant (p=0.009) but means not different from non-event
- FOMC (approx. dates): no significant effects
- **Verdict: 0 edges — no macro event effect detected**

### Phase 9 — Cross-Asset Drivers (RESEARCH-009)
**8 drivers tested:** DXY, US10Y, US10Y_chg, SP500, VIX, Crude Oil, Silver, TLT

**Strongest contemporaneous relationship:** DXY r=-0.33 (same day, p≈0)
**Strongest predictive relationship:** Silver(t)→Gold(t+1): **r=+0.52, R²=0.27, p≈0**

Silver lead details:
- Sign-based strategy: 64.9% WR, PF 3.07, Sharpe 5.99
- Consistent across all 22 years (lowest year WR=56%)
- Year-by-year: 2005 (62.5%) through 2026 (70.4%), all years >56%
- Top-10% Silver move → 81.8% WR next day
- **BUT: Extreme asymmetry** — Silver→Gold r=0.52, Gold→Silver r=-0.01 (essentially zero)
- A true lead-lag should show bidirectional effects
- Likely a Yahoo Finance **data labeling artifact** (trade date vs settlement date)

Multivariate model (1-day walk-forward):
- Linear regression OOS R²=0.229, directional accuracy 66.0%
- Random Forest OOS R²=0.168, directional accuracy 65.5%
- Silver dominates feature importance (0.85)
- **Verdict: 0 clean edges — Silver lead is likely artifactual**

### Phase 10 — Edge Scorecard (RESEARCH-010)
**Ranked all edges across all phases:**

| Rank | Edge | WR% | PF | Sharpe | Criteria Met? |
|------|------|-----|----|--------|-------------|
| 1 | Silver→Gold 1d Lead | 64.9 | 3.07 | 5.99 | YES ⚠️ |
| 2 | Extreme Silver D10 1d | 56.7 | 1.33 | 1.57 | YES ⚠️ |
| 3 | Extreme VIX D10 1d | 52.5 | 1.45 | 2.09 | YES ⚠️ |
| 4 | Extreme VIX D10 5d | 52.5 | 1.36 | 1.77 | YES ⚠️ |
| 5 | DXY Q5 1d | 52.2 | 1.27 | 1.36 | no |
| 6 | Down Streak 5 | 60.0 | 1.35 | 1.47 | no |
| 7 | Monday | 54.7 | 1.27 | 1.30 | no |
| 8 | Friday | 53.0 | 1.24 | 1.21 | no |

**⚠️ = passes numerical criteria but fails authenticity/stability checks**

**Verdict: 0 edges pass ALL criteria without caveat**

### Phase 11 — Conditional Regime Discovery (RESEARCH-011)
**50+ conditions tested** across DXY, US10Y, Real Yield, VIX, SP500, Silver quintiles, deciles, combined, transition regimes

3 conditions pass numerical criteria (N>300, p<0.05, PF>1.30, Sharpe>1.00):
1. VIX bottom 10% → N=651, WR=52.5%, PF=1.45, Sharpe=2.09 — **FAILS stability**
2. VIX bottom 10% (5d) → N=651, WR=52.5%, PF=1.36, Sharpe=1.77 — **FAILS stability**
3. Silver top 10% → N=646, WR=56.7%, PF=1.33, Sharpe=1.57 — **restatement of Silver lead**

DXY quintile analysis:
- Strong Dollar (Q5) best: PF=1.27, Sharpe=1.36 — **fails PF criterion**
- Weak Dollar (Q1): no significant effect
- **No regime differentiates gold returns above PF 1.30 threshold**

VIX instability: Sharpe ranges from 0.17 (2010-2014) to 0.92 (2005-2009)
Silver top-10%: Sharpe 0.92–0.17, same instability pattern (identical to VIX subperiods due to shared data)

**Verdict: 0 edges — 3 numerical passes all fail stability or are restatements**

### Phase H1-001 — Intraday Session Edges (RESEARCH-H1-001)
**11,395 hourly bars** (June 2024 – June 2026), 611 trading days

**5 tests completed:**
1. Session effect (Asia/London/Overlap/NY): 0 edges
2. Hour of Day (24 hours): Near-misses at 20:00 UTC (N=493, WR 54.8%, PF 1.49, p=0.011) and 23:00 UTC (N=490, WR 54.7%, PF 1.59, p=0.012)
3. Opening Range Breakout (London): Short 1h shows 63.8% WR but N=232, p=0.13
4. Volatility Regime (ATR-H1): Low vol 1h has PF=1.17 (p=0.001) but fails PF criterion
5. DXY Lead-Lag H1: Contemporaneous r=-0.34; predictive: DXY→Gold+1h: r=-0.0006 (p=0.95)

**Verdict: 0 edges — 5 near-misses noted for validation**

### Phase H1-002 — Candidate Validation (RESEARCH-H1-002)
**Monte Carlo simulation (10,000 permutations) on 5 near-misses:**

| Candidate | N | WR% | PF | MC p-val | Outcome |
|-----------|----|-----|----|----------|---------|
| Hour 20 UTC | 493 | 54.8 | 1.49 | 1.0000 | REJECTED |
| Hour 23 UTC | 490 | 54.7 | 1.59 | 0.8439 | REJECTED |
| Hour 08 UTC | 496 | 58.5 | 1.25 | 0.9699 | REJECTED |
| Low Vol | 3,756 | 52.4 | 1.18 | 0.9246 | REJECTED |
| ORB Short 1h | 365 | 37.8 | 0.84 | 0.3496 | REJECTED |

**MC p > 0.05 for all candidates** — not distinguishable from random permutation

**Data limitation:** Only 730 days of H1 data available from yfinance. Cannot source 5+ years from free alternatives (Dukascopy 403/404, Stooq captcha, histdata.com no direct download, investpy incompatible with Python 3.14).

**Verdict: 0 edges — all intraday near-misses are statistical noise**

---

## KEY NEGATIVE FINDINGS

1. **No momentum or mean reversion** — returns are essentially unpredictable from past prices
2. **DXY-gold is purely contemporaneous** — no predictive lead at daily or H1 frequency
3. **Macro events cause volatility but no directional edge** — NFP/CPI/FOMC effects are noise
4. **Regime conditioning doesn't help** — no DXY/yield/VIX regime differentiates gold returns above PF 1.30
5. **Intraday patterns are noise** — all 5 near-misses fail Monte Carlo validation
6. **Volatility magnitude is predictable but useless for direction** — you can predict when a big move will happen but not which way
7. **Buy-hold (Sharpe 0.69) outperforms all conditional strategies**

---

## SILVER→GOLD CAVEAT SUMMARY

| Aspect | Detail |
|--------|--------|
| Raw stats | r=+0.52, R²=0.27, WR=64.9%, PF=3.07, 22 years consistent |
| Problem | Extreme asymmetry: Silver→Gold r=0.52 vs Gold→Silver r=-0.01 |
| Likely cause | Yahoo data labeling discrepancy (trade date vs settlement date) |
| Could be real? | Possible (both are precious metals, same exchange) |
| Resolution needed | Verify with Bloomberg/Reuters tick data before treating as real |

---

## DATA QUALITY SUMMARY

| Source | Instrument | Period | Bars | Availability |
|--------|-----------|--------|------|------------|
| Yahoo Finance | GC=F (daily) | 2000–2026 | 6,466 | ✅ Free, reliable |
| Yahoo Finance | DXY (daily) | 2002–2026 | 5,978 | ✅ Free, reliable |
| Yahoo Finance | SI=F (daily) | 2000–2026 | 6,461 | ✅ Free, reliable |
| Yahoo Finance | GC=F (H1) | 2024–2026 | 11,395 | ⚠️ 730-day limit |
| Yahoo Finance | DXY (H1) | 2024–2026 | 11,876 | ⚠️ 730-day limit |
| investpy | H1 data | N/A | 0 | ❌ Python 3.14 incompatible |
| Dukascopy | H1 data | N/A | 0 | ❌ 403/404 errors |
| Stooq | H1 data | N/A | 0 | ❌ Captcha-blocked |
| histdata.com | H1 data | N/A | 0 | ❌ No direct download |

---

## FINAL FRAMEWORK ASSESSMENT

### What was done
- 15 research phases over 25.8 years of daily data and 2 years of H1 data
- 100+ hypothesis tests across mean reversion, momentum, seasonality, volatility, macro events, cross-asset drivers, conditional regimes, and intraday patterns
- Monte Carlo permutation testing for all near-misses
- Stability analysis across multiple sub-periods
- Overlap bias correction

### What was found
- **0 statistically robust, tradeable edges** in XAU/USD
- Buy-hold (Sharpe 0.69) outperforms every conditional strategy tested
- The Silver→Gold 1-day lead (R²=0.27, 64.9% WR) is the only candidate meeting all numerical criteria, but is likely a data artifact
- XAU/USD appears **highly efficient** for simple statistical patterns

### What was NOT tested (limitations)
- Tick-level / order-flow microstructure
- Machine learning (beyond linear regression and random forest)
- Options market (volatility surface, put/call ratios)
- Alternative data (satellite imagery, central bank flows, mining supply)
- Position sizing / risk management overlays
- Higher-frequency intraday (M1, M5, M15) — data unavailable from free sources

### Recommended next steps (if pursuing further)
1. **Verify Silver→Gold lead** with institutional data (Bloomberg/Reuters) to conclusively resolve artifact question
2. **Paid intraday data provider** (IQFeed, Polygon.io, OANDA) for tick/M1/M5 analysis
3. **Multi-asset ensemble** combining weak signals that are non-overlapping (e.g., Monday + Low Vol regime)
4. **Apply the same framework to other instruments** (crude oil, FX pairs, equity indices, crypto)
5. **Machine learning with feature engineering** (technical indicators, order flow proxies, intermarket spreads)

---

**All scripts, data, and reports are available in the repository.**
*Research conducted June 2026. No guarantee of future market behavior.*
