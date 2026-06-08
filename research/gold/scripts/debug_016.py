"""Quick debug of RESEARCH-016 signal generation"""
import pandas as pd
import numpy as np
from pathlib import Path

# Load saved data
DATA_DIR = Path('data')
gcf = pd.read_csv(DATA_DIR / 'gcf.csv', parse_dates=['Date'], index_col=0)
tnx = pd.read_csv(DATA_DIR / 'tnx.csv', parse_dates=['Date'], index_col=0)
gld = pd.read_csv(DATA_DIR / 'gld.csv', parse_dates=['Date'], index_col=0)
tip = pd.read_csv(DATA_DIR / 'tip.csv', parse_dates=['Date'], index_col=0)

# Clean tz
for df in [gcf, tnx, gld, tip]:
    if hasattr(df.index, 'tz') and df.index.tz is not None:
        df.index = df.index.tz_localize(None)

# Load gold
px = pd.read_csv('data/XAUUSD_cleaned.csv', parse_dates=['Date'])
px = px.sort_values('Date').set_index('Date')['Close']
px.index.name = 'Date'

# Align
aligned = px.to_frame('Gold_Close')
aligned = aligned.join(gcf['Close'].rename('GC_Close'), how='left')
aligned = aligned.join(gld['Close'].rename('GLD_Close'), how='left')
aligned = aligned.join(gld['Volume'].rename('GLD_Volume'), how='left')
aligned = aligned.join(tnx['Close'].rename('US10Y'), how='left')
aligned = aligned.join(tip['Close'].rename('TIP_Close'), how='left')

print(f'Aligned: {len(aligned)} rows')
print(f'Columns: {list(aligned.columns)}')
print(f'GC_Close non-null: {aligned["GC_Close"].notna().sum()}')
print(f'GLD_Close non-null: {aligned["GLD_Close"].notna().sum()}')
print(f'US10Y non-null: {aligned["US10Y"].notna().sum()}')
print(f'TIP_Close non-null: {aligned["TIP_Close"].notna().sum()}')

# Term structure
ts = aligned.dropna(subset=['GC_Close', 'GLD_Close']).copy()
print(f'\nTerm structure subset: {len(ts)} rows')
ts['Spot_Proxy'] = ts['GLD_Close'] * 10
ts['TS_Ratio'] = ts['GC_Close'] / ts['Spot_Proxy']
ts['TS_Spread%'] = (ts['TS_Ratio'] - 1) * 100
ts['TS_Change'] = ts['TS_Spread%'].diff()
print(f'TS_Spread% non-null: {ts["TS_Spread%"].notna().sum()}')
print(f'TS_Spread% range: {ts["TS_Spread%"].min():.4f} to {ts["TS_Spread%"].max():.4f}')
print(f'TS_Spread% mean: {ts["TS_Spread%"].mean():.4f}')

# Forward returns
from scipy import stats

HORIZONS = {1: 'Ret_1d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 252, 5: 252/5, 10: 252/10, 20: 252/20, 60: 252/60}
for h, col in HORIZONS.items():
    ts[col] = ts['Gold_Close'].pct_change(h).shift(-h)

ts = ts.dropna(subset=['Ret_1d'])
print(f'\nWith returns: {len(ts)} rows')

# Test quantile evaluation
def compute_metrics(returns, label, ppy=252):
    g = returns.dropna()
    n = len(g)
    if n < 5:
        return None
    mu = g.mean()
    std = g.std()
    se = std / np.sqrt(n)
    t = mu / se if se > 0 else 0
    p = 2 * (1 - stats.t.cdf(abs(t), n - 1)) if n > 1 and se > 0 else 1
    sharpe = mu / std * np.sqrt(ppy) if std > 0 else 0
    pos_sum = g[g > 0].sum()
    neg_sum = abs(g[g < 0].sum())
    pf = pos_sum / neg_sum if neg_sum != 0 else (np.inf if pos_sum > 0 else 0)
    wr = (g > 0).mean() * 100
    return {'Signal': label, 'N': n, 'Mean_Ret%': mu * 100, 'Sharpe': sharpe, 'PF': pf, 'WR%': wr, 'p_val': p}

def evaluate_quantile(df, sort_col, ret_col, label_base, ppy, nq=5):
    d = df[[sort_col, ret_col]].dropna().copy()
    print(f'  evaluate_quantile: sort_col={sort_col}, ret_col={ret_col}, d.shape={d.shape}')
    if len(d) < 50:
        print(f'    Too small: {len(d)}')
        return []
    d['Q'] = pd.qcut(d[sort_col].rank(method='first'), nq,
                     labels=[f'Q{i+1}' for i in range(nq)])
    print(f'    Quintiles: {d["Q"].value_counts().to_dict()}')
    results = []
    for q in [f'Q{i+1}' for i in range(nq)]:
        r = compute_metrics(d[d['Q'] == q][ret_col], f'{label_base} {q}', ppy)
        if r is not None:
            results.append(r)
    print(f'    Results: {len(results)}')
    return results

# Test with 1d
print('\nTesting TS_Level_1d quantile:')
res = evaluate_quantile(ts, 'TS_Spread%', 'Ret_1d', 'TS_Level_1d', 252)
print(f'  Got {len(res)} signals')

# Test yield data
print('\nYield subset:')
ry = aligned.dropna(subset=['US10Y', 'TIP_Close']).copy()
print(f'  {len(ry)} rows')
ry['TNX_Chg'] = ry['US10Y'].diff()
for h, col in HORIZONS.items():
    ry[col] = ry['Gold_Close'].pct_change(h).shift(-h)
ry = ry.dropna(subset=['Ret_1d'])
print(f'  With returns: {len(ry)} rows')
print(f'  TNX_Chg non-null: {ry["TNX_Chg"].notna().sum()}')

# Test yield evaluate_quantile
print('\nTesting Yield_Level_1d quantile:')
res = evaluate_quantile(ry, 'US10Y', 'Ret_1d', 'Yield_Level_1d', 252)
print(f'  Got {len(res)} signals')
