"""
OIL-004: Cross-Asset Drivers for Crude Oil
"""
import pandas as pd, numpy as np
from scipy import stats
from pathlib import Path
import warnings, yfinance as yf
warnings.filterwarnings('ignore')

DATA_DIR = Path('data/oil'); REPORTS_DIR = Path('reports/oil')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_DIR / 'CLF_cleaned.csv', parse_dates=['Date'], index_col='Date')
close = df['Close'].dropna(); ret = close.pct_change().dropna()
HORIZONS = {1: 'Ret_1d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 252, 5: 252/5, 10: 252/10, 20: 252/20, 60: 252/60}
for h, col in HORIZONS.items():
    df[col] = close.pct_change(h).shift(-h)

def compute_metrics(g, label, ppy=252):
    g = g.dropna(); n = len(g)
    if n < 5: return None
    mu = g.mean(); std = g.std(); se = std/np.sqrt(n) if n > 0 else 0
    t = mu/se if se > 0 else 0; p = 2*(1-stats.t.cdf(abs(t), max(n-1,1))) if n > 1 and se > 0 else 1
    sharpe = mu/std*np.sqrt(ppy) if std > 0 else 0
    pos = g[g>0].sum(); neg = abs(g[g<0].sum()); pf = pos/neg if neg>0 else (np.inf if pos>0 else 0)
    wr = (g>0).mean()*100
    return {'Signal': label, 'N': n, 'Mean_Ret%': mu*100, 'Sharpe': sharpe, 'PF': pf, 'WR%': wr, 'p_val': p}

def evaluate_quantile(dff, sort_col, ret_col, label, ppy, nq=5):
    d = dff[[sort_col, ret_col]].dropna().copy()
    if len(d) < 50: return []
    d['Q'] = pd.qcut(d[sort_col].rank(method='first'), nq, labels=[f'Q{i+1}' for i in range(nq)])
    results = []
    for q in [f'Q{i+1}' for i in range(nq)]:
        r = compute_metrics(d[d['Q'] == q][ret_col], f'{label} {q}', ppy)
        if r: results.append(r)
    return results

report = []
report.append("# OIL-004: Cross-Asset Drivers")
report.append(f"**Period:** {df.index[0].date()} to {df.index[-1].date()}")
report.append("")

print("--- Downloading drivers ---")
drivers = {'DXY': 'DX-Y.NYB', 'SP500': '^GSPC', 'VIX': '^VIX', 'US10Y': '^TNX', 'USO': 'USO', 'XLE': 'XLE', 'GLD': 'GLD', 'Brent': 'BZ=F'}
driver_data = {}
for name, ticker in drivers.items():
    try:
        t = yf.Ticker(ticker); h = t.history(period='max')
        if len(h) > 0:
            if hasattr(h.index, 'tz') and h.index.tz is not None: h.index = h.index.tz_localize(None)
            h.index = pd.to_datetime(h.index.date); h.index.name = 'Date'
            driver_data[name] = h['Close'].dropna()
            print(f"  {name}: {len(driver_data[name])} rows")
    except: print(f"  {name}: error")

ALL = []
print("--- Running cross-asset analysis ---")
report.append("## A. Contemporaneous Correlation")
report.append("")
report.append("| Driver | r (same-day) | p-value | N |")
report.append("|--------|-------------|---------|---|")
for name, ds in driver_data.items():
    common = ret.index.intersection(ds.dropna().index)
    if len(common) < 50: continue
    d_ret = ds.pct_change().dropna()
    common2 = ret.index.intersection(d_ret.index)
    r, p = stats.pearsonr(ret.loc[common2], d_ret.loc[common2])
    report.append(f"| {name} | {r:.4f} | {p:.4e} | {len(common2)} |")
report.append("")

print("--- Predictive analysis ---")
report.append("## B. Predictive (Driver to Oil)")
report.append("")
for name, ds in driver_data.items():
    common = df.index.intersection(ds.dropna().index)
    if len(common) < 50: continue
    d_ret = ds.pct_change().dropna()
    temp = pd.DataFrame(index=common)
    temp['Driver_Ret'] = d_ret
    for h, rcol in HORIZONS.items():
        temp2 = temp.join(df[rcol], how='inner').dropna(subset=['Driver_Ret', rcol])
        if len(temp2) < 50: continue
        ALL.extend(evaluate_quantile(temp2, 'Driver_Ret', rcol, f'{name}_Ret_{h}d', PPY[h]))

# Macro levels
for name, ds in driver_data.items():
    common = df.index.intersection(ds.dropna().index)
    if len(common) < 50: continue
    temp = pd.DataFrame(index=common)
    temp['Level'] = ds
    temp['Chg'] = ds.diff()
    for h, rcol in HORIZONS.items():
        temp2 = temp.join(df[rcol], how='inner').dropna(subset=['Level', rcol])
        if len(temp2) < 50: continue
        ALL.extend(evaluate_quantile(temp2, 'Level', rcol, f'{name}_Level_{h}d', PPY[h]))
        temp3 = temp.dropna(subset=['Chg']).join(df[rcol], how='inner')
        if len(temp3) > 50:
            ALL.extend(evaluate_quantile(temp3, 'Chg', rcol, f'{name}_Chg_{h}d', PPY[h]))

if ALL:
    report.append("## C. T1 Candidates")
    report.append("")
    report.append("| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |")
    report.append("|--------|---|-----------|--------|----|-----|-------|")
    df_all = pd.DataFrame(ALL)
    t1 = df_all[(df_all.p_val < 0.05) & (df_all.Sharpe > 1.0) & (df_all.PF > 1.30) & (df_all.N > 50)]
    print(f"  T1 candidates: {len(t1)}")
    for _, r in t1.sort_values('Sharpe', ascending=False).head(20).iterrows():
        report.append(f"| {r['Signal']} | {r['N']} | {r['Mean_Ret%']:.3f}% | {r['Sharpe']:.2f} | {r['PF']:.2f} | {r['WR%']:.1f}% | {r['p_val']:.4f} |")

report.append("")
report.append("---")
report.append("*Generated by research/oil/scripts/oil_004_cross_asset.py*")
with open(REPORTS_DIR / 'OIL-004_Driver_Analysis.md', 'w') as f:
    f.write('\n'.join(report))
print("OIL-004 COMPLETE")
