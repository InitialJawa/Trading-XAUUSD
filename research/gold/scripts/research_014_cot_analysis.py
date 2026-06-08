"""RESEARCH-014: COT Positioning Edge Discovery

5 tests to determine whether CFTC COT data contains predictive
information for gold weekly returns.
"""
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

REPORTS_DIR = Path('reports')
REPORTS_DIR.mkdir(exist_ok=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
cot = pd.read_csv('data/gold_cot.csv', parse_dates=['Report_Date_as_YYYY-MM-DD'])
px = pd.read_csv('data/XAUUSD_cleaned.csv', parse_dates=['Date'])

# Sort
cot = cot.sort_values('Report_Date_as_YYYY-MM-DD').reset_index(drop=True)
px = px.sort_values('Date').reset_index(drop=True)

# Weekly gold close: align to Tuesday (COT report date)
px['Weekday'] = px['Date'].dt.weekday
px_tue = px[px['Weekday'] == 1].copy()  # Tuesday=1
if len(px_tue) == 0:
    px_tue = px[px['Weekday'] == 2].copy()  # fallback to Wednesday
    print('  Using Wednesday as proxy for weekly close')

px_tue['Weekly_Close'] = px_tue['Close']
weekly = px_tue[['Date', 'Weekly_Close']].copy()

# Merge COT with weekly gold prices
merged = pd.merge_asof(cot, weekly, left_on='Report_Date_as_YYYY-MM-DD', right_on='Date', direction='nearest', tolerance=pd.Timedelta('3D'))
merged = merged.drop(columns=['Date'])

# Forward returns: 1w, 2w, 4w, 8w
weekly_px = px.set_index('Date')['Close'].resample('W-TUE').last().dropna().to_frame('Close')
weekly_px['Ret_1w'] = weekly_px['Close'].pct_change(1).shift(-1)
weekly_px['Ret_2w'] = weekly_px['Close'].pct_change(2).shift(-2)
weekly_px['Ret_4w'] = weekly_px['Close'].pct_change(4).shift(-4)
weekly_px['Ret_8w'] = weekly_px['Close'].pct_change(8).shift(-8)

merged = merged.merge(weekly_px[['Close', 'Ret_1w', 'Ret_2w', 'Ret_4w', 'Ret_8w']],
                       left_on='Report_Date_as_YYYY-MM-DD', right_index=True, how='left')
merged = merged.dropna(subset=['Ret_1w'])

print(f'Merged COT + Gold: {len(merged)} rows ({merged["Report_Date_as_YYYY-MM-DD"].min()} to {merged["Report_Date_as_YYYY-MM-DD"].max()})')

# ── Helper Functions ───────────────────────────────────────────────────────────

GROUPS = {
    'Commercial': 'Net_Commercial',
    'Managed_Money': 'Net_Managed_Money',
    'Large_Spec': 'Net_Large_Spec',
    'Small_Spec': 'Net_Small_Spec',
}

HORIZONS = {'1w': 'Ret_1w', '2w': 'Ret_2w', '4w': 'Ret_4w', '8w': 'Ret_8w'}

def test_row(g, name, periods_per_year=52):
    n = len(g.dropna())
    mu = g.mean()
    se = g.std() / np.sqrt(n)
    t = mu / se if se > 0 else 0
    p = 2 * (1 - stats.t.cdf(abs(t), n - 1)) if n > 1 and se > 0 else 1
    sharpe = mu / g.std() * np.sqrt(periods_per_year) if g.std() > 0 else 0
    pf = g[g > 0].sum() / abs(g[g < 0].sum()) if g[g < 0].sum() != 0 else np.inf
    wr = (g > 0).mean() * 100
    return pd.Series({
        'Group': name, 'N': n, 'Mean_Ret%': mu * 100,
        'Std%': g.std() * 100, 't_stat': t, 'p_val': p,
        'Sharpe': sharpe, 'Profit_Factor': pf, 'Win_Rate%': wr
    })

HORIZON_PERIODS = {'1w': 52, '2w': 26, '4w': 13, '8w': 6.5}

def quintile_analysis(df, col, ret_col, label, ppy=52):
    df = df[[col, ret_col]].dropna().copy()
    if len(df) < 50:
        return pd.DataFrame()
    df['Quintile'] = pd.qcut(df[col].rank(method='first'), 5, labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
    results = []
    for q, grp in df.groupby('Quintile', observed=True):
        r = test_row(grp[ret_col], f'{label} {q}', ppy)
        results.append(r)
    q1 = df[df['Quintile'] == 'Q1_Low'][ret_col]
    q5 = df[df['Quintile'] == 'Q5_High'][ret_col]
    if len(q1) > 5 and len(q5) > 5:
        t, p = stats.ttest_ind(q5, q1)
        results.append(pd.Series({
            'Group': f'{label} Q5-Q1 diff', 'N': len(q5) + len(q1),
            'Mean_Ret%': (q5.mean() - q1.mean()) * 100, 'Std%': np.nan,
            't_stat': t, 'p_val': p, 'Sharpe': np.nan,
            'Profit_Factor': np.nan, 'Win_Rate%': np.nan
        }))
    return pd.DataFrame(results)

PERCENTILES = {'Net_Commercial': -166136, 'Net_Managed_Money': 98134,
               'Net_Large_Spec': 44650, 'Net_Small_Spec': 23351}

def print_results(results, title):
    print(f'\n{"="*70}')
    print(f'  {title}')
    print(f'{"="*70}')
    if isinstance(results, list) and len(results) > 0:
        results = pd.concat(results, ignore_index=True)
    if isinstance(results, pd.DataFrame) and len(results) > 0:
        for _, r in results.iterrows():
            sig = ' ***' if r['p_val'] < 0.01 else (' **' if r['p_val'] < 0.05 else (' *' if r['p_val'] < 0.10 else ''))
            print(f'  {r["Group"]:<30s} N={r["N"]:<4d}  Ret={r["Mean_Ret%"]:>7.3f}%  '
                  f't={r["t_stat"]:>6.3f}  p={r["p_val"]:>6.4f}{sig}  '
                  f'SR={r["Sharpe"]:>6.2f}  PF={r["Profit_Factor"]:>6.2f}  WR={r["Win_Rate%"]:>5.1f}%')
    elif isinstance(results, pd.DataFrame):
        print('  No results')

def run_test(name, results_df):
    print(f'\n  ✓ {name}: {len(results_df)} results' if len(results_df) > 0 else f'\n  ✗ {name}: empty')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 1: Net Position Level (Quintile Analysis)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#'*70)
print('# TEST 1: Net Position Level - Quintile Analysis')
print('#'*70)

t1_results = []
for gname, gcol in GROUPS.items():
    for hname, rcol in HORIZONS.items():
        ppy = HORIZON_PERIODS[hname]
        qdf = quintile_analysis(merged, gcol, rcol, f'{gname} ({hname})', ppy)
        if len(qdf) > 0:
            t1_results.append(qdf)
t1_all = pd.concat(t1_results, ignore_index=True) if t1_results else pd.DataFrame()
print_results(t1_all, 'TEST 1: Net Position Level')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 2: Position Change (Delta)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#'*70)
print('# TEST 2: Position Change (Delta) - Quintile Analysis')
print('#'*70)

merged_deltas = merged.copy()
for gcol in GROUPS.values():
    merged_deltas[f'{gcol}_D'] = merged_deltas[gcol].diff()

t2_results = []
for gname, gcol in GROUPS.items():
    dcol = f'{gcol}_D'
    for hname, rcol in HORIZONS.items():
        ppy = HORIZON_PERIODS[hname]
        qdf = quintile_analysis(merged_deltas, dcol, rcol, f'D{gname} ({hname})', ppy)
        if len(qdf) > 0:
            t2_results.append(qdf)
t2_all = pd.concat(t2_results, ignore_index=True) if t2_results else pd.DataFrame()
print_results(t2_all, 'TEST 2: Position Change (Delta)')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: Divergence (Commercial vs Managed Money)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#'*70)
print('# TEST 3: Divergence - Commercial vs Managed Money')
print('#'*70)

div = merged.copy()
for gcol in GROUPS.values():
    div[f'{gcol}_Z'] = (div[gcol] - div[gcol].mean()) / div[gcol].std()

# Define divergence: Commercials net short EXTREME, Managed Money net long EXTREME
div['Divergence_Bearish'] = (div['Net_Commercial_Z'] < -1.0) & (div['Net_Managed_Money_Z'] > 1.0)
div['Divergence_Bullish'] = (div['Net_Commercial_Z'] > 1.0) & (div['Net_Managed_Money_Z'] < -1.0)

t3_results = []
for div_type, div_col in [('Bearish Divergence', 'Divergence_Bearish'),
                           ('Bullish Divergence', 'Divergence_Bullish')]:
    div_mask = div[div_col] == True
    no_div_mask = div[div_col] == False
    for hname, rcol in HORIZONS.items():
        g1 = div[div_mask][rcol]; g2 = div[no_div_mask][rcol]
        if len(g1.dropna()) < 5 or len(g2.dropna()) < 5:
            continue
        ppy = HORIZON_PERIODS[hname]
        r1 = test_row(g1, f'{div_type} ({hname})', ppy)
        r2 = test_row(g2, f'No_{div_type} ({hname})', ppy)
        t, p = stats.ttest_ind(g1.dropna(), g2.dropna())
        r3 = pd.Series({'Group': f'{div_type} vs None ({hname})', 'N': len(g1.dropna()) + len(g2.dropna()),
                        'Mean_Ret%': (g1.mean() - g2.mean()) * 100, 'Std%': np.nan,
                        't_stat': t, 'p_val': p, 'Sharpe': np.nan,
                        'Profit_Factor': np.nan, 'Win_Rate%': np.nan})
        t3_results.extend([r1, r2, r3])

t3_all = pd.DataFrame(t3_results) if t3_results else pd.DataFrame()
print_results(t3_all, 'TEST 3: Divergence')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 4: Crowding Analysis (Extreme Percentiles)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#'*70)
print('# TEST 4: Crowding Analysis - Extreme Percentiles')
print('#'*70)

crowd = merged.copy()
for gcol in GROUPS.values():
    crowd[f'{gcol}_Pctl'] = crowd[gcol].rank(pct=True)
    crowd[f'{gcol}_Extreme_Long'] = crowd[f'{gcol}_Pctl'] > 0.90
    crowd[f'{gcol}_Extreme_Short'] = crowd[f'{gcol}_Pctl'] < 0.10

t4_results = []
for gname, gcol in GROUPS.items():
    for extreme_type, extreme_label in [(f'{gcol}_Extreme_Long', 'Extreme Long'),
                                         (f'{gcol}_Extreme_Short', 'Extreme Short')]:
        mask = crowd[extreme_type] == True
        nomask = crowd[extreme_type] == False
        for hname, rcol in HORIZONS.items():
            g1 = crowd[mask][rcol]; g2 = crowd[nomask][rcol]
            if len(g1.dropna()) < 5 or len(g2.dropna()) < 5:
                continue
            ppy = HORIZON_PERIODS[hname]
            r1 = test_row(g1, f'{gname} {extreme_label} ({hname})', ppy)
            r2 = test_row(g2, f'{gname} Not {extreme_label} ({hname})', ppy)
            t, p = stats.ttest_ind(g1.dropna(), g2.dropna())
            r3 = pd.Series({
                'Group': f'{gname} {extreme_label} vs not ({hname})',
                'N': len(g1.dropna()) + len(g2.dropna()), 'Mean_Ret%': (g1.mean() - g2.mean()) * 100,
                'Std%': np.nan, 't_stat': t, 'p_val': p, 'Sharpe': np.nan,
                'Profit_Factor': np.nan, 'Win_Rate%': np.nan
            })
            t4_results.extend([r1, r2, r3])

t4_all = pd.DataFrame(t4_results) if t4_results else pd.DataFrame()
print_results(t4_all, 'TEST 4: Crowding Analysis')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 5: Regime Analysis (COT + Price)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#'*70)
print('# TEST 5: Regime Analysis - COT + Price Trend')
print('#'*70)

reg = merged.copy()

# Price regime: 8w EMA cross
reg['EMA_8w'] = reg['Close'].ewm(span=8).mean()
reg['Price_Regime'] = 'Sideways'
reg.loc[reg['Close'] > reg['EMA_8w'] * 1.03, 'Price_Regime'] = 'Up'
reg.loc[reg['Close'] < reg['EMA_8w'] * 0.97, 'Price_Regime'] = 'Down'

# COT regime: quintile
for gcol in GROUPS.values():
    reg[f'{gcol}_Quintile'] = pd.qcut(reg[gcol].rank(method='first'), 5,
                                       labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])

t5_results = []
for gname, gcol in GROUPS.items():
    qcol = f'{gcol}_Quintile'
    for price_reg in ['Up', 'Down', 'Sideways']:
        subset = reg[reg['Price_Regime'] == price_reg]
        if len(subset) < 20:
            continue
        for hname, rcol in HORIZONS.items():
            ppy = HORIZON_PERIODS[hname]
            qdf = quintile_analysis(subset, gcol, rcol, f'{gname} {price_reg} ({hname})', ppy)
            if len(qdf) > 0:
                t5_results.append(qdf)

t5_all = pd.concat(t5_results, ignore_index=True) if t5_results else pd.DataFrame()
print_results(t5_all, 'TEST 5: Regime Analysis')

# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════

def count_significant(df, p_thresh=0.05):
    if len(df) == 0:
        return 0, 0
    sig_mask = df['p_val'] < p_thresh
    return sig_mask.sum(), df['Group'].str.contains('Q5-Q1 diff|vs None|vs not').sum()

def capture_significant(df, label):
    if len(df) == 0:
        return []
    sig = df[df['p_val'] < 0.05].copy()
    if len(sig) == 0:
        return []
    out = [f'\n  --- {label} ---']
    for _, r in sig.iterrows():
        s = f'  {r["Group"]:<35s} Ret={r["Mean_Ret%"]:>7.3f}%  p={r["p_val"]:>6.4f}  SR={r["Sharpe"]:>6.2f}  PF={r["Profit_Factor"]:>6.2f}'
        out.append(s)
    return out

sig_lines = []
sig_lines.append('\n--- RESEARCH-014: SIGNIFICANT RESULTS (p < 0.05) ---')
for test_name, test_df in [('Test 1: Net Position Level', t1_all),
                             ('Test 2: Position Change', t2_all),
                             ('Test 3: Divergence', t3_all),
                             ('Test 4: Crowding', t4_all),
                             ('Test 5: Regime', t5_all)]:
    sig_lines.extend(capture_significant(test_df, test_name))

sig_lines.append('\n--- FULL CRITERIA CHECK (p<0.05, Sharpe>1.0, PF>1.30) ---')
pass_all = []
for test_name, test_df in [('Test 1: Net Position Level', t1_all),
                             ('Test 2: Position Change', t2_all),
                             ('Test 3: Divergence', t3_all),
                             ('Test 4: Crowding', t4_all),
                             ('Test 5: Regime', t5_all)]:
    if len(test_df) == 0:
        continue
    for _, r in test_df.iterrows():
        if r['p_val'] < 0.05 and r['Sharpe'] > 1.0 and r['Profit_Factor'] > 1.30:
            pass_all.append(f'  ✓ {test_name} | {r["Group"]}')
            pass_all.append(f'      Ret={r["Mean_Ret%"]:.3f}%  p={r["p_val"]:.4f}  SR={r["Sharpe"]:.2f}  PF={r["Profit_Factor"]:.2f}  WR={r["Win_Rate%"]:.1f}%')
if not pass_all:
    sig_lines.append('  No tests survive ALL criteria (p<0.05, SR>1.0, PF>1.30)')

for s in sig_lines:
    print(s)

# ── Save full report ──────────────────────────────────────────────────────────
with open(REPORTS_DIR / 'RESEARCH-014_COT_Analysis.md', 'w') as f:
    f.write('# RESEARCH-014: COT Positioning Edge Discovery\n\n')
    f.write(f'Data: {len(merged)} weeks ({merged["Report_Date_as_YYYY-MM-DD"].min().date()} to {merged["Report_Date_as_YYYY-MM-DD"].max().date()})\n\n')
    f.write('## Summary\n```\n')
    for s in sig_lines:
        f.write(s + '\n')
    f.write('```\n\n')

    for test_name, test_df in [('Test 1: Net Position Level', t1_all),
                                 ('Test 2: Position Change', t2_all),
                                 ('Test 3: Divergence', t3_all),
                                 ('Test 4: Crowding', t4_all),
                                 ('Test 5: Regime', t5_all)]:
        f.write(f'## {test_name}\n\n')
        f.write('| Group | N | Mean_Ret% | t_stat | p_val | Sharpe | PF | WR% |\n')
        f.write('|-------|---|-----------|--------|-------|--------|----|-----|\n')
        if len(test_df) > 0:
            for _, r in test_df.iterrows():
                sig_m = '*' if r['p_val'] < 0.1 else ''
                f.write(f'| {r["Group"]} | {r["N"]} | {r["Mean_Ret%"]:.3f} | {r["t_stat"]:.3f} | {r["p_val"]:.4f}{sig_m} | {r["Sharpe"]:.2f} | {r["Profit_Factor"]:.2f} | {r["Win_Rate%"]:.1f} |\n')
        f.write('\n')

    f.write('\n---\n*Generated by scripts/research_014_cot_analysis.py*\n')

print(f'\nReport saved to {REPORTS_DIR / "RESEARCH-014_COT_Analysis.md"}')
