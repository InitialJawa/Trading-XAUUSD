"""
OIL-005: Term Structure (Contango/Backwardation) for Crude Oil
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
    if len(d) < 20: return []
    d['Q'] = pd.qcut(d[sort_col].rank(method='first'), nq, labels=[f'Q{i+1}' for i in range(nq)])
    rs = []
    for q in [f'Q{i+1}' for i in range(nq)]:
        r = compute_metrics(d[d['Q'] == q][ret_col], f'{label} {q}', ppy)
        if r: rs.append(r)
    return rs

report = []
report.append("# OIL-005: Term Structure Analysis")
report.append("")

print("--- Downloading futures contracts ---")
contracts = {
    'CL=F': 'CL=F', 'CLc1': 'CL=F',
    'CLc2': None, 'CLc3': None,
}
# Try to get front vs 2nd month via Yahoo
try:
    cl1 = yf.Ticker('CL=F')
    h1 = cl1.history(period='max')
    if hasattr(h1.index, 'tz') and h1.index.tz is not None: h1.index = h1.index.tz_localize(None)
    h1.index = pd.to_datetime(h1.index.date); h1.index.name = 'Date'
    c1 = h1['Close']
    print(f"  CL=F: {len(c1)} rows")
    
    # USO as term structure proxy (holds front-month futures, rolls)
    uso = yf.Ticker('USO')
    hu = uso.history(period='max')
    if hasattr(hu.index, 'tz') and hu.index.tz is not None: hu.index = hu.index.tz_localize(None)
    hu.index = pd.to_datetime(hu.index.date); hu.index.name = 'Date'
    uso_c = hu['Close']
    print(f"  USO: {len(uso_c)} rows")
except: pass

print("--- Term Structure via USO/CL=F spread ---")
report.append("## A. Term Structure Proxy (USO vs CL=F spread)")
report.append("")
report.append("USO rolls front-month futures. CL=F is front-month. The spread USO/CL=F reflects roll yield + decay.")
report.append("")
common = c1.dropna().index.intersection(uso_c.dropna().index)
term = pd.DataFrame(index=common)
term['Spread'] = uso_c / c1 - 1
term['CL_Ret'] = c1.pct_change()
term = term.join(df[list(HORIZONS.values())])
term = term.dropna(subset=['Spread'])

results = []
for h, rcol in HORIZONS.items():
    results.extend(evaluate_quantile(term.dropna(subset=[rcol]), 'Spread', rcol, f'TermSpread_{h}d', PPY[h]))
    # Contango (negative spread) vs Backwardation (positive spread)
    contango = term[term['Spread'] < 0]
    backward = term[term['Spread'] > 0]
    for cond, label in [(contango, 'Contango'), (backward, 'Backwardation')]:
        if len(cond) > 10:
            r = compute_metrics(cond[rcol].dropna(), f'{label}_{h}d', PPY[h])
            if r: results.append(r)

report.append("| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |")
report.append("|--------|---|-----------|--------|----|-----|-------|")
df_r = pd.DataFrame(results) if results else pd.DataFrame()
t1 = df_r[(df_r.p_val < 0.05) & (df_r.Sharpe > 1.0) & (df_r.PF > 1.30)] if len(df_r) > 0 else pd.DataFrame()
print(f"  Total signals: {len(results)}, T1: {len(t1)}")
for _, r in t1.sort_values('Sharpe', ascending=False).iterrows() if len(t1) > 0 else []:
    report.append(f"| {r['Signal']} | {r['N']} | {r['Mean_Ret%']:.3f}% | {r['Sharpe']:.2f} | {r['PF']:.2f} | {r['WR%']:.1f}% | {r['p_val']:.4f} |")
report.append("")

print("--- Roll Yield ---")
report.append("## B. Roll Yield Signal (USO rolling cost)")
report.append("")
uso_ret = uso_c.pct_change().dropna()
cl_ret = c1.dropna().pct_change().dropna()
roll = pd.DataFrame(index=c1.dropna().index.intersection(uso_c.dropna().index))
roll['RollYield'] = uso_ret - cl_ret
roll['Roll_MA5'] = roll['RollYield'].rolling(5).mean()
roll = roll.join(df[list(HORIZONS.values())])

results2 = []
for h, rcol in HORIZONS.items():
    results2.extend(evaluate_quantile(roll.dropna(subset=[rcol]), 'RollYield', rcol, f'RollYield_{h}d', PPY[h]))
    results2.extend(evaluate_quantile(roll.dropna(subset=[rcol]), 'Roll_MA5', rcol, f'RollMA5_{h}d', PPY[h]))

if results2:
    df_r2 = pd.DataFrame(results2)
    t1_2 = df_r2[(df_r2.p_val < 0.05) & (df_r2.Sharpe > 0.8) & (df_r2.PF > 1.20)]
    print(f"  Roll yield signals: {len(results2)}, T1: {len(t1_2)}")
    report.append("| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |")
    report.append("|--------|---|-----------|--------|----|-----|-------|")
    for _, r in t1_2.sort_values('Sharpe', ascending=False).head(10).iterrows():
        report.append(f"| {r['Signal']} | {r['N']} | {r['Mean_Ret%']:.3f}% | {r['Sharpe']:.2f} | {r['PF']:.2f} | {r['WR%']:.1f}% | {r['p_val']:.4f} |")
report.append("")

report.append("---")
report.append("*Generated by research/oil/scripts/oil_005_term_structure.py*")
with open(REPORTS_DIR / 'OIL-005_Term_Structure.md', 'w') as f:
    f.write('\n'.join(report))
print("OIL-005 COMPLETE")
