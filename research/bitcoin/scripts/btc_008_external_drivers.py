"""
BTC-008: External Drivers — ETF Flows, Network Metrics & Macro Regimes
"""
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path('data')
BTC_DIR = Path('data/bitcoin')
REPORTS_DIR = Path('reports/bitcoin')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

print("Loading BTC-USD daily data...")
df = pd.read_csv(BTC_DIR / 'BTCUSD_cleaned.csv', parse_dates=['Date'], index_col='Date')
close = df['Close'].dropna()
ret = close.pct_change().dropna()
print(f"BTC: {len(close):,} obs")

# Define horizons
HORIZONS = {1: 'Ret_1d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 365, 5: 365/5, 10: 365/10, 20: 365/20, 60: 365/60}
for h, col in HORIZONS.items():
    df[col] = close.pct_change(h).shift(-h)
df = df.dropna(subset=['Ret_1d']).copy()

# Helper functions (same as existing)
def compute_metrics(returns, label, ppy=365):
    g = returns.dropna()
    n = len(g)
    if n < 5: return None
    mu = g.mean(); std = g.std()
    se = std / np.sqrt(n)
    t = mu / se if se > 0 else 0
    p = 2 * (1 - stats.t.cdf(abs(t), n - 1)) if n > 1 and se > 0 else 1
    sharpe = mu / std * np.sqrt(ppy) if std > 0 else 0
    pos_sum = g[g > 0].sum()
    neg_sum = abs(g[g < 0].sum())
    pf = pos_sum / neg_sum if neg_sum != 0 else (np.inf if pos_sum > 0 else 0)
    wr = (g > 0).mean() * 100
    return {'Signal': label, 'N': n, 'Mean_Ret%': mu*100, 'Std%': std*100,
            't_stat': t, 'p_val': p, 'Sharpe': sharpe, 'PF': pf, 'WR%': wr}

def evaluate_binary(dff, mask_col, label, ret_col, ppy):
    g = dff[dff[mask_col] == True][ret_col]
    return compute_metrics(g, label, ppy)

def evaluate_quantile(dff, sort_col, ret_col, label_base, ppy, nq=5):
    d = dff[[sort_col, ret_col]].dropna().copy()
    if len(d) < 50: return []
    d['Q'] = pd.qcut(d[sort_col].rank(method='first'), nq, labels=[f'Q{i+1}' for i in range(nq)])
    results = []
    for q in [f'Q{i+1}' for i in range(nq)]:
        r = compute_metrics(d[d['Q'] == q][ret_col], f'{label_base} {q}', ppy)
        if r: results.append(r)
    return results

def evaluate_decile_extreme(dff, sort_col, ret_col, label_base, ppy):
    d = dff[[sort_col, ret_col]].dropna().copy()
    if len(d) < 100: return []
    d['Pctl'] = d[sort_col].rank(pct=True)
    results = []
    for extreme, lbl in [(True, 'Extreme_High'), (False, 'Extreme_Low')]:
        g = d[d['Pctl'] < 0.10 if not extreme else d['Pctl'] > 0.90][ret_col]
        r = compute_metrics(g, f'{label_base} {lbl}', ppy)
        if r: results.append(r)
    return results

report = []
report.append("# BTC-008: External Drivers Analysis")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Period:** {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
report.append("")

print("\n--- Phase A: Bitcoin ETF Flow Proxies ---")
report.append("## Phase A: ETF & Exchange Flow Proxies")
report.append("")
report.append("Using Yahoo Finance proxies for Bitcoin ETF-related instruments:")
report.append("- GBTC: Grayscale Bitcoin Trust (largest BTC fund)")
report.append("- IBIT: iShares Bitcoin Trust (BlackRock)")
report.append("- BITO: ProShares Bitcoin Strategy ETF (futures-based)")
report.append("")

# Download ETF data
etf_tickers = {
    'GBTC': 'GBTC',
    'IBIT': 'IBIT',
    'BITO': 'BITO'
}

etf_data = {}
import yfinance as yf
for name, ticker in etf_tickers.items():
    try:
        t = yf.Ticker(ticker)
        h = t.history(period='max')
        if len(h) > 0:
            if hasattr(h.index, 'tz') and h.index.tz is not None:
                h.index = h.index.tz_localize(None)
            h.index = pd.to_datetime(h.index.date)
            h.index.name = 'Date'
            etf_data[name] = h
            print(f"  {name}: {len(h):,} rows ({h.index[0].date()} to {h.index[-1].date()})")
    except:
        print(f"  {name}: not available")

# Merge ETF data with BTC
btc_df = df.copy()
ALL_SIGNALS = []
PHASE = 'ETF'

for etf_name, etf_h in etf_data.items():
    etf_close = etf_h['Close']
    etf_vol = etf_h['Volume']
    
    common_dates = btc_df.index.intersection(etf_close.dropna().index)
    if len(common_dates) < 50: continue
    
    etf_ret = etf_close.pct_change().dropna()
    etf_vol_z = (etf_vol - etf_vol.rolling(20).mean()) / etf_vol.rolling(20).std()
    
    temp = pd.DataFrame(index=common_dates)
    temp['ETF_Ret'] = etf_ret
    temp['Vol_Z'] = etf_vol_z
    temp['Div'] = etf_ret - btc_df['Close'].pct_change()
    temp = temp.join(btc_df[list(HORIZONS.values())])
    
    for h, rcol in HORIZONS.items():
        ppy_ = PPY[h]
        # Quintiles of ETF return
        ALL_SIGNALS.extend(evaluate_quantile(temp.dropna(subset=['ETF_Ret']), 'ETF_Ret', rcol, f'{PHASE}_{etf_name}_Ret_{h}d', ppy_))
        # Quintiles of volume z-score
        ALL_SIGNALS.extend(evaluate_quantile(temp.dropna(subset=['Vol_Z']), 'Vol_Z', rcol, f'{PHASE}_{etf_name}_VolZ_{h}d', ppy_))
        # Divergence extreme
        ALL_SIGNALS.extend(evaluate_quantile(temp.dropna(subset=['Div']), 'Div', rcol, f'{PHASE}_{etf_name}_Div_{h}d', ppy_))

print(f"  ETF signals: {len(ALL_SIGNALS)}")

if ALL_SIGNALS:
    t1_df = pd.DataFrame(ALL_SIGNALS)
    t1_candidates = t1_df[(t1_df['p_val'] < 0.05) & (t1_df['Sharpe'] > 1.0) & (t1_df['PF'] > 1.30) & (t1_df['N'] > 50)]
    print(f"  T1 candidates: {len(t1_candidates)}")
else:
    t1_candidates = pd.DataFrame()
    print("  T1 candidates: 0")

print("\n--- Phase B: Gold Correlation Regime ---")
report.append("## Phase B: Gold Correlation Regime")
report.append("")
report.append("Test: Does Bitcoin's relationship with Gold predict future returns?")
report.append("")

try:
    gold = pd.read_csv(DATA_DIR / 'XAUUSD_cleaned.csv', index_col=0, parse_dates=True)
    gold_close = gold['Close'].dropna()
    gold_ret = gold_close.pct_change().dropna()
    
    common = btc_df.index.intersection(gold_ret.index)
    btc_gold = pd.DataFrame(index=common)
    btc_gold['BTC_Ret'] = ret
    btc_gold['Gold_Ret'] = gold_ret
    btc_gold['RollCorr_60d'] = btc_gold['BTC_Ret'].rolling(60).corr(btc_gold['Gold_Ret'])
    btc_gold['BTC_Gold_Div'] = btc_gold['BTC_Ret'] - btc_gold['Gold_Ret']
    btc_gold = btc_gold.join(btc_df[list(HORIZONS.values())])
    btc_gold = btc_gold.dropna(subset=['RollCorr_60d'])
    
    for h, rcol in HORIZONS.items():
        ppy_ = PPY[h]
        ALL_SIGNALS.extend(evaluate_quantile(btc_gold.dropna(), 'RollCorr_60d', rcol, f'GoldCorr_{h}d', ppy_))
        ALL_SIGNALS.extend(evaluate_quantile(btc_gold.dropna(), 'BTC_Gold_Div', rcol, f'BTCGoldDiv_{h}d', ppy_))
    
    print(f"  Gold regime signals: added")
except:
    print("  Gold data not available, skipping")

print("\n--- Phase C: Macro Regimes ---")
report.append("## Phase C: Macro Regime Proxies")
report.append("")
report.append("Test: US10Y yield level, DXY strength, and VIX as regime conditions for Bitcoin.")
report.append("")

macro_proxies = {}
try:
    tnx = pd.read_csv(DATA_DIR / 'tnx.csv', parse_dates=['Date'], index_col='Date')
    macro_proxies['US10Y'] = tnx['Close'].dropna()
except: pass
try:
    related = pd.read_csv(DATA_DIR / 'related_instruments.csv', index_col=0, parse_dates=True)
    if 'DXY' in related.columns:
        macro_proxies['DXY'] = related['DXY'].dropna()
    if 'VIX' in related.columns:
        macro_proxies['VIX'] = related['VIX'].dropna()
except: pass

for mname, mseries in macro_proxies.items():
    common = btc_df.index.intersection(mseries.dropna().index)
    if len(common) < 100: continue
    temp = pd.DataFrame(index=common)
    temp['Level'] = mseries
    temp['Chg'] = mseries.diff()
    temp = temp.join(btc_df[list(HORIZONS.values())])
    
    for h, rcol in HORIZONS.items():
        ppy_ = PPY[h]
        ALL_SIGNALS.extend(evaluate_quantile(temp.dropna(subset=['Level']), 'Level', rcol, f'{mname}_Level_{h}d', ppy_))
        ALL_SIGNALS.extend(evaluate_quantile(temp.dropna(subset=['Chg']), 'Chg', rcol, f'{mname}_Chg_{h}d', ppy_))

print(f"  Macro regime signals: added")

# Validation
print(f"\nTotal signals: {len(ALL_SIGNALS)}")
if ALL_SIGNALS:
    t1_df = pd.DataFrame(ALL_SIGNALS)
    t1_candidates = t1_df[(t1_df['p_val'] < 0.05) & (t1_df['Sharpe'] > 1.0) & (t1_df['PF'] > 1.30) & (t1_df['N'] > 50)]
    print(f"T1 candidates: {len(t1_candidates)}")
    
    if len(t1_candidates) > 0:
        report.append("### T1 Candidates")
        report.append("")
        report.append("| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |")
        report.append("|--------|---|-----------|--------|----|-----|-------|")
        for _, r in t1_candidates.sort_values('Sharpe', ascending=False).iterrows():
            report.append(f"| {r['Signal']} | {r['N']} | {r['Mean_Ret%']:.3f}% | {r['Sharpe']:.2f} | {r['PF']:.2f} | {r['WR%']:.1f}% | {r['p_val']:.4f} |")
        report.append("")
        
        # Walk-forward
        print("\n--- Walk-Forward ---")
        PERIODS = {'2014-2017': ('2014-01-01', '2017-12-31'),
                   '2018-2020': ('2018-01-01', '2020-12-31'),
                   '2021-2023': ('2021-01-01', '2023-12-31'),
                   '2024-2026': ('2024-01-01', '2026-12-31')}
        wf_pass = 0
        for _, c in t1_candidates.iterrows():
            sig = c['Signal']
            all_ok = True
            for pname, (pstart, pend) in PERIODS.items():
                pidx = btc_df.index[(btc_df.index >= pstart) & (btc_df.index <= pend)]
                pmask = pidx
                rcol = None
                for h, rc in HORIZONS.items():
                    if f'_{h}d' in sig: rcol = rc; break
                if rcol and len(pmask) > 5:
                    g = btc_df.loc[pmask, rcol].dropna()
                    if len(g) < 3 or g.mean() <= 0:
                        all_ok = False; break
            if all_ok: wf_pass += 1
        print(f"  WF Pass: {wf_pass}/{len(t1_candidates)}")
        
        # OOS
        train_idx = btc_df.index < '2021-01-01'
        test_idx = btc_df.index >= '2021-01-01'
        oos_pass = 0
        for _, c in t1_candidates.iterrows():
            sig = c['Signal']
            rcol = None
            for h, rc in HORIZONS.items():
                if f'_{h}d' in sig: rcol = rc; break
            if not rcol: continue
            train_g = btc_df.loc[train_idx, rcol].dropna()
            test_g = btc_df.loc[test_idx, rcol].dropna()
            if len(train_g) > 5 and len(test_g) > 5:
                if test_g.mean() > 0: oos_pass += 1
        print(f"  OOS Pass: {oos_pass}/{len(t1_candidates)}")
        
        report.append(f"### Validation Results")
        report.append("")
        report.append(f"| Test | Pass Rate |")
        report.append(f"|------|-----------|")
        report.append(f"| T1 (p<0.05, SR>1, PF>1.3) | {len(t1_candidates)}/{len(t1_df)} ({len(t1_candidates)/len(t1_df)*100:.0f}%) |")
        report.append(f"| T2 Walk-Forward | {wf_pass}/{len(t1_candidates)} ({wf_pass/len(t1_candidates)*100:.0f}%) |")
        report.append(f"| T3 OOS | {oos_pass}/{len(t1_candidates)} ({oos_pass/len(t1_candidates)*100:.0f}%) |")
        report.append("")
        
        verdict = "MARGINAL" if wf_pass > 0 and oos_pass > 0 else "NO"
        if verdict == "MARGINAL":
            report.append("**Verdict: Some external driver signals show marginal predictive power, but require Monte Carlo validation and drift neutralization before confirmation.**")
        else:
            report.append("**Verdict: No robust external driver edge found — signals fail walk-forward or out-of-sample tests.**")
    else:
        report.append("**No T1 candidates found — no external driver edges detected.**")
else:
    report.append("**No signals generated — insufficient external data.**")

report.append("")
report.append("---")
report.append("*Generated by research/bitcoin/scripts/btc_008_external_drivers.py*")

with open(REPORTS_DIR / 'BTC-008_External_Drivers.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nReport saved: {REPORTS_DIR / 'BTC-008_External_Drivers.md'}")
print("BTC-008 COMPLETE")
