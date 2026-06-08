# RESEARCH-010: Edge Scorecard

**Date:** 2026-06-08 17:52
**Instrument:** XAU/USD (GC=F)
**Total Edges Tested:** 11
**Edges Meeting Success Criteria:** 0 (*see Silver Lead caveat below*)

*3 additional conditions from RESEARCH-011 meet numerical criteria but fail stability or are restatements of earlier findings.*

## Success Criteria

| Criterion | Requirement |
|-----------|-------------|
| Sample Size | > 300 |
| P-value | < 0.05 |
| Profit Factor | > 1.30 |
| Sharpe Ratio | > 1.00 |
| Stability | Consistent across periods |

## Full Ranking

| Rank | Edge | Phase | Sample | Win Rate | PF | Sharpe | P-value | Stability | Meets Criteria? |
|------|------|-------|--------|----------|----|--------|---------|-----------|-----------------|
| 1 | SI_Lead_1d_Sign | 9 - Cross Asset | 6,461 | 64.88% | 3.07 | 5.99 | ~0 | 0.9832 | **YES** ⚠️ |
| 2 | Extreme_Silver_D10_1d | 11 - Cond. Regime | 646 | 56.70% | 1.33 | 1.57 | 0.0123 | — | **YES** ⚠️ |
| 3 | Extreme_VIX_D1__1d | 11 - Cond. Regime | 651 | 52.50% | 1.45 | 2.09 | 0.0008 | 0.3795 | **YES** ⚠️ |
| 4 | Extreme_VIX_D1__5d | 11 - Cond. Regime | 651 | 52.50% | 1.36 | 1.77 | 0.0046 | 0.3482 | **YES** ⚠️ |
| 5 | DXY_Q5_1d_near | 11 - Cond. Regime | 1,292 | 52.20% | 1.27 | 1.36 | 0.0021 | 0.5026 | no |
| 6 | TP_Down5 | 4 - Trend Persistence | 115 | 60.00% | 1.35 | 1.47 | 0.039751 | 0.6787 | no |
| 7 | DoW_Mon | 7 - Day of Week | 1,211 | 54.67% | 1.27 | 1.30 | 0.001280 | 0.6537 | no |
| 8 | DoW_Fri | 7 - Day of Week | 1,292 | 53.02% | 1.24 | 1.21 | 0.032138 | 0.6153 | no |
| 9 | TP_Down2 | 4 - Trend Persistence | 1,338 | 55.23% | 1.19 | 0.95 | 0.000143 | 0.5685 | no |
| 10 | TP_Down3 | 4 - Trend Persistence | 589 | 55.18% | 1.19 | 0.95 | 0.013359 | 0.5240 | no |
| 11 | MR_W50_T1.0 | 3 - Mean Reversion | 3,455 | 47.87% | 0.81 | -0.19 | 0.012985 | 0.2695 | no |
| 12 | MR_W50_T2.0 | 3 - Mean Reversion | 912 | 45.61% | 0.72 | -0.29 | 0.008861 | 0.0421 | no |

*⚠️ SI_Lead_1d meets all numerical criteria but is flagged as potentially
exploitable — see detailed note below.*

## Edges Meeting All Success Criteria

Three additional conditions meet ALL numerical success criteria (see caveats below):

| Metric | Value | Criterion | Met? |
|--------|-------|-----------|------|
| Sample Size | 6,461 | > 300 | ✅ |
| P-value | ~0 (p < 10^-100) | < 0.05 | ✅ |
| Profit Factor | 3.07 | > 1.30 | ✅ |
| Sharpe Ratio | 5.99 (ann.) | > 1.00 | ✅ |
| Stability | r=0.29–0.69 across 22 years | Consistent | ✅ |

However, see **Caveats** below before concluding any are genuine tradeable edges.

### Silver Lead Edge Details (SI_Lead_1d)

**Discovery:** Silver (SI=F) return today is a strong predictor of Gold (GC=F)
return tomorrow. This was discovered in Research-009 (Cross-Asset Driver
Analysis) and is the strongest predictive relationship found across all 10
phases of the framework.

**Core Statistics:**
- Correlation: Silver(t) → Gold(t+1): r = +0.52 (p ≈ 0)
- R²: 0.272 (27% of next-day gold variance explained)
- Direction accuracy: 64.9% (sign-based strategy)
- Consistent across all 22 years tested (2005–2026, lowest year WR=56%)

**Trading Strategy (Sign-Based):**
- If Silver close positive today → Long Gold tomorrow at close
- If Silver close negative today → Short Gold tomorrow at close
- Hold for 1 day, flatten at next close

**Year-by-Year Performance:**
| Year | N | Correlation | Win Rate |
|------|---|-------------|----------|
| 2005 | 248 | +0.40 | 62.5% |
| 2006 | 249 | +0.41 | 63.5% |
| 2007 | 252 | +0.39 | 58.3% |
| 2008 | 253 | +0.52 | 67.2% |
| 2009 | 252 | +0.57 | 69.4% |
| 2010 | 252 | +0.29 | 56.0% |
| 2011 | 252 | +0.66 | 71.4% |
| 2012 | 250 | +0.67 | 69.2% |
| 2013 | 250 | +0.68 | 74.8% |
| 2014 | 252 | +0.69 | 66.7% |
| 2015 | 252 | +0.59 | 68.3% |
| 2016 | 250 | +0.50 | 72.8% |
| 2017 | 251 | +0.53 | 68.5% |
| 2018 | 250 | +0.52 | 61.6% |
| 2019 | 252 | +0.48 | 64.3% |
| 2020 | 253 | +0.62 | 70.8% |
| 2021 | 252 | +0.59 | 64.7% |
| 2022 | 251 | +0.57 | 69.3% |
| 2023 | 250 | +0.49 | 57.2% |
| 2024 | 252 | +0.57 | 70.2% |
| 2025 | 252 | +0.47 | 68.7% |
| 2026 | 108 | +0.59 | 70.4% |

### Condition Caveats

Despite passing numerical criteria, all three conditions require qualification:

**1. SI_Lead_1d_Sign:** Silver-leads-Gold edge from RESEARCH-009.

1. **Extreme Asymmetry:** Silver(t) → Gold(t+1) has r=+0.52, but
   Gold(t) → Silver(t+1) has r=-0.01 (essentially zero). A true lead-lag
   relationship should show at least weak effects in both directions. This
   extreme asymmetry is more consistent with a **data alignment artifact**
   than a genuine market inefficiency.

2. **Potential Cause — Settlement Timing:** GC=F settles at 1:30 PM ET and
   SI=F at 1:25 PM ET (both CME). A 5-minute window exists where SI=F is
   already settled while GC=F is still trading. However, this would predict
   Gold leading Silver, which is the opposite of what we observe.

3. **Potential Cause — Yahoo Data Labeling:** Yahoo may label SI=F data
   differently than GC=F (e.g., trade date vs. settlement date convention
   differences). This could create a systematic 1-day offset.

4. **Execution Feasibility:** The relationship is between daily close-to-close
   returns. In practice, you cannot trade at the observed silver close and
   instantly enter gold at the same closing price. Slippage and the close/open
   gap would need to be accounted for.

**2. Extreme_Silver_D10_1d:** Silver in top 10% price level → Gold next day. N=646, WR=56.7%, PF=1.33, Sharpe=1.57. This is an alternative framing of the SI_Lead_1d effect (conditioning on Silver LEVEL rather than Silver RETURN). Not an independent edge — it captures the same Silver→Gold predictive relationship.

**3. Extreme_VIX_D1__1d / Extreme_VIX_D1__5d:** VIX in bottom 10% → Gold positive returns. N=651, WR=52.5%, PF=1.45, Sharpe=2.09. **FAILS stability** — 5-year subperiod analysis shows extreme instability:
- 2005-2009: Sharpe 0.92 (meaningful)
- 2010-2014: Sharpe 0.17 (no edge)
- 2015-2019: Sharpe 0.45 (weak)
- 2020-2024: Sharpe 0.75 (moderate)
  
  Additionally, WR=52.5% is nearly random. The high PF/Sharpe is driven by a few outlier positive returns, not a consistent directional edge. This is a **statistical artifact** of small-sample tail events, not a genuine edge.

**Recommendation:** Before treating any as tradeable, verify with:
- Tick-level or intraday data to confirm the lead direction
- Alternative data sources (Bloomberg, Reuters) to rule out labeling artifacts
- Paper trading to measure real-world slippage and transaction costs

## Summary by Phase

| Phase | Total Edges | Significant (p<0.05) | Meeting All Criteria |
|-------|-------------|---------------------|---------------------|
| 3 - Mean Reversion | 2 | 2 | 0 |
| 4 - Trend Persistence | 3 | 3 | 0 |
| 7 - Day of Week | 2 | 2 | 0 |
| 9 - Cross Asset Drivers | 1 | 1 | 0* |
| 11 - Conditional Regime | 3 | 3 | 0* |

*Conditions meet numerical criteria but fail stability or data authenticity checks.

## Final Verdict

**Number of statistically significant edges found: 11**
**Number of edges meeting ALL success criteria: 0** (all caveated)

### Framework Conclusion

After 10 phases of rigorous hypothesis testing on XAU/USD (GC=F):

- **Mean reversion:** 0 edges (anti-edges; mean reversion is unprofitable)
- **Trend persistence:** 0 edges (weak momentum, insufficient sample)
- **Day of week:** 0 edges (Monday/Friday near-misses, PF < 1.30)
- **Session effects:** N/A (no intraday data available)
- **Macro events:** 0 edges (no NFP/CPI/FOMC effects detected)
- **Cross-asset drivers:** 1 strong candidate (Silver→Gold 1-day lead), but
  flagged for artifact investigation
- **Conditional regimes:** 3 numerical near-misses; all fail stability tests or are restatements of earlier findings

**The XAU/USD market appears highly efficient for simple statistical patterns.**
No robust conditional or unconditional edges were discovered. The only candidate
(Silver's predictive power for next-day Gold) requires independent data
verification before being treated as genuine.

---
*Generated automatically by XAU/USD Edge Discovery Framework*
