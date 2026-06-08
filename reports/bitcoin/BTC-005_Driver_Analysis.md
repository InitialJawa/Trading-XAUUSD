# BTC-005: Cross-Asset Driver Analysis

**Date:** 2026-06-09 00:18
**Period:** 2014-09-18 to 2026-06-05
**Aligned Observations:** 2,944
**Drivers:** DXY, SP500, VIX, VIX_Chg, US10Y, US10Y_Chg, GLD, IEF

## TEST 1: Contemporaneous Return Correlation

### Daily

| Driver | Correlation | R² | P-value |
|--------|-------------|-----|---------|
| DXY | +0.0096 | 0.0001 | 6.0434e-01 |
| SP500 | +0.0286 | 0.0008 | 1.2078e-01 |
| VIX | +0.0306 | 0.0009 | 9.7305e-02 |
| VIX_Chg | +0.0253 | 0.0006 | 1.6958e-01 |
| US10Y | -0.0353 | 0.0012 | 5.5264e-02 |
| US10Y_Chg | -0.0038 | 0.0000 | 8.3488e-01 |
| GLD | +0.0954 | 0.0091 | 2.1568e-07 |
| IEF | -0.0022 | 0.0000 | 9.0295e-01 |

**Strongest: GLD (r=+0.0954)**

### Weekly

| Driver | Correlation | R² | P-value |
|--------|-------------|-----|---------|

## TEST 2: Lead-Lag Analysis

### DXY

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0017 | DXY leads 20d |
| -10 | -0.0247 | DXY leads 10d |
|  -5 | -0.0098 | DXY leads 5d |
|  -2 | +0.0137 | DXY leads 2d |
|  -1 | -0.0015 | DXY leads 1d |
|  +0 | +0.0096 | Same day |
|  +1 | -0.0841* | BTC leads 1d |
|  +2 | -0.0230 | BTC leads 2d |
|  +5 | -0.0259 | BTC leads 5d |
| +10 | -0.0105 | BTC leads 10d |
| +20 | -0.0049 | BTC leads 20d |

**Best: lag=1, r=-0.0841**

### SP500

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | -0.0137 | SP500 leads 20d |
| -10 | +0.0037 | SP500 leads 10d |
|  -5 | -0.0185 | SP500 leads 5d |
|  -2 | -0.0004 | SP500 leads 2d |
|  -1 | +0.0076 | SP500 leads 1d |
|  +0 | +0.0286 | Same day |
|  +1 | +0.1855* | BTC leads 1d |
|  +2 | +0.0169 | BTC leads 2d |
|  +5 | +0.0207 | BTC leads 5d |
| +10 | +0.0021 | BTC leads 10d |
| +20 | -0.0127 | BTC leads 20d |

**Best: lag=1, r=+0.1855**

### VIX

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0135 | VIX leads 20d |
| -10 | +0.0197 | VIX leads 10d |
|  -5 | +0.0278 | VIX leads 5d |
|  -2 | +0.0380* | VIX leads 2d |
|  -1 | +0.0228 | VIX leads 1d |
|  +0 | +0.0306 | Same day |
|  +1 | -0.0281 | BTC leads 1d |
|  +2 | -0.0216 | BTC leads 2d |
|  +5 | -0.0325 | BTC leads 5d |
| +10 | -0.0354 | BTC leads 10d |
| +20 | -0.0344 | BTC leads 20d |

**Best: lag=-2, r=+0.0380**

### VIX_Chg

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0079 | VIX_Chg leads 20d |
| -10 | -0.0012 | VIX_Chg leads 10d |
|  -5 | +0.0251 | VIX_Chg leads 5d |
|  -2 | +0.0427* | VIX_Chg leads 2d |
|  -1 | -0.0548* | VIX_Chg leads 1d |
|  +0 | +0.0253 | Same day |
|  +1 | -0.2044* | BTC leads 1d |
|  +2 | +0.0225 | BTC leads 2d |
|  +5 | -0.0263 | BTC leads 5d |
| +10 | -0.0150 | BTC leads 10d |
| +20 | +0.0219 | BTC leads 20d |

**Best: lag=1, r=-0.2044**

### US10Y

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | -0.0325 | US10Y leads 20d |
| -10 | -0.0358 | US10Y leads 10d |
|  -5 | -0.0328 | US10Y leads 5d |
|  -2 | -0.0343 | US10Y leads 2d |
|  -1 | -0.0352 | US10Y leads 1d |
|  +0 | -0.0353 | Same day |
|  +1 | -0.0345 | BTC leads 1d |
|  +2 | -0.0328 | BTC leads 2d |
|  +5 | -0.0303 | BTC leads 5d |
| +10 | -0.0258 | BTC leads 10d |
| +20 | -0.0268 | BTC leads 20d |

**Best: lag=-10, r=-0.0358**

### US10Y_Chg

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0051 | US10Y_Chg leads 20d |
| -10 | -0.0338 | US10Y_Chg leads 10d |
|  -5 | +0.0075 | US10Y_Chg leads 5d |
|  -2 | -0.0189 | US10Y_Chg leads 2d |
|  -1 | -0.0219 | US10Y_Chg leads 1d |
|  +0 | -0.0038 | Same day |
|  +1 | +0.0039 | BTC leads 1d |
|  +2 | +0.0343 | BTC leads 2d |
|  +5 | +0.0172 | BTC leads 5d |
| +10 | +0.0153 | BTC leads 10d |
| +20 | +0.0074 | BTC leads 20d |

**Best: lag=2, r=+0.0343**

### GLD

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | -0.0074 | GLD leads 20d |
| -10 | +0.0110 | GLD leads 10d |
|  -5 | -0.0320 | GLD leads 5d |
|  -2 | +0.0032 | GLD leads 2d |
|  -1 | -0.0071 | GLD leads 1d |
|  +0 | +0.0954* | Same day |
|  +1 | +0.0105 | BTC leads 1d |
|  +2 | -0.0109 | BTC leads 2d |
|  +5 | +0.0301 | BTC leads 5d |
| +10 | -0.0263 | BTC leads 10d |
| +20 | -0.0119 | BTC leads 20d |

**Best: lag=0, r=+0.0954**

### IEF

| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | -0.0075 | IEF leads 20d |
| -10 | +0.0353 | IEF leads 10d |
|  -5 | -0.0077 | IEF leads 5d |
|  -2 | +0.0117 | IEF leads 2d |
|  -1 | +0.0337 | IEF leads 1d |
|  +0 | -0.0022 | Same day |
|  +1 | -0.0025 | BTC leads 1d |
|  +2 | -0.0445* | BTC leads 2d |
|  +5 | -0.0027 | BTC leads 5d |
| +10 | -0.0129 | BTC leads 10d |
| +20 | -0.0014 | BTC leads 20d |

**Best: lag=2, r=-0.0445**

## TEST 3: Predictive Power (Univariate)

### 1-Day

| Driver | R² | Correlation | P-value | Sig? |
|--------|-----|-------------|---------|------|
| DXY | 0.000002 | -0.0015 | 9.3316e-01 | no |
| SP500 | 0.000058 | +0.0076 | 6.7929e-01 | no |
| VIX | 0.000520 | +0.0228 | 2.1635e-01 | no |
| VIX_Chg | 0.003008 | -0.0548 | 2.9174e-03 | YES |
| US10Y | 0.001242 | -0.0352 | 5.5931e-02 | no |
| US10Y_Chg | 0.000480 | -0.0219 | 2.3459e-01 | no |
| GLD | 0.000051 | -0.0071 | 6.9864e-01 | no |
| IEF | 0.001137 | +0.0337 | 6.7434e-02 | no |

**Significant at 1-Day:**
- VIX_Chg: r=-0.0548, p=2.9174e-03

### 5-Day

| Driver | R² | Correlation | P-value | Sig? |
|--------|-----|-------------|---------|------|
| DXY | 0.000096 | -0.0098 | 5.9623e-01 | no |
| SP500 | 0.000343 | -0.0185 | 3.1535e-01 | no |
| VIX | 0.000775 | +0.0278 | 1.3127e-01 | no |
| VIX_Chg | 0.000632 | +0.0251 | 1.7318e-01 | no |
| US10Y | 0.001077 | -0.0328 | 7.5215e-02 | no |
| US10Y_Chg | 0.000056 | +0.0075 | 6.8508e-01 | no |
| GLD | 0.001024 | -0.0320 | 8.2768e-02 | no |
| IEF | 0.000060 | -0.0077 | 6.7467e-01 | no |

### 20-Day

| Driver | R² | Correlation | P-value | Sig? |
|--------|-----|-------------|---------|------|
| DXY | 0.000003 | +0.0017 | 9.2859e-01 | no |
| SP500 | 0.000187 | -0.0137 | 4.5970e-01 | no |
| VIX | 0.000183 | +0.0135 | 4.6430e-01 | no |
| VIX_Chg | 0.000063 | +0.0079 | 6.6789e-01 | no |
| US10Y | 0.001059 | -0.0325 | 7.8480e-02 | no |
| US10Y_Chg | 0.000026 | +0.0051 | 7.8403e-01 | no |
| GLD | 0.000055 | -0.0074 | 6.8848e-01 | no |
| IEF | 0.000056 | -0.0075 | 6.8573e-01 | no |

## TEST 4: Conditional Returns After Extreme Driver Moves

### DXY — Top 10% increase (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.2014 | 53.2% | 4.3304e-01 | NO |
| 5d | 0.2360 | 53.6% | 2.5304e-01 | NO |
| 20d | 0.2849 | 52.9% | 2.0456e-01 | NO |

### DXY — Top 10% decrease (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.1345 | 53.6% | 5.2632e-01 | NO |
| 5d | 0.1468 | 54.2% | 4.8250e-01 | NO |
| 20d | 0.2829 | 53.6% | 1.5269e-01 | NO |

### SP500 — Top 10% increase (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.4417 | 55.3% | 2.6230e-02 | YES |
| 5d | 0.2716 | 50.5% | 1.5204e-01 | NO |
| 20d | 0.1642 | 52.9% | 4.3687e-01 | NO |

### SP500 — Top 10% decrease (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.3763 | 54.9% | 1.0321e-01 | NO |
| 5d | 0.2606 | 49.0% | 3.0035e-01 | NO |
| 20d | 0.1995 | 48.3% | 3.7483e-01 | NO |

### VIX — Top 10% increase (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.6953 | 56.9% | 6.1478e-03 | YES |
| 5d | 0.4988 | 53.9% | 4.7093e-02 | YES |
| 20d | 0.5143 | 54.6% | 1.2715e-02 | YES |

### VIX — Top 10% decrease (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.7955 | 60.7% | 9.1005e-03 | YES |
| 5d | 0.7233 | 59.0% | 1.9613e-02 | YES |
| 20d | 0.5317 | 57.6% | 9.3388e-02 | NO |

### VIX_Chg — Top 10% increase (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0267 | 52.9% | 9.1908e-01 | NO |
| 5d | 0.4177 | 53.6% | 6.6892e-02 | NO |
| 20d | 0.5163 | 53.6% | 2.3891e-02 | YES |

### VIX_Chg — Top 10% decrease (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.7459 | 55.6% | 4.9496e-04 | YES |
| 5d | 0.1631 | 52.5% | 4.3800e-01 | NO |
| 20d | 0.0863 | 51.2% | 6.7848e-01 | NO |

### US10Y — Top 10% increase (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0944 | 48.6% | 5.3090e-01 | NO |
| 5d | 0.2049 | 49.3% | 1.9178e-01 | NO |
| 20d | 0.2483 | 51.6% | 1.2142e-01 | NO |

### US10Y — Top 10% decrease (294 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.8710 | 58.8% | 1.0356e-03 | YES |
| 5d | 0.7490 | 58.5% | 5.4947e-03 | YES |
| 20d | 0.8763 | 59.2% | 1.3295e-04 | YES |

### US10Y_Chg — Top 10% increase (292 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0806 | 50.0% | 7.4098e-01 | NO |
| 5d | -0.0031 | 48.6% | 9.8807e-01 | NO |
| 20d | 0.2117 | 49.1% | 2.5335e-01 | NO |

### US10Y_Chg — Top 10% decrease (289 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.1867 | 50.5% | 3.6557e-01 | NO |
| 5d | 0.2696 | 52.9% | 2.6828e-01 | NO |
| 20d | -0.0370 | 49.1% | 8.6446e-01 | NO |

### GLD — Top 10% increase (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0906 | 50.2% | 6.8078e-01 | NO |
| 5d | 0.1490 | 51.9% | 5.0636e-01 | NO |
| 20d | 0.0625 | 49.7% | 7.3835e-01 | NO |

### GLD — Top 10% decrease (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0176 | 53.4% | 9.3329e-01 | NO |
| 5d | 0.3949 | 53.6% | 6.4342e-02 | NO |
| 20d | -0.0535 | 47.2% | 8.0469e-01 | NO |

### IEF — Top 10% increase (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.1879 | 50.5% | 3.5421e-01 | NO |
| 5d | 0.1668 | 51.5% | 4.7553e-01 | NO |
| 20d | 0.1013 | 49.3% | 6.4499e-01 | NO |

### IEF — Top 10% decrease (295 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0903 | 49.3% | 6.9617e-01 | NO |
| 5d | 0.1503 | 53.4% | 4.5722e-01 | NO |
| 20d | 0.2481 | 49.8% | 1.8969e-01 | NO |

## TEST 5: Regime Dependence

### Bull BTC (>200d MA)  (N=1,313)

| Driver | Correlation (Regime) | Correlation (Full) | Difference |
|--------|---------------------|--------------------|------------|
| DXY | -0.0246 | +0.0096 | -0.0342 |
| SP500 | -0.0340 | +0.0286 | -0.0626 |
| VIX | +0.0734 | +0.0306 | +0.0428 |
| VIX_Chg | +0.0490 | +0.0253 | +0.0236 |
| US10Y | -0.1463 | -0.0353 | -0.1110 |
| US10Y_Chg | -0.0548 | -0.0038 | -0.0509 |
| GLD | +0.0239 | +0.0954 | -0.0714 |
| IEF | +0.0372 | -0.0022 | +0.0394 |

### Bear BTC (<200d MA)  (N=1,380)

| Driver | Correlation (Regime) | Correlation (Full) | Difference |
|--------|---------------------|--------------------|------------|
| DXY | +0.0252 | +0.0096 | +0.0156 |
| SP500 | +0.1502 | +0.0286 | +0.1216 |
| VIX | -0.0533 | +0.0306 | -0.0839 |
| VIX_Chg | -0.1045 | +0.0253 | -0.1298 |
| US10Y | +0.0544 | -0.0353 | +0.0897 |
| US10Y_Chg | +0.0293 | -0.0038 | +0.0332 |
| GLD | +0.0384 | +0.0954 | -0.0570 |
| IEF | -0.0331 | -0.0022 | -0.0308 |

## TEST 6: Multivariate Models (Walk-Forward)

### 1-Day

| Metric | Linear Reg | Random Forest | Baseline |
|--------|-----------|---------------|----------|
| OOS R² | -0.0128 | -0.0731 | 0.0 |
| OOS MAE | 0.024997 | 0.025172 | 0.024856 |
| Dir Acc | 51.1% | 53.1% | 50.8% |
| Samples | 648 | 648 | 648 |

**Verdict: NO predictive ability**

### 5-Day

| Metric | Linear Reg | Random Forest | Baseline |
|--------|-----------|---------------|----------|
| OOS R² | 0.0090 | -0.0141 | 0.0 |
| OOS MAE | 0.025332 | 0.025621 | 0.025183 |
| Dir Acc | 51.9% | 52.1% | 48.2% |
| Samples | 647 | 647 | 647 |

**Verdict: MARGINAL**

## Driver Ranking Summary

| Rank | Driver | Avg |r| | Best Lag | 1d R² | 5d R² | 20d R² | Cond Edge? |
|------|--------|---------|----------|--------|-------|--------|------------|
| 1 | GLD | 0.095 | — | 0.0001 | 0.0010 | 0.0001 | no |
| 2 | US10Y | 0.035 | — | 0.0012 | 0.0011 | 0.0011 | YES |
| 3 | VIX | 0.031 | — | 0.0005 | 0.0008 | 0.0002 | YES |
| 4 | SP500 | 0.029 | — | 0.0001 | 0.0003 | 0.0002 | YES |
| 5 | VIX_Chg | 0.025 | — | 0.0030 | 0.0006 | 0.0001 | YES |
| 6 | DXY | 0.010 | — | 0.0000 | 0.0001 | 0.0000 | no |
| 7 | US10Y_Chg | 0.004 | — | 0.0005 | 0.0001 | 0.0000 | no |
| 8 | IEF | 0.002 | — | 0.0011 | 0.0001 | 0.0001 | no |

---
*Generated by research/bitcoin/scripts/btc_005_driver_analysis.py*