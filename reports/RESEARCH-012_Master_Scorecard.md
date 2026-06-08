# RESEARCH-012: Indicator Ensemble Framework — Master Scorecard

**Date:** 2026-06-08 18:21
**Instrument:** XAU/USD (GC=F)
**Data:** Daily, 6,437 bars
**Period:** 2000-10-09 to 2026-06-08
**Monte Carlo:** 10,000 permutations

## Models Tested

| Model | Description |
|-------|------------|
| A | Trend Following: EMA50>EMA200 & ADX>25 & MACD>0 (Long) | EMA50<EMA200 & ADX>25 & MACD<0 (Short) |
| B | Trend Pullback: EMA50>EMA200 & RSI 40-50 & ADX>20 (Long) | EMA50<EMA200 & RSI 50-60 & ADX>20 (Short) |
| C | Mean Reversion Extreme: Close<BB_lower & RSI<30 (Long) | Close>BB_upper & RSI>70 (Short) |
| D | Volatility Expansion: BB Width bottom20% & ATR rising 3d & MACD>0 (Long) | MACD<0 (Short) |
| E | Breakout Confirmation: Close>BB_upper & ADX>25 & EMA50>EMA200 (Long) | Close<BB_lower & ADX>25 & EMA50<EMA200 (Short) |
| F | Consensus: Bull Score>=4 (Long) | Bear Score>=4 (Short) |

## Signal Frequency

| Model | Total Signals | Long | Short | Long/Short |
|-------|--------------|------|-------|-----------|
| A | 2,072 | 1,637 | 435 | 3.76 |
| B | 833 | 626 | 207 | 3.02 |
| C | 409 | 136 | 273 | 0.50 |
| D | 690 | 371 | 319 | 1.16 |
| E | 294 | 234 | 60 | 3.90 |
| F | 3,915 | 2,810 | 1,105 | 2.54 |

## Combined Performance (1d forward)

| Rank | Model | N | WR% | PF | Sharpe | MaxDD% | Expectancy% | P-value | Stability | MC p-val |
|------|-------|----|-----|----|--------|--------|-------------|---------|-----------|----------|
| 4 | D Volatility Expansion | 690 | 53.3 | 1.1335 | 0.7368 | -23.2853 | 0.0466 | 2.2318e-01 | 0.07 | 0.4785 ❌ |
| 3 | C Mean Reversion Extreme | 409 | 49.4 | 1.1232 | 0.5964 | -18.1679 | 0.0509 | 4.4783e-01 | -0.30 | 0.5540 ❌ |
| 6 | F Consensus | 3,915 | 52.6 | 1.1163 | 0.6024 | -37.6153 | 0.0438 | 1.7632e-02 | 0.51 | 0.7110 ❌ |
| 1 | A Trend Following | 2,072 | 51.6 | 1.1113 | 0.5683 | -29.7832 | 0.0430 | 1.0333e-01 | 0.51 | 0.6585 ❌ |
| 2 | B Trend Pullback | 833 | 51.3 | 1.1076 | 0.5731 | -17.8214 | 0.0375 | 2.9772e-01 | -1.26 | 0.5790 ❌ |
| 5 | E Breakout Confirmation | 294 | 50.7 | 1.0537 | 0.2591 | -20.5367 | 0.0232 | 7.7981e-01 | -1.35 | 0.7015 ❌ |

## Long vs Short Breakdown (1d)

| Model | Long N | Long WR% | Long Sharpe | Long PF | Short N | Short WR% | Short Sharpe | Short PF |
|-------|--------|----------|-------------|---------|---------|-----------|-------------|----------|
| A | 1,637 | 52.2 | 0.8060 | 1.1602 | 435 | 49.4 | -0.2081 | 0.9614 |
| B | 626 | 51.3 | 0.4920 | 1.0909 | 207 | 51.2 | 0.7988 | 1.1574 |
| C | 136 | 56.6 | 0.7635 | 1.1669 | 273 | 45.8 | 0.4908 | 1.0940 |
| D | 371 | 54.2 | 0.6938 | 1.1301 | 319 | 52.4 | 0.7858 | 1.1370 |
| E | 234 | 50.4 | 0.5760 | 1.1102 | 60 | 51.7 | -0.2946 | 0.9395 |
| F | 2,810 | 52.4 | 0.6480 | 1.1226 | 1,105 | 53.0 | 0.4886 | 1.0993 |

## 5-Day and 20-Day Horizons

| Model | 5d WR% | 5d Sharpe | 5d PF | 5d P | 20d WR% | 20d Sharpe | 20d PF | 20d P |
|-------|--------|-----------|-------|------|---------|------------|--------|-------|
| A | 55.0 | 1.0982 | 1.2041 | 1.6609e-03 | 56.5 | 3.0064 | 1.6555 | 1.3233e-17 |
| B | 53.5 | 1.2176 | 1.2260 | 2.7111e-02 | 58.4 | 3.3271 | 1.7428 | 2.5108e-09 |
| C | 57.5 | 1.4791 | 1.2987 | 6.0228e-02 | 63.1 | 4.9589 | 2.2803 | 6.9600e-10 |
| D | 54.1 | 1.8644 | 1.3491 | 2.1168e-03 | 59.7 | 4.2841 | 1.9297 | 3.3513e-12 |
| E | 56.5 | 1.1327 | 1.2072 | 2.2214e-01 | 59.2 | 3.4504 | 1.7424 | 2.3265e-04 |
| F | 56.3 | 1.4563 | 1.2811 | 1.0191e-08 | 58.2 | 3.2808 | 1.7192 | 2.1908e-37 |

## Success Criteria Check

| Criterion | Required |
|-----------|----------|
| Sample Size | > 300 |
| P-value | < 0.05 |
| Profit Factor | > 1.30 |
| Sharpe Ratio | > 1.00 |
| Stability | Survive all 4 periods |
| Monte Carlo | p < 0.05 |

| Model | N>300 | P<0.05 | PF>1.30 | Sharpe>1.0 | Stable | MC<0.05 | PASS ALL? |
|-------|-------|--------|---------|------------|--------|---------|-----------|
| D Volatility Expansion | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| C Mean Reversion Extreme | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| F Consensus | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| A Trend Following | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| B Trend Pullback | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| E Breakout Confirmation | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Stability Across Periods (1d Sharpe)

| Model | 2000-2008 | 2009-2015 | 2016-2020 | 2021-2026 | Stability |
|-------|-----------|-----------|-----------|-----------|-----------|
| A | 0.30 | 0.44 | 0.66 | 1.12 | 0.51 |
| B | 0.75 | 0.30 | 2.78 | -1.27 | -1.26 |
| C | 1.08 | -0.48 | 2.65 | 0.30 | -0.30 |
| D | 1.47 | -0.55 | 1.20 | 1.68 | 0.07 |
| E | -1.00 | -0.40 | 2.06 | 1.52 | -1.35 |
| F | 0.81 | 0.11 | 0.65 | 0.86 | 0.51 |

## Monte Carlo Results

| Model | Actual Sharpe | MC Mean | MC 95th | MC p-value | Significant? |
|-------|--------------|---------|---------|-----------|-------------|
| D Volatility Expansion | 0.7368 | — | — | 0.4785 | no |
| C Mean Reversion Extreme | 0.5964 | — | — | 0.5540 | no |
| F Consensus | 0.6024 | — | — | 0.7110 | no |
| A Trend Following | 0.5683 | — | — | 0.6585 | no |
| B Trend Pullback | 0.5731 | — | — | 0.5790 | no |
| E Breakout Confirmation | 0.2591 | — | — | 0.7015 | no |

## Final Verdict

| Metric | Value |
|--------|-------|
| Models Tested | 6 |
| Models with Sufficient Signals | 6 |
| Models Passing All Criteria | 0 |

**Classical technical indicator ensembles do not produce a robust edge in XAU/USD under this framework.**

Despite testing 6 distinct multi-indicator models (Trend Following, Trend Pullback, Mean Reversion Extreme, Volatility Expansion, Breakout Confirmation, and Multi-Indicator Consensus), none survived the full battery of success criteria including sample size, statistical significance, profit factor, Sharpe ratio, stability across market regimes, and Monte Carlo permutation testing.

The best performer was **D Volatility Expansion** (PF=1.1335, Sharpe=0.7368), but this did not meet all criteria.

This confirms the findings of RESEARCH-001 through RESEARCH-H1-002: XAU/USD does not contain simple, exploitable statistical patterns. Adding technical indicator ensembles — combinations of classical signals that traders commonly use — does not unlock an edge that single-factor tests missed.

### What Was Tested
- Trend Following (EMA crossover + ADX filter + MACD confirmation)
- Trend Pullback (pullback to moving average in trending market)
- Mean Reversion Extreme (Bollinger Band extremes + RSI oversold/overbought)
- Volatility Expansion (squeeze detection + ATR expansion)
- Breakout Confirmation (Bollinger breakout + trend filter)
- Multi-Indicator Consensus (voting system across 5 indicators)

### Why This Matters
These are not exotic strategies. These are the indicator combinations found in every trading platform, every beginner's guide, and every 'gold trading system' sold online. If they worked, they would have been found. They don't.

### Limitations
- Only daily frequency tested (H1 may differ, but H1 data is limited to 2 years)
- Fixed parameters only (no optimization allowed by design)
- Classical indicators only (no machine learning, no alternative data)
- Equal-weighted consensus only (no dynamic weighting)
---
*Generated automatically by XAU/USD Edge Discovery Framework — Indicator Ensemble Module*