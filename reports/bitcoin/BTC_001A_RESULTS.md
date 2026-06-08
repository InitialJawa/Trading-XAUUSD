# BTC-001A: Price Structure Baseline Results

**Data:** 4282 days (2014-09-17 to 2026-06-07)
**Instrument:** BTC-USD (Bitcoin)
**Ann. Volatility:** 66.7%
**Ann. Sharpe:** 0.9664

## Summary

| Hypothesis | Total Signals | T1 Candidates | WF Pass | OOS Pass | MC Pass | Drift Pass |
|-----------|--------------|--------------|---------|----------|---------|------------|
| H1_Trend | 72 | 0 | - | - | - | - |
| H1_Trend | 72 | 0 | - | - | - | - |
| H2_MeanRev | 120 | 22 | - | - | - | - |
| H3_VolClust | 840 | 494 (300 VolPersist) | - | - | - | - |
| H4_Regime | 85 | 31 | - | - | - | - |

**Total signals tested:** 1117
**T1 candidates:** 547
**VolPersist (excluded):** 300
**Non-VolPersist T1 candidates:** 247
**Valid validation masks:** 112
**Walk-Forward PASS:** 80 / 112
**OOS PASS:** 48 / 112
**MC PASS:** 85 / 112
**Drift Neutralization PASS:** 108 / 112
**Pass ALL 4 tests:** 31 / 112 (but trend artifacts — see Verdict)

**BH FDR survivors:** 835 / 1117
**Bonferroni threshold:** 0.000045

## Verdict (Post VolPersist Filter)

**VolPersist signals excluded (300 trivially true vol-persistence entries):**
- Non-VolPersist T1 candidates: 247 (H2: 22, H3: 194, H4: 31)
- Valid validation masks: 112
- Walk-Forward PASS: 80 / 112
- OOS PASS: 48 / 112
- MC PASS: 85 / 112
- Drift Neutralization PASS: 108 / 112

**Survivors passing ALL 4 tests: 31 / 112**

However, these 31 survivors are predominantly long-only signals (LowVol buy, Bull regime, HighVol+Bull regime) that capture Bitcoin's strong upward trend (Sharpe 0.97). Key examples:
- H3 LowVol (15 signals): buy when volatility is low — captures Bitcoin's tendency to rally from calm periods
- H3 HighVol (8 signals): buy when volatility is high — mixed, mostly ATR-based
- H4 TrendRegime_Bull (2 signals): buy when in bull trend — trend-following artifact
- H4 Combined_Bull (6 signals): regime-conditional buying — riding uptrend

**Verdict: No price-derived edge survives the same rigorous standard applied to Gold.** The 31 survivors are overwhelmingly driven by Bitcoin's secular uptrend rather than market-timing alpha. H2 Mean Reversion produces 0 survivors — exactly like Gold. Proceeding to BTC-002 (Funding Rate Research).

## Comparison: Bitcoin vs Gold

| Metric | Bitcoin (BTC-USD) | Gold (GC=F) |
|--------|------------------|-------------|
| Data range | 2014-09-17 to 2026-06-07 | 2000-08-30 to 2026-06-08 |
| Observations | 4282 | 6,463 |
| Ann. Volatility | 66.7% | ~18% |
| Ann. Sharpe | 0.9664 | 0.69 |
| Win Rate | 52.4% | ~55% |
| Signals tested | 1117 | 440+ |
| T1 candidates (excl VolPersist) | 247 | 90 |
| WF survivors | 80 / 112 | 9 |
| OOS survivors | 48 / 112 | 24 |
| MC survivors | 85 / 112 | 75 (but all fail drift) |
| Pass ALL 4 | 31 / 112 (trend artifacts) | 0 |
| Final verdict | No edge | No edge |

## T1 Candidates

| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |
|--------|---|-----------|--------|----|-----|-------|
| H2_MeanRev_1d_Q_ Q4 | 856 | 0.290% | 1.75 | 1.33 | 50.0% | 0.0076 |
| H2_MeanRev_1d_Q_ Q4 | 856 | 0.700% | 2.03 | 1.57 | 55.4% | 0.0000 |
| H2_MeanRev_1d_Q_ Q5 | 856 | 0.506% | 1.25 | 1.31 | 51.9% | 0.0067 |
| H2_MeanRev_1d_Q_ Q4 | 855 | 1.353% | 1.55 | 1.69 | 54.9% | 0.0000 |
| H2_MeanRev_1d_Q_ Q5 | 856 | 1.356% | 1.29 | 1.51 | 53.2% | 0.0000 |
| H2_MeanRev_1d_Q_ Q4 | 854 | 2.505% | 1.35 | 1.88 | 56.2% | 0.0000 |
| H2_MeanRev_1d_Q_ Q5 | 855 | 2.354% | 1.08 | 1.66 | 54.3% | 0.0000 |
| H2_MeanRev_1d_Q_ Q4 | 852 | 4.718% | 1.14 | 2.18 | 55.0% | 0.0000 |
| H2_MeanRev_1d_Q_ Q5 | 853 | 5.161% | 1.10 | 2.12 | 54.4% | 0.0000 |
| H2_MeanRev_5d_Q_ Q5 | 856 | 0.418% | 2.06 | 1.36 | 52.9% | 0.0017 |
| H2_MeanRev_5d_Q_ Q5 | 855 | 0.806% | 1.90 | 1.50 | 55.6% | 0.0000 |
| H2_MeanRev_5d_Q_ Q4 | 854 | 0.960% | 1.10 | 1.43 | 51.5% | 0.0002 |
| H2_MeanRev_5d_Q_ Q5 | 855 | 1.687% | 1.52 | 1.64 | 55.1% | 0.0000 |
| H2_MeanRev_5d_Q_ Q4 | 853 | 1.942% | 1.06 | 1.63 | 53.3% | 0.0000 |
| H2_MeanRev_5d_Q_ Q5 | 854 | 3.426% | 1.49 | 2.01 | 58.2% | 0.0000 |
| H2_MeanRev_5d_Q_ Q4 | 851 | 4.514% | 1.08 | 2.11 | 53.6% | 0.0000 |
| H2_MeanRev_5d_Q_ Q5 | 852 | 6.098% | 1.25 | 2.39 | 57.0% | 0.0000 |
| H2_MeanRev_10d_Q_ Q5 | 855 | 0.545% | 2.58 | 1.47 | 55.4% | 0.0001 |
| H2_MeanRev_10d_Q_ Q5 | 854 | 0.979% | 2.24 | 1.60 | 57.6% | 0.0000 |
| H2_MeanRev_10d_Q_ Q5 | 854 | 2.446% | 2.24 | 2.05 | 58.2% | 0.0000 |
| H2_MeanRev_10d_Q_ Q5 | 853 | 4.788% | 2.05 | 2.60 | 62.6% | 0.0000 |
| H2_MeanRev_10d_Q_ Q5 | 851 | 7.785% | 1.58 | 3.02 | 60.3% | 0.0000 |
| H3_ATR_5d_Q_ Q1 | 856 | 0.195% | 1.58 | 1.32 | 54.7% | 0.0160 |
| H3_ATR_5d_LowVol_1d | 856 | 0.195% | 1.58 | 1.32 | 54.7% | 0.0160 |
| H3_ATR_5d_VolPersist_Q_ Q1 | 856 | 182.189% | 51.86 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q2 | 855 | 286.951% | 92.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q3 | 855 | 369.022% | 102.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q4 | 855 | 485.940% | 87.75 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q5 | 856 | 822.286% | 50.74 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q1 | 856 | 989.783% | 30.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q2 | 855 | 1577.549% | 47.15 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q3 | 855 | 2086.157% | 58.05 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q4 | 855 | 2819.785% | 59.25 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q5 | 855 | 4786.551% | 46.61 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q1 | 856 | 971.214% | 30.84 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q2 | 855 | 1592.097% | 51.71 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q3 | 855 | 2115.785% | 62.89 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q4 | 855 | 2868.911% | 69.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q5 | 855 | 4814.284% | 49.53 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_Q_ Q1 | 855 | 1.167% | 1.75 | 1.81 | 58.9% | 0.0000 |
| H3_ATR_5d_Q_ Q3 | 854 | 0.975% | 1.14 | 1.45 | 54.6% | 0.0001 |
| H3_ATR_5d_Q_ Q4 | 855 | 1.048% | 1.07 | 1.42 | 56.4% | 0.0003 |
| H3_ATR_5d_LowVol_5d | 856 | 1.168% | 1.75 | 1.81 | 59.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q1 | 856 | 182.189% | 51.86 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q2 | 855 | 286.951% | 92.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q3 | 855 | 369.022% | 102.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q4 | 855 | 485.940% | 87.75 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q5 | 856 | 822.286% | 50.74 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_Q_ Q1 | 855 | 1.058% | 1.53 | 1.68 | 57.7% | 0.0000 |
| H3_RollStd_5d_Q_ Q4 | 854 | 1.290% | 1.26 | 1.53 | 56.3% | 0.0000 |
| H3_RollStd_5d_LowVol_5d | 856 | 1.060% | 1.54 | 1.68 | 57.7% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q1 | 856 | 989.783% | 30.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q2 | 855 | 1577.549% | 47.15 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q3 | 855 | 2086.157% | 58.05 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q4 | 855 | 2819.785% | 59.25 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q5 | 855 | 4786.551% | 46.61 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_Q_ Q1 | 855 | 1.090% | 1.66 | 1.77 | 58.2% | 0.0000 |
| H3_RealVol_5d_Q_ Q3 | 855 | 1.049% | 1.17 | 1.47 | 53.3% | 0.0001 |
| H3_RealVol_5d_Q_ Q4 | 854 | 1.290% | 1.29 | 1.55 | 55.0% | 0.0000 |
| H3_RealVol_5d_LowVol_5d | 856 | 1.097% | 1.67 | 1.77 | 58.3% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q1 | 856 | 971.214% | 30.84 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q2 | 855 | 1592.097% | 51.71 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q3 | 855 | 2115.785% | 62.89 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q4 | 855 | 2868.911% | 69.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q5 | 855 | 4814.284% | 49.53 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_Q_ Q1 | 854 | 2.495% | 1.65 | 2.22 | 62.2% | 0.0000 |
| H3_ATR_5d_Q_ Q4 | 854 | 2.162% | 1.10 | 1.68 | 57.4% | 0.0000 |
| H3_ATR_5d_Q_ Q5 | 854 | 2.514% | 1.08 | 1.63 | 54.8% | 0.0000 |
| H3_ATR_5d_HighVol_10d | 854 | 2.514% | 1.08 | 1.63 | 54.8% | 0.0000 |
| H3_ATR_5d_LowVol_10d | 855 | 2.493% | 1.65 | 2.22 | 62.2% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q1 | 856 | 182.189% | 51.86 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q2 | 855 | 286.951% | 92.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q3 | 855 | 369.022% | 102.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q4 | 855 | 485.940% | 87.75 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q5 | 856 | 822.286% | 50.74 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_Q_ Q1 | 854 | 2.517% | 1.63 | 2.19 | 61.6% | 0.0000 |
| H3_RollStd_5d_Q_ Q4 | 853 | 2.593% | 1.23 | 1.79 | 56.4% | 0.0000 |
| H3_RollStd_5d_LowVol_10d | 854 | 2.517% | 1.63 | 2.19 | 61.6% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q1 | 856 | 989.783% | 30.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q2 | 855 | 1577.549% | 47.15 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q3 | 855 | 2086.157% | 58.05 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q4 | 855 | 2819.785% | 59.25 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q5 | 855 | 4786.551% | 46.61 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_Q_ Q1 | 854 | 2.440% | 1.64 | 2.21 | 63.2% | 0.0000 |
| H3_RealVol_5d_Q_ Q4 | 853 | 2.854% | 1.41 | 1.96 | 56.7% | 0.0000 |
| H3_RealVol_5d_LowVol_10d | 854 | 2.440% | 1.64 | 2.21 | 63.2% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q1 | 856 | 971.214% | 30.84 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q2 | 855 | 1592.097% | 51.71 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q3 | 855 | 2115.785% | 62.89 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q4 | 855 | 2868.911% | 69.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q5 | 855 | 4814.284% | 49.53 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_Q_ Q1 | 852 | 5.762% | 1.58 | 2.82 | 65.0% | 0.0000 |
| H3_ATR_5d_Q_ Q5 | 852 | 5.585% | 1.13 | 2.18 | 55.6% | 0.0000 |
| H3_ATR_5d_HighVol_20d | 854 | 5.537% | 1.12 | 2.16 | 55.5% | 0.0000 |
| H3_ATR_5d_LowVol_20d | 851 | 5.753% | 1.57 | 2.82 | 65.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q1 | 856 | 182.189% | 51.86 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q2 | 855 | 286.951% | 92.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q3 | 855 | 369.022% | 102.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q4 | 855 | 485.940% | 87.75 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q5 | 856 | 822.286% | 50.74 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_Q_ Q1 | 852 | 4.946% | 1.36 | 2.45 | 61.9% | 0.0000 |
| H3_RollStd_5d_LowVol_20d | 849 | 4.962% | 1.37 | 2.46 | 62.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q1 | 856 | 989.783% | 30.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q2 | 855 | 1577.549% | 47.15 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q3 | 855 | 2086.157% | 58.05 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q4 | 855 | 2819.785% | 59.25 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q5 | 855 | 4786.551% | 46.61 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_Q_ Q1 | 852 | 4.685% | 1.31 | 2.38 | 61.4% | 0.0000 |
| H3_RealVol_5d_Q_ Q5 | 852 | 5.085% | 1.01 | 1.99 | 56.6% | 0.0000 |
| H3_RealVol_5d_HighVol_20d | 855 | 5.140% | 1.02 | 2.00 | 56.6% | 0.0000 |
| H3_RealVol_5d_LowVol_20d | 849 | 4.715% | 1.32 | 2.40 | 61.5% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q1 | 856 | 971.214% | 30.84 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q2 | 855 | 1592.097% | 51.71 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q3 | 855 | 2115.785% | 62.89 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q4 | 855 | 2868.911% | 69.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q5 | 855 | 4814.284% | 49.53 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_Q_ Q1 | 844 | 19.367% | 1.43 | 4.85 | 70.4% | 0.0000 |
| H3_ATR_5d_LowVol_60d | 839 | 19.206% | 1.42 | 4.80 | 70.3% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q1 | 856 | 182.189% | 51.86 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q2 | 855 | 286.951% | 92.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q3 | 855 | 369.022% | 102.48 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q4 | 855 | 485.940% | 87.75 | inf | 100.0% | 0.0000 |
| H3_ATR_5d_VolPersist_Q_ Q5 | 856 | 822.286% | 50.74 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_Q_ Q1 | 844 | 16.257% | 1.23 | 3.86 | 64.3% | 0.0000 |
| H3_RollStd_5d_LowVol_60d | 834 | 16.210% | 1.23 | 3.85 | 64.3% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q1 | 856 | 989.783% | 30.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q2 | 855 | 1577.549% | 47.15 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q3 | 855 | 2086.157% | 58.05 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q4 | 855 | 2819.785% | 59.25 | inf | 100.0% | 0.0000 |
| H3_RollStd_5d_VolPersist_Q_ Q5 | 855 | 4786.551% | 46.61 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_Q_ Q1 | 844 | 16.181% | 1.22 | 3.85 | 65.2% | 0.0000 |
| H3_RealVol_5d_LowVol_60d | 833 | 16.304% | 1.23 | 3.89 | 65.2% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q1 | 856 | 971.214% | 30.84 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q2 | 855 | 1592.097% | 51.71 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q3 | 855 | 2115.785% | 62.89 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q4 | 855 | 2868.911% | 69.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_5d_VolPersist_Q_ Q5 | 855 | 4814.284% | 49.53 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_Q_ Q1 | 855 | 0.206% | 1.80 | 1.35 | 55.1% | 0.0060 |
| H3_ATR_10d_LowVol_1d | 855 | 0.206% | 1.80 | 1.35 | 55.1% | 0.0060 |
| H3_ATR_10d_VolPersist_Q_ Q1 | 855 | 188.382% | 65.40 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q2 | 854 | 291.577% | 142.34 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q3 | 854 | 376.225% | 163.52 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q4 | 854 | 479.903% | 142.79 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q5 | 855 | 805.719% | 61.01 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_Q_ Q1 | 855 | 0.265% | 2.35 | 1.47 | 56.3% | 0.0003 |
| H3_RollStd_10d_LowVol_1d | 855 | 0.265% | 2.35 | 1.47 | 56.3% | 0.0003 |
| H3_RollStd_10d_VolPersist_Q_ Q1 | 855 | 768.875% | 55.31 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q2 | 854 | 1218.364% | 90.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q3 | 854 | 1593.575% | 105.18 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q4 | 854 | 2108.763% | 101.42 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q5 | 854 | 3403.695% | 60.92 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_Q_ Q1 | 855 | 0.192% | 1.78 | 1.34 | 55.2% | 0.0066 |
| H3_RealVol_10d_LowVol_1d | 855 | 0.192% | 1.78 | 1.34 | 55.2% | 0.0066 |
| H3_RealVol_10d_VolPersist_Q_ Q1 | 855 | 760.736% | 55.57 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q2 | 854 | 1229.208% | 91.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q3 | 854 | 1597.059% | 108.54 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q4 | 854 | 2136.180% | 103.39 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q5 | 854 | 3411.607% | 63.50 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_Q_ Q1 | 854 | 1.029% | 1.49 | 1.67 | 57.3% | 0.0000 |
| H3_ATR_10d_Q_ Q5 | 854 | 1.343% | 1.09 | 1.40 | 54.2% | 0.0002 |
| H3_ATR_10d_HighVol_5d | 855 | 1.344% | 1.09 | 1.40 | 54.3% | 0.0002 |
| H3_ATR_10d_LowVol_5d | 855 | 1.029% | 1.49 | 1.67 | 57.3% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q1 | 855 | 188.382% | 65.40 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q2 | 854 | 291.577% | 142.34 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q3 | 854 | 376.225% | 163.52 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q4 | 854 | 479.903% | 142.79 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q5 | 855 | 805.719% | 61.01 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_Q_ Q1 | 854 | 1.228% | 1.76 | 1.84 | 58.4% | 0.0000 |
| H3_RollStd_10d_Q_ Q4 | 853 | 1.036% | 1.00 | 1.39 | 56.2% | 0.0007 |
| H3_RollStd_10d_LowVol_5d | 855 | 1.223% | 1.75 | 1.83 | 58.4% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q1 | 855 | 768.875% | 55.31 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q2 | 854 | 1218.364% | 90.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q3 | 854 | 1593.575% | 105.18 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q4 | 854 | 2108.763% | 101.42 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q5 | 854 | 3403.695% | 60.92 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_Q_ Q1 | 854 | 0.972% | 1.48 | 1.67 | 57.5% | 0.0000 |
| H3_RealVol_10d_Q_ Q4 | 853 | 1.345% | 1.37 | 1.56 | 59.1% | 0.0000 |
| H3_RealVol_10d_LowVol_5d | 855 | 0.968% | 1.47 | 1.67 | 57.4% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q1 | 855 | 760.736% | 55.57 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q2 | 854 | 1229.208% | 91.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q3 | 854 | 1597.059% | 108.54 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q4 | 854 | 2136.180% | 103.39 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q5 | 854 | 3411.607% | 63.50 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_Q_ Q1 | 853 | 2.440% | 1.58 | 2.12 | 61.4% | 0.0000 |
| H3_ATR_10d_Q_ Q5 | 853 | 3.215% | 1.36 | 1.83 | 55.8% | 0.0000 |
| H3_ATR_10d_HighVol_10d | 855 | 3.200% | 1.35 | 1.83 | 55.8% | 0.0000 |
| H3_ATR_10d_LowVol_10d | 853 | 2.440% | 1.58 | 2.12 | 61.4% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q1 | 855 | 188.382% | 65.40 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q2 | 854 | 291.577% | 142.34 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q3 | 854 | 376.225% | 163.52 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q4 | 854 | 479.903% | 142.79 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q5 | 855 | 805.719% | 61.01 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_Q_ Q1 | 853 | 2.316% | 1.51 | 2.07 | 60.7% | 0.0000 |
| H3_RollStd_10d_Q_ Q4 | 852 | 2.810% | 1.33 | 1.90 | 60.2% | 0.0000 |
| H3_RollStd_10d_LowVol_10d | 852 | 2.322% | 1.51 | 2.07 | 60.8% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q1 | 855 | 768.875% | 55.31 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q2 | 854 | 1218.364% | 90.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q3 | 854 | 1593.575% | 105.18 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q4 | 854 | 2108.763% | 101.42 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q5 | 854 | 3403.695% | 60.92 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_Q_ Q1 | 853 | 1.914% | 1.32 | 1.88 | 59.3% | 0.0000 |
| H3_RealVol_10d_Q_ Q4 | 852 | 3.095% | 1.46 | 2.01 | 61.3% | 0.0000 |
| H3_RealVol_10d_LowVol_10d | 852 | 1.921% | 1.32 | 1.88 | 59.4% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q1 | 855 | 760.736% | 55.57 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q2 | 854 | 1229.208% | 91.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q3 | 854 | 1597.059% | 108.54 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q4 | 854 | 2136.180% | 103.39 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q5 | 854 | 3411.607% | 63.50 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_Q_ Q1 | 851 | 5.707% | 1.55 | 2.78 | 63.5% | 0.0000 |
| H3_ATR_10d_Q_ Q5 | 851 | 6.357% | 1.21 | 2.34 | 57.1% | 0.0000 |
| H3_ATR_10d_HighVol_20d | 855 | 6.387% | 1.22 | 2.35 | 57.3% | 0.0000 |
| H3_ATR_10d_LowVol_20d | 848 | 5.728% | 1.55 | 2.79 | 63.6% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q1 | 855 | 188.382% | 65.40 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q2 | 854 | 291.577% | 142.34 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q3 | 854 | 376.225% | 163.52 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q4 | 854 | 479.903% | 142.79 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q5 | 855 | 805.719% | 61.01 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_Q_ Q1 | 851 | 5.585% | 1.47 | 2.62 | 62.2% | 0.0000 |
| H3_RollStd_10d_Q_ Q4 | 850 | 4.620% | 1.08 | 2.11 | 56.8% | 0.0000 |
| H3_RollStd_10d_Q_ Q5 | 851 | 5.640% | 1.09 | 2.13 | 57.2% | 0.0000 |
| H3_RollStd_10d_HighVol_20d | 855 | 5.707% | 1.10 | 2.15 | 57.4% | 0.0000 |
| H3_RollStd_10d_LowVol_20d | 842 | 5.593% | 1.47 | 2.63 | 62.2% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q1 | 855 | 768.875% | 55.31 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q2 | 854 | 1218.364% | 90.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q3 | 854 | 1593.575% | 105.18 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q4 | 854 | 2108.763% | 101.42 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q5 | 854 | 3403.695% | 60.92 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_Q_ Q1 | 851 | 4.932% | 1.35 | 2.41 | 62.3% | 0.0000 |
| H3_RealVol_10d_Q_ Q4 | 850 | 4.751% | 1.12 | 2.16 | 58.1% | 0.0000 |
| H3_RealVol_10d_Q_ Q5 | 851 | 6.033% | 1.15 | 2.23 | 57.6% | 0.0000 |
| H3_RealVol_10d_HighVol_20d | 855 | 6.028% | 1.15 | 2.23 | 57.5% | 0.0000 |
| H3_RealVol_10d_LowVol_20d | 842 | 4.918% | 1.35 | 2.40 | 62.2% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q1 | 855 | 760.736% | 55.57 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q2 | 854 | 1229.208% | 91.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q3 | 854 | 1597.059% | 108.54 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q4 | 854 | 2136.180% | 103.39 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q5 | 854 | 3411.607% | 63.50 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_Q_ Q1 | 843 | 19.543% | 1.43 | 4.79 | 69.8% | 0.0000 |
| H3_ATR_10d_HighVol_60d | 855 | 16.044% | 1.00 | 3.23 | 60.7% | 0.0000 |
| H3_ATR_10d_LowVol_60d | 837 | 19.619% | 1.43 | 4.80 | 69.8% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q1 | 855 | 188.382% | 65.40 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q2 | 854 | 291.577% | 142.34 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q3 | 854 | 376.225% | 163.52 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q4 | 854 | 479.903% | 142.79 | inf | 100.0% | 0.0000 |
| H3_ATR_10d_VolPersist_Q_ Q5 | 855 | 805.719% | 61.01 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_Q_ Q1 | 843 | 17.783% | 1.31 | 4.09 | 66.1% | 0.0000 |
| H3_RollStd_10d_LowVol_60d | 821 | 17.989% | 1.31 | 4.12 | 66.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q1 | 855 | 768.875% | 55.31 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q2 | 854 | 1218.364% | 90.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q3 | 854 | 1593.575% | 105.18 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q4 | 854 | 2108.763% | 101.42 | inf | 100.0% | 0.0000 |
| H3_RollStd_10d_VolPersist_Q_ Q5 | 854 | 3403.695% | 60.92 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_Q_ Q1 | 843 | 16.570% | 1.24 | 3.80 | 65.0% | 0.0000 |
| H3_RealVol_10d_LowVol_60d | 820 | 16.987% | 1.26 | 3.90 | 65.6% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q1 | 855 | 760.736% | 55.57 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q2 | 854 | 1229.208% | 91.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q3 | 854 | 1597.059% | 108.54 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q4 | 854 | 2136.180% | 103.39 | inf | 100.0% | 0.0000 |
| H3_RealVol_10d_VolPersist_Q_ Q5 | 854 | 3411.607% | 63.50 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_Q_ Q1 | 853 | 0.239% | 1.99 | 1.42 | 55.8% | 0.0025 |
| H3_ATR_20d_LowVol_1d | 853 | 0.239% | 1.99 | 1.42 | 55.8% | 0.0025 |
| H3_ATR_20d_VolPersist_Q_ Q1 | 853 | 198.131% | 74.73 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q2 | 852 | 299.077% | 191.49 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q3 | 852 | 383.599% | 193.08 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q4 | 852 | 476.592% | 204.33 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q5 | 853 | 777.781% | 68.09 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q1 | 853 | 612.395% | 75.59 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q2 | 852 | 933.531% | 141.67 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q3 | 852 | 1203.171% | 145.53 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q4 | 852 | 1531.840% | 169.41 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q5 | 852 | 2361.858% | 76.99 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_Q_ Q4 | 852 | 0.381% | 1.96 | 1.34 | 55.5% | 0.0028 |
| H3_RealVol_20d_VolPersist_Q_ Q1 | 853 | 610.336% | 76.59 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q2 | 852 | 943.322% | 144.91 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q3 | 852 | 1201.980% | 145.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q4 | 852 | 1554.365% | 164.00 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q5 | 852 | 2363.363% | 78.35 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_Q_ Q1 | 852 | 1.367% | 1.95 | 1.98 | 59.9% | 0.0000 |
| H3_ATR_20d_Q_ Q2 | 852 | 0.949% | 1.22 | 1.52 | 52.7% | 0.0000 |
| H3_ATR_20d_Q_ Q5 | 852 | 1.788% | 1.49 | 1.60 | 57.2% | 0.0000 |
| H3_ATR_20d_HighVol_5d | 853 | 1.789% | 1.49 | 1.60 | 57.2% | 0.0000 |
| H3_ATR_20d_LowVol_5d | 853 | 1.363% | 1.95 | 1.98 | 59.8% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q1 | 853 | 198.131% | 74.73 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q2 | 852 | 299.077% | 191.49 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q3 | 852 | 383.599% | 193.08 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q4 | 852 | 476.592% | 204.33 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q5 | 853 | 777.781% | 68.09 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_Q_ Q1 | 852 | 1.013% | 1.47 | 1.68 | 55.0% | 0.0000 |
| H3_RollStd_20d_Q_ Q4 | 851 | 1.341% | 1.30 | 1.54 | 55.6% | 0.0000 |
| H3_RollStd_20d_Q_ Q5 | 852 | 1.365% | 1.21 | 1.45 | 56.1% | 0.0000 |
| H3_RollStd_20d_HighVol_5d | 853 | 1.362% | 1.21 | 1.45 | 56.0% | 0.0000 |
| H3_RollStd_20d_LowVol_5d | 853 | 1.003% | 1.46 | 1.67 | 55.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q1 | 853 | 612.395% | 75.59 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q2 | 852 | 933.531% | 141.67 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q3 | 852 | 1203.171% | 145.53 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q4 | 852 | 1531.840% | 169.41 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q5 | 852 | 2361.858% | 76.99 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_Q_ Q1 | 852 | 0.757% | 1.14 | 1.49 | 54.8% | 0.0001 |
| H3_RealVol_20d_Q_ Q2 | 851 | 0.890% | 1.11 | 1.44 | 54.6% | 0.0002 |
| H3_RealVol_20d_Q_ Q4 | 851 | 1.365% | 1.35 | 1.55 | 57.1% | 0.0000 |
| H3_RealVol_20d_Q_ Q5 | 852 | 1.543% | 1.31 | 1.51 | 55.8% | 0.0000 |
| H3_RealVol_20d_HighVol_5d | 853 | 1.541% | 1.31 | 1.51 | 55.7% | 0.0000 |
| H3_RealVol_20d_LowVol_5d | 853 | 0.763% | 1.15 | 1.50 | 54.9% | 0.0001 |
| H3_RealVol_20d_VolPersist_Q_ Q1 | 853 | 610.336% | 76.59 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q2 | 852 | 943.322% | 144.91 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q3 | 852 | 1201.980% | 145.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q4 | 852 | 1554.365% | 164.00 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q5 | 852 | 2363.363% | 78.35 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_Q_ Q1 | 851 | 2.839% | 1.72 | 2.32 | 62.0% | 0.0000 |
| H3_ATR_20d_Q_ Q2 | 851 | 2.097% | 1.32 | 1.84 | 58.8% | 0.0000 |
| H3_ATR_20d_Q_ Q4 | 851 | 1.900% | 1.07 | 1.62 | 55.8% | 0.0000 |
| H3_ATR_20d_Q_ Q5 | 851 | 3.414% | 1.39 | 1.89 | 57.1% | 0.0000 |
| H3_ATR_20d_HighVol_10d | 853 | 3.417% | 1.39 | 1.89 | 57.2% | 0.0000 |
| H3_ATR_20d_LowVol_10d | 852 | 2.833% | 1.72 | 2.32 | 62.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q1 | 853 | 198.131% | 74.73 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q2 | 852 | 299.077% | 191.49 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q3 | 852 | 383.599% | 193.08 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q4 | 852 | 476.592% | 204.33 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q5 | 853 | 777.781% | 68.09 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_Q_ Q1 | 851 | 2.657% | 1.65 | 2.27 | 59.3% | 0.0000 |
| H3_RollStd_20d_Q_ Q4 | 850 | 2.203% | 1.12 | 1.68 | 58.6% | 0.0000 |
| H3_RollStd_20d_Q_ Q5 | 851 | 3.048% | 1.27 | 1.79 | 56.2% | 0.0000 |
| H3_RollStd_20d_HighVol_10d | 853 | 3.064% | 1.28 | 1.79 | 56.3% | 0.0000 |
| H3_RollStd_20d_LowVol_10d | 850 | 2.660% | 1.65 | 2.27 | 59.3% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q1 | 853 | 612.395% | 75.59 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q2 | 852 | 933.531% | 141.67 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q3 | 852 | 1203.171% | 145.53 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q4 | 852 | 1531.840% | 169.41 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q5 | 852 | 2361.858% | 76.99 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_Q_ Q1 | 851 | 2.199% | 1.37 | 1.96 | 58.8% | 0.0000 |
| H3_RealVol_20d_Q_ Q4 | 850 | 2.373% | 1.17 | 1.71 | 59.2% | 0.0000 |
| H3_RealVol_20d_Q_ Q5 | 851 | 3.211% | 1.34 | 1.85 | 56.1% | 0.0000 |
| H3_RealVol_20d_HighVol_10d | 853 | 3.206% | 1.34 | 1.85 | 56.0% | 0.0000 |
| H3_RealVol_20d_LowVol_10d | 850 | 2.183% | 1.36 | 1.96 | 58.7% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q1 | 853 | 610.336% | 76.59 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q2 | 852 | 943.322% | 144.91 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q3 | 852 | 1201.980% | 145.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q4 | 852 | 1554.365% | 164.00 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q5 | 852 | 2363.363% | 78.35 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_Q_ Q1 | 849 | 6.354% | 1.66 | 3.03 | 65.0% | 0.0000 |
| H3_ATR_20d_Q_ Q2 | 849 | 3.589% | 1.05 | 1.98 | 59.5% | 0.0000 |
| H3_ATR_20d_Q_ Q5 | 849 | 6.455% | 1.17 | 2.24 | 57.2% | 0.0000 |
| H3_ATR_20d_HighVol_20d | 853 | 6.445% | 1.17 | 2.24 | 57.3% | 0.0000 |
| H3_ATR_20d_LowVol_20d | 845 | 6.393% | 1.67 | 3.05 | 65.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q1 | 853 | 198.131% | 74.73 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q2 | 852 | 299.077% | 191.49 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q3 | 852 | 383.599% | 193.08 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q4 | 852 | 476.592% | 204.33 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q5 | 853 | 777.781% | 68.09 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_Q_ Q1 | 849 | 5.827% | 1.49 | 2.68 | 61.8% | 0.0000 |
| H3_RollStd_20d_Q_ Q4 | 848 | 4.392% | 1.05 | 2.01 | 55.9% | 0.0000 |
| H3_RollStd_20d_Q_ Q5 | 849 | 6.884% | 1.28 | 2.47 | 59.8% | 0.0000 |
| H3_RollStd_20d_HighVol_20d | 853 | 6.914% | 1.29 | 2.48 | 59.9% | 0.0000 |
| H3_RollStd_20d_LowVol_20d | 840 | 5.896% | 1.51 | 2.72 | 62.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q1 | 853 | 612.395% | 75.59 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q2 | 852 | 933.531% | 141.67 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q3 | 852 | 1203.171% | 145.53 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q4 | 852 | 1531.840% | 169.41 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q5 | 852 | 2361.858% | 76.99 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_Q_ Q1 | 849 | 4.849% | 1.29 | 2.33 | 59.6% | 0.0000 |
| H3_RealVol_20d_Q_ Q4 | 848 | 4.842% | 1.12 | 2.12 | 56.7% | 0.0000 |
| H3_RealVol_20d_Q_ Q5 | 849 | 6.758% | 1.27 | 2.45 | 60.0% | 0.0000 |
| H3_RealVol_20d_HighVol_20d | 853 | 6.776% | 1.28 | 2.46 | 59.9% | 0.0000 |
| H3_RealVol_20d_LowVol_20d | 840 | 4.906% | 1.30 | 2.35 | 59.8% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q1 | 853 | 610.336% | 76.59 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q2 | 852 | 943.322% | 144.91 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q3 | 852 | 1201.980% | 145.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q4 | 852 | 1554.365% | 164.00 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q5 | 852 | 2363.363% | 78.35 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_Q_ Q1 | 841 | 20.361% | 1.49 | 4.90 | 71.6% | 0.0000 |
| H3_ATR_20d_LowVol_60d | 836 | 20.495% | 1.50 | 4.93 | 71.7% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q1 | 853 | 198.131% | 74.73 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q2 | 852 | 299.077% | 191.49 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q3 | 852 | 383.599% | 193.08 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q4 | 852 | 476.592% | 204.33 | inf | 100.0% | 0.0000 |
| H3_ATR_20d_VolPersist_Q_ Q5 | 853 | 777.781% | 68.09 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_Q_ Q1 | 841 | 16.021% | 1.21 | 3.63 | 65.8% | 0.0000 |
| H3_RollStd_20d_LowVol_60d | 823 | 16.224% | 1.22 | 3.66 | 66.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q1 | 853 | 612.395% | 75.59 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q2 | 852 | 933.531% | 141.67 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q3 | 852 | 1203.171% | 145.53 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q4 | 852 | 1531.840% | 169.41 | inf | 100.0% | 0.0000 |
| H3_RollStd_20d_VolPersist_Q_ Q5 | 852 | 2361.858% | 76.99 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_Q_ Q1 | 841 | 14.980% | 1.11 | 3.27 | 63.0% | 0.0000 |
| H3_RealVol_20d_LowVol_60d | 823 | 15.038% | 1.11 | 3.27 | 62.9% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q1 | 853 | 610.336% | 76.59 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q2 | 852 | 943.322% | 144.91 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q3 | 852 | 1201.980% | 145.42 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q4 | 852 | 1554.365% | 164.00 | inf | 100.0% | 0.0000 |
| H3_RealVol_20d_VolPersist_Q_ Q5 | 852 | 2363.363% | 78.35 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_Q_ Q1 | 845 | 0.372% | 2.73 | 1.60 | 56.4% | 0.0000 |
| H3_ATR_60d_LowVol_1d | 845 | 0.372% | 2.73 | 1.60 | 56.4% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q1 | 845 | 215.857% | 93.41 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q2 | 844 | 313.380% | 213.43 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q3 | 844 | 391.750% | 261.75 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q4 | 844 | 469.277% | 257.11 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q5 | 845 | 727.725% | 57.03 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_Q_ Q1 | 845 | 0.214% | 1.72 | 1.34 | 54.0% | 0.0090 |
| H3_RollStd_60d_Q_ Q5 | 845 | 0.456% | 1.82 | 1.31 | 53.3% | 0.0057 |
| H3_RollStd_60d_HighVol_1d | 845 | 0.456% | 1.82 | 1.31 | 53.3% | 0.0057 |
| H3_RollStd_60d_LowVol_1d | 845 | 0.214% | 1.72 | 1.34 | 54.0% | 0.0090 |
| H3_RollStd_60d_VolPersist_Q_ Q1 | 845 | 441.850% | 116.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q2 | 844 | 617.445% | 196.23 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q3 | 844 | 767.256% | 358.04 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q4 | 844 | 899.488% | 322.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q5 | 844 | 1287.702% | 105.43 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_Q_ Q1 | 845 | 0.213% | 1.71 | 1.33 | 53.8% | 0.0096 |
| H3_RealVol_60d_Q_ Q5 | 845 | 0.488% | 1.93 | 1.33 | 53.5% | 0.0035 |
| H3_RealVol_60d_HighVol_1d | 845 | 0.488% | 1.93 | 1.33 | 53.5% | 0.0035 |
| H3_RealVol_60d_LowVol_1d | 845 | 0.213% | 1.71 | 1.33 | 53.8% | 0.0096 |
| H3_RealVol_60d_VolPersist_Q_ Q1 | 845 | 442.343% | 116.83 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q2 | 844 | 620.331% | 195.40 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q3 | 844 | 768.293% | 371.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q4 | 844 | 901.961% | 319.63 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q5 | 844 | 1295.199% | 108.42 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_Q_ Q1 | 844 | 1.771% | 2.35 | 2.34 | 61.0% | 0.0000 |
| H3_ATR_60d_Q_ Q5 | 844 | 1.285% | 1.11 | 1.41 | 54.7% | 0.0002 |
| H3_ATR_60d_HighVol_5d | 845 | 1.286% | 1.11 | 1.41 | 54.8% | 0.0002 |
| H3_ATR_60d_LowVol_5d | 845 | 1.772% | 2.35 | 2.34 | 61.1% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q1 | 845 | 215.857% | 93.41 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q2 | 844 | 313.380% | 213.43 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q3 | 844 | 391.750% | 261.75 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q4 | 844 | 469.277% | 257.11 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q5 | 845 | 727.725% | 57.03 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_Q_ Q1 | 844 | 0.975% | 1.33 | 1.60 | 55.1% | 0.0000 |
| H3_RollStd_60d_Q_ Q5 | 844 | 2.016% | 1.67 | 1.68 | 55.7% | 0.0000 |
| H3_RollStd_60d_HighVol_5d | 845 | 2.034% | 1.68 | 1.69 | 55.7% | 0.0000 |
| H3_RollStd_60d_LowVol_5d | 841 | 1.013% | 1.39 | 1.63 | 55.3% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q1 | 845 | 441.850% | 116.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q2 | 844 | 617.445% | 196.23 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q3 | 844 | 767.256% | 358.04 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q4 | 844 | 899.488% | 322.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q5 | 844 | 1287.702% | 105.43 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_Q_ Q1 | 844 | 0.922% | 1.29 | 1.57 | 55.1% | 0.0000 |
| H3_RealVol_60d_Q_ Q5 | 844 | 2.092% | 1.71 | 1.70 | 56.2% | 0.0000 |
| H3_RealVol_60d_HighVol_5d | 845 | 2.096% | 1.72 | 1.70 | 56.2% | 0.0000 |
| H3_RealVol_60d_LowVol_5d | 841 | 0.920% | 1.28 | 1.57 | 55.1% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q1 | 845 | 442.343% | 116.83 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q2 | 844 | 620.331% | 195.40 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q3 | 844 | 768.293% | 371.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q4 | 844 | 901.961% | 319.63 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q5 | 844 | 1295.199% | 108.42 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_Q_ Q1 | 843 | 3.411% | 2.05 | 2.82 | 66.0% | 0.0000 |
| H3_ATR_60d_Q_ Q3 | 842 | 2.491% | 1.25 | 1.87 | 54.0% | 0.0000 |
| H3_ATR_60d_Q_ Q5 | 843 | 2.597% | 1.13 | 1.64 | 55.4% | 0.0000 |
| H3_ATR_60d_HighVol_10d | 845 | 2.597% | 1.13 | 1.65 | 55.5% | 0.0000 |
| H3_ATR_60d_LowVol_10d | 845 | 3.394% | 2.04 | 2.80 | 65.9% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q1 | 845 | 215.857% | 93.41 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q2 | 844 | 313.380% | 213.43 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q3 | 844 | 391.750% | 261.75 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q4 | 844 | 469.277% | 257.11 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q5 | 845 | 727.725% | 57.03 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_Q_ Q1 | 843 | 1.862% | 1.11 | 1.72 | 57.1% | 0.0000 |
| H3_RollStd_60d_Q_ Q2 | 842 | 1.742% | 1.02 | 1.60 | 59.7% | 0.0000 |
| H3_RollStd_60d_Q_ Q5 | 843 | 3.817% | 1.55 | 2.02 | 56.7% | 0.0000 |
| H3_RollStd_60d_HighVol_10d | 845 | 3.872% | 1.57 | 2.04 | 56.8% | 0.0000 |
| H3_RollStd_60d_LowVol_10d | 836 | 1.932% | 1.15 | 1.76 | 57.3% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q1 | 845 | 441.850% | 116.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q2 | 844 | 617.445% | 196.23 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q3 | 844 | 767.256% | 358.04 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q4 | 844 | 899.488% | 322.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q5 | 844 | 1287.702% | 105.43 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_Q_ Q1 | 843 | 1.851% | 1.11 | 1.73 | 56.9% | 0.0000 |
| H3_RealVol_60d_Q_ Q2 | 842 | 1.828% | 1.06 | 1.64 | 60.8% | 0.0000 |
| H3_RealVol_60d_Q_ Q5 | 843 | 3.823% | 1.54 | 2.01 | 56.2% | 0.0000 |
| H3_RealVol_60d_HighVol_10d | 845 | 3.834% | 1.55 | 2.02 | 56.3% | 0.0000 |
| H3_RealVol_60d_LowVol_10d | 836 | 1.787% | 1.08 | 1.70 | 56.8% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q1 | 845 | 442.343% | 116.83 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q2 | 844 | 620.331% | 195.40 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q3 | 844 | 768.293% | 371.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q4 | 844 | 901.961% | 319.63 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q5 | 844 | 1295.199% | 108.42 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_Q_ Q1 | 841 | 6.115% | 1.72 | 3.23 | 69.1% | 0.0000 |
| H3_ATR_60d_Q_ Q3 | 840 | 4.753% | 1.17 | 2.34 | 55.4% | 0.0000 |
| H3_ATR_60d_LowVol_20d | 845 | 6.092% | 1.72 | 3.21 | 69.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q1 | 845 | 215.857% | 93.41 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q2 | 844 | 313.380% | 213.43 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q3 | 844 | 391.750% | 261.75 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q4 | 844 | 469.277% | 257.11 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q5 | 845 | 727.725% | 57.03 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_Q_ Q2 | 840 | 3.943% | 1.13 | 2.05 | 58.9% | 0.0000 |
| H3_RollStd_60d_Q_ Q5 | 841 | 7.387% | 1.36 | 2.51 | 57.4% | 0.0000 |
| H3_RollStd_60d_HighVol_20d | 845 | 7.496% | 1.37 | 2.54 | 57.6% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q1 | 845 | 441.850% | 116.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q2 | 844 | 617.445% | 196.23 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q3 | 844 | 767.256% | 358.04 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q4 | 844 | 899.488% | 322.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q5 | 844 | 1287.702% | 105.43 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_Q_ Q2 | 840 | 3.804% | 1.09 | 2.00 | 58.6% | 0.0000 |
| H3_RealVol_60d_Q_ Q5 | 841 | 7.611% | 1.38 | 2.56 | 57.2% | 0.0000 |
| H3_RealVol_60d_HighVol_20d | 845 | 7.577% | 1.37 | 2.55 | 57.2% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q1 | 845 | 442.343% | 116.83 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q2 | 844 | 620.331% | 195.40 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q3 | 844 | 768.293% | 371.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q4 | 844 | 901.961% | 319.63 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q5 | 844 | 1295.199% | 108.42 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_Q_ Q1 | 833 | 22.526% | 1.59 | 6.36 | 71.5% | 0.0000 |
| H3_ATR_60d_LowVol_60d | 845 | 22.483% | 1.57 | 6.29 | 71.6% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q1 | 845 | 215.857% | 93.41 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q2 | 844 | 313.380% | 213.43 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q3 | 844 | 391.750% | 261.75 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q4 | 844 | 469.277% | 257.11 | inf | 100.0% | 0.0000 |
| H3_ATR_60d_VolPersist_Q_ Q5 | 845 | 727.725% | 57.03 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_Q_ Q2 | 832 | 15.726% | 1.06 | 3.59 | 60.2% | 0.0000 |
| H3_RollStd_60d_LowVol_60d | 809 | 12.229% | 1.02 | 2.92 | 61.4% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q1 | 845 | 441.850% | 116.86 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q2 | 844 | 617.445% | 196.23 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q3 | 844 | 767.256% | 358.04 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q4 | 844 | 899.488% | 322.54 | inf | 100.0% | 0.0000 |
| H3_RollStd_60d_VolPersist_Q_ Q5 | 844 | 1287.702% | 105.43 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_Q_ Q2 | 832 | 15.242% | 1.04 | 3.44 | 60.5% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q1 | 845 | 442.343% | 116.83 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q2 | 844 | 620.331% | 195.40 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q3 | 844 | 768.293% | 371.09 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q4 | 844 | 901.961% | 319.63 | inf | 100.0% | 0.0000 |
| H3_RealVol_60d_VolPersist_Q_ Q5 | 844 | 1295.199% | 108.42 | inf | 100.0% | 0.0000 |
| H4_Combined_LowVol_Bull_1d | 277 | 0.510% | 3.25 | 1.65 | 58.5% | 0.0050 |
| H4_Combined_HighVol_Sideways_1d | 203 | 0.599% | 2.79 | 1.56 | 53.7% | 0.0389 |
| H4_Combined_HighVol_Bull_1d | 628 | 0.446% | 1.86 | 1.31 | 54.8% | 0.0149 |
| H4_VolRegime_LowVol_5d | 1418 | 1.017% | 1.38 | 1.61 | 55.7% | 0.0000 |
| H4_VolRegime_HighVol_5d | 1421 | 1.478% | 1.35 | 1.53 | 55.9% | 0.0000 |
| H4_TrendRegime_Bull_5d | 1407 | 1.705% | 1.65 | 1.70 | 55.5% | 0.0000 |
| H4_Combined_LowVol_Bear_5d | 358 | 0.779% | 1.46 | 1.63 | 63.7% | 0.0013 |
| H4_Combined_LowVol_Bull_5d | 277 | 2.185% | 2.41 | 2.23 | 57.8% | 0.0000 |
| H4_Combined_HighVol_Sideways_5d | 203 | 2.557% | 2.27 | 2.08 | 58.6% | 0.0002 |
| H4_Combined_HighVol_Bull_5d | 628 | 2.405% | 2.06 | 1.91 | 58.6% | 0.0000 |
| H4_VolRegime_LowVol_10d | 1413 | 2.273% | 1.37 | 1.91 | 58.8% | 0.0000 |
| H4_VolRegime_HighVol_10d | 1421 | 2.692% | 1.22 | 1.75 | 57.1% | 0.0000 |
| H4_TrendRegime_Bull_10d | 1407 | 3.434% | 1.56 | 2.07 | 56.6% | 0.0000 |
| H4_Combined_LowVol_Bear_10d | 358 | 2.226% | 1.96 | 2.56 | 64.0% | 0.0000 |
| H4_Combined_LowVol_Bull_10d | 277 | 4.237% | 2.13 | 2.67 | 61.0% | 0.0000 |
| H4_Combined_HighVol_Sideways_10d | 203 | 3.211% | 1.30 | 1.79 | 61.6% | 0.0024 |
| H4_Combined_HighVol_Bull_10d | 628 | 4.780% | 2.00 | 2.53 | 61.1% | 0.0000 |
| H4_VolRegime_LowVol_20d | 1403 | 5.176% | 1.38 | 2.48 | 60.2% | 0.0000 |
| H4_VolRegime_HighVol_20d | 1421 | 5.905% | 1.18 | 2.27 | 58.4% | 0.0000 |
| H4_TrendRegime_Bull_20d | 1407 | 6.827% | 1.37 | 2.65 | 58.1% | 0.0000 |
| H4_Combined_LowVol_Bear_20d | 358 | 4.686% | 1.59 | 2.86 | 65.9% | 0.0000 |
| H4_Combined_LowVol_Sideways_20d | 768 | 4.782% | 1.21 | 2.19 | 57.4% | 0.0000 |
| H4_Combined_LowVol_Bull_20d | 277 | 6.904% | 1.70 | 3.11 | 60.3% | 0.0000 |
| H4_Combined_HighVol_Sideways_20d | 203 | 5.518% | 1.10 | 1.96 | 61.1% | 0.0003 |
| H4_Combined_HighVol_Bull_20d | 628 | 11.029% | 1.87 | 4.00 | 65.9% | 0.0000 |
| H4_VolRegime_LowVol_60d | 1365 | 16.580% | 1.21 | 3.79 | 65.1% | 0.0000 |
| H4_TrendRegime_Bull_60d | 1404 | 22.706% | 1.22 | 4.94 | 67.5% | 0.0000 |
| H4_Combined_LowVol_Bear_60d | 358 | 15.157% | 1.26 | 3.33 | 68.7% | 0.0000 |
| H4_Combined_LowVol_Sideways_60d | 733 | 15.323% | 1.05 | 3.31 | 57.8% | 0.0000 |
| H4_Combined_LowVol_Bull_60d | 274 | 21.805% | 1.67 | 7.41 | 79.6% | 0.0000 |
| H4_Combined_HighVol_Bull_60d | 628 | 31.036% | 1.41 | 6.50 | 68.2% | 0.0000 |

---
*Generated by research/bitcoin/scripts/research_btc_001a.py*