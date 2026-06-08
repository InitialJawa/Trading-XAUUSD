# XAU/USD Edge Discovery Framework — Master Chronicle

> *A systematic 15-phase journey through 25.8 years of gold price data, testing 100+ hypotheses, searching for a statistically robust trading edge — and finding none.*

---

## Prologue: Why This Research Exists

Gold (XAU/USD) is the world's oldest stores of value. It trades 24 hours a day across global markets, with deep liquidity and massive institutional participation. The question: *can a retail trader, using free data and simple statistical methods, find any predictable pattern that others have missed?*

Most trading systems fail. Most "edges" are data-mined illusions. This research was built from the ground up to avoid those traps — with pre-registered success criteria, out-of-sample validation, Monte Carlo permutation testing, and honest failure reporting.

---

## Phase 1 — Data Foundation (RESEARCH-001, 001A, 001B)

**Scripts:** `phase1_data_audit.py`, `investigate_outliers.py`, `compare_futures_vs_spot.py`

Before any analysis, the data itself had to be trustworthy.

We downloaded GC=F (Gold Futures) from Yahoo Finance — 6,466 daily observations from August 30, 2000 to June 8, 2026. The data was 99.47% complete with zero missing values in any column (Open, High, Low, Close, Volume). Quality score: 90/100, with the only deduction being expected gaps from futures contract rolls (holidays, weekends).

**The outlier investigation** examined every extreme return. All 40 events (>4% or <-4%) had known market causes: 9/11 aftermath, the 2008 Financial Crisis, the 2013 Gold Crash, COVID-19, and the 2026 volatility events. Zero data anomalies. Zero futures roll artifacts. The data was clean.

**Futures vs Spot** addressed a critical question: does GC=F (futures) accurately represent the gold spot market? The daily correlation with GLD (ETF proxy) was r=0.92, below the 0.98 threshold. But weekly correlation hit r=0.98, and paired t-tests showed statistically equal means. The conclusion: GC=F is the best available proxy. Minor daily deviations exist but don't invalidate the research.

---

## Phase 2 — Return Distribution (RESEARCH-002)

**Script:** `phase2_return_dist.py`

Gold's daily returns tell a story: mean +0.049% (annualized +12.4%), volatility 18.03%, Sharpe 0.6884. The distribution has fat tails (kurtosis 8.94) and slight negative skew (-0.09). It is definitively NOT normal (Jarque-Bera p≈0).

This matters because many trading models assume normality. Gold's fat tails mean extreme moves happen more often than standard models predict — a fact that would haunt every subsequent phase.

---

## Phase 3 — Mean Reversion (RESEARCH-003)

**Script:** `phase3_mean_reversion.py`

Theory: If gold deviates too far from its moving average, it should revert back.

We tested 20 parameter combinations — windows of 10, 20, 30, 50 days with z-score thresholds from 1.0 to 3.0 sigma. The result was unambiguous: **mean reversion doesn't work on gold.**

Two combinations were statistically significant (p<0.05), but both were *anti-edges* with negative average returns. The best case (Window 50, threshold 2.0) had a 45.6% win rate and profit factor of 0.72 — a reliable way to lose money. The 50-day/1.0-sigma combo had 3,455 events and a binomial p=0.013, but again negative returns.

A key insight emerged: what looks like mean reversion is actually trend continuation. Gold that has moved far doesn't snap back — it keeps going.

---

## Phase 4 — Trend Persistence (RESEARCH-004)

**Script:** `phase4_trend_persistence.py`

Maybe gold *trends* rather than reverts. We tested consecutive up/down streaks from N=1 to N=6, with magnitude splits (small/medium/large) and four macro regimes.

The full-period analysis showed nothing. Down streaks of length 1 had a weak anti-persistence signal (p=0.04) — after one down day, the probability of another down day drops to 45%. But the effect is tiny and economically meaningless.

Magnitude analysis found 3 significant results out of 36 combinations, all anti-edges or small-sample artifacts. Cross-regime stability tested 72 sub-period combinations: **zero significant.** The pattern held across bull/bear markets: no momentum exists in gold.

---

## Phase 5 — Volatility Clustering (RESEARCH-005, 005A)

**Scripts:** `phase5_volatility.py`, `audit_overlap_bias.py`

This phase produced gold's one genuine statistical truth: **volatility clusters strongly.**

ATR(14) autocorrelation at lag 1 is 0.989. At lag 22 (one trading month), it's still 0.503. If volatility is high today, there's a 93% chance it stays high tomorrow. If gold is in the top quintile of volatility, it has a 52% chance of staying there 20 days later (vs 20% random).

The overlap bias audit was critical. The initial R² of 0.91 for predicting future volatility was largely an artifact of overlapping windows. After correction to non-overlapping 20-day forward predictions, the true R² was 0.26 — still significant, but dramatically smaller.

**The crucial limitation: volatility magnitude is predictable, but direction is not.** You can know a big move is coming, but not which way.

---

## Phase 6 — (Skipped: No Intraday Data)

Phase 6 was intended for session-effect analysis. At this point we only had daily data, so it was deferred to later H1 research.

---

## Phase 7 — Day of Week (RESEARCH-007)

**Script:** `phase7_dayofweek.py`

A classic seasonal pattern: do certain weekdays favor gold?

ANOVA said no (F=1.74, p=0.137). Kruskal-Wallis hinted at some difference (H=11.95, p=0.018). Individual t-tests showed Monday (p=0.004) and Friday (p=0.006) having positive mean returns. Monday's win rate was 54.7% with PF 1.27; Friday's was 53.0% with PF 1.24.

Both failed the PF > 1.30 criterion. Tuesday was the worst day (mean return near zero, 49.6% WR). But even Monday and Friday, while statistically significant vs zero, lack the edge magnitude for a viable trading strategy.

---

## Phase 8 — Macro Events (RESEARCH-008)

**Script:** `phase8_macro_events.py`

Does gold react predictably to NFP, CPI, and FOMC announcements?

We tested using approximate event dates (NFP: first Friday of each month; CPI/FOMC: scheduled dates). NFP showed no significant post-event edge (p=0.55). CPI had a pre-event run-up that differed from post-event (p=0.009), but neither was different from non-event returns. FOMC showed nothing.

The macro event analysis was limited by approximate dates — precise economic calendar data would improve accuracy. But the signal, if it exists, is too weak to detect with free data.

---

## Phase 9 — Cross-Asset Drivers (RESEARCH-009)

**Script:** `phase9_driver_analysis.py`

The most ambitious phase: test whether 8 related instruments (DXY, US10Y, SP500, VIX, Crude Oil, Silver, TLT) can predict gold's direction.

**Contemporaneous relationships:**
- DXY: r=-0.33 (strongest same-day relationship — weaker dollar, stronger gold)
- Silver: r=+0.23 (precious metals move together)
- Everything else: negligible (|r| < 0.08)

**Predictive relationships (Driver[t] → Gold[t+1]):**
- **Silver: r=+0.52, R²=0.27, p≈0** — the single strongest predictive relationship in the entire framework
- US10Y change: r=-0.16 (rising yields → falling gold)
- Everything else: r < 0.08

The Silver lead was remarkable: a sign-based strategy (buy gold when silver closes up, short when silver closes down) achieved 64.9% win rate, profit factor 3.07, Sharpe 5.99, consistent across all 22 years tested. The lowest annual win rate was 56% (2010). The highest was 74.8% (2013). Every single year exceeded 56%.

**But then the asymmetry test.** If Silver→Gold is real, then Gold→Silver should show at least *some* predictive power. It didn't. Gold→Silver+1d had r=-0.01, p=0.60 — essentially zero. This extreme asymmetry is the hallmark of a data alignment artifact, not a genuine lead-lag relationship.

The multivariate model confirmed Silver's dominance: random forest feature importance for Silver was 0.85 (next closest: US10Y at 0.05). The model achieved 66% directional accuracy out-of-sample — but with 85% of that coming from a single potentially artifactual feature.

---

## Phase 10 — Edge Scorecard (RESEARCH-010)

**Script:** `phase10_scorecard.py`

Every edge discovered across all phases was ranked by performance metrics:

| Rank | Edge | WR% | PF | Sharpe | Passes? |
|------|------|-----|----|--------|---------|
| 1 | Silver→Gold 1d Lead | 64.9 | 3.07 | 5.99 | ⚠️ (artifact) |
| 2 | Extreme Silver D10 1d | 56.7 | 1.33 | 1.57 | ⚠️ (restatement) |
| 3 | Extreme VIX D10 1d | 52.5 | 1.45 | 2.09 | ⚠️ (unstable) |
| 4 | Extreme VIX D10 5d | 52.5 | 1.36 | 1.77 | ⚠️ (unstable) |
| 5 | DXY Q5 1d (Strong Dollar) | 52.2 | 1.27 | 1.36 | no |
| 6 | Down Streak 5 | 60.0 | 1.35 | 1.47 | no |
| 7 | Monday | 54.7 | 1.27 | 1.30 | no |
| 8 | Friday | 53.0 | 1.24 | 1.21 | no |

**11 edges found significant. Zero passed all criteria.**

---

## Phase 11 — Conditional Regime Discovery (RESEARCH-011)

**Script:** `research_011_conditional_regime.py`

The final daily-data phase asked: does conditioning on market regimes reveal edges hidden in the unconditional data?

**50+ conditions tested:** DXY quintiles, US10Y quintiles, Real Yield quintiles, VIX quintiles, SP500 quintiles, Silver quintiles, Gold volatility regimes, combined conditions (e.g., Weak DXY + High VIX), extreme deciles (top/bottom 10%), and regime transitions.

Three conditions passed numerical criteria:
1. VIX bottom 10% → Gold 1d: WR 52.5%, PF 1.45, Sharpe 2.09, N=651, p=0.001
2. VIX bottom 10% → Gold 5d: WR 52.5%, PF 1.36, Sharpe 1.77, N=651, p=0.005
3. Silver top 10% → Gold 1d: WR 56.7%, PF 1.33, Sharpe 1.57, N=646, p=0.012

**All failed stability testing.** The VIX conditions had Sharpe ratios ranging from 0.17 (2010-2014) to 0.92 (2005-2009) across sub-periods — wildly inconsistent. The Silver condition was just a restatement of the Phase 9 Silver lead.

The most insightful finding was also the most discouraging: *even the best regime conditions barely outperform buy-and-hold* (Sharpe 0.69). After 50+ conditions, nothing beat simply owning gold.

---

## Phase H1-001 — Intraday Session Edges (RESEARCH-H1-001)

**Script:** `research_h1_001_intraday.py`

With 11,395 hourly bars from June 2024 to June 2026 (611 trading days), we tested whether intraday patterns exist in gold.

**Five tests:**
1. **Session Effect** (Asia/London/Overlap/NY): Asia had p=0.03 but PF 1.11 — below threshold. No session outperforms.
2. **Hour of Day** (24 hours): Best hours were 20:00 UTC (WR 54.8%, PF 1.49, p=0.011, N=493) and 23:00 UTC (WR 54.7%, PF 1.59, p=0.012, N=490). Both failed the N>500 criterion by 7-10 observations.
3. **Opening Range Breakout** (London Open): Short-side breakouts at 1h showed 63.8% WR but N=232, p=0.13 — statistically insignificant.
4. **Volatility Regime** (ATR-H1): Low volatility showed positive returns (p=0.001) but PF 1.17 — below the 1.30 threshold.
5. **DXY Lead-Lag** (H1 frequency): Same-hour correlation r=-0.34 (p≈0). Predictive: DXY→Gold+1h r=-0.0006 (p=0.95). **No predictive power at all.**

---

## Phase H1-002 — Candidate Validation (RESEARCH-H1-002)

**Script:** `research_h1_002_validation.py`

The five near-misses from H1-001 were subjected to rigorous Monte Carlo permutation testing (10,000 iterations each):

| Candidate | N | WR% | PF | MC p-value | Result |
|-----------|----|-----|----|-----------|--------|
| Hour 20 UTC | 493 | 54.8 | 1.49 | 1.0000 | Noise |
| Hour 23 UTC | 490 | 54.7 | 1.59 | 0.8439 | Noise |
| Hour 08 UTC | 496 | 58.5 | 1.25 | 0.9699 | Noise |
| Low Vol Regime | 3,756 | 52.4 | 1.18 | 0.9246 | Noise |
| ORB Short 1h | 365 | 37.8 | 0.84 | 0.3496 | Noise |

Every single candidate had MC p > 0.05. The observed patterns were indistinguishable from random shuffles of the data. The hourly "edges" were statistical noise amplified by a small sample.

The data limitation was insurmountable: Yahoo Finance restricts H1 data to 730 days. Attempts to source 5+ years from alternatives (Dukascopy, Stooq, histdata.com, investpy) all failed. Without longer history, the intraday question remains technically unanswered but practically settled: if an edge existed, it would show some signal beyond random permutation.

---

## The Silver Question: Artifact or Edge?

The Silver→Gold 1-day lead deserves a dedicated discussion because it's the closest this framework came to finding a real edge.

**The case for it being real:**
- r=+0.52, R²=0.27 — highest predictive power across all 11 phases
- Consistent for 22 consecutive years (2005-2026)
- Every year >56% win rate (even in 2010 at 56%, even in 2023 at 57.2%)
- Peak years: 2013 at 74.8%, 2016 at 72.8%, 2020 at 70.8%
- Both linear and nonlinear models (Random Forest) confirm Silver as dominant feature
- Both metals trade on CME, settled minutes apart — the relationship could be genuine

**The case against:**
- Extreme asymmetry: Silver→Gold r=0.52, Gold→Silver r=-0.01 (p=0.60)
- A true lead-lag should show bidirectional effects, even if weaker
- Asymmetry is consistent with Yahoo labeling Silver one day ahead (trade date vs settlement date)
- The 5-minute settlement gap (SI=F at 1:25 PM ET, GC=F at 1:30 PM ET) would predict Gold→Silver, the opposite direction
- Without alternative data source verification, the artifact hypothesis cannot be ruled out

**Verdict: Interesting but inconclusive. Not tradeable without independent verification.**

---

## Epilogue: What We Learned

After 15 phases, 14 scripts, 17 reports, 100+ hypotheses, and 87,000 lines of output, the answer is clear: **XAU/USD contains no simple statistical edges.**

The implications are worth stating:

1. **Gold is efficient.** This is not a failure of methodology — it's a finding. A market with decades of institutional participation, 24-hour trading, and massive liquidity should be hard to beat with simple patterns. It is.

2. **Buy-and-hold wins.** The unconditional buy-and-hold Sharpe of 0.69 outperformed every conditional strategy tested. After 50+ regime conditions, zero beat simple ownership.

3. **Volatility is predictable, direction is not.** The strongest statistical signal in gold is that volatility clusters. But knowing a big move is coming without knowing its direction is useless for directional trading.

4. **Most "edges" are noise.** The intraday near-misses (Hour 20, 23 UTC) looked promising until Monte Carlo testing revealed they were indistinguishable from random permutations. This is why rigorous validation matters.

5. **Data artifacts masquerade as edges.** The Silver→Gold relationship — the strongest signal in the entire framework — is likely a Yahoo Finance labeling issue. Without cross-referencing with institutional data, we cannot be sure.

6. **Free data has limits.** The 730-day cap on Yahoo Finance H1 data made robust intraday analysis impossible. For serious intraday research, paid data is unavoidable.

### What's Next

If this research were to continue, the most promising directions would be:

- **Verify Silver→Gold** with Bloomberg or Reuters tick data
- **Paid intraday data** (IQFeed, Polygon.io) for tick-level microstructure analysis
- **Multi-asset ensemble** combining non-overlapping weak signals
- **Same framework on other instruments** (crude oil, FX, equities, crypto)
- **Machine learning with engineered features** beyond the simple statistical tests used here

But for the question this framework was built to answer — *does XAU/USD have a simple, statistically robust, tradeable edge?* — the answer is no.

---

## Technical Appendix

### Repository Structure
```
├── scripts/           # 14 Python research scripts
├── reports/           # 17 Markdown research reports
├── charts/            # 15 visualization PNGs
├── data/              # 7 CSV datasets
├── validasi.py        # Validation entry point
├── .gitignore
└── README.md
```

### Data Sources
| Source | Data | Period | Observations |
|--------|------|--------|-------------|
| Yahoo Finance (GC=F) | Gold Futures Daily | 2000-08-30 to 2026-06-08 | 6,466 |
| Yahoo Finance (GC=F) | Gold Futures H1 | 2024-06-09 to 2026-06-08 | 11,395 |
| Yahoo Finance (SI=F) | Silver Futures Daily | 2005-01-03 to 2026-06-08 | 6,461 |
| Yahoo Finance (DX-Y.NYB) | DXY Daily | 2002-07-31 to 2026-06-08 | 5,978 |
| Yahoo Finance (DX-Y.NYB) | DXY H1 | 2024-06-09 to 2026-06-08 | 11,876 |
| Yahoo Finance (^TNX) | US10Y Daily | 2000-08-30 to 2026-06-08 | 6,466 |

### Success Criteria
- Sample size > 300
- P-value < 0.05
- Profit factor > 1.30
- Sharpe ratio > 1.00 (annualized)
- Stable across sub-periods
- Survives Monte Carlo permutation test

### Software Stack
- Python 3.14
- pandas, numpy, scipy for statistics
- matplotlib for visualization
- yfinance for data acquisition
- scikit-learn for multivariate models (Linear Regression, Random Forest)
- requests for alternative data source attempts

---

## Phase 16 — Signal Persistence & Holding Period Analysis (RESEARCH-013)

**Script:** `research_013_signal_persistence.py`
**Reports:** 6 (A–E + Master)
**Date:** 2026-06-08
**Status:** COMPLETE — 0 edges

### Hypothesis

The 6 indicator-based models from RESEARCH-012 all failed at the 1-day horizon. But medium-term information might be invisible in 1-day tests. RESEARCH-013 tested whether these same signals contain predictive information at holding periods from 1 to 60 days.

### Methodology

- Same 6 models from RESEARCH-012 (Trend Following, Trend Pullback, Mean Reversion Extreme, Volatility Expansion, Breakout Confirmation, Consensus)
- 9 holding periods: 1d, 2d, 3d, 5d, 10d, 15d, 20d, 30d, 60d
- Overlapping forward returns with block bootstrap Monte Carlo (10,000 permutations, block size = holding period)
- Sharpe correctly annualized for each holding period

### Bug Fixes During Execution

The initial run contained two critical bugs discovered during validation:
1. **Sharpe annualization error:** Used `sqrt(252)` for all holding periods instead of `sqrt(252/d)`, inflating Sharpe by up to 7.75× at 60d
2. **MC validation scoping error:** Only ran at 1d, with MC_p defaulting to 0.0 for all longer horizons — producing 4 false-positive "passes"

Both bugs were corrected before final results.

### Results: 0/6 Models Pass All Criteria

| Model | Best Hold | Sharpe | PF | MC p |
|-------|-----------|--------|----|-------|
| A — Trend Following | 1d | 0.67 | 1.13 | 0.1548 |
| B — Trend Pullback | 60d | 0.81 | 2.73 | 0.0000 |
| C — Mean Reversion Extreme | 5d | 0.52 | 1.23 | 0.1428 |
| D — Volatility Expansion | 10d | 0.11 | 1.06 | 0.3668 |
| E — Breakout Confirmation | 1d | 0.45 | 1.10 | 0.3725 |
| F — Consensus | 60d | 0.35 | 1.54 | 0.0310 |

### Statistical Significance ≠ Economic Viability

Three models (B, C, F) show MC p < 0.05 at peak hold, meaning directional signals contain non-random information. But no model reaches Sharpe > 1.0. Best Sharpe is Model B at 60d (0.81), yet Buy & Hold gold (0.69) still nearly matches it without any timing effort.

### Conclusion

**Extending holding periods to 10–60 days does not unlock a hidden edge.** Weak directional information exists in some technical signals at medium-term horizons, but the signal-to-noise ratio is too low for any economically viable strategy. This confirms and extends RESEARCH-001 through RESEARCH-012: XAU/USD does not contain simple, exploitable statistical patterns at any holding period from 1 to 60 days.

---

*End of Master Chronicle. Research conducted June 2026. All scripts reproducible. All reports generated automatically. No guarantee of future market behavior.*

*"The market can remain irrational longer than you can remain solvent." — John Maynard Keynes*
