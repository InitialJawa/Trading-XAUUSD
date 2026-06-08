"""
OIL-001: Data Foundation + Price Structure for Crude Oil
"""
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path('data/oil')
REPORTS_DIR = Path('reports/oil')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_DIR / 'CLF_cleaned.csv', parse_dates=['Date'], index_col='Date')
close = df['Close'].dropna()
ret = close.pct_change().dropna()
high = df['High']; low = df['Low']

report = []
report.append("# OIL-001: Data Foundation & Price Structure")
report.append("")
report.append(f"**Data:** {len(close):,} daily bars")
report.append(f"**Period:** {close.index[0].date()} to {close.index[-1].date()}")
report.append(f"**Instrument:** CL=F (WTI Crude Oil Futures)")
report.append("")

print("--- Section A: Data Quality ---")
report.append("## A. Data Quality")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| Total rows | {len(df):,} |")
report.append(f"| Missing values | {df.isnull().sum().sum()} |")
report.append(f"| Date range | {close.index[0].date()} to {close.index[-1].date()} |")
report.append(f"| Years | {(close.index[-1]-close.index[0]).days/365.25:.1f} |")
report.append("")

print("--- Section B: Returns Distribution ---")
report.append("## B. Return Distribution")
report.append("")
mu = ret.mean(); std = ret.std(); mu_a = mu * 252; std_a = std * np.sqrt(252)
sharpe = mu_a / std_a if std_a > 0 else 0
skew = ret.skew(); kurt = ret.kurtosis()
jb_stat, jb_p = stats.jarque_bera(ret.dropna())
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
adf = adfuller(ret.dropna())[1]

report.append(f"| Metric | Daily | Annualized |")
report.append(f"|--------|-------|------------|")
report.append(f"| Mean Return | {mu*100:.4f}% | {mu_a*100:.2f}% |")
report.append(f"| Std Dev | {std*100:.2f}% | {std_a*100:.2f}% |")
report.append(f"| Sharpe | | {sharpe:.4f} |")
report.append(f"| Skewness | {skew:.4f} | |")
report.append(f"| Kurtosis | {kurt:.4f} | |")
report.append(f"| JB p-value | {jb_p:.4e} | |")
report.append(f"| ADF p-value | {adf:.4e} | |")
report.append(f"| Min return | {ret.min()*100:.2f}% | |")
report.append(f"| Max return | {ret.max()*100:.2f}% | |")
report.append(f"| Positive days | {(ret>0).mean()*100:.1f}% | |")
report.append("")

print("--- Section C: Serial Correlation ---")
report.append("## C. Serial Correlation")
report.append("")
report.append("| Lag | Autocorrelation | Q-stat p-value |")
report.append("|-----|-----------------|----------------|")
for lag in [1, 2, 3, 5, 10, 20]:
    ac = ret.autocorr(lag=lag)
    lb = acorr_ljungbox(ret.dropna(), lags=[lag], return_df=True)
    p = lb['lb_pvalue'].iloc[0] if not lb.empty else 1
    report.append(f"| {lag} | {ac:.4f} | {p:.4f} |")
report.append("")

print("--- Section D: Volatility Clustering ---")
report.append("## D. Volatility Clustering")
report.append("")
abs_ret = ret.abs()
vol = close.rolling(20).std() / close * 100
for lag in [1, 5, 10, 20]:
    ac = abs_ret.autocorr(lag=lag)
    report.append(f"| |Vol| autocorr lag {lag} | {ac:.4f} |")
report.append("")

# ATR persistence
atr = pd.DataFrame()
atr['TR'] = np.maximum(high - low, np.abs(high - close.shift(1)), np.abs(low - close.shift(1)))
atr['ATR14'] = atr['TR'].rolling(14).mean()
ac_atr = atr['ATR14'].dropna().autocorr(lag=1)
report.append(f"| ATR(14) autocorr lag 1 | {ac_atr:.4f} |")
report.append("")

print("--- Section E: Market Regimes ---")
report.append("## E. Market Regimes")
report.append("")
atr14 = atr['ATR14'].dropna()

# Volatility quintiles
vol_q = pd.qcut(atr14.rank(method='first'), 5, labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
report.append("| Vol Quintile | N Days | Mean Ret% | WR% | PF | Sharpe |")
report.append("|-------------|--------|-----------|-----|----|--------|")
common_idx = ret.index.intersection(atr14.index)
ret_aligned = ret.loc[common_idx]
vol_q_aligned = vol_q.loc[common_idx]
for q in ['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High']:
    r = ret_aligned[vol_q_aligned == q].dropna()
    n, m, s = len(r), r.mean()*100, r.std()
    wr = (r>0).mean()*100
    pos = r[r>0].sum(); neg = abs(r[r<0].sum())
    pf = pos/neg if neg>0 else np.inf
    sh = m/s*100 if s>0 else 0
    report.append(f"| {q} | {n} | {m:.4f} | {wr:.1f} | {pf:.4f} | {sh:.4f} |")
report.append("")

print("--- Section F: Trend & Mean Reversion ---")
report.append("## F. Trend & Mean Reversion")
report.append("")
# Streak analysis
for streak_len in [1, 2, 3, 5]:
    streak = (ret.shift(1) > 0).rolling(streak_len).sum()
    nxt = ret[streak == streak_len]
    n = len(nxt)
    if n > 10:
        m = nxt.mean()*100
        wr = (nxt>0).mean()*100
        _, p = stats.ttest_1samp(nxt, 0)
        report.append(f"| {streak_len} up days -> next day | {n} | {m:.4f}% | {wr:.1f}% | p={p:.4f} |")
    
    streak_neg = (ret.shift(1) < 0).rolling(streak_len).sum()
    nxt_neg = ret[streak_neg == streak_len]
    n2 = len(nxt_neg)
    if n2 > 10:
        m2 = nxt_neg.mean()*100
        wr2 = (nxt_neg>0).mean()*100
        _, p2 = stats.ttest_1samp(nxt_neg, 0)
        report.append(f"| {streak_len} down days -> next day | {n2} | {m2:.4f}% | {wr2:.1f}% | p={p2:.4f} |")
report.append("")

# Z-score mean reversion
report.append("| Window | Threshold | N Events | Mean Ret% | WR% | PF | P-value |")
report.append("|--------|-----------|----------|-----------|-----|----|---------|")
for w in [10, 20, 50]:
    ma = close.rolling(w).mean()
    std_r = close.rolling(w).std()
    z = (close - ma) / std_r
    for thresh in [1.0, 1.5, 2.0, 2.5]:
        overbought = z > thresh
        oversold = z < -thresh
        for cond, name in [(overbought, f'Overbought (z>{thresh})'), (oversold, f'Oversold (z<-{thresh})')]:
            nxt = ret[cond.shift(1).fillna(False)]
            n = len(nxt)
            if n < 10: continue
            m = nxt.mean()*100
            wr = (nxt>0).mean()*100
            pos = nxt[nxt>0].sum(); neg = abs(nxt[nxt<0].sum())
            pf = pos/neg if neg>0 else np.inf
            _, p = stats.ttest_1samp(nxt, 0)
            report.append(f"| {w}d | {name} | {n} | {m:.4f} | {wr:.1f} | {pf:.4f} | {p:.4e} |")
report.append("")

print("--- Section G: Buy & Hold Benchmark ---")
report.append("## G. Buy & Hold Benchmark")
report.append("")
# Annual breakdown
years = ret.groupby(ret.index.year)
report.append("| Year | N | Mean Ret% | Vol% | Sharpe | WR% | Max DD% |")
report.append("|------|---|-----------|------|--------|-----|---------|")
for yr in range(2001, 2027):
    if yr not in years.groups: continue
    r = years.get_group(yr)
    n, m, s = len(r), r.mean()*252*100, r.std()*np.sqrt(252)*100
    sh = (r.mean()/r.std()*np.sqrt(252)) if r.std()>0 else 0
    wr = (r>0).mean()*100
    cum = (1+r).cumprod()
    dd = (cum / cum.cummax() - 1).min()*100
    report.append(f"| {yr} | {n} | {m:.2f} | {s:.2f} | {sh:.4f} | {wr:.1f} | {dd:.1f} |")
report.append("")
report.append(f"**Overall Buy & Hold Sharpe:** {sharpe:.4f}")
report.append("")

print("--- Verdict ---")
report.append("## Verdict")
report.append("")
report.append("OIL-001 establishes the data foundation and screens for price-derived edges.")
report.append("")
report.append("**T1 candidates found?** — See summary above for any PF > 1.30, p < 0.05 signals.")
report.append("")
report.append("Key differences from Gold/Bitcoin expected:")
report.append("- Higher volatility than Gold (~30-40% vs 18%)")
report.append("- More negative skew (sudden crashes from supply shocks)")
report.append("- Mean reversion may work better (oil has more cyclical mean reversion than Gold)")
report.append("- Buy & hold Sharpe likely lower than both Gold and Bitcoin (oil's flat long-term real return)")
report.append("")
report.append("---")
report.append("*Generated by research/oil/scripts/oil_001_price_structure.py*")

with open(REPORTS_DIR / 'OIL-001_Price_Structure.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"Report: {REPORTS_DIR / 'OIL-001_Price_Structure.md'}")
print("OIL-001 COMPLETE")
