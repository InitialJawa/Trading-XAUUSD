# RESEARCH-H1-001: Intraday Session Edges

**Date:** 2026-06-08 17:52
**Instrument:** XAU/USD (GC=F)
**Data:** H1 (hourly), 11,395 bars
**Period:** 2024-06-09 23:00 to 2026-06-08 10:00 UTC
**Trading Days:** 611
**Data Source:** Yahoo Finance (yfinance)

**Note:** Yahoo Finance limits H1 data to the last 730 days. Data covers ~2 years.
**Sessions (UTC):** Asia 00-08, London 08-13, Overlap 13-16, New York 16-21

## TEST 1: Session Effect

| Session | N | Mean% | WR% | Sharpe | PF | P-value |
|---------|---|-------|-----|--------|----|---------|
| Asia | 4,931 | 0.0087 | 51.1 | 2.4103 | 1.1073 | 2.9573e-02* |
| London | 2,482 | 0.0087 | 53.6 | 2.5305 | 1.1057 | 1.0513e-01 |
| Overlap | 1,502 | -0.0087 | 51.7 | -1.6961 | 0.9378 | 3.9811e-01 |
| NewYork | 2,480 | 0.0065 | 52.3 | 1.7699 | 1.0871 | 2.5718e-01 |

## TEST 2: Hour of Day (UTC)

| Hour (UTC) | N | Mean% | WR% | Sharpe | PF | P-value | Vol% |
|------------|---|-------|-----|--------|----|---------|------|
| 00:00 | 492 | 0.0072 | 50.2 | 2.0369 | 1.0890 | 5.6153e-01 | 0.2736 |
| 01:00 | 492 | 0.0226 | 50.8 | 4.8555 | 1.2070 | 1.6672e-01 | 0.3616 |
| 02:00 | 492 | -0.0129 | 49.0 | -3.5522 | 0.8680 | 3.1148e-01 | 0.2831 |
| 03:00 | 491 | 0.0111 | 52.5 | 4.6667 | 1.1844 | 1.8424e-01 | 0.1854 |
| 04:00 | 495 | 0.0157 | 48.1 | 6.8925 | 1.3214 | 4.9183e-02 | 0.1767 |
| 05:00 | 495 | -0.0177 | 51.7 | -4.6103 | 0.8295 | 1.8780e-01 | 0.2993 |
| 06:00 | 495 | 0.0135 | 55.2 | 3.9558 | 1.1658 | 2.5831e-01 | 0.2647 |
| 07:00 | 496 | 0.0181 | 52.0 | 5.1869 | 1.2245 | 1.3807e-01 | 0.2707 |
| 08:00 | 496 | 0.0192 | 58.5 | 5.9997 | 1.2534 | 8.6392e-02 | 0.2483 |
| 09:00 | 497 | -0.0086 | 48.1 | -3.1153 | 0.8860 | 3.7226e-01 | 0.2153 |
| 10:00 | 497 | -0.0008 | 50.7 | -0.2722 | 0.9894 | 9.3783e-01 | 0.2351 |
| 11:00 | 496 | 0.0212 | 57.3 | 6.1093 | 1.2891 | 8.0814e-02 | 0.2703 |
| 12:00 | 496 | 0.0128 | 53.4 | 2.8245 | 1.1156 | 4.1898e-01 | 0.3526 |
| 13:00 | 498 | -0.0115 | 51.6 | -2.3381 | 0.9223 | 5.0258e-01 | 0.3833 |
| 14:00 | 502 | 0.0001 | 52.4 | 0.0199 | 1.0007 | 9.9544e-01 | 0.4103 |
| 15:00 | 502 | -0.0147 | 51.0 | -2.8306 | 0.8826 | 4.1518e-01 | 0.4052 |
| 16:00 | 501 | 0.0188 | 55.1 | 5.2214 | 1.2186 | 1.3353e-01 | 0.2795 |
| 17:00 | 498 | -0.0033 | 48.0 | -1.1604 | 0.9570 | 7.3929e-01 | 0.2206 |
| 18:00 | 495 | -0.0167 | 52.1 | -3.1621 | 0.8042 | 3.6610e-01 | 0.4102 |
| 19:00 | 493 | 0.0062 | 51.7 | 2.1080 | 1.0908 | 5.4754e-01 | 0.2284 |
| 20:00 | 493 | 0.0274 | 54.8 | 8.9493 | 1.4941 | 1.0915e-02 | 0.2378 |
| 21:00 | 167 | -0.0020 | 50.9 | -0.8221 | 0.9677 | 8.9151e-01 | 0.1878 |
| 22:00 | 326 | -0.0111 | 45.1 | -2.4324 | 0.8869 | 5.7265e-01 | 0.3539 |
| 23:00 | 490 | 0.0379 | 54.7 | 8.8744 | 1.5917 | 1.1852e-02 | 0.3323 |

**Best hour:** 23:00 UTC (mean=+0.0379%, WR=54.7%)
**Worst hour:** 05:00 UTC (mean=-0.0177%, WR=51.7%)

## TEST 3: Opening Range Breakout (London Open)

Method: London opens at 08:00 UTC. First 2 hours (08:00-09:00 UTC) establish the opening range.
Breakout above range high = Long. Breakout below range low = Short.
Forward returns measured at 1h, 3h, 6h after breakout (from 10:00 UTC onward).

**Total breakout signals:** 1,416

| Horizon | Type | N | Mean% | WR% | Sharpe | PF | P-value |
|---------|------|---|-------|-----|--------|----|---------|
| 1h | Long | 240 | 0.0001 | 50.8 | 2.7154 | 1.1179 | 5.8907e-01 |
| 1h | Short | 232 | 0.0003 | 63.8 | 7.7265 | 1.3529 | 1.3157e-01 |
| 3h | Long | 240 | -0.0000 | 51.2 | -0.1075 | 0.9959 | 9.8293e-01 |
| 3h | Short | 232 | 0.0005 | 56.5 | 5.8785 | 1.2360 | 2.5078e-01 |
| 6h | Long | 240 | -0.0006 | 47.9 | -4.5482 | 0.8355 | 3.6584e-01 |
| 6h | Short | 232 | 0.0003 | 59.9 | 2.7339 | 1.1056 | 5.9286e-01 |

**Combined (Long + Short):**
| Horizon | N | Mean% | WR% | Sharpe | PF | P-value |
|---------|---|-------|-----|--------|----|---------|
| 1h | 472 | 0.0002 | 57.2 | 5.2895 | 1.2357 | 1.4016e-01 |
| 3h | 472 | 0.0002 | 53.8 | 2.9570 | 1.1161 | 4.0918e-01 |
| 6h | 472 | -0.0001 | 53.8 | -1.0000 | 0.9627 | 7.8008e-01 |

## TEST 4: Volatility Regime (ATR-H1)

### High Volatility (top 33% ATR)

| Horizon | N | Mean% | WR% | Sharpe | PF | P-value |
|---------|---|-------|-----|--------|----|---------|
| 1h | 3,755 | 0.0026 | 51.5 | 0.4734 | 1.0198 | 7.0916e-01 |
| 3h | 3,753 | 0.0057 | 51.6 | 1.0600 | 1.0449 | 4.0376e-01 |
| 6h | 3,750 | 0.0010 | 50.9 | 0.1940 | 1.0081 | 8.7862e-01 |
| 12h | 3,744 | 0.0019 | 50.7 | 0.3494 | 1.0145 | 7.8338e-01 |

### Low Volatility (bottom 33% ATR)

| Horizon | N | Mean% | WR% | Sharpe | PF | P-value |
|---------|---|-------|-----|--------|----|---------|
| 1h | 3,756 | 0.0108 | 52.1 | 4.2670 | 1.1735 | 7.7984e-04 |
| 3h | 3,756 | 0.0063 | 51.3 | 2.3994 | 1.0955 | 5.8725e-02 |
| 6h | 3,756 | 0.0075 | 52.3 | 2.8373 | 1.1150 | 2.5413e-02 |
| 12h | 3,756 | 0.0083 | 51.7 | 3.3489 | 1.1399 | 8.3471e-03 |

## TEST 5: DXY Lead-Lag (H1)

**Aligned bars:** 11,381

| Lag | Cross-Corr | Interpretation | P-value |
|-----|------------|----------------|---------|
| +1h | -0.0006 | DXY leads by 1h | 9.5265e-01 |
| +2h | -0.0074 | DXY leads by 2h | 4.2911e-01 |
| +3h | -0.0096 | DXY leads by 3h | 3.0726e-01 |
| +4h | +0.0063 | DXY leads by 4h | 4.9867e-01 |
| +6h | -0.0061 | DXY leads by 6h | 5.1726e-01 |
| +8h | -0.0034 | DXY leads by 8h | 7.1981e-01 |
| +12h | +0.0152 | DXY leads by 12h | 1.0506e-01 |

| Lag | Cross-Corr | Interpretation | P-value |
|-----|------------|----------------|---------|
| +1h | -0.0183 | Gold leads by 1h | 5.0509e-02 |
| +2h | +0.0103 | Gold leads by 2h | 2.7247e-01 |
| +3h | +0.0026 | Gold leads by 3h | 7.8305e-01 |
| +4h | -0.0131 | Gold leads by 4h | 1.6265e-01 |
| +6h | +0.0193* | Gold leads by 6h | 3.9221e-02 |
| +8h | -0.0053 | Gold leads by 8h | 5.7249e-01 |
| +12h | +0.0091 | Gold leads by 12h | 3.2960e-01 |

**Contemporaneous (same hour):** r=-0.3401, p=3.4517e-306

**Strongest relationship is contemporaneous (same hour, r=-0.3401)**

### DXY H1 Predictive Power

- DXY(t) → Gold(t+1h): r=-0.0006, p=9.5265e-01
- DXY(t) → Gold(t+3h): r=-0.0096, p=3.0726e-01
- DXY(t) → Gold(t+6h): r=-0.0061, p=5.1726e-01

## Edge Scorecard

**Total candidates tested:** ~50 across 5 tests
**Meeting criteria (N>500, p<0.05, PF>1.30, Sharpe>1.00):** 0

*No candidates meet all success criteria.*

## Stability Analysis

No candidates to analyze.

## Summary

**Data limitation:** Yahoo Finance limits H1 data to 730 days. Analysis covers ~2 years (June 2024 – June 2026).
Results should be interpreted with caution due to the short sample period.

**No candidates meet all success criteria.**

### Near-Misses (for reference)
| Condition | N | WR% | PF | Sharpe | P-value | Criteria Failed |
|-----------|----|-----|----|--------|---------|-----------------|
| Hour 23:00 UTC | 490 | 54.7% | 1.59 | 8.87 | 0.012 | N < 500 |
| Hour 20:00 UTC | 493 | 54.8% | 1.49 | 8.95 | 0.011 | N < 500 |
| ORB Short 1h | 232 | 63.8% | 1.35 | 7.73 | 0.132 | N, p-value |
| Low Vol 1h | 3,756 | 52.1% | 1.17 | 4.27 | 0.001 | PF < 1.30 |
| Hour 08:00 (London Open) | 496 | 58.5% | 1.25 | 6.00 | 0.086 | PF, p-value |

None of these survive all five criteria. The highest-WR condition (ORB Short 1h at 63.8%) suffers from insufficient sample (N=232) and statistical insignificance (p=0.13).

### Key Negative Findings:
- **Session Effect:** No session produces significantly different gold returns. Asia session has p=0.03 but PF=1.11 (below threshold).
- **Hour of Day:** Best hours (20:00, 23:00 UTC) have N ~490, just below the 500 threshold. 2 more years of data might clarify.
- **Opening Range Breakout:** London open breakouts produce no consistent edge. Short-side breakouts show higher WR (63.8%) but N is small.
- **Volatility Regime:** Low volatility shows statistically significant positive returns (p=0.001) but PF=1.17 below 1.30 threshold.
- **DXY Lead-Lag:** Contemporaneous correlation (r=-0.34) dominates at H1 frequency. No predictive lead beyond the same hour. DXY(t) → Gold(t+1h): r=-0.0006 (p=0.95).

**Chart:** `charts/h1_intraday_analysis.png`

## H1 Volatility Reference

| Metric | Value |
|--------|-------|
| H1 Return Std | 0.2976% |
| Daily Return Std | 1.3267% |
| H1 Bars / Day | ~35 |
| Total Bars | 11,395 |
| Trading Days | 611 |

## Recommended Follow-Up

1. **Source 5+ years of H1 or M15 data** from a paid provider (e.g., Dukascopy, OANDA, IQFeed) for robust intraday analysis.
2. **Microstructure edges** like bid-ask bounce, order flow, and volume profile require tick data.
3. **Session transition analysis** (e.g., 30 min before/after London open) might reveal edges invisible in full-hour buckets.
4. **Correlate with intraday news calendar** — gold often reacts to US data releases (NFP, CPI, FOMC) with specific intraday patterns.
