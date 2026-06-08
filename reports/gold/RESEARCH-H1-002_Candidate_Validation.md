# RESEARCH-H1-002: H1 Candidate Validation

**Date:** 2026-06-08 17:59
**Instrument:** XAU/USD (GC=F)
**Data:** H1 (hourly), 11,395 bars
**Period:** 2024-06-09 23:00 to 2026-06-08 10:00 UTC
**Trading Days:** 611
**Data Source:** Yahoo Finance (yfinance)

> **Data Limitation:** Yahoo Finance restricts H1 data to the last 730 days.
> This analysis covers ~2 years (June 2024 – June 2026). The user requested
> 2018–present (5+ years). Only 2024–2026 is available from free sources.
> Results should be interpreted with this limitation in mind.

## 1. Candidate Retests

| Candidate | N | Mean% | WR% | Sharpe | PF | P-value | MC p-val |
|-----------|----|-------|-----|--------|----|---------|----------|
| Hour 20 UTC | 493 | 0.0274 | 54.8 | 8.9493 | 1.4941 | 1.0915e-02 | | 1.0000 |
| Hour 23 UTC | 490 | 0.0379 | 54.7 | 8.8744 | 1.5917 | 1.1852e-02 | | 0.8562 |
| Hour 08 UTC | 496 | 0.0192 | 58.5 | 5.9997 | 1.2534 | 8.6392e-02 | | 0.9684 |
| Low Vol Regime | 3,756 | 0.0106 | 52.4 | 4.3144 | 1.1782 | 6.8089e-04 | | 0.9288 |
| ORB London Short | 365 | — | — | — | — | — | — |

## 2. Stability Analysis

### Hour 20 UTC

Full sample: N=493, WR=54.8%, PF=1.4941, Sharpe=8.9493, p=1.0915e-02

| Period | N | Mean% | WR% | PF | Sharpe | P-value |
|--------|----|-------|-----|----|--------|---------|
| Early Period (2024-06-09 to 2025-02-03) | 161 | 0.0097 | 55.9 | 1.2812 | 6.8659 | 2.6430e-01 |
| Middle Period (2025-02-04 to 2025-10-05) | 167 | 0.0267 | 55.7 | 1.6432 | 12.2366 | 4.3609e-02 |
| Late Period (2025-10-06 to 2026-06-08) | 165 | 0.0453 | 52.7 | 1.5044 | 9.8394 | 1.0604e-01 |

**Stability score:** 0.77 (1.0 = perfect consistency, lower = erratic)

---

### Hour 23 UTC

Full sample: N=490, WR=54.7%, PF=1.5917, Sharpe=8.8744, p=1.1852e-02

| Period | N | Mean% | WR% | PF | Sharpe | P-value |
|--------|----|-------|-----|----|--------|---------|
| Early Period (2024-06-09 to 2025-02-03) | 162 | 0.0018 | 53.7 | 1.0597 | 1.3756 | 8.2216e-01 |
| Middle Period (2025-02-04 to 2025-10-05) | 166 | 0.0098 | 53.0 | 1.1847 | 4.4198 | 4.6507e-01 |
| Late Period (2025-10-06 to 2026-06-08) | 162 | 0.1029 | 57.4 | 1.9402 | 14.8991 | 1.5838e-02 |

**Stability score:** 0.16 (1.0 = perfect consistency, lower = erratic)

---

### Hour 08 UTC

Full sample: N=496, WR=58.5%, PF=1.2534, Sharpe=5.9997, p=8.6392e-02

| Period | N | Mean% | WR% | PF | Sharpe | P-value |
|--------|----|-------|-----|----|--------|---------|
| Early Period (2024-06-09 to 2025-02-03) | 161 | 0.0363 | 61.5 | 1.8108 | 15.0535 | 1.5115e-02 |
| Middle Period (2025-02-04 to 2025-10-05) | 170 | 0.0251 | 59.4 | 1.3657 | 9.0467 | 1.3120e-01 |
| Late Period (2025-10-06 to 2026-06-08) | 165 | -0.0037 | 54.5 | 0.9669 | -0.9056 | 8.8127e-01 |

**Stability score:** 0.15 (1.0 = perfect consistency, lower = erratic)

---

### Low Vol Regime

Full sample: N=3,756, WR=52.4%, PF=1.1782, Sharpe=4.3144, p=6.8089e-04

| Period | N | Mean% | WR% | PF | Sharpe | P-value |
|--------|----|-------|-----|----|--------|---------|
| Early Period (2024-06-09 to 2025-02-03) | 2,124 | 0.0104 | 53.1 | 1.1850 | 4.4282 | 8.7480e-03 |
| Middle Period (2025-02-04 to 2025-10-05) | 1,384 | 0.0084 | 50.8 | 1.1341 | 3.3922 | 1.0488e-01 |
| Late Period (2025-10-06 to 2026-06-08) | 248 | 0.0249 | 55.2 | 1.3484 | 7.7543 | 1.1764e-01 |

**Stability score:** 0.64 (1.0 = perfect consistency, lower = erratic)

---

### ORB London Short (1h)

Full sample: N=365 signals

| Period | N | Mean% | WR% | PF | Sharpe | P-value |
|--------|----|-------|-----|----|--------|---------|
| Early Period (2024-06-09 to 2025-02-03) | 111 | -0.0005 | 32.4 | 0.5559 | -15.5566 | 3.8195e-02 |
| Middle Period (2025-02-04 to 2025-10-05) | 122 | 0.0001 | 42.6 | 1.1372 | 3.5357 | 6.1791e-01 |
| Late Period (2025-10-06 to 2026-06-08) | 132 | -0.0002 | 37.9 | 0.8544 | -4.2271 | 5.3495e-01 |

## 3. Monte Carlo Simulation

Method: Shuffle return labels 10,000 times to estimate probability that observed results occur by chance alone.

### Hour 20 UTC

| Metric | Actual | MC Mean | MC 95th | MC p-value | Significant? |
|--------|--------|---------|---------|------------|--------------|
| Mean Ret% | 0.0274 | 0.0274 | 0.0274 | 1.0000 | no |
| Win Rate% | 54.8 | 54.8 | 54.8 | 1.0000 | no |
| Sharpe | 8.9584 | 8.9584 | 8.9584 | 0.9984 | no |
| T-stat | 2.5551 | 2.5551 | 2.5551 | 1.0000 | no |

### Hour 23 UTC

| Metric | Actual | MC Mean | MC 95th | MC p-value | Significant? |
|--------|--------|---------|---------|------------|--------------|
| Mean Ret% | 0.0379 | 0.0379 | 0.0379 | 1.0000 | no |
| Win Rate% | 54.7 | 54.7 | 54.7 | 1.0000 | no |
| Sharpe | 8.8834 | 8.8834 | 8.8834 | 1.0000 | no |
| T-stat | 2.5260 | 2.5260 | 2.5260 | 0.8525 | no |

### Hour 08 UTC

| Metric | Actual | MC Mean | MC 95th | MC p-value | Significant? |
|--------|--------|---------|---------|------------|--------------|
| Mean Ret% | 0.0192 | 0.0192 | 0.0192 | 1.0000 | no |
| Win Rate% | 58.5 | 58.5 | 58.5 | 1.0000 | no |
| Sharpe | 6.0058 | 6.0058 | 6.0058 | 0.9665 | no |
| T-stat | 1.7182 | 1.7182 | 1.7182 | 0.9665 | no |

### Low Vol Regime

| Metric | Actual | MC Mean | MC 95th | MC p-value | Significant? |
|--------|--------|---------|---------|------------|--------------|
| Mean Ret% | 0.0106 | 0.0106 | 0.0106 | 1.0000 | no |
| Win Rate% | 52.4 | 52.4 | 52.4 | 1.0000 | no |
| Sharpe | 4.3150 | 4.3150 | 4.3150 | 1.0000 | no |
| T-stat | 3.4000 | 3.4000 | 3.4000 | 0.9294 | no |

### ORB London Short

| Metric | Actual | MC Mean | MC 95th | MC p-value | Significant? |
|--------|--------|---------|---------|------------|--------------|
| Mean Ret% | -0.0195 | -0.0195 | -0.0195 | 0.5328 | no |
| Win Rate% | 37.8 | 37.8 | 37.8 | 1.0000 | no |
| Sharpe | -4.6045 | -4.6045 | -4.6045 | 0.5328 | no |
| T-stat | -1.1296 | -1.1296 | -1.1296 | 0.3538 | no |

## 4. Final Verdict

### Hour 20 UTC
- **Full sample:** N=493, WR=54.8%, PF=1.4941, Sharpe=8.9493, p=1.0915e-02
- **MC validation:** FAILS randomization test (p=1.0000)
- **Issues:** Sample N=493 < 500; MC p=1.0000 >= 0.05 (not distinguishable from noise)
- **Verdict: REJECTED - NOT A VALID EDGE

### Hour 23 UTC
- **Full sample:** N=490, WR=54.7%, PF=1.5917, Sharpe=8.8744, p=1.1852e-02
- **MC validation:** FAILS randomization test (p=0.8439)
- **Issues:** Sample N=490 < 500; MC p=0.8439 >= 0.05 (not distinguishable from noise)
- **Verdict: REJECTED - NOT A VALID EDGE

### Hour 08 UTC
- **Full sample:** N=496, WR=58.5%, PF=1.2534, Sharpe=5.9997, p=8.6392e-02
- **MC validation:** FAILS randomization test (p=0.9682)
- **Issues:** Sample N=496 < 500; p=0.0864 >= 0.05; PF=1.2534 < 1.30; MC p=0.9682 >= 0.05 (not distinguishable from noise)
- **Verdict: REJECTED - NOT A VALID EDGE

### Low Vol Regime
- **Full sample:** N=3,756, WR=52.4%, PF=1.1782, Sharpe=4.3144, p=6.8089e-04
- **MC validation:** FAILS randomization test (p=0.9295)
- **Issues:** PF=1.1782 < 1.30; MC p=0.9295 >= 0.05 (not distinguishable from noise)
- **Verdict: REJECTED - NOT A VALID EDGE

### ORB London Short
- **Full sample:** N=365, WR=37.8%, PF=0.8417, Sharpe=-4.5982, p=2.5939e-01
- **MC validation:** FAILS randomization test (p=0.3496)
- **Issues:** Sample N=365 < 500; p=0.2594 >= 0.05; PF=0.8417 < 1.30; Sharpe=-4.5982 < 1.0; MC p=0.3496 >= 0.05 (not distinguishable from noise)
- **Verdict: REJECTED - NOT A VALID EDGE

## 5. Summary

- **Hour 20 UTC**: REJECTED (full criteria, MC test). MC p=1.0000. ❌
- **Hour 23 UTC**: REJECTED (full criteria, MC test). MC p=0.8443. ❌
- **Hour 08 UTC**: REJECTED (full criteria, MC test). MC p=0.9699. ❌
- **Low Vol Regime**: REJECTED (full criteria, MC test). MC p=0.9246. ❌
- **ORB London Short**: REJECTED (full criteria, MC test). MC p=0.3532. ❌

**No H1 intraday edge survives all validation tests.**

All 5 near-misses from RESEARCH-H1-001 are confirmed as statistical noise
when subjected to Monte Carlo permutation testing and stability analysis.
The 2-year sample is insufficient to distinguish these patterns from random chance.

---
*Generated automatically by XAU/USD Edge Discovery Framework*