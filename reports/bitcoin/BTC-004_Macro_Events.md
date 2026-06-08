# BTC-004: Macro Event Effect

**Date:** 2026-06-09 00:17
**Instrument:** BTC-USD
**Period:** 2014-09-18 to 2026-06-08

## Methodology

For each event type:
- Find the nearest trading day to the event date
- Calculate return 1 day before, 1 day after, and 3 days after
- Calculate volatility around event vs normal periods
- Test if event returns differ significantly from non-event returns

## NFP Events

| Metric | Pre-Event (-3d) | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |
|--------|----------------|----------------|-----------|------------------|--------------------|-----------|
| Avg Return % | 0.7086 | -0.2722 | 0.4092 | 0.2265 | 0.8375 | 0.1688 |
| Std Dev % | 5.7811 | 3.3895 | 3.2373 | 2.6738 | 5.7697 | 3.4985 |
| Win Rate % | 58.8652 | 48.2270 | 58.1560 | 56.0284 | 63.8298 | 52.2096 |

### Significance Tests

- **Post+1d vs Non-Event**: t=0.1940, p=0.846177 (Not significant)
- **Post+3d vs Non-Event**: t=2.1709, p=0.029992 (SIGNIFICANT)
- **Pre-1d vs Non-Event**: t=-1.4730, p=0.140814 (Not significant)
- **Pre-Event vs Post-Event**: t=-1.3668, p=0.172773 (Not significant)
- **Volatility ratio (event/non-event):** 0.93x

**Potential edge detected**: Post+3d for NFP (WR=63.8%, p=0.0013)

---

## CPI Events

| Metric | Pre-Event (-3d) | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |
|--------|----------------|----------------|-----------|------------------|--------------------|-----------|
| Avg Return % | -0.3371 | 0.0256 | 0.2109 | 0.4073 | 0.5150 | 0.1756 |
| Std Dev % | 6.9270 | 3.6834 | 4.8875 | 3.9740 | 6.2925 | 3.4333 |
| Win Rate % | 46.4286 | 54.2857 | 56.4286 | 52.8571 | 52.1429 | 52.2694 |

### Significance Tests

- **Post+1d vs Non-Event**: t=0.7809, p=0.434926 (Not significant)
- **Post+3d vs Non-Event**: t=1.1082, p=0.267848 (Not significant)
- **Pre-1d vs Non-Event**: t=-0.5069, p=0.612248 (Not significant)
- **Pre-Event vs Post-Event**: t=-0.8304, p=0.407004 (Not significant)
- **Volatility ratio (event/non-event):** 1.42x

---

## FOMC Events

| Metric | Pre-Event (-3d) | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |
|--------|----------------|----------------|-----------|------------------|--------------------|-----------|
| Avg Return % | 0.8481 | 0.3176 | 0.6664 | -0.9462 | -0.6071 | 0.1657 |
| Std Dev % | 6.7582 | 3.9766 | 4.4271 | 3.7318 | 5.5938 | 3.4657 |
| Win Rate % | 48.9362 | 54.2553 | 55.3191 | 36.1702 | 46.8085 | 52.3400 |

### Significance Tests

- **Post+1d vs Non-Event**: t=-3.0702, p=0.002153 (SIGNIFICANT)
- **Post+3d vs Non-Event**: t=-2.1011, p=0.035695 (SIGNIFICANT)
- **Pre-1d vs Non-Event**: t=0.4186, p=0.675518 (Not significant)
- **Pre-Event vs Post-Event**: t=2.2348, p=0.026617 (SIGNIFICANT)
- **Volatility ratio (event/non-event):** 1.28x

**Potential edge detected**: Post+1d for FOMC (WR=36.2%, p=0.0095)

---

## Halving Events

| Metric | Pre-Event (-3d) | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |
|--------|----------------|----------------|-----------|------------------|--------------------|-----------|
| Avg Return % | -5.4836 | -0.3424 | -1.1933 | 1.3044 | 6.6456 | 0.1777 |
| Std Dev % | 5.2880 | 5.9326 | 1.2342 | 1.1192 | 4.7267 | 3.4913 |
| Win Rate % | 33.3333 | 66.6667 | 33.3333 | 66.6667 | 100.0000 | 52.4188 |

### Significance Tests

- **Post+1d vs Non-Event**: t=0.5588, p=0.576326 (Not significant)
- **Post+3d vs Non-Event**: t=3.2059, p=0.001356 (SIGNIFICANT)
- **Pre-1d vs Non-Event**: t=-0.2577, p=0.796657 (Not significant)
- **Pre-Event vs Post-Event**: t=-0.3858, p=0.719319 (Not significant)
- **Volatility ratio (event/non-event):** 0.35x

---

## ETF_Events Events

| Metric | Pre-Event (-3d) | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |
|--------|----------------|----------------|-----------|------------------|--------------------|-----------|
| Avg Return % | 0.0745 | 0.0680 | -0.0268 | 0.5572 | -2.0495 | 0.1770 |
| Std Dev % | 5.4290 | 2.2539 | 3.2899 | 4.4751 | 7.5927 | 3.4907 |
| Win Rate % | 40.0000 | 60.0000 | 60.0000 | 60.0000 | 40.0000 | 52.3965 |

### Significance Tests

- **Post+1d vs Non-Event**: t=0.2433, p=0.807814 (Not significant)
- **Post+3d vs Non-Event**: t=-1.4220, p=0.155108 (Not significant)
- **Pre-1d vs Non-Event**: t=-0.0698, p=0.944376 (Not significant)
- **Pre-Event vs Post-Event**: t=-0.1953, p=0.850060 (Not significant)
- **Volatility ratio (event/non-event):** 0.94x

---

## Crash_Events Events

| Metric | Pre-Event (-3d) | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |
|--------|----------------|----------------|-----------|------------------|--------------------|-----------|
| Avg Return % | -21.6086 | -1.7579 | -17.9970 | 2.5479 | -0.5818 | 0.1937 |
| Std Dev % | 9.4219 | 1.4686 | 11.1541 | 10.3962 | 6.2390 | 3.4306 |
| Win Rate % | 0.0000 | 25.0000 | 0.0000 | 75.0000 | 50.0000 | 52.4544 |

### Significance Tests

- **Post+1d vs Non-Event**: t=1.3663, p=0.171925 (Not significant)
- **Post+3d vs Non-Event**: t=-0.4513, p=0.651792 (Not significant)
- **Pre-1d vs Non-Event**: t=-1.1374, p=0.255434 (Not significant)
- **Pre-Event vs Post-Event**: t=-0.7103, p=0.504171 (Not significant)
- **Volatility ratio (event/non-event):** 3.25x

---

## Summary

| Event Period | N Events | Avg Ret% | WR% | Binom P | Significant? |
|-------------|----------|----------|-----|---------|--------------|
| NFP Post+3d | 141 | 0.8375 | 63.83 | 0.00129 | YES |
| FOMC Post+1d | 94 | -0.9462 | 36.17 | 0.009548 | YES |

## Conclusion

- 2 potential macro event edges identified
  - NFP Post+3d: WR=63.83%, p=0.00129
  - FOMC Post+1d: WR=36.17%, p=0.009548
- Note: CPI and FOMC dates are approximate; precise economic calendar data would improve accuracy

---
*Generated by research/bitcoin/scripts/btc_004_macro_events.py*