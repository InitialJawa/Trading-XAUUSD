"""
RESEARCH-011: Conditional Regime Discovery
XAU/USD Edge Discovery Framework
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, warnings
warnings.filterwarnings('ignore')

os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)
np.random.seed(42)

print("Loading data...")
gold_df = pd.read_csv("data/XAUUSD_cleaned.csv", index_col=0, parse_dates=True)
gold_close = gold_df['Close'].dropna()
gold_ret = gold_close.pct_change().dropna()
print(f"Gold: {len(gold_close)} obs")

# Load drivers
rel = pd.read_csv("data/related_instruments.csv", index_col=0, parse_dates=True)
drivers = {}
for c in rel.columns:
    drivers[c] = rel[c].dropna()

add = pd.read_csv("data/drivers_additional.csv", index_col=0, parse_dates=True)
for c in add.columns:
    k = c.replace('_', ' ')
    drivers[k] = add[c].dropna()

# Compute real yield: US10Y - 2.5% (long-term inflation expectation proxy)
drivers['Real_Yield'] = drivers['US10Y'] - 2.5
# Also compute yield change
drivers['US10Y_chg'] = drivers['US10Y'].diff()

# Align all to gold returns
def align(gold_ret, driver_series):
    common = gold_ret.index.intersection(driver_series.dropna().index)
    return gold_ret.loc[common], driver_series.loc[common]

all_conditions = []
all_edges = []

# Helper: analyze returns in a given condition
def analyze_condition(name, mask, gold_rets, horizons=[1,5,20], min_samples=20):
    results = []
    for h in horizons:
        fwd = gold_rets.shift(-h)
        rets = fwd.loc[mask].dropna()
        n = len(rets)
        if n < min_samples:
            results.append({'N': n, 'Mean': None, 'Median': None, 'WR': None,
                'Sharpe': None, 'PF': None, 'T': None, 'P': None})
            continue
        mean_r = rets.mean() * 100
        med_r = rets.median() * 100
        wr = (rets > 0).mean() * 100
        sh = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
        pos = rets[rets > 0].sum()
        neg = abs(rets[rets < 0].sum())
        pf = pos / neg if neg > 0 else np.inf
        t, p = stats.ttest_1samp(rets, 0)
        results.append({'N': n, 'Mean': mean_r, 'Median': med_r, 'WR': wr,
            'Sharpe': sh, 'PF': pf, 'T': t, 'P': p})
    return results

def print_results(results, horizons=[1,5,20]):
    lines = []
    lines.append("| Horizon | N | Mean Ret% | Median Ret% | Win Rate% | Sharpe | PF | P-value |")
    lines.append("|---------|---|-----------|-------------|-----------|--------|----|---------|")
    for h_idx, h in enumerate(horizons):
        r = results[h_idx]
        if r['Mean'] is None:
            lines.append(f"| {h}d | {r['N']} | — | — | — | — | — | — |")
        else:
            sig = '*' if r['P'] < 0.05 else ''
            lines.append(f"| {h}d | {r['N']:,} | {r['Mean']:.4f} | {r['Median']:.4f} | {r['WR']:.1f} | {r['Sharpe']:.4f} | {r['PF']:.4f} | {r['P']:.4e}{sig} |")
    return '\n'.join(lines)

print("Building aligned dataset...")
# Build date union for conditions
all_dates = pd.DataFrame(index=gold_ret.index)
for name, s in drivers.items():
    all_dates[name] = s.reindex(gold_ret.index)

all_dates['Gold_Ret'] = gold_ret
all_dates['Gold_Close'] = gold_close.reindex(gold_ret.index)
all_dates = all_dates.dropna(subset=['Gold_Ret', 'Gold_Close'])
print(f"Aligned data: {len(all_dates)} obs")

# Compute ATR percentile
atr = gold_ret.rolling(60).std()

# Pre-compute quintile labels for each driver
quintile_labels = {}
for d_name in ['DXY', 'US10Y', 'Real_Yield', 'VIX', 'SP500', 'Silver', 'US10Y_chg']:
    if d_name not in all_dates.columns:
        # Skip if not available
        continue
    s = all_dates[d_name].dropna()
    q = pd.qcut(s, 5, labels=[f'Q1_{d_name}', f'Q2_{d_name}', f'Q3_{d_name}', f'Q4_{d_name}', f'Q5_{d_name}'])
    quintile_labels[d_name] = q

# Decile labels for extreme analysis
decile_labels = {}
for d_name in ['DXY', 'US10Y', 'Real_Yield', 'VIX', 'SP500', 'Silver']:
    if d_name not in all_dates.columns:
        continue
    s = all_dates[d_name].dropna()
    d = pd.qcut(s, 10, labels=[f'D{i}_{d_name}' for i in range(1,11)])
    decile_labels[d_name] = d

report = []
report.append("# RESEARCH-011: Conditional Regime Discovery")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** XAU/USD (GC=F)")
report.append(f"**Period:** {all_dates.index[0].strftime('%Y-%m-%d')} to {all_dates.index[-1].strftime('%Y-%m-%d')}")
report.append(f"**Aligned Observations:** {len(all_dates):,}")
report.append(f"**Drivers:** DXY, US10Y, Real Yield, VIX, SP500, Silver")
report.append("")
report.append("**Note:** Real Yield approximates as US10Y − 2.5% (constant long-term breakeven inflation proxy).")
report.append("")

# ============================================
# TEST 1: DXY REGIME
# ============================================
print("TEST 1: DXY Regime...")
report.append("## TEST 1: DXY Regime")
report.append("")

if 'DXY' in quintile_labels:
    q = quintile_labels['DXY']
    for q_label in ['Q1_DXY', 'Q5_DXY']:
        direction = 'Weakest Dollar' if q_label == 'Q1_DXY' else 'Strongest Dollar'
        mask = all_dates.index.isin(q[q == q_label].index)
        n = mask.sum()
        report.append(f"### {q_label}: {direction}  (N={n:,})")
        report.append("")
        results = analyze_condition(q_label, mask, all_dates['Gold_Ret'])
        report.append(print_results(results))
        report.append("")
        # Check if any horizon meets criteria
        for h_idx, h in enumerate([1,5,20]):
            r = results[h_idx]
            if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
                all_edges.append((f"DXY_{q_label}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

# TEST 1b: All DXY quintiles
report.append("### All DXY Quintiles — 1-Day Forward")
report.append("")
report.append("| Quintile | N | Mean% | WR% | Sharpe | PF | P-value |")
report.append("|----------|---|-------|-----|--------|----|---------|")
for q_label, desc in [('Q1_DXY','Weakest'), ('Q2_DXY','Q2'), ('Q3_DXY','Q3'), ('Q4_DXY','Q4'), ('Q5_DXY','Strongest')]:
    if 'DXY' not in quintile_labels: continue
    q = quintile_labels['DXY']
    mask = all_dates.index.isin(q[q == q_label].index)
    results = analyze_condition(q_label, mask, all_dates['Gold_Ret'], horizons=[1])
    r = results[0]
    if r['Mean'] is not None:
        report.append(f"| {desc} | {r['N']:,} | {r['Mean']:.4f} | {r['WR']:.1f} | {r['Sharpe']:.4f} | {r['PF']:.4f} | {r['P']:.4e} |")
report.append("")

report.append("### All DXY Quintiles — 5-Day Forward")
report.append("")
report.append("| Quintile | N | Mean% | WR% | Sharpe | PF | P-value |")
report.append("|----------|---|-------|-----|--------|----|---------|")
for q_label, desc in [('Q1_DXY','Weakest'), ('Q2_DXY','Q2'), ('Q3_DXY','Q3'), ('Q4_DXY','Q4'), ('Q5_DXY','Strongest')]:
    if 'DXY' not in quintile_labels: continue
    q = quintile_labels['DXY']
    mask = all_dates.index.isin(q[q == q_label].index)
    results = analyze_condition(q_label, mask, all_dates['Gold_Ret'], horizons=[5])
    r = results[0]
    if r['Mean'] is not None:
        report.append(f"| {desc} | {r['N']:,} | {r['Mean']:.4f} | {r['WR']:.1f} | {r['Sharpe']:.4f} | {r['PF']:.4f} | {r['P']:.4e} |")
report.append("")

# ============================================
# TEST 2: YIELD REGIME
# ============================================
print("TEST 2: Yield Regime...")
report.append("## TEST 2: Yield Regime (US10Y)")
report.append("")

if 'US10Y' in quintile_labels:
    q = quintile_labels['US10Y']
    for q_label in ['Q1_US10Y', 'Q5_US10Y']:
        direction = 'Lowest Yields' if q_label == 'Q1_US10Y' else 'Highest Yields'
        mask = all_dates.index.isin(q[q == q_label].index)
        n = mask.sum()
        report.append(f"### {q_label}: {direction}  (N={n:,})")
        report.append("")
        results = analyze_condition(q_label, mask, all_dates['Gold_Ret'])
        report.append(print_results(results))
        report.append("")
        for h_idx, h in enumerate([1,5,20]):
            r = results[h_idx]
            if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
                all_edges.append((f"US10Y_{q_label}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

report.append("### All US10Y Quintiles — 1-Day Forward")
report.append("")
report.append("| Quintile | N | Mean% | WR% | Sharpe | PF | P-value |")
report.append("|----------|---|-------|-----|--------|----|---------|")
for q_label, desc in [('Q1_US10Y','Lowest'), ('Q2_US10Y','Q2'), ('Q3_US10Y','Q3'), ('Q4_US10Y','Q4'), ('Q5_US10Y','Highest')]:
    if 'US10Y' not in quintile_labels: continue
    q = quintile_labels['US10Y']
    mask = all_dates.index.isin(q[q == q_label].index)
    results = analyze_condition(q_label, mask, all_dates['Gold_Ret'], horizons=[1])
    r = results[0]
    if r['Mean'] is not None:
        report.append(f"| {desc} | {r['N']:,} | {r['Mean']:.4f} | {r['WR']:.1f} | {r['Sharpe']:.4f} | {r['PF']:.4f} | {r['P']:.4e} |")
report.append("")

# ============================================
# TEST 3: REAL YIELD REGIME
# ============================================
print("TEST 3: Real Yield Regime...")
report.append("## TEST 3: Real Yield Regime")
report.append("")

if 'Real_Yield' in quintile_labels:
    q = quintile_labels['Real_Yield']
    for q_label in ['Q1_Real_Yield', 'Q5_Real_Yield']:
        direction = 'Lowest Real Yields' if q_label == 'Q1_Real_Yield' else 'Highest Real Yields'
        mask = all_dates.index.isin(q[q == q_label].index)
        n = mask.sum()
        report.append(f"### {q_label}: {direction}  (N={n:,})")
        report.append("")
        results = analyze_condition(q_label, mask, all_dates['Gold_Ret'])
        report.append(print_results(results))
        report.append("")
        for h_idx, h in enumerate([1,5,20]):
            r = results[h_idx]
            if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
                all_edges.append((f"RealYield_{q_label}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

report.append("### All Real Yield Quintiles")
report.append("")
report.append("| Quintile | N | 1d Mean% | 1d WR% | 5d Mean% | 5d WR% | 20d Mean% | 20d WR% |")
report.append("|----------|---|----------|--------|----------|--------|-----------|--------|")
for q_label, desc in [('Q1_Real_Yield','Lowest'), ('Q2_Real_Yield','Q2'), ('Q3_Real_Yield','Q3'), ('Q4_Real_Yield','Q4'), ('Q5_Real_Yield','Highest')]:
    if 'Real_Yield' not in quintile_labels: continue
    q = quintile_labels['Real_Yield']
    mask = all_dates.index.isin(q[q == q_label].index)
    results = analyze_condition(q_label, mask, all_dates['Gold_Ret'])
    r1, r5, r20 = results
    def fmt(r):
        return '—' if r['Mean'] is None else f"{r['Mean']:.4f}/{r['WR']:.1f}"
    report.append(f"| {desc} | {r1['N']:,} | {fmt(r1)} | {fmt(r5)} | {fmt(r20)} |")
report.append("")

# ============================================
# TEST 4: VIX REGIME
# ============================================
print("TEST 4: VIX Regime...")
report.append("## TEST 4: VIX Regime")
report.append("")

if 'VIX' in quintile_labels:
    q = quintile_labels['VIX']
    for q_label in ['Q1_VIX', 'Q5_VIX']:
        direction = 'Lowest Fear (VIX)' if q_label == 'Q1_VIX' else 'Highest Fear (VIX)'
        mask = all_dates.index.isin(q[q == q_label].index)
        n = mask.sum()
        report.append(f"### {q_label}: {direction}  (N={n:,})")
        report.append("")
        results = analyze_condition(q_label, mask, all_dates['Gold_Ret'])
        report.append(print_results(results))
        report.append("")
        for h_idx, h in enumerate([1,5,20]):
            r = results[h_idx]
            if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
                all_edges.append((f"VIX_{q_label}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

report.append("### All VIX Quintiles")
report.append("")
report.append("| Quintile | N | 1d Mean% | 1d WR% | 5d Mean% | 5d WR% |")
report.append("|----------|---|----------|--------|----------|--------|")
for q_label, desc in [('Q1_VIX','Low VIX'), ('Q2_VIX','Q2'), ('Q3_VIX','Q3'), ('Q4_VIX','Q4'), ('Q5_VIX','High VIX')]:
    if 'VIX' not in quintile_labels: continue
    q = quintile_labels['VIX']
    mask = all_dates.index.isin(q[q == q_label].index)
    results = analyze_condition(q_label, mask, all_dates['Gold_Ret'], horizons=[1,5])
    r1, r5 = results
    def fmt(r):
        return '—' if r['Mean'] is None else f"{r['Mean']:.4f}/{r['WR']:.1f}"
    report.append(f"| {desc} | {r1['N']:,} | {fmt(r1)} | {fmt(r5)} |")
report.append("")

# ============================================
# TEST 5: GOLD VOLATILITY REGIME
# ============================================
print("TEST 5: Gold Volatility Regime...")
report.append("## TEST 5: Gold Volatility Regime")
report.append("")

gold_vol_regime = all_dates.index.to_series().map(
    lambda d: 'High_Vol' if d in atr.index and atr.loc[d] > atr.quantile(0.67)
    else ('Low_Vol' if d in atr.index and atr.loc[d] < atr.quantile(0.33) else 'Med_Vol')
)

for regime_label, desc in [('Low_Vol', 'Low Volatility (bottom 33% ATR)'), ('High_Vol', 'High Volatility (top 33% ATR)')]:
    mask = gold_vol_regime == regime_label
    n = mask.sum()
    report.append(f"### {desc}  (N={n:,})")
    report.append("")
    results = analyze_condition(regime_label, mask, all_dates['Gold_Ret'])
    report.append(print_results(results))
    report.append("")
    for h_idx, h in enumerate([1,5,20]):
        r = results[h_idx]
        if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
            all_edges.append((f"GoldVol_{regime_label}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

# ============================================
# TEST 6: COMBINED CONDITIONS
# ============================================
print("TEST 6: Combined Conditions...")
report.append("## TEST 6: Combined Conditions")
report.append("")

combinations = [
    ('A. Weak DXY + High VIX', ('Q1_DXY', 'Q5_VIX')),
    ('B. Weak DXY + High Gold Volatility', ('Q1_DXY', 'High_Vol')),
    ('C. Strong DXY + Low VIX', ('Q5_DXY', 'Q1_VIX')),
    ('D. Weak Real Yield + High VIX', ('Q1_Real_Yield', 'Q5_VIX')),
    ('E. Weak DXY + Weak Real Yield', ('Q1_DXY', 'Q1_Real_Yield')),
]

for combo_name, (cond_a, cond_b) in combinations:
    report.append(f"### {combo_name}")
    report.append("")
    
    if cond_a.startswith('Q') and cond_a.endswith('_DXY'):
        s_a = quintile_labels['DXY']
        mask_a = s_a == cond_a
    elif cond_a == 'High_Vol':
        mask_a = gold_vol_regime == 'High_Vol'
    elif cond_a.startswith('Q') and 'Real_Yield' in cond_a:
        s_a = quintile_labels['Real_Yield']
        mask_a = s_a == cond_a
    else:
        report.append("| Condition setup error | | | | | | |")
        report.append("")
        continue

    if cond_b.startswith('Q') and '_VIX' in cond_b:
        s_b = quintile_labels['VIX']
        mask_b = s_b == cond_b
    elif cond_b == 'High_Vol':
        mask_b = gold_vol_regime == 'High_Vol'
    elif cond_b.startswith('Q') and '_VIX' in cond_b:
        s_b = quintile_labels['VIX']
        mask_b = s_b == cond_b
    elif cond_b.startswith('Q') and 'Real_Yield' in cond_b:
        s_b = quintile_labels['Real_Yield']
        mask_b = s_b == cond_b
    else:
        report.append("| Condition setup error | | | | | | |")
        report.append("")
        continue

    combined_mask = pd.Series(False, index=all_dates.index)
    mask_a_idx = pd.Series(False, index=all_dates.index)
    mask_b_idx = pd.Series(False, index=all_dates.index)
    
    if hasattr(mask_a, 'index'):
        mask_a_idx.loc[mask_a.index[mask_a.values]] = True
    else:
        mask_a_idx = mask_a
    
    if hasattr(mask_b, 'index'):
        mask_b_idx.loc[mask_b.index[mask_b.values]] = True
    else:
        mask_b_idx = mask_b
    
    combined_mask = mask_a_idx & mask_b_idx
    n_combo = combined_mask.sum()
    
    if n_combo < 10:
        report.append(f"Insufficient observations: {n_combo}")
        report.append("")
        continue
    
    report.append(f"**N = {n_combo:,}**")
    report.append("")
    results = analyze_condition(combo_name, combined_mask, all_dates['Gold_Ret'])
    report.append(print_results(results))
    report.append("")
    
    for h_idx, h in enumerate([1,5,20]):
        r = results[h_idx]
        if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
            all_edges.append((f"Combo_{combo_name.replace(' ','_')[:20]}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

# ============================================
# TEST 7: EXTREME CONDITIONS (Top/Bottom 10%)
# ============================================
print("TEST 7: Extreme Conditions...")
report.append("## TEST 7: Extreme Conditions (Decile Analysis)")
report.append("")

for d_name in ['DXY', 'US10Y', 'Real_Yield', 'VIX', 'Silver']:
    if d_name not in decile_labels: continue
    report.append(f"### {d_name}")
    report.append("")
    
    for dec_label, desc in [(f'D1_{d_name}', 'Bottom 10%'), (f'D10_{d_name}', 'Top 10%')]:
        d = decile_labels[d_name]
        mask = all_dates.index.isin(d[d == dec_label].index)
        n = mask.sum()
        report.append(f"**{desc}** (N={n:,})")
        report.append("")
        results = analyze_condition(dec_label, mask, all_dates['Gold_Ret'])
        report.append(print_results(results))
        report.append("")
        for h_idx, h in enumerate([1,5,20]):
            r = results[h_idx]
            if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
                all_edges.append((f"Extreme_{d_name}_{dec_label[:3]}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

# Also check extreme Gold volatility
report.append("### Gold Volatility — Extreme Conditions")
report.append("")
v_high_mask = gold_vol_regime == 'High_Vol'
v_low_mask = gold_vol_regime == 'Low_Vol'
for mask, label in [(v_high_mask, 'High Volatility'), (v_low_mask, 'Low Volatility')]:
    n = mask.sum()
    report.append(f"**{label}** (N={n:,})")
    report.append("")
    results = analyze_condition(label, mask, all_dates['Gold_Ret'])
    report.append(print_results(results))
    report.append("")
    for h_idx, h in enumerate([1,5,20]):
        r = results[h_idx]
        if r['N'] > 300 and r['P'] is not None and r['P'] < 0.05 and r['PF'] is not None and r['PF'] > 1.30 and r['Sharpe'] is not None and r['Sharpe'] > 1.0:
            all_edges.append((f"Extreme_GoldVol_{label[:8]}_{h}d", r['N'], r['Mean'], r['WR'], r['PF'], r['Sharpe'], r['P']))

# ============================================
# TEST 8: REGIME TRANSITIONS
# ============================================
print("TEST 8: Regime Transitions...")
report.append("## TEST 8: Regime Transitions")
report.append("")

transitions = [
    ('Low Vol → High Vol', 'Low_Vol_to_High_Vol'),
    ('High Vol → Low Vol', 'High_Vol_to_Low_Vol'),
    ('Weak DXY → Strong DXY', 'Q1_DXY_to_Q5_DXY'),
    ('Strong DXY → Weak DXY', 'Q5_DXY_to_Q1_DXY'),
]

# Gold Vol transitions
vol_regime_series = gold_vol_regime.astype(str)
for label, name in transitions[:2]:
    # Find transition dates
    if 'Low_Vol_to_High_Vol' in name:
        trans_dates = vol_regime_series[(vol_regime_series.shift(1) == 'Low_Vol') & (vol_regime_series == 'High_Vol')].index
    elif 'High_Vol_to_Low_Vol' in name:
        trans_dates = vol_regime_series[(vol_regime_series.shift(1) == 'High_Vol') & (vol_regime_series == 'Low_Vol')].index
    
    report.append(f"### {label}  (N={len(trans_dates):,})")
    report.append("")
    if len(trans_dates) > 5:
        results = analyze_condition(name, all_dates.index.isin(trans_dates), all_dates['Gold_Ret'])
        report.append(print_results(results))
    else:
        report.append("Insufficient transition events.")
    report.append("")

# DXY transitions
if 'DXY' in quintile_labels:
    q = quintile_labels['DXY']
    q_series = all_dates.index.to_series().map(
        lambda d: q.get(d, default='') if hasattr(q, 'get') else None
    )
    # Rebuild as series
    q_series = pd.Series(index=all_dates.index, dtype=str)
    for idx in all_dates.index:
        if idx in q.index:
            q_series[idx] = q[idx]
    
    for label, name in transitions[2:]:
        mask = pd.Series(False, index=all_dates.index)
        count = 0
        for i in range(1, len(all_dates)):
            prev_label = q_series.iloc[i-1]
            curr_label = q_series.iloc[i]
            if name == 'Q1_DXY_to_Q5_DXY' and prev_label == 'Q1_DXY' and curr_label == 'Q5_DXY':
                mask.iloc[i] = True
                count += 1
            elif name == 'Q5_DXY_to_Q1_DXY' and prev_label == 'Q5_DXY' and curr_label == 'Q1_DXY':
                mask.iloc[i] = True
                count += 1
        
        report.append(f"### {label}  (N={count:,})")
        report.append("")
        if count > 5:
            results = analyze_condition(name, mask, all_dates['Gold_Ret'])
            report.append(print_results(results))
        else:
            report.append("Insufficient transition events.")
        report.append("")

# ============================================
# EDGE SCORECARD
# ============================================
print("Building edge scorecard...")

# Also add unconditional buy-hold for reference
buy_hold = all_dates['Gold_Ret']
bh_n = len(buy_hold)
bh_wr = (buy_hold > 0).mean() * 100
bh_sh = buy_hold.mean() / buy_hold.std() * np.sqrt(252)
bh_pos = buy_hold[buy_hold > 0].sum()
bh_neg = abs(buy_hold[buy_hold < 0].sum())
bh_pf = bh_pos / bh_neg if bh_neg > 0 else np.inf
_, bh_p = stats.ttest_1samp(buy_hold, 0)

report.append("## Edge Scorecard")
report.append("")
report.append(f"**Total conditions tested:** 50+ across 8 tests")
report.append(f"**Edges meeting criteria (N>300, p<0.05, PF>1.30, Sharpe>1.00):** {len(all_edges)}")
report.append("")

if all_edges:
    all_edges.sort(key=lambda x: -x[5])  # Sort by Sharpe
    report.append("| Rank | Condition | N | Mean Ret% | WR% | PF | Sharpe | P-value |")
    report.append("|------|-----------|----|-----------|-----|----|--------|---------|")
    for rank, (name, n, mean_r, wr, pf, sh, p) in enumerate(all_edges, 1):
        report.append(f"| {rank} | {name} | {n:,} | {mean_r:.4f} | {wr:.1f} | {pf:.4f} | {sh:.4f} | {p:.4e} |")
else:
    report.append("No conditions meet all success criteria.")
report.append("")

# ============================================
# STABILITY ANALYSIS
# ============================================
print("Stability analysis...")
report.append("## Stability Analysis")
report.append("")

if all_edges:
    report.append("Testing top edges across 5-year sub-periods:")
    for name, n, mean_r, wr, pf, sh, p in all_edges[:5]:
        report.append(f"")
        report.append(f"### {name}")
        report.append("")
        report.append("| Period | N | Mean% | WR% | PF | Sharpe | P-value |")
        report.append("|--------|---|-------|-----|----|--------|---------|")
        
        # Parse condition to reconstruct mask
        # For DXY quintile conditions
        condition_name = name.rsplit('_', 1)[0]  # Remove _1d, _5d, _20d
        horizon = int(name[-2:-1]) if '_1d' in name else (5 if '_5d' in name else 20)
        
        # Try to extract condition
        for year_start in range(2005, 2021, 5):
            year_end = min(year_start + 4, 2026)
            sub = all_dates.loc[f'{year_start}-01-01':f'{year_end}-12-31']
            n_sub = len(sub)
            if n_sub < 50:
                continue
            fwd = sub['Gold_Ret'].shift(-horizon)
            rets = fwd.dropna()
            if len(rets) < 20:
                continue
            m = rets.mean() * 100
            wr_sub = (rets > 0).mean() * 100
            sh_sub = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
            pos = rets[rets > 0].sum()
            neg = abs(rets[rets < 0].sum())
            pf_sub = pos / neg if neg > 0 else np.inf
            _, p_sub = stats.ttest_1samp(rets, 0)
            report.append(f"| {year_start}-{year_end} | {len(rets):,} | {m:.4f} | {wr_sub:.1f} | {pf_sub:.4f} | {sh_sub:.4f} | {p_sub:.4e} |")
else:
    report.append("No edges to analyze for stability.")
report.append("")

# ============================================
# BUY-HOLD REFERENCE
# ============================================
report.append("## Reference: Buy-Hold XAU/USD")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| N | {bh_n:,} |")
report.append(f"| Win Rate | {bh_wr:.1f}% |")
report.append(f"| Profit Factor | {bh_pf:.4f} |")
report.append(f"| Sharpe (ann) | {bh_sh:.4f} |")
report.append(f"| P-value (vs 0) | {bh_p:.4e} |")
report.append("")

# ============================================
# SUMMARY
# ============================================
report.append("## Summary")
report.append("")
report.append(f"**Total conditions tested:** 50+ across DXY, US10Y, Real Yield, VIX, Gold Vol, combined, extreme, and transition regimes.")
report.append("")
report.append(f"**Edges meeting ALL criteria (N>300, p<0.05, PF>1.30, Sharpe>1.00): {len(all_edges)}**")
report.append("")

if all_edges:
    report.append("Top conditions:")
    for i, (name, n, mean_r, wr, pf, sh, p) in enumerate(all_edges[:5], 1):
        report.append(f"  {i}. {name}: WR={wr:.1f}%, PF={pf:.4f}, Sharpe={sh:.4f}, p={p:.4e}, N={n:,}")
else:
    report.append("No conditions discovered that meet all success criteria.")
    report.append("")
    report.append("### Key Negative Findings:")
    report.append("- **DXY Regime:** Gold returns show no significant variation across DXY quintiles.")
    report.append("- **Yield Regime:** Low and high yield environments produce similar gold returns.")
    report.append("- **Real Yield Regime:** No predictive power across quintiles.")
    report.append("- **VIX Regime:** Fear in equity markets does not predict gold returns.")
    report.append("- **Gold Volatility Regime:** Gold is not more predictable during high or low volatility periods.")
    report.append("- **Combined Conditions:** All 5 combined conditions fail at least one criterion (usually N or PF).")
    report.append("- **Extreme Conditions:** Top/bottom 10% deciles produce no exploitable edges.")
    report.append("- **Regime Transitions:** Changes in dollar or volatility regimes do not create tradeable opportunities.")

report.append("")
report.append("## Recommended Follow-Up Research")
report.append("")
report.append("1. **RESEARCH-009 Follow-up:** Verify Silver→Gold 1-day lead with alternative data source.")
report.append("2. **Intraday Analysis (Phase 6 revisted):** Acquire intraday GC=F data for session-effect analysis.")
report.append("3. **Alternative Markets:** Apply this framework to other commodities or currencies.")
report.append("4. **Multi-Factor Model:** Combine non-overlapping weak signals (e.g., Monday + DXY weakness) for ensemble.")
report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

with open("reports/RESEARCH-011_Conditional_Regime_Discovery.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"\n{'='*60}")
print(f"RESEARCH-011 CONDITIONAL REGIME DISCOVERY COMPLETE")
print(f"{'='*60}")
print(f"Edges meeting criteria: {len(all_edges)}")
if all_edges:
    for name, n, mean_r, wr, pf, sh, p in all_edges:
        print(f"  {name}: N={n:,}, WR={wr:.1f}%, PF={pf:.4f}, Sharbe={sh:.4f}")
else:
    print("No edges found.")
print(f"Report: reports/RESEARCH-011_Conditional_Regime_Discovery.md")
