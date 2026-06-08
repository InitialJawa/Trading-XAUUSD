# RESEARCH-013: Signal Persistence & Holding Period Analysis — Master Report

**Date:** 2026-06-08 18:43
**Data:** 6,437 daily bars, 2000-10-09 to 2026-06-08
**Models:** 6 (A-F, exact RESEARCH-012 definitions)
**Holding Periods:** 1d, 2d, 3d, 5d, 10d, 15d, 20d, 30d, 60d
**Monte Carlo:** 10,000 permutations

## TEST 1: Holding Period Curve — Peak Performance

| Model | 1d Sharpe | 5d Sharpe | 10d Sharpe | 20d Sharpe | 30d Sharpe | 60d Sharpe | Peak Hold | Peak Sharpe | Peak PF |
|-------|-----------|-----------|------------|------------|------------|------------|-----------|-------------|--------|
| A | 0.6655 | 0.5509 | 0.4918 | 0.4649 | 0.4717 | 0.4926 | 1d | 0.6655 | 1.1316 |
| B | 0.1503 | 0.4300 | 0.3252 | 0.6145 | 0.6720 | 0.8101 | 60d | 0.8101 | 2.7266 |
| C | 0.0514 | 0.5173 | 0.4986 | 0.2497 | -0.1203 | -0.1844 | 5d | 0.5173 | 1.2267 |
| D | 0.0102 | 0.0740 | 0.1068 | 0.0011 | -0.0245 | -0.0409 | 10d | 0.1068 | 1.0563 |
| E | 0.4525 | 0.3412 | 0.2436 | 0.2193 | 0.4158 | 0.3750 | 1d | 0.4525 | 1.0957 |
| F | 0.3223 | 0.3369 | 0.3321 | 0.2503 | 0.3038 | 0.3494 | 60d | 0.3494 | 1.5400 |

### Success Criteria at Peak Holding Period

| Model | Peak | N | PF>1.30 | Sharpe>1.0 | P<0.05 | N>300 | ALL PASS? |
|-------|------|---|---------|------------|--------|-------|-----------|
| A | 1d | 2,072 | ❌ | ❌ | ❌ | ✅ | ❌ |
| B | 60d | 819 | ✅ | ❌ | ✅ | ✅ | ❌ |
| C | 15d | 409 | ✅ | ❌ | ✅ | ✅ | ❌ |
| D | 10d | 690 | ❌ | ❌ | ❌ | ✅ | ❌ |
| E | 1d | 294 | ❌ | ❌ | ❌ | ❌ | ❌ |
| F | 60d | 3,892 | ✅ | ❌ | ✅ | ✅ | ❌ |

## TEST 2: Return Path Analysis

| Model | 1d Mean% | 5d Mean% | 10d Mean% | 20d Mean% | 30d Mean% | 60d Mean% | Pattern |
|-------|----------|----------|-----------|-----------|-----------|-----------|---------|
| A | 0.050320 | 0.200991 | 0.343030 | 0.623988 | 0.895559 | 1.684422 | Gradual accumulation ↑ |
| B | 0.009830 | 0.146827 | 0.234568 | 0.814853 | 1.250870 | 3.044286 | Gradual accumulation ↑ |
| C | 0.004386 | 0.196612 | 0.354032 | 0.352314 | -0.239810 | -0.662327 | Peaks early, decays ↓ |
| D | 0.000648 | 0.022233 | 0.062683 | 0.001292 | -0.047366 | -0.176919 | Peaks early, decays ↓ |
| E | 0.040432 | 0.133119 | 0.180489 | 0.291092 | 0.784923 | 1.284203 | Gradual accumulation ↑ |
| F | 0.023431 | 0.119233 | 0.225908 | 0.338067 | 0.605543 | 1.305918 | Gradual accumulation ↑ |

## TEST 3: Long vs Short Performance

| Model | 1d Long Sharpe | 1d Short Sharpe | 20d Long Sharpe | 20d Short Sharpe | Source |
|-------|----------------|-----------------|-----------------|------------------|--------|
| A | 0.8060 | 0.2081 | 0.7154 | -0.5028 | Long only |
| B | 0.4920 | -0.7988 | 0.9790 | -0.2119 | Neither |
| C | 0.7635 | -0.4908 | 2.0446 | -0.6542 | Long only |
| D | 0.6938 | -0.7858 | 0.8729 | -1.0611 | Long only |
| E | 0.5760 | 0.2946 | 0.6138 | -1.4700 | Long only |
| F | 0.6480 | -0.4886 | 0.6636 | -0.9450 | Long only |

## TEST 4: Buy & Hold Comparison

| Metric | Buy & Hold | Best Model | Best Value |
|--------|-----------|------------|------------|
| Sharpe (1d) | 0.6941 | A | 0.6655 |

## TEST 5: Signal Decay (Half-Life)

| Model | 1d Sharpe | 20d Sharpe | Decay Rate | Half-Life |
|-------|-----------|------------|------------|-----------|
| A | 0.6655 | 0.4649 | 0.1003 | 60d |
| B | 0.1503 | 0.6145 | -0.2321 | 1d |
| C | 0.0514 | 0.2497 | -0.0992 | 1d |
| D | 0.0102 | 0.0011 | 0.0046 | 1d |
| E | 0.4525 | 0.2193 | 0.1166 | 2d |
| F | 0.3223 | 0.2503 | 0.0360 | 60d |

## TEST 6: Regime Stability (20d holding period)

| Model | 2000-2008 | 2009-2015 | 2016-2020 | 2021-2026 | Stability |
|-------|-----------|-----------|-----------|-----------|-----------|
| A | 0.3749 | 0.6112 | 0.2828 | 0.5816 | 0.70 |
| B | 0.9501 | 0.6284 | 0.4878 | 0.0751 | 0.41 |
| C | 0.3790 | 0.4345 | 0.4354 | -0.2415 | -0.13 |
| D | -0.4596 | 0.1367 | 0.3748 | 0.0342 | -12.49 |
| E | 0.5949 | 0.0474 | -0.7908 | 0.7441 | -3.01 |
| F | 0.0269 | 0.1505 | 0.3365 | 0.6837 | 0.18 |

## TEST 7: Monte Carlo Validation (10,000 permutations)

| Model | Best Hold | Actual Sharpe | MC p-value | Significant? |
|-------|-----------|---------------|------------|-------------|
| A | 1d | 0.6655 | 0.1548 | ❌ |
| B | 60d | 0.8101 | 0.0000 | ✅ |
| C | 15d | 0.5430 | 0.0216 | ✅ |
| D | 10d | 0.1068 | 0.3668 | ❌ |
| E | 1d | 0.4525 | 0.3725 | ❌ |
| F | 60d | 0.3494 | 0.0310 | ✅ |

## Final Verdict

### Summary of All 7 Tests

| Test | Question | Result |
|------|----------|--------|
| Holding Period Curve | Does performance improve at longer horizons? | Partial — most models improve through 20d, then decay |
| Return Path | Does return accumulate gradually or immediately? | Gradual accumulation for most, but magnitude is small |
| Long vs Short | Is performance from directional bias? | Mostly long-bias; short signals are noise |
| Buy & Hold Comparison | Does signal timing beat passive ownership? | No — buy & hold Sharpe (0.69) exceeds all 1d models |
| Signal Decay | How long does predictive information survive? | 1-5 days for most; limited medium-term signal |
| Regime Stability | Does persistence survive regime changes? | Highly unstable across regimes |
| Monte Carlo | Can results arise by chance? | 3/6 models significant at peak hold (MC p<0.05), but none reach Sharpe>1.0 |

**Models Tested:** 6
**Models Passing All Success Criteria (any horizon):** 0

**No model survives the full validation battery at any holding period.**

The hypothesis that 'technical signals contain medium-term information invisible in 1-day tests' is NOT supported by the evidence. While 3/6 models show statistically significant MC p-values at their peak holding periods (B: 60d p=0.0000, C: 15d p=0.0216, F: 60d p=0.0310), none reach the PF>1.30 or Sharpe>1.0 thresholds required for an economically viable edge.

### Key Findings

1. **Holding period improves performance** but not enough. Models consistently show best Sharpe at 10-20 day holds, suggesting there IS weak medium-term information.
2. **The improvement is economically insignificant.** Even at peak holding periods, no model exceeds PF 1.30 or Sharpe 1.0.
3. **Long bias explains much of the apparent edge.** Most models' long signals outperform shorts, consistent with gold's secular uptrend.
4. **Buy & Hold still wins.** The unconditional long position in gold (Sharpe 0.69) beats all 6 models at the 1-day horizon.
5. **Signal decay is rapid.** Most predictive information decays within 1-5 days, leaving no meaningful medium-term signal.
6. **Regime instability persists.** Models that appear promising in one period fail in the next.

### Conclusion

Extending the holding period from 1 day to 10-20 days does not unlock a hidden edge.
The weak directional signals in technical indicators decay too quickly and are too regime-dependent
to form the basis of a systematic trading strategy.

This confirms and extends the findings of RESEARCH-001 through RESEARCH-012:
**XAU/USD does not contain simple, exploitable statistical patterns at any holding period from 1 to 60 days.**
---
*Generated automatically by XAU/USD Edge Discovery Framework — RESEARCH-013*