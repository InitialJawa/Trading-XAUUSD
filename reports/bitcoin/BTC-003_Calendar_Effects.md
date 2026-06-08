# BTC-003: Calendar Effects

**Date:** 2026-06-09 00:17
**Instrument:** BTC-USD
**Period:** 2014-09-18 to 2026-06-08
**Observations:** 4,282

## 1. Day of Week Effect

| Day | Count | Mean Ret% | Median Ret% | Std% | Win Rate% | Avg Win% | Avg Loss% | PF | Sharpe (ann) |
|-----|-------|-----------|-------------|------|-----------|----------|-----------|----|-------------|
| Monday | 612 | 0.4966 | 0.2553 | 3.7675 | 54.58 | 2.8530 | -2.3346 | 1.4683 | 2.5182 |
| Tuesday | 611 | 0.0641 | 0.0259 | 3.5226 | 50.41 | 2.4649 | -2.3841 | 1.0544 | 0.3477 |
| Wednesday | 611 | 0.2608 | 0.0914 | 3.7998 | 51.72 | 2.7341 | -2.3887 | 1.2261 | 1.3111 |
| Thursday | 612 | -0.0169 | -0.0521 | 4.1898 | 49.51 | 2.6030 | -2.5859 | 0.9871 | -0.0771 |
| Friday | 612 | 0.2012 | 0.2129 | 3.4520 | 54.25 | 2.3500 | -2.3466 | 1.1874 | 1.1137 |
| Saturday | 612 | 0.1652 | 0.1238 | 2.6868 | 54.90 | 1.6454 | -1.6368 | 1.2238 | 1.1747 |
| Sunday | 612 | 0.0660 | 0.0677 | 2.7425 | 51.47 | 1.8863 | -1.8646 | 1.0730 | 0.4601 |

### ANOVA: Are mean returns equal across all days?
F-statistic: 1.4447, P-value: 0.193409, Significant? NO

### Kruskal-Wallis (non-parametric)
H-statistic: 6.7367, P-value: 0.345886, Significant? NO

### T-test: Is each day's mean return different from zero?
| Day | T-stat | P-value | Significant? |
|-----|--------|---------|--------------|
| Monday | 3.2607 | 0.001173 | YES |
| Tuesday | 0.4499 | 0.652937 | NO |
| Wednesday | 1.6963 | 0.090342 | NO |
| Thursday | -0.0998 | 0.920535 | NO |
| Friday | 1.4420 | 0.149801 | NO |
| Saturday | 1.5211 | 0.128752 | NO |
| Sunday | 0.5958 | 0.551532 | NO |

### Binomial Test: Is win rate different from 50%?
| Day | Win Rate% | N Wins | N Total | Binom P | Significant? |
|-----|-----------|--------|---------|---------|--------------|
| Monday | 54.58 | 334 | 612 | 0.026119 | YES |
| Tuesday | 50.41 | 308 | 611 | 0.871462 | NO |
| Wednesday | 51.72 | 316 | 611 | 0.418472 | NO |
| Thursday | 49.51 | 303 | 612 | 0.839849 | NO |
| Friday | 54.25 | 332 | 612 | 0.039163 | YES |
| Saturday | 54.90 | 336 | 612 | 0.017011 | YES |
| Sunday | 51.47 | 315 | 612 | 0.491998 | NO |

### Day Ranking by Mean Return
  1. Monday: 0.4966% (WR: 54.58%, PF: 1.4683)
  2. Wednesday: 0.2608% (WR: 51.72%, PF: 1.2261)
  3. Friday: 0.2012% (WR: 54.25%, PF: 1.1874)
  4. Saturday: 0.1652% (WR: 54.90%, PF: 1.2238)
  5. Sunday: 0.0660% (WR: 51.47%, PF: 1.0730)
  6. Tuesday: 0.0641% (WR: 50.41%, PF: 1.0544)
  7. Thursday: -0.0169% (WR: 49.51%, PF: 0.9871)

---

## 2. Month of Year Effect

| Month | Count | Mean Ret% | Win Rate% | PF | Sharpe (ann) | T-test P |
|-------|-------|-----------|-----------|----|-------------|----------|
| Jan | 372 | -0.0166 | 51.88 | 0.9879 | -0.0748 | 9.3985e-01 |
| Feb | 339 | 0.3646 | 51.92 | 1.3437 | 1.8611 | 7.3766e-02 |
| Mar | 372 | 0.0549 | 53.23 | 1.0422 | 0.2539 | 7.9784e-01 |
| Apr | 360 | 0.3226 | 55.00 | 1.3865 | 2.1240 | 3.5601e-02 |
| May | 372 | 0.1973 | 54.03 | 1.1840 | 1.1089 | 2.6365e-01 |
| Jun | 338 | 0.0307 | 53.85 | 1.0249 | 0.1595 | 8.7813e-01 |
| Jul | 341 | 0.3175 | 51.32 | 1.3405 | 1.8028 | 8.2328e-02 |
| Aug | 341 | -0.0186 | 46.92 | 0.9823 | -0.1169 | 9.1014e-01 |
| Sep | 343 | -0.0679 | 48.69 | 0.9307 | -0.4227 | 6.8224e-01 |
| Oct | 372 | 0.4894 | 55.91 | 1.7662 | 3.6273 | 2.8673e-04 |
| Nov | 360 | 0.1996 | 52.22 | 1.1741 | 1.0466 | 2.9929e-01 |
| Dec | 372 | 0.2323 | 53.23 | 1.2159 | 1.2083 | 2.2332e-01 |

**ANOVA (month):** F=0.9279, p=0.512041, Not significant

**Best month:** Oct (0.4894%, WR: 55.91%)
**Worst month:** Sep (-0.0679%, WR: 48.69%)

---

## 3. Halving Cycle Effect

| Phase | N Halvings | Mean Cum Ret% | Std% | WR% | Min% | Max% |
|-------|-----------|--------------|------|-----|------|------|
| Pre-Halving (-180d to -1d) | 3 | 53.47 | 46.23 | 67 | -0.67 | 112.29 |
| Post-Halving (+1d to +180d) | 3 | 44.68 | 28.26 | 100 | 5.90 | 72.45 |
| Post-Halving (+1d to +365d) | 3 | 293.11 | 214.78 | 100 | 33.24 | 559.22 |
| Halving Year | 3 | 396.57 | 153.69 | 100 | 184.32 | 543.23 |

### Returns by Halving Era

| Era | Period | Daily Mean% | Ann Sharpe | Ann Vol% | CAGR% |
|-----|--------|------------|------------|---------|-------|
| 1st Halving | 2012-11-28 to 2016-07-08 | 0.1161 | 0.6503 | 65.19 | 52.75 |
| 2nd Halving | 2016-07-09 to 2020-05-10 | 0.2720 | 1.2449 | 79.75 | 169.51 |
| 3rd Halving | 2020-05-11 to 2024-04-18 | 0.1913 | 1.1169 | 62.51 | 100.87 |
| 4th Halving | 2024-04-19 to 2026-06-08 | 0.0301 | 0.2352 | 46.70 | 11.61 |
| Full Period | 2014-09-18 to 2026-06-08 | 0.1767 | 0.9672 | 66.69 | 90.50 |

---

## 4. Monthly Return Patterns

| Month | Average Monthly Return% | Positive Years / Total | WR% |
|-------|----------------------|----------------------|-----|
| Jan | -1.15 | 6/12 | 50 |
| Feb | 10.19 | 9/12 | 75 |
| Mar | 0.48 | 6/12 | 50 |
| Apr | 10.16 | 8/12 | 67 |
| May | 8.08 | 6/12 | 50 |
| Jun | 0.63 | 6/12 | 50 |
| Jul | 9.03 | 8/11 | 73 |
| Aug | -0.15 | 3/11 | 27 |
| Sep | -2.96 | 5/12 | 42 |
| Oct | 16.63 | 9/12 | 75 |
| Nov | 7.51 | 7/12 | 58 |
| Dec | 7.14 | 5/12 | 42 |

### Quarterly Returns

| Quarter | Months | Avg Return% | Win Rate% |
|---------|--------|-------------|-----------|
| Q1 | Jan, Feb, Mar | 11.79 | 42 |
| Q2 | Apr, May, Jun | 26.58 | 58 |
| Q3 | Jul, Aug, Sep | 4.76 | 50 |
| Q4 | Oct, Nov, Dec | 44.46 | 58 |

---

## Summary

### Day of Week
- **Monday**: WR=54.6%, PF=1.47, Sharpe=2.52 — passes criteria (but check stability)

### Month of Year
- Apr: passes edge criteria
- Oct: passes edge criteria

### Halving Cycle
- Best phase: Halving Year (mean 396.6%)
- All halvings produced positive returns post-event

### Verdict
Some calendar effects show statistical significance, but require regime stability and OOS testing.

---
*Generated by research/bitcoin/scripts/btc_003_calendar.py*