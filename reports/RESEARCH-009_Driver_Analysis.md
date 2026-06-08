# RESEARCH-009: Cross-Asset Driver Analysis

**Date:** 2026-06-08 17:32
**Period:** 2002-07-31 to 2026-06-05
**Aligned Observations:** 5,978
**Drivers:** DXY, US10Y, US10Y_chg, SP500, VIX, Crude Oil, Silver, TLT_ret

## TEST 1: Contemporaneous Return Correlation

### Daily

| Driver | Correlation | R² | P-value |
|--------|-------------|-----|---------|
| DXY | -0.3325 | 0.1106 | 2.7123e-154 |
| US10Y | -0.0261 | 0.0007 | 4.3944e-02 |
| US10Y_chg | -0.0183 | 0.0003 | 1.5822e-01 |
| SP500 | +0.0303 | 0.0009 | 1.8986e-02 |
| VIX | -0.0358 | 0.0013 | 5.6547e-03 |
| Crude Oil | +0.0420 | 0.0018 | 1.1576e-03 |
| Silver | +0.2316 | 0.0537 | 1.2255e-73 |
| TLT_ret | +0.0829 | 0.0069 | 1.3625e-10 |

**Strongest: DXY (r=-0.3325)**

### Weekly

| Driver | Correlation | R² | P-value |
|--------|-------------|-----|---------|

### Monthly

| Driver | Correlation | R² | P-value |
|--------|-------------|-----|---------|
| DXY | -0.0328 | 0.0011 | 6.4472e-01 |
| US10Y | -0.0050 | 0.0000 | 9.4400e-01 |
| US10Y_chg | +0.0398 | 0.0016 | 5.7577e-01 |
| SP500 | -0.1190 | 0.0142 | 9.3147e-02 |
| VIX | +0.0870 | 0.0076 | 2.2058e-01 |
| Crude Oil | +0.1279 | 0.0164 | 7.1110e-02 |
| Silver | -0.0474 | 0.0022 | 5.0542e-01 |
| TLT_ret | +0.0619 | 0.0038 | 3.8383e-01 |

**Strongest: Crude Oil (r=+0.1279)**

## TEST 2: Lead-Lag Analysis

### DXY
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0175 | DXY leads 20d |
| -10 | +0.0030 | DXY leads 10d |
|  -5 | +0.0074 | DXY leads 5d |
|  -2 | +0.0183 | DXY leads 2d |
|  -1 | -0.0226 | DXY leads 1d |
|  +0 | -0.3325* | Same day |
|  +1 | -0.0946* | Gold leads 1d |
|  +2 | -0.0314* | Gold leads 2d |
|  +5 | -0.0170 | Gold leads 5d |
| +10 | +0.0046 | Gold leads 10d |
| +20 | +0.0065 | Gold leads 20d |

**Best: lag=0, r=-0.3325**

### US10Y
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0141 | US10Y leads 20d |
| -10 | -0.0113 | US10Y leads 10d |
|  -5 | +0.0034 | US10Y leads 5d |
|  -2 | -0.0408* | US10Y leads 2d |
|  -1 | -0.1487* | US10Y leads 1d |
|  +0 | -0.0261* | Same day |
|  +1 | +0.0090 | Gold leads 1d |
|  +2 | +0.0180 | Gold leads 2d |
|  +5 | +0.0050 | Gold leads 5d |
| +10 | +0.0152 | Gold leads 10d |
| +20 | -0.0083 | Gold leads 20d |

**Best: lag=-1, r=-0.1487**

### US10Y_chg
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0133 | US10Y_chg leads 20d |
| -10 | -0.0207 | US10Y_chg leads 10d |
|  -5 | -0.0050 | US10Y_chg leads 5d |
|  -2 | -0.0176 | US10Y_chg leads 2d |
|  -1 | -0.1608* | US10Y_chg leads 1d |
|  +0 | -0.0183 | Same day |
|  +1 | +0.0105 | Gold leads 1d |
|  +2 | +0.0222 | Gold leads 2d |
|  +5 | +0.0172 | Gold leads 5d |
| +10 | +0.0046 | Gold leads 10d |
| +20 | -0.0084 | Gold leads 20d |

**Best: lag=-1, r=-0.1608**

### SP500
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | -0.0048 | SP500 leads 20d |
| -10 | -0.0019 | SP500 leads 10d |
|  -5 | +0.0196 | SP500 leads 5d |
|  -2 | -0.0113 | SP500 leads 2d |
|  -1 | +0.0252 | SP500 leads 1d |
|  +0 | +0.0303* | Same day |
|  +1 | +0.0050 | Gold leads 1d |
|  +2 | +0.0456* | Gold leads 2d |
|  +5 | +0.0001 | Gold leads 5d |
| +10 | +0.0146 | Gold leads 10d |
| +20 | -0.0321* | Gold leads 20d |

**Best: lag=2, r=+0.0456**

### VIX
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0024 | VIX leads 20d |
| -10 | -0.0243 | VIX leads 10d |
|  -5 | -0.0086 | VIX leads 5d |
|  -2 | -0.0188 | VIX leads 2d |
|  -1 | -0.0107 | VIX leads 1d |
|  +0 | -0.0358* | Same day |
|  +1 | -0.0012 | Gold leads 1d |
|  +2 | +0.0065 | Gold leads 2d |
|  +5 | +0.0152 | Gold leads 5d |
| +10 | -0.0044 | Gold leads 10d |
| +20 | +0.0053 | Gold leads 20d |

**Best: lag=0, r=-0.0358**

### Crude Oil
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | -0.0103 | Crude Oil leads 20d |
| -10 | -0.0155 | Crude Oil leads 10d |
|  -5 | -0.0050 | Crude Oil leads 5d |
|  -2 | -0.0141 | Crude Oil leads 2d |
|  -1 | +0.0652* | Crude Oil leads 1d |
|  +0 | +0.0420* | Same day |
|  +1 | +0.0241 | Gold leads 1d |
|  +2 | +0.0062 | Gold leads 2d |
|  +5 | -0.0382* | Gold leads 5d |
| +10 | -0.0258* | Gold leads 10d |
| +20 | -0.0016 | Gold leads 20d |

**Best: lag=-1, r=+0.0652**

### Silver
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | +0.0077 | Silver leads 20d |
| -10 | +0.0304* | Silver leads 10d |
|  -5 | +0.0008 | Silver leads 5d |
|  -2 | -0.0194 | Silver leads 2d |
|  -1 | +0.5301* | Silver leads 1d |
|  +0 | +0.2316* | Same day |
|  +1 | -0.0070 | Gold leads 1d |
|  +2 | +0.0085 | Gold leads 2d |
|  +5 | -0.0219 | Gold leads 5d |
| +10 | +0.0056 | Gold leads 10d |
| +20 | +0.0068 | Gold leads 20d |

**Best: lag=-1, r=+0.5301**

### TLT_ret
| Lag | Cross-Corr | Interpretation |
|-----|------------|----------------|
| -20 | -0.0137 | TLT_ret leads 20d |
| -10 | +0.0239 | TLT_ret leads 10d |
|  -5 | -0.0048 | TLT_ret leads 5d |
|  -2 | +0.0068 | TLT_ret leads 2d |
|  -1 | +0.0803* | TLT_ret leads 1d |
|  +0 | +0.0829* | Same day |
|  +1 | -0.0043 | Gold leads 1d |
|  +2 | -0.0045 | Gold leads 2d |
|  +5 | -0.0038 | Gold leads 5d |
| +10 | -0.0144 | Gold leads 10d |
| +20 | -0.0168 | Gold leads 20d |

**Best: lag=0, r=+0.0829**


## TEST 3: Predictive Power (Univariate)

### 1-Day
| Driver | R² | Correlation | P-value | Sig? |
|--------|-----|-------------|---------|------|
| DXY | 0.000511 | -0.0226 | 8.0497e-02 | no |
| US10Y | 0.022114 | -0.1487 | 6.5915e-31 | YES |
| US10Y_chg | 0.025873 | -0.1609 | 6.1386e-36 | YES |
| SP500 | 0.000637 | +0.0252 | 5.1074e-02 | no |
| VIX | 0.000111 | -0.0105 | 4.1490e-01 | no |
| Crude Oil | 0.004289 | +0.0655 | 4.0267e-07 | YES |
| Silver | 0.282119 | +0.5311 | 0.0000e+00 | YES |
| TLT_ret | 0.006450 | +0.0803 | 5.0326e-10 | YES |

**Significant at 1-Day:**
- Silver: r=+0.5311, p=0.0000e+00
- US10Y_chg: r=-0.1609, p=6.1386e-36
- US10Y: r=-0.1487, p=6.5915e-31
### 5-Day
| Driver | R² | Correlation | P-value | Sig? |
|--------|-----|-------------|---------|------|
| DXY | 0.000059 | +0.0077 | 5.5196e-01 | no |
| US10Y | 0.000011 | +0.0033 | 7.9776e-01 | no |
| US10Y_chg | 0.000026 | -0.0051 | 6.9629e-01 | no |
| SP500 | 0.000387 | +0.0197 | 1.2849e-01 | no |
| VIX | 0.000065 | -0.0081 | 5.3359e-01 | no |
| Crude Oil | 0.000035 | -0.0059 | 6.4710e-01 | no |
| Silver | 0.000001 | +0.0011 | 9.3501e-01 | no |
| TLT_ret | 0.000020 | -0.0045 | 7.2852e-01 | no |
### 20-Day
| Driver | R² | Correlation | P-value | Sig? |
|--------|-----|-------------|---------|------|
| DXY | 0.000370 | +0.0192 | 1.3785e-01 | no |
| US10Y | 0.000137 | +0.0117 | 3.6638e-01 | no |
| US10Y_chg | 0.000081 | +0.0090 | 4.8777e-01 | no |
| SP500 | 0.000036 | -0.0060 | 6.4514e-01 | no |
| VIX | 0.000032 | +0.0056 | 6.6414e-01 | no |
| Crude Oil | 0.000094 | -0.0097 | 4.5366e-01 | no |
| Silver | 0.000056 | +0.0075 | 5.6207e-01 | no |
| TLT_ret | 0.000207 | -0.0144 | 2.6713e-01 | no |

## TEST 4: Conditional Returns After Extreme Driver Moves

### DXY — Top 10% increase (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0067 | 52.7% | 9.1083e-01 | NO |
| 5d | 0.1245 | 52.3% | 3.8814e-02 | YES |
| 20d | 0.1111 | 53.5% | 2.9325e-02 | YES |

### DXY — Top 10% decrease (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0923 | 51.3% | 7.2713e-02 | NO |
| 5d | 0.0942 | 54.2% | 7.7897e-02 | NO |
| 20d | 0.0764 | 52.2% | 1.3752e-01 | NO |

### US10Y — Top 10% increase (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | -0.3457 | 35.3% | 2.0788e-10 | YES |
| 5d | 0.0826 | 54.3% | 9.9659e-02 | NO |
| 20d | 0.0468 | 53.4% | 3.0328e-01 | NO |

### US10Y — Top 10% decrease (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.3884 | 63.9% | 2.5815e-11 | YES |
| 5d | 0.0722 | 52.7% | 1.2920e-01 | NO |
| 20d | -0.0016 | 51.7% | 9.7118e-01 | NO |

### US10Y_chg — Top 10% increase (597 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | -0.2737 | 39.0% | 3.8177e-07 | YES |
| 5d | 0.1036 | 55.4% | 2.9340e-02 | YES |
| 20d | 0.1425 | 57.2% | 2.4523e-03 | YES |

### US10Y_chg — Top 10% decrease (597 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.3707 | 65.3% | 5.4867e-09 | YES |
| 5d | 0.1009 | 53.6% | 5.4548e-02 | NO |
| 20d | 0.0285 | 52.3% | 5.3735e-01 | NO |

### SP500 — Top 10% increase (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.1046 | 50.7% | 7.2565e-02 | NO |
| 5d | 0.0620 | 54.2% | 2.2517e-01 | NO |
| 20d | 0.0897 | 55.4% | 8.9337e-02 | NO |

### SP500 — Top 10% decrease (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0549 | 52.7% | 3.6401e-01 | NO |
| 5d | 0.0511 | 55.3% | 3.7057e-01 | NO |
| 20d | 0.1152 | 55.8% | 3.0440e-02 | YES |

### VIX — Top 10% increase (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0463 | 52.7% | 4.3102e-01 | NO |
| 5d | 0.0177 | 53.3% | 7.4578e-01 | NO |
| 20d | 0.0960 | 54.8% | 6.1805e-02 | NO |

### VIX — Top 10% decrease (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.0043 | 50.3% | 9.4079e-01 | NO |
| 5d | 0.0871 | 54.0% | 8.5004e-02 | NO |
| 20d | 0.0675 | 54.5% | 1.7115e-01 | NO |

### Crude Oil — Top 10% increase (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.3252 | 61.7% | 3.3216e-09 | YES |
| 5d | 0.0021 | 51.3% | 9.6711e-01 | NO |
| 20d | 0.0166 | 55.0% | 7.2177e-01 | NO |

### Crude Oil — Top 10% decrease (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | -0.2376 | 45.0% | 2.2420e-04 | YES |
| 5d | 0.1253 | 55.5% | 3.0287e-02 | YES |
| 20d | 0.0640 | 53.5% | 2.2499e-01 | NO |

### Silver — Top 10% increase (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 1.0795 | 81.8% | 7.2990e-65 | YES |
| 5d | 0.0250 | 52.2% | 6.6803e-01 | NO |
| 20d | 0.1296 | 53.9% | 1.7798e-02 | YES |

### Silver — Top 10% decrease (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | -1.1704 | 18.9% | 2.3174e-57 | YES |
| 5d | 0.0542 | 53.5% | 3.7029e-01 | NO |
| 20d | 0.0893 | 52.9% | 9.0584e-02 | NO |

### TLT_ret — Top 10% increase (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | 0.2234 | 58.9% | 7.2357e-05 | YES |
| 5d | 0.0302 | 52.6% | 5.4130e-01 | NO |
| 20d | -0.0284 | 49.7% | 5.5671e-01 | NO |

### TLT_ret — Top 10% decrease (598 events)

| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |
|---------|-----------|----------|----------|------|
| 1d | -0.1295 | 46.5% | 1.3185e-02 | YES |
| 5d | 0.0823 | 54.0% | 9.1858e-02 | NO |
| 20d | -0.0224 | 51.6% | 6.4392e-01 | NO |


## TEST 5: Regime Dependence

### Bull Gold (>200d MA)  (N=4,400)

| Driver | Correlation | Full Period | Difference |
|--------|-------------|-------------|------------|
| DXY | -0.3087 | -0.3325 | +0.0238 |
| US10Y | -0.0251 | -0.0261 | +0.0010 |
| US10Y_chg | -0.0126 | -0.0183 | +0.0057 |
| SP500 | -0.0072 | +0.0303 | -0.0375 |
| VIX | -0.0181 | -0.0358 | +0.0177 |
| Crude Oil | +0.0454 | +0.0420 | +0.0034 |
| Silver | +0.2373 | +0.2316 | +0.0056 |
| TLT_ret | +0.0890 | +0.0829 | +0.0060 |

### Bear Gold (<200d MA)  (N=1,578)

| Driver | Correlation | Full Period | Difference |
|--------|-------------|-------------|------------|
| DXY | -0.3894 | -0.3325 | -0.0569 |
| US10Y | -0.0344 | -0.0261 | -0.0083 |
| US10Y_chg | -0.0409 | -0.0183 | -0.0226 |
| SP500 | +0.1258 | +0.0303 | +0.0954 |
| VIX | -0.0856 | -0.0358 | -0.0498 |
| Crude Oil | +0.0266 | +0.0420 | -0.0154 |
| Silver | +0.2093 | +0.2316 | -0.0223 |
| TLT_ret | +0.0691 | +0.0829 | -0.0138 |


## TEST 6: Multivariate Models (Walk-Forward)

### 1-Day

| Metric | Linear Reg | Random Forest | Baseline |
|--------|-----------|---------------|----------|
| OOS R² | 0.2294 | 0.1683 | 0.0 |
| OOS MAE | 0.006399 | 0.006661 | 0.007452 |
| Dir Acc | 66.0% | 65.5% | 51.2% |
| Samples | 553 | 553 | 553 |

**Top LR features:** Silver(+0.2858), DXY(+0.0499), SP500(-0.0330)

**Top RF features:** Silver(0.847), US10Y(0.046), US10Y_chg(0.040)

**Verdict: MARGINAL predictive ability**

### 5-Day

| Metric | Linear Reg | Random Forest | Baseline |
|--------|-----------|---------------|----------|
| OOS R² | -0.0112 | -0.0612 | 0.0 |
| OOS MAE | 0.008575 | 0.008738 | 0.008637 |
| Dir Acc | 54.1% | 53.2% | 55.3% |
| Samples | 553 | 553 | 553 |

**Top LR features:** DXY(+0.0247), SP500(+0.0233), US10Y(+0.0120)

**Top RF features:** SP500(0.337), Silver(0.301), US10Y(0.104)

**Verdict: NO predictive ability**

### 20-Day

| Metric | Linear Reg | Random Forest | Baseline |
|--------|-----------|---------------|----------|
| OOS R² | 0.0017 | -0.0099 | 0.0 |
| OOS MAE | 0.008107 | 0.008129 | 0.008100 |
| Dir Acc | 52.8% | 52.8% | 53.2% |
| Samples | 551 | 551 | 551 |

**Top LR features:** DXY(+0.0404), TLT_ret(-0.0119), Silver(+0.0067)

**Top RF features:** US10Y_chg(0.198), VIX(0.159), TLT_ret(0.155)

**Verdict: MARGINAL predictive ability**


## Driver Ranking Summary

| Rank | Driver | Avg |r| | Best Lag | 1d R² | 5d R² | 20d R² | Cond Edge? |
|------|--------|---------|----------|--------|-------|--------|------------|
| 1 | DXY | 0.333 | — | 0.0005 | 0.0001 | 0.0004 | YES |
| 2 | Silver | 0.232 | — | 0.2821 | 0.0000 | 0.0001 | YES |
| 3 | TLT_ret | 0.083 | — | 0.0064 | 0.0000 | 0.0002 | YES |
| 4 | Crude Oil | 0.042 | — | 0.0043 | 0.0000 | 0.0001 | YES |
| 5 | VIX | 0.036 | — | 0.0001 | 0.0001 | 0.0000 | no |
| 6 | SP500 | 0.030 | — | 0.0006 | 0.0004 | 0.0000 | no |
| 7 | US10Y | 0.026 | — | 0.0221 | 0.0000 | 0.0001 | YES |
| 8 | US10Y_chg | 0.018 | — | 0.0259 | 0.0000 | 0.0001 | YES |

---
*Generated by XAU/USD Edge Discovery Framework*