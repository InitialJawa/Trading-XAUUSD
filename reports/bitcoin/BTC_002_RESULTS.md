# BTC-002: Funding Rate Research Results

**Data:** 2394 days (2019-11-18 to 2026-06-07)
**Instrument:** BTC-USD (Bitcoin) with Gate.io BTC_USDT perpetual funding rates
**Funding rate source:** Gate.io API (8h frequency, resampled to daily)
**Ann. Volatility:** 60.2%
**Ann. Sharpe:** 0.8203

## Summary

| Hypothesis | Description | Total Signals | T1 Candidates |
|-----------|------------|--------------|--------------|
| H1 | Funding Extremes (P5/P1) | 20 | 5 |
| H2 | Funding Level (quintiles) | 60 | 14 |
| H3 | Funding Change (delta) | 48 | 15 |
| H4 | Cumulative Funding | 128 | 38 |
| H5 | Funding Streaks | 24 | 4 |

**Total signals tested:** 280
**T1 candidates:** 76
**Valid masks:** 25
**Walk-Forward PASS:** 13 / 25
**OOS PASS:** 8 / 25
**MC PASS:** 15 / 25
**Drift Neutralization PASS:** 25 / 25
**Pass ALL 4 tests:** 3 / 25

## Verdict

**3 funding rate signals survive full validation — an edge distinct from anything found in Gold.**

### Survivors (pass all 4 tests)

| Signal | Description | N | Ret% | Sharpe | PF | WR% |
|--------|------------|---|------|--------|----|-----|
| H1_FR_extreme_P5_LowFR_10d | Bottom 5% funding → hold 10d | 120 | 4.0% | 2.51 | 3.26 | 65.0% |
| H1_FR_extreme_P5_LowFR_20d | Bottom 5% funding → hold 20d | 120 | 7.2% | 2.20 | 4.35 | 65.8% |
| H4_FR_cum_5d_LowCum_1d | Bottom 20% cumulative 5d → hold 1d | 478 | 0.4% | 2.53 | 1.48 | 54.4% |

### Economic Interpretation

All 3 survivors share the same logic: **low/negative funding predicts positive returns**. When shorts pay longs excessively (negative funding rates), shorts are underwater and forced to cover, creating upward price pressure. This is a genuine short-squeeze premium — a market microstructure signal unavailable in traditional assets like Gold.

### Comparison vs BTC-001A (Price Structure)

| Metric | BTC-001A (Price) | BTC-002 (Funding) |
|--------|-----------------|-------------------|
| Signals tested | 1,117 | 280 |
| T1 candidates | 547 (247 non-VP) | 76 |
| Pass ALL 4 | 0 (trend artifacts only) | 3 (genuine edge) |
| Economic basis | Price patterns (efficient) | Market microstructure |
| Replication needed | N/A | Yes — test on Binance/Bybit data |

## T1 Candidates

| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |
|--------|---|-----------|--------|----|-----|-------|
| H1_FR_extreme_P5_LowFR_1d | 120 | 0.684% | 4.56 | 2.06 | 58.3% | 0.0101 |
| H1_FR_extreme_P5_LowFR_2d | 120 | 0.990% | 3.31 | 2.03 | 60.0% | 0.0082 |
| H1_FR_extreme_P5_LowFR_5d | 120 | 2.122% | 2.76 | 2.47 | 62.5% | 0.0006 |
| H1_FR_extreme_P5_LowFR_10d | 120 | 3.996% | 2.51 | 3.26 | 65.0% | 0.0000 |
| H1_FR_extreme_P5_LowFR_20d | 120 | 7.238% | 2.20 | 4.35 | 65.8% | 0.0000 |
| H2_FR_Level_Q_ Q1 | 479 | 0.438% | 2.95 | 1.58 | 54.9% | 0.0008 |
| H2_FR_Last_Q_ Q1 | 479 | 0.386% | 2.87 | 1.54 | 54.3% | 0.0011 |
| H2_FR_Level_Q_ Q1 | 479 | 0.704% | 2.35 | 1.65 | 55.9% | 0.0002 |
| H2_FR_Last_Q_ Q1 | 479 | 0.685% | 2.34 | 1.65 | 56.2% | 0.0002 |
| H2_FR_Level_Q_ Q1 | 478 | 1.583% | 2.06 | 2.01 | 59.4% | 0.0000 |
| H2_FR_Last_Q_ Q1 | 478 | 1.497% | 1.95 | 1.94 | 58.6% | 0.0000 |
| H2_FR_Last_Q_ Q3 | 478 | 0.928% | 1.09 | 1.46 | 54.8% | 0.0056 |
| H2_FR_Level_Q_ Q1 | 477 | 2.361% | 1.48 | 2.00 | 60.2% | 0.0000 |
| H2_FR_Last_Q_ Q1 | 477 | 2.324% | 1.50 | 2.02 | 59.7% | 0.0000 |
| H2_FR_Last_Q_ Q3 | 477 | 2.387% | 1.32 | 1.90 | 57.9% | 0.0000 |
| H2_FR_Level_Q_ Q1 | 475 | 4.354% | 1.39 | 2.50 | 60.2% | 0.0000 |
| H2_FR_Level_Q_ Q4 | 475 | 4.540% | 1.28 | 2.31 | 58.9% | 0.0000 |
| H2_FR_Last_Q_ Q1 | 475 | 4.089% | 1.24 | 2.29 | 59.6% | 0.0000 |
| H2_FR_Last_Q_ Q3 | 475 | 6.044% | 1.54 | 2.75 | 59.4% | 0.0000 |
| H3_FR_delta_1d_Q_ Q1 | 479 | 0.375% | 2.11 | 1.38 | 56.2% | 0.0162 |
| H3_FR_delta_1d_NegDelta_1d | 481 | 0.372% | 2.09 | 1.38 | 56.1% | 0.0166 |
| H3_FR_delta_1d_Q_ Q1 | 479 | 0.711% | 1.97 | 1.52 | 58.2% | 0.0015 |
| H3_FR_delta_1d_Q_ Q5 | 479 | 0.514% | 1.52 | 1.37 | 55.7% | 0.0143 |
| H3_FR_delta_1d_PosDelta_2d | 479 | 0.514% | 1.52 | 1.37 | 55.7% | 0.0143 |
| H3_FR_delta_1d_NegDelta_2d | 481 | 0.704% | 1.96 | 1.52 | 58.0% | 0.0016 |
| H3_FR_delta_1d_Q_ Q1 | 478 | 1.348% | 1.53 | 1.63 | 59.4% | 0.0001 |
| H3_FR_delta_1d_NegDelta_5d | 479 | 1.338% | 1.52 | 1.63 | 59.3% | 0.0001 |
| H3_FR_delta_3d_Q_ Q1 | 479 | 0.479% | 2.44 | 1.50 | 54.7% | 0.0054 |
| H3_FR_delta_3d_NegDelta_1d | 479 | 0.479% | 2.44 | 1.50 | 54.7% | 0.0054 |
| H3_FR_delta_3d_Q_ Q1 | 478 | 0.764% | 2.14 | 1.59 | 56.1% | 0.0006 |
| H3_FR_delta_3d_NegDelta_2d | 479 | 0.761% | 2.14 | 1.59 | 55.9% | 0.0006 |
| H3_FR_delta_3d_Q_ Q1 | 478 | 1.588% | 1.66 | 1.72 | 58.8% | 0.0000 |
| H3_FR_delta_3d_Q_ Q2 | 477 | 1.165% | 1.58 | 1.65 | 56.0% | 0.0001 |
| H3_FR_delta_3d_NegDelta_5d | 478 | 1.588% | 1.66 | 1.72 | 58.8% | 0.0000 |
| H4_FR_cum_5d_Q_ Q1 | 478 | 0.389% | 2.53 | 1.48 | 54.4% | 0.0039 |
| H4_FR_cum_5d_LowCum_1d | 478 | 0.389% | 2.53 | 1.48 | 54.4% | 0.0039 |
| H4_FR_cum_5d_Q_ Q1 | 478 | 1.332% | 1.71 | 1.78 | 59.0% | 0.0000 |
| H4_FR_cum_5d_Q_ Q4 | 477 | 0.742% | 1.04 | 1.39 | 52.4% | 0.0078 |
| H4_FR_cum_5d_LowCum_5d | 478 | 1.332% | 1.71 | 1.78 | 59.0% | 0.0000 |
| H4_FR_cum_5d_Q_ Q1 | 477 | 2.043% | 1.29 | 1.83 | 58.3% | 0.0000 |
| H4_FR_cum_5d_Q_ Q4 | 476 | 2.118% | 1.39 | 1.87 | 55.3% | 0.0000 |
| H4_FR_cum_5d_LowCum_10d | 477 | 2.043% | 1.29 | 1.83 | 58.3% | 0.0000 |
| H4_FR_cum_5d_Q_ Q1 | 475 | 3.808% | 1.22 | 2.17 | 60.4% | 0.0000 |
| H4_FR_cum_5d_Q_ Q4 | 474 | 5.480% | 1.62 | 2.87 | 60.5% | 0.0000 |
| H4_FR_cum_5d_LowCum_20d | 475 | 3.808% | 1.22 | 2.17 | 60.4% | 0.0000 |
| H4_FR_cum_10d_Q_ Q1 | 477 | 0.982% | 1.31 | 1.56 | 56.0% | 0.0009 |
| H4_FR_cum_10d_Q_ Q4 | 476 | 1.092% | 1.48 | 1.61 | 51.7% | 0.0002 |
| H4_FR_cum_10d_LowCum_5d | 477 | 0.982% | 1.31 | 1.56 | 56.0% | 0.0009 |
| H4_FR_cum_10d_Q_ Q1 | 476 | 1.651% | 1.11 | 1.68 | 58.6% | 0.0001 |
| H4_FR_cum_10d_Q_ Q4 | 475 | 2.390% | 1.58 | 2.03 | 56.6% | 0.0000 |
| H4_FR_cum_10d_LowCum_10d | 476 | 1.651% | 1.11 | 1.68 | 58.6% | 0.0001 |
| H4_FR_cum_10d_Q_ Q1 | 474 | 3.040% | 1.04 | 1.94 | 59.5% | 0.0000 |
| H4_FR_cum_10d_Q_ Q4 | 473 | 6.342% | 1.78 | 3.18 | 62.6% | 0.0000 |
| H4_FR_cum_10d_LowCum_20d | 474 | 3.040% | 1.04 | 1.94 | 59.5% | 0.0000 |
| H4_FR_cum_20d_Q_ Q3 | 475 | 0.273% | 1.87 | 1.34 | 51.4% | 0.0336 |
| H4_FR_cum_20d_Q_ Q3 | 474 | 1.669% | 2.26 | 2.08 | 58.2% | 0.0000 |
| H4_FR_cum_20d_Q_ Q4 | 474 | 0.770% | 1.05 | 1.40 | 51.7% | 0.0077 |
| H4_FR_cum_20d_Q_ Q3 | 473 | 2.995% | 1.90 | 2.45 | 57.3% | 0.0000 |
| H4_FR_cum_20d_Q_ Q4 | 473 | 1.935% | 1.28 | 1.76 | 55.6% | 0.0000 |
| H4_FR_cum_20d_Q_ Q1 | 472 | 3.309% | 1.18 | 2.05 | 62.7% | 0.0000 |
| H4_FR_cum_20d_Q_ Q3 | 471 | 5.390% | 1.72 | 3.07 | 59.2% | 0.0000 |
| H4_FR_cum_20d_Q_ Q4 | 471 | 4.049% | 1.19 | 2.12 | 55.2% | 0.0000 |
| H4_FR_cum_20d_LowCum_20d | 472 | 3.309% | 1.18 | 2.05 | 62.7% | 0.0000 |
| H4_FR_cum_60d_Q_ Q2 | 467 | 0.301% | 2.23 | 1.42 | 50.7% | 0.0121 |
| H4_FR_cum_60d_Q_ Q2 | 466 | 1.420% | 2.24 | 2.13 | 58.6% | 0.0000 |
| H4_FR_cum_60d_Q_ Q4 | 466 | 1.359% | 1.79 | 1.77 | 56.9% | 0.0000 |
| H4_FR_cum_60d_Q_ Q2 | 465 | 2.733% | 2.00 | 2.60 | 60.4% | 0.0000 |
| H4_FR_cum_60d_Q_ Q4 | 465 | 2.884% | 1.82 | 2.27 | 58.9% | 0.0000 |
| H4_FR_cum_60d_Q_ Q1 | 464 | 3.064% | 1.05 | 1.91 | 66.6% | 0.0000 |
| H4_FR_cum_60d_Q_ Q2 | 463 | 3.509% | 1.03 | 1.98 | 49.7% | 0.0000 |
| H4_FR_cum_60d_Q_ Q4 | 463 | 5.141% | 1.62 | 2.93 | 57.9% | 0.0000 |
| H4_FR_cum_60d_LowCum_20d | 464 | 3.064% | 1.05 | 1.91 | 66.6% | 0.0000 |
| H5_FR_streak_NegFR_3d_1d | 149 | 0.545% | 3.27 | 1.73 | 53.7% | 0.0386 |
| H5_FR_streak_NegFR_3d_5d | 149 | 1.670% | 2.14 | 2.20 | 62.4% | 0.0027 |
| H5_FR_streak_NegFR_3d_10d | 149 | 2.823% | 1.72 | 2.45 | 69.1% | 0.0007 |
| H5_FR_streak_NegFR_5d_10d | 72 | 2.641% | 1.66 | 2.42 | 76.4% | 0.0225 |

---
*Generated by research/bitcoin/scripts/research_btc_002.py*