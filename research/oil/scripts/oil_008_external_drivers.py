"""
OIL-008: External Drivers — COT, Macro, Oil-Equity, Inventory proxies
"""
import pandas as pd, numpy as np
from scipy import stats
from pathlib import Path
import warnings, yfinance as yf
warnings.filterwarnings('ignore')

DATA_DIR = Path('data'); OIL_DIR = Path('data/oil'); REPORTS_DIR = Path('reports/oil')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(OIL_DIR / 'CLF_cleaned.csv', parse_dates=['Date'], index_col='Date')
close = df['Close'].dropna(); ret = close.pct_change().dropna()
HORIZONS = {1: 'Ret_1d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 252, 5: 252/5, 10: 252/10, 20: 252/20, 60: 252/60}
for h, col in HORIZONS.items():
    df[col] = close.pct_change(h).shift(-h)
df = df.dropna(subset=['Ret_1d']).copy()

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
    rs = []
    for q in [f'Q{i+1}' for i in range(nq)]:
        r = compute_metrics(d[d['Q'] == q][ret_col], f'{label} {q}', ppy)
        if r: rs.append(r)
    return rs

ALL = []
report = []
report.append("# OIL-008: External Drivers Analysis")
report.append(f"**Period:** {df.index[0].date()} to {df.index[-1].date()}")
report.append("")

print("--- Phase A: Oil Inventory Proxy (USO volume spikes) ---")
report.append("## Phase A: Inventory Proxy (USO Volume)")
report.append("")
report.append("USO volume spikes may proxy for EIA inventory surprise days.")
report.append("")
try:
    uso = pd.read_csv(OIL_DIR / 'USO.csv', parse_dates=['Date'], index_col='Date')
    vol_z = (uso['Volume'] - uso['Volume'].rolling(20).mean()) / uso['Volume'].rolling(20).std()
    uso_ret = uso['Close'].pct_change().dropna()
    temp = pd.DataFrame(index=df.index.intersection(uso.index))
    temp['USO_Ret'] = uso_ret
    temp['Vol_Z'] = vol_z
    temp['USO_OIL_Div'] = uso_ret - ret
    for h, rcol in HORIZONS.items():
        t = temp.join(df[rcol], how='inner')
        ALL.extend(evaluate_quantile(t.dropna(subset=['Vol_Z', rcol]), 'Vol_Z', rcol, f'USO_VolZ_{h}d', PPY[h]))
        ALL.extend(evaluate_quantile(t.dropna(subset=['USO_Ret', rcol]), 'USO_Ret', rcol, f'USO_Ret_{h}d', PPY[h]))
        ALL.extend(evaluate_quantile(t.dropna(subset=['USO_OIL_Div', rcol]), 'USO_OIL_Div', rcol, f'USO_OIL_Div_{h}d', PPY[h]))
    print("  USO done")
except: print("  USO data not found")

print("--- Phase B: Oil-Equity (XLE) ---")
report.append("## Phase B: Oil-Equity (XLE)")
report.append("")
try:
    xle = pd.read_csv(OIL_DIR / 'XLE.csv', parse_dates=['Date'], index_col='Date')
    xle_ret = xle['Close'].pct_change().dropna()
    temp = pd.DataFrame(index=df.index.intersection(xle.index))
    temp['XLE_Ret'] = xle_ret
    temp['XLE_OIL_Div'] = xle_ret - ret
    for h, rcol in HORIZONS.items():
        t = temp.join(df[rcol], how='inner')
        ALL.extend(evaluate_quantile(t.dropna(subset=['XLE_Ret', rcol]), 'XLE_Ret', rcol, f'XLE_Ret_{h}d', PPY[h]))
        ALL.extend(evaluate_quantile(t.dropna(subset=['XLE_OIL_Div', rcol]), 'XLE_OIL_Div', rcol, f'XLE_OIL_Div_{h}d', PPY[h]))
    print("  XLE done")
except: print("  XLE not found")

print("--- Phase C: Macro Regimes ---")
report.append("## Phase C: Macro Regimes")
report.append("")
# DXY, SPY, VIX as regimes
macro = {}
for path, name in [(Path('data')/'related_instruments.csv', 'DXY'), (Path('data')/'tnx.csv', 'US10Y')]:
    try:
        m = pd.read_csv(path, parse_dates=['Date'], index_col='Date')
        macro[name] = m['Close'].dropna()
    except: pass

for mname, mseries in macro.items():
    common = df.index.intersection(mseries.dropna().index)
    if len(common) < 50: continue
    temp = pd.DataFrame(index=common)
    temp['Level'] = mseries
    temp['Chg'] = mseries.diff()
    for h, rcol in HORIZONS.items():
        t = temp.join(df[rcol], how='inner')
        ALL.extend(evaluate_quantile(t.dropna(subset=['Level', rcol]), 'Level', rcol, f'{mname}_Level_{h}d', PPY[h]))
        ALL.extend(evaluate_quantile(t.dropna(subset=['Chg', rcol]), 'Chg', rcol, f'{mname}_Chg_{h}d', PPY[h]))
print(f"  Macro done")

print("--- Validation ---")
report.append("## D. T1 Candidates")
report.append("")
df_all = pd.DataFrame(ALL) if ALL else pd.DataFrame()
t1 = df_all[(df_all.p_val < 0.05) & (df_all.Sharpe > 1.0) & (df_all.PF > 1.30) & (df_all.N > 50)] if len(df_all) > 0 else pd.DataFrame()
print(f"  Total: {len(ALL)}, T1: {len(t1)}")
if len(t1) > 0:
    report.append("| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |")
    report.append("|--------|---|-----------|--------|----|-----|-------|")
    for _, r in t1.sort_values('Sharpe', ascending=False).iterrows():
        report.append(f"| {r['Signal']} | {r['N']} | {r['Mean_Ret%']:.3f}% | {r['Sharpe']:.2f} | {r['PF']:.2f} | {r['WR%']:.1f}% | {r['p_val']:.4f} |")
    report.append("")
    # Walk-forward
    wf_pass = 0
    PERIODS = {'2000-2006':'2000-01-01~2006-12-31', '2007-2013':'2007-01-01~2013-12-31', '2014-2019':'2014-01-01~2019-12-31', '2020-2026':'2020-01-01~2026-12-31'}
    for _, c in t1.iterrows():
        sig = c['Signal']; ok = True
        rcol = None
        for h, rc in HORIZONS.items():
            if f'_{h}d' in sig: rcol = rc; break
        if not rcol: continue
        for pname, pr in PERIODS.items():
            ps, pe = pr.split('~')
            m = df.loc[ps:pe, rcol] if ps in df.index or pe in df.index else df[(df.index >= ps)&(df.index <= pe)][rcol]
            m = m.dropna()
            if len(m) > 5 and m.mean() <= 0: ok = False; break
        if ok: wf_pass += 1
    report.append(f"**Walk-Forward Pass:** {wf_pass}/{len(t1)}")
    
    oos_pass = 0
    train = df.index < '2013-01-01'; test = df.index >= '2013-01-01'
    for _, c in t1.iterrows():
        rcol = None
        for h, rc in HORIZONS.items():
            if f'_{h}d' in sig: rcol = rc; break
        if rcol:
            test_g = df.loc[test, rcol].dropna()
            if len(test_g) > 10 and test_g.mean() > 0: oos_pass += 1
    report.append(f"**OOS Pass:** {oos_pass}/{len(t1)}")
    report.append("")
    if wf_pass > 0 and oos_pass > 0:
        report.append("**Verdict:** Some external driver signals survive screening — require MC validation.")
    else:
        report.append("**Verdict:** No robust external driver edge found.")
else:
    report.append("**No T1 candidates found.**")

report.append("")
report.append("---")
report.append("*Generated by research/oil/scripts/oil_008_external_drivers.py*")
with open(REPORTS_DIR / 'OIL-008_External_Drivers.md', 'w') as f:
    f.write('\n'.join(report))
print("OIL-008 COMPLETE")
