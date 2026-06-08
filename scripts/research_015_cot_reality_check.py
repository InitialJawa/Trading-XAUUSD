"""RESEARCH-015: COT Edge Validation & Reality Check

Validates RESEARCH-014 signals through 8 increasingly stringent tests.
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
cot = cot.sort_values('Report_Date_as_YYYY-MM-DD').reset_index(drop=True)
px = px.sort_values('Date').reset_index(drop=True)

# Weekly gold prices
weekly_px = px.set_index('Date')['Close'].resample('W-TUE').last().dropna().to_frame('Close')
weekly_px['Ret_1w'] = weekly_px['Close'].pct_change(1).shift(-1)
weekly_px['Ret_2w'] = weekly_px['Close'].pct_change(2).shift(-2)
weekly_px['Ret_4w'] = weekly_px['Close'].pct_change(4).shift(-4)
weekly_px['Ret_8w'] = weekly_px['Close'].pct_change(8).shift(-8)

# Merge COT with weekly gold
merged = pd.merge_asof(cot, weekly_px[['Close', 'Ret_1w', 'Ret_2w', 'Ret_4w', 'Ret_8w']],
                       left_on='Report_Date_as_YYYY-MM-DD', right_index=True,
                       direction='nearest', tolerance=pd.Timedelta('3D'))
merged = merged.dropna(subset=['Ret_1w'])
print(f'Merged data: {len(merged)} rows ({merged["Report_Date_as_YYYY-MM-DD"].min().date()} to {merged["Report_Date_as_YYYY-MM-DD"].max().date()})')

GROUPS = {'Commercial': 'Net_Commercial', 'Managed_Money': 'Net_Managed_Money',
          'Large_Spec': 'Net_Large_Spec', 'Small_Spec': 'Net_Small_Spec'}
HORIZONS = {'1w': 'Ret_1w', '2w': 'Ret_2w', '4w': 'Ret_4w', '8w': 'Ret_8w'}
HORIZON_PERIODS = {'1w': 52, '2w': 26, '4w': 13, '8w': 6.5}

# ── Metric computation ────────────────────────────────────────────────────────
def compute_metrics(returns, label, ppy=52):
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
    return {'Signal': label, 'N': n, 'Mean_Ret%': mu * 100, 'Std%': std * 100,
            't_stat': t, 'p_val': p, 'Sharpe': sharpe, 'PF': pf, 'WR%': wr}

def evaluate_signal(df, mask_col, label, ret_col='Ret_1w', ppy=52):
    """Evaluate a binary signal: go long when mask_col is True."""
    g = df[df[mask_col] == True][ret_col]
    if len(g.dropna()) < 5:
        return None
    return compute_metrics(g, label, ppy)

# ═══════════════════════════════════════════════════════════════════════════════
# Enumerate ALL Signals from RESEARCH-014
# ═══════════════════════════════════════════════════════════════════════════════

all_signals = []  # Each element: dict with signal metadata + returns Series

# --- Test 1: Quintile signals ---
for gname, gcol in GROUPS.items():
    for hname, rcol in HORIZONS.items():
        ppy = HORIZON_PERIODS[hname]
        df = merged[[gcol, rcol]].dropna().copy()
        if len(df) < 50:
            continue
        df['Q'] = pd.qcut(df[gcol].rank(method='first'), 5,
                          labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
        for q in ['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High']:
            mask = df['Q'] == q
            label = f'T1|{gname} {hname} {q}'
            r = compute_metrics(df[mask][rcol], label, ppy)
            if r is not None:
                all_signals.append(r)

# --- Test 2: Delta signals ---
merged_d = merged.copy()
for gcol in GROUPS.values():
    merged_d[f'{gcol}_D'] = merged_d[gcol].diff()

for gname, gcol in GROUPS.items():
    dcol = f'{gcol}_D'
    for hname, rcol in HORIZONS.items():
        ppy = HORIZON_PERIODS[hname]
        df = merged_d[[dcol, rcol]].dropna().copy()
        if len(df) < 50:
            continue
        df['Q'] = pd.qcut(df[dcol].rank(method='first'), 5,
                          labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
        for q in ['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High']:
            mask = df['Q'] == q
            label = f'T2|D{gname} {hname} {q}'
            r = compute_metrics(df[mask][rcol], label, ppy)
            if r is not None:
                all_signals.append(r)

# --- Test 3: Divergence signals ---
div = merged.copy()
for gcol in GROUPS.values():
    div[f'{gcol}_Z'] = (div[gcol] - div[gcol].mean()) / div[gcol].std()
div['Bullish_Div'] = (div['Net_Commercial_Z'] > 1.0) & (div['Net_Managed_Money_Z'] < -1.0)
div['Bearish_Div'] = (div['Net_Commercial_Z'] < -1.0) & (div['Net_Managed_Money_Z'] > 1.0)

for hname, rcol in HORIZONS.items():
    ppy = HORIZON_PERIODS[hname]
    for div_type, div_col in [('Bullish_Div', 'Bullish_Div'), ('Bearish_Div', 'Bearish_Div')]:
        r = evaluate_signal(div, div_col, f'T3|{div_type.replace("_Div"," Div")} {hname}', rcol, ppy)
        if r is not None:
            all_signals.append(r)

# --- Test 4: Crowding signals ---
crowd = merged.copy()
for gcol in GROUPS.values():
    crowd[f'{gcol}_Pctl'] = crowd[gcol].rank(pct=True)
    crowd[f'{gcol}_Extreme_Long'] = crowd[f'{gcol}_Pctl'] > 0.90
    crowd[f'{gcol}_Extreme_Short'] = crowd[f'{gcol}_Pctl'] < 0.10

for gname, gcol in GROUPS.items():
    for hname, rcol in HORIZONS.items():
        ppy = HORIZON_PERIODS[hname]
        for etype, elabel in [(f'{gcol}_Extreme_Long', 'Extreme_Long'),
                              (f'{gcol}_Extreme_Short', 'Extreme_Short')]:
            r = evaluate_signal(crowd, etype, f'T4|{gname} {elabel} {hname}', rcol, ppy)
            if r is not None:
                all_signals.append(r)

# --- Test 5: Regime signals ---
reg = merged.copy()
reg['EMA_8w'] = reg['Close'].ewm(span=8).mean()
reg['Price_Regime'] = 'Sideways'
reg.loc[reg['Close'] > reg['EMA_8w'] * 1.03, 'Price_Regime'] = 'Up'
reg.loc[reg['Close'] < reg['EMA_8w'] * 0.97, 'Price_Regime'] = 'Down'

for gname, gcol in GROUPS.items():
    for price_reg in ['Up', 'Down', 'Sideways']:
        subset = reg[reg['Price_Regime'] == price_reg].copy()
        if len(subset) < 20:
            continue
        for hname, rcol in HORIZONS.items():
            ppy = HORIZON_PERIODS[hname]
            df = subset[[gcol, rcol]].dropna().copy()
            if len(df) < 20:
                continue
            df['Q'] = pd.qcut(df[gcol].rank(method='first'), 5,
                              labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
            for q in ['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High']:
                mask = df['Q'] == q
                label = f'T5|{gname} {price_reg} {hname} {q}'
                r = compute_metrics(df[mask][rcol], label, ppy)
                if r is not None:
                    all_signals.append(r)

sig_df = pd.DataFrame(all_signals)
print(f'\nTotal signals enumerated: {len(sig_df)}')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 1: Edge Selection
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 1: Edge Selection')
print('#' * 70)

candidates = sig_df[(sig_df['p_val'] < 0.05) & (sig_df['Sharpe'] > 1.0) &
                    (sig_df['PF'] > 1.30) & (sig_df['N'] > 100)].copy()
candidates = candidates.sort_values('Sharpe', ascending=False)

if len(candidates) == 0:
    print('  NO candidates survive Test 1.')
else:
    print(f'  Candidates: {len(candidates)}')
    print(f'  {"Rank":<5s} {"Signal":<50s} {"N":<5s} {"Ret%":<8s} {"Sharpe":<8s} {"PF":<8s} {"WR%":<6s} {"p_val":<8s}')
    print(f'  {"-"*5} {"-"*50} {"-"*5} {"-"*8} {"-"*8} {"-"*8} {"-"*6} {"-"*8}')
    for i, (_, r) in enumerate(candidates.iterrows()):
        print(f'  {i+1:<5d} {r["Signal"]:<50s} {r["N"]:<5d} {r["Mean_Ret%"]:>7.3f}% {r["Sharpe"]:>7.2f} {r["PF"]:>7.2f} {r["WR%"]:>5.1f}% {r["p_val"]:>7.4f}')

# Build mask column lookup for each candidate signal for subsequent tests
# We need to map back from signal label string to actual boolean series
CACHE = {}
def mask_for_signal(signal_label, df=merged, df_d=merged_d, div_df=div, crowd_df=crowd, reg_df=reg):
    if signal_label in CACHE:
        return CACHE[signal_label]
    parts = signal_label.split('|')
    test = parts[0]
    rest = parts[1]
    mask = None

    if test == 'T1':
        # T1|Group horizon Quintile
        gname = rest.split(' ')[0]
        _, hname, qname = rest.split(' ')
        gcol = GROUPS[gname]
        rcol = HORIZONS[hname]
        sdf = df[[gcol]].dropna().copy()
        sdf['Q'] = pd.qcut(sdf[gcol].rank(method='first'), 5,
                           labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
        mask = df.index.isin(sdf[sdf['Q'] == qname].index)

    elif test == 'T2':
        # T2|DGroup horizon Quintile
        inner = rest[1:]  # remove D
        gname = inner.split(' ')[0]
        _, hname, qname = inner.split(' ')
        gcol = GROUPS[gname]
        dcol = f'{gcol}_D'
        rcol = HORIZONS[hname]
        sdf = df_d[[dcol]].dropna().copy()
        sdf['Q'] = pd.qcut(sdf[dcol].rank(method='first'), 5,
                           labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
        mask = df_d.index.isin(sdf[sdf['Q'] == qname].index)

    elif test == 'T3':
        # T3|Bullish_Div or Bearish_Div and horizon
        div_name = rest.rsplit(' ', 1)[0].replace(' ', '_')
        hname = rest.rsplit(' ', 1)[1]
        col_map = {'Bullish_Div': 'Bullish_Div', 'Bearish_Div': 'Bearish_Div',
                   'Bullish Div': 'Bullish_Div', 'Bearish Div': 'Bearish_Div'}
        mask = div_df[col_map[div_name]] == True

    elif test == 'T4':
        # T4|Group Extreme_Long/Short horizon
        gname = rest.split(' ')[0]
        etype = rest.split(' ')[1]
        hname = rest.split(' ')[2]
        gcol = GROUPS[gname]
        col_map = {'Extreme_Long': f'{gcol}_Extreme_Long',
                   'Extreme_Short': f'{gcol}_Extreme_Short'}
        mask = crowd_df[col_map[etype]] == True

    elif test == 'T5':
        # T5|Group PriceRegime horizon Quintile
        gname = rest.split(' ')[0]
        price_reg = rest.split(' ')[1]
        hname = rest.split(' ')[2]
        qname = rest.split(' ')[3]
        gcol = GROUPS[gname]
        subset = reg_df[reg_df['Price_Regime'] == price_reg].copy()
        sdf = subset[[gcol]].dropna().copy()
        sdf['Q'] = pd.qcut(sdf[gcol].rank(method='first'), 5,
                           labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
        idx = sdf[sdf['Q'] == qname].index
        mask = reg_df.index.isin(idx)

    if mask is not None:
        CACHE[signal_label] = mask
    return mask

def ret_col_for_signal(signal_label):
    for hname, rcol in HORIZONS.items():
        if hname in signal_label:
            return rcol
    return 'Ret_1w'

def ppy_for_signal(signal_label):
    for hname, ppy in HORIZON_PERIODS.items():
        if hname in signal_label:
            return ppy
    return 52

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 2: Walk-Forward Validation
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 2: Walk-Forward Validation')
print('#' * 70)

PERIODS = {'2006-2011': ('2006-01-01', '2011-12-31'),
           '2012-2016': ('2012-01-01', '2016-12-31'),
           '2017-2021': ('2017-01-01', '2021-12-31'),
           '2022-2026': ('2022-01-01', '2026-12-31')}

wf_results = {}
for _, c in candidates.iterrows():
    sig = c['Signal']
    rcol = ret_col_for_signal(sig)
    ppy = ppy_for_signal(sig)
    mask = mask_for_signal(sig)
    if mask is None:
        wf_results[sig] = {'PASS': False, 'reason': 'Cannot reconstruct mask'}
        continue

    period_metrics = {}
    passed_all = True
    full_sharpe = c['Sharpe']
    for pname, (pstart, pend) in PERIODS.items():
        pidx = merged.index[(merged['Report_Date_as_YYYY-MM-DD'] >= pstart) &
                            (merged['Report_Date_as_YYYY-MM-DD'] <= pend)]
        pmask = mask & merged.index.isin(pidx)
        g = merged.loc[pmask, rcol].dropna()
        if len(g) < 3:
            period_metrics[pname] = {'N': 0, 'Mean_Ret%': 0, 'Sharpe': 0, 'PF': 0, 'WR%': 0}
            passed_all = False
            continue
        mu = g.mean()
        std = g.std()
        sharpe = mu / std * np.sqrt(ppy) if std > 0 else 0
        pos_sum = g[g > 0].sum()
        neg_sum = abs(g[g < 0].sum())
        pf = pos_sum / neg_sum if neg_sum != 0 else (np.inf if pos_sum > 0 else 0)
        wr = (g > 0).mean() * 100
        period_metrics[pname] = {'N': len(g), 'Mean_Ret%': mu * 100, 'Sharpe': sharpe,
                                 'PF': pf, 'WR%': wr}
        if mu <= 0 or pf <= 1.0:
            passed_all = False
        if full_sharpe > 0 and abs(sharpe) < full_sharpe * 0.5:
            passed_all = False

    stability = sum(1 for p in period_metrics.values() if p['PF'] > 1.0 and p['Mean_Ret%'] > 0)
    wf_results[sig] = {'PASS': passed_all, 'stability': stability / len(PERIODS),
                       'periods': period_metrics}

wf_pass = [s for s, v in wf_results.items() if v['PASS']]
print(f'  Walk-forward PASS: {len(wf_pass)} / {len(candidates)}')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: Out-of-Sample
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 3: Out-of-Sample Validation')
print('#' * 70)

train_idx = merged['Report_Date_as_YYYY-MM-DD'] < '2021-01-01'
test_idx = merged['Report_Date_as_YYYY-MM-DD'] >= '2021-01-01'

oos_results = {}
for _, c in candidates.iterrows():
    sig = c['Signal']
    rcol = ret_col_for_signal(sig)
    ppy = ppy_for_signal(sig)
    mask = mask_for_signal(sig)
    if mask is None:
        oos_results[sig] = {'PASS': False, 'reason': 'No mask'}
        continue

    train_g = merged.loc[mask & train_idx, rcol].dropna()
    test_g = merged.loc[mask & test_idx, rcol].dropna()

    def period_metrics(g, ppy_):
        n = len(g)
        if n < 5:
            return {'N': 0, 'Mean_Ret%': 0, 'Sharpe': 0, 'PF': 0, 'WR%': 0}
        mu = g.mean()
        std = g.std()
        sharpe = mu / std * np.sqrt(ppy_) if std > 0 else 0
        pos_sum = g[g > 0].sum()
        neg_sum = abs(g[g < 0].sum())
        pf = pos_sum / neg_sum if neg_sum != 0 else (np.inf if pos_sum > 0 else 0)
        wr = (g > 0).mean() * 100
        return {'N': n, 'Mean_Ret%': mu * 100, 'Sharpe': sharpe, 'PF': pf, 'WR%': wr}

    train_m = period_metrics(train_g, ppy)
    test_m = period_metrics(test_g, ppy)

    degrade = {}
    for metric in ['Sharpe', 'PF', 'WR%']:
        if train_m[metric] != 0:
            degrade[metric] = abs((test_m[metric] - train_m[metric]) / train_m[metric] * 100)
        else:
            degrade[metric] = np.inf

    oos_pass = (test_m['Mean_Ret%'] > 0) & (test_m['PF'] > 1.0) & \
               all(d < 30 for d in degrade.values())
    oos_results[sig] = {'PASS': oos_pass, 'train': train_m, 'test': test_m,
                        'degradation': degrade}

oos_pass = [s for s, v in oos_results.items() if v['PASS']]
print(f'  OOS PASS: {len(oos_pass)} / {len(candidates)}')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 4: Multiple Testing Correction
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 4: Multiple Testing Correction')
print('#' * 70)

n_tests = len(sig_df)
raw_sig = len(sig_df[sig_df['p_val'] < 0.05])
bonferroni_thresh = 0.05 / n_tests
bonf_sig = len(sig_df[sig_df['p_val'] < bonferroni_thresh])

# Benjamini-Hochberg FDR
p_vals = sig_df['p_val'].sort_values().values
m = len(p_vals)
fdr_thresholds = np.array([(i + 1) / m * 0.05 for i in range(m)])
significant_bh = p_vals <= fdr_thresholds
max_idx = np.argmax(~significant_bh) if not all(significant_bh) else m
bh_thresh = p_vals[max_idx] if max_idx > 0 else 0
bh_sig = len(sig_df[sig_df['p_val'] <= bh_thresh if bh_thresh > 0 else sig_df['p_val'] < 0])

print(f'  Total tests: {n_tests}')
print(f'  Raw significant (p<0.05): {raw_sig}')
print(f'  Bonferroni threshold: {bonferroni_thresh:.6f}')
print(f'  Bonferroni survivors: {bonf_sig}')
print(f'  BH FDR survivors: {bh_sig}')

# Filter candidates by correction
candidates_bonf = candidates[candidates['p_val'] < bonferroni_thresh]
candidates_bh = candidates[candidates['p_val'] <= bh_thresh if bh_thresh > 0 else pd.Series(False, index=candidates.index)]

print(f'\n  Candidates surviving Bonferroni: {len(candidates_bonf)}')
print(f'  Candidates surviving FDR (BH): {len(candidates_bh)}')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 5: Monte Carlo Simulation
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 5: Monte Carlo Simulation')
print('#' * 70)

mc_results = {}
n_perm = 10000
for _, c in candidates.iterrows():
    sig = c['Signal']
    rcol = ret_col_for_signal(sig)
    ppy = ppy_for_signal(sig)
    mask = mask_for_signal(sig)
    if mask is None:
        mc_results[sig] = {'PASS': False, 'MC_p': 1.0}
        continue
    actual = merged.loc[mask, rcol].dropna()
    all_returns = merged[rcol].dropna()
    if len(actual) < 5 or len(all_returns) < 10:
        mc_results[sig] = {'PASS': False, 'MC_p': 1.0}
        continue

    actual_sharpe = actual.mean() / actual.std() * np.sqrt(ppy) if actual.std() > 0 else 0
    perm_sharpes = np.zeros(n_perm)
    for i in range(n_perm):
        perm = np.random.choice(all_returns, size=len(actual), replace=False)
        perm_sharpes[i] = perm.mean() / perm.std() * np.sqrt(ppy) if perm.std() > 0 else 0

    mc_p = np.mean(perm_sharpes >= actual_sharpe)
    mc_pass = mc_p < 0.05
    mc_results[sig] = {'PASS': mc_pass, 'actual_Sharpe': actual_sharpe,
                       'MC_mean': perm_sharpes.mean(), 'MC_95th': np.percentile(perm_sharpes, 95),
                       'MC_p': mc_p}

mc_pass = [s for s, v in mc_results.items() if v['PASS']]
print(f'  MC PASS: {len(mc_pass)} / {len(candidates)}')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 6: Gold Drift Neutralization
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 6: Gold Drift Neutralization')
print('#' * 70)

drift_results = {}
for _, c in candidates.iterrows():
    sig = c['Signal']
    rcol = ret_col_for_signal(sig)
    ppy = ppy_for_signal(sig)
    mask = mask_for_signal(sig)
    if mask is None:
        drift_results[sig] = {'PASS': False, 'alpha': -np.inf}
        continue
    signal_ret = merged.loc[mask, rcol].dropna()
    bh_ret = merged[rcol]  # Buy and hold all weeks

    sign_mu = signal_ret.mean()
    bh_mu = bh_ret.mean()
    alpha = sign_mu - bh_mu
    # Excess return at full sample
    excess = alpha
    excess_annualized = excess * ppy * 100  # in %

    # Test: alpha > 0
    if len(signal_ret) < 5 or len(bh_ret) < 5:
        p_alpha = 1
    else:
        t_alpha, p_alpha = stats.ttest_ind(signal_ret, bh_ret)

    alpha_pass = (alpha > 0) and (p_alpha < 0.05)
    drift_results[sig] = {'PASS': alpha_pass, 'Signal_Ret%': sign_mu * 100,
                          'BH_Ret%': bh_mu * 100, 'Alpha_bps': excess * 10000,
                          'Alpha_Ann%': excess_annualized, 'p_alpha': p_alpha}

drift_pass = [s for s, v in drift_results.items() if v['PASS']]
print(f'  Positive alpha PASS: {len(drift_pass)} / {len(candidates)}')

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 7: Directional Consistency (Monotonicity)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 7: Directional Consistency')
print('#' * 70)

# For each group+horizon, check quintile monotonicity
mono_results = {}
for gname, gcol in GROUPS.items():
    for hname, rcol in HORIZONS.items():
        ppy = HORIZON_PERIODS[hname]
        df = merged[[gcol, rcol]].dropna().copy()
        if len(df) < 50:
            continue
        df['Q'] = pd.qcut(df[gcol].rank(method='first'), 5,
                          labels=['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High'])
        q_means = []
        for q in ['Q1_Low', 'Q2', 'Q3', 'Q4', 'Q5_High']:
            g = df[df['Q'] == q][rcol]
            q_means.append(g.mean())
        q_means = np.array(q_means)
        # Spearman rank correlation between quintile rank (0-4) and mean return
        rank = np.arange(5)
        sp, sp_p = stats.spearmanr(rank, q_means)
        # Monotonicity: count how many adjacent pairs move in same direction
        monotonic = np.sum(np.diff(q_means) > 0)
        monotonic_rev = np.sum(np.diff(q_means) < 0)
        mono_score = max(monotonic, monotonic_rev) / 4.0
        mono_results[f'{gname} {hname}'] = {
            'Q1': q_means[0] * 100, 'Q2': q_means[1] * 100, 'Q3': q_means[2] * 100,
            'Q4': q_means[3] * 100, 'Q5': q_means[4] * 100,
            'Spearman_r': sp, 'Spearman_p': sp_p, 'Mono_Score': mono_score}

print(f'  {"Group":<20s} {"Horizon":<6s} {"Q1%":<8s} {"Q2%":<8s} {"Q3%":<8s} {"Q4%":<8s} {"Q5%":<8s} {"Spearman":<10s} {"Mono":<6s}')
print(f'  {"-"*20} {"-"*6} {"-"*8} {"-"*8} {"-"*8} {"-"*8} {"-"*8} {"-"*10} {"-"*6}')
for key, val in sorted(mono_results.items()):
    print(f'  {key:<20s} {val["Q1"]:>7.3f}% {val["Q2"]:>7.3f}% {val["Q3"]:>7.3f}% {val["Q4"]:>7.3f}% {val["Q5"]:>7.3f}% {val["Spearman_r"]:>+7.3f} (p={val["Spearman_p"]:.3f}) {val["Mono_Score"]:>5.2f}')

# Test if any candidate's group/horizon shows strong monotonicity
def get_group_horizon(signal_label):
    parts = signal_label.split('|')
    rest = parts[1]
    for g in GROUPS:
        if g in rest:
            for h in HORIZONS:
                if h in rest:
                    return f'{g} {h}'
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 8: Implementable Strategy
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# TEST 8: Implementable Strategy')
print('#' * 70)

if len(candidates) > 0:
    # Build a composite strategy: take long when ANY survivor signal is active
    merged['Composite_Signal'] = False
    active_signals = []
    for _, c in candidates.iterrows():
        sig = c['Signal']
        mask = mask_for_signal(sig)
        if mask is not None:
            merged['Composite_Signal'] = merged['Composite_Signal'] | mask
            active_signals.append(sig)

    n_signal_weeks = merged['Composite_Signal'].sum()
    print(f'  Active signals contributing to composite: {len(active_signals)}')
    print(f'  Weeks with signal active: {n_signal_weeks} / {len(merged)}')

    strat_results = {}
    for hname, rcol in HORIZONS.items():
        ppy = HORIZON_PERIODS[hname]
        strat_ret = merged.loc[merged['Composite_Signal'], rcol].dropna()
        bh_ret = merged[rcol].dropna()

        if len(strat_ret) < 5:
            strat_results[hname] = None
            continue

        n = len(strat_ret)
        mu = strat_ret.mean()
        std = strat_ret.std()
        sharpe = mu / std * np.sqrt(ppy) if std > 0 else 0
        pos_sum = strat_ret[strat_ret > 0].sum()
        neg_sum = abs(strat_ret[strat_ret < 0].sum())
        pf = pos_sum / neg_sum if neg_sum != 0 else (np.inf if pos_sum > 0 else 0)
        wr = (strat_ret > 0).mean() * 100
        cum = (1 + strat_ret).prod()
        cagr = cum ** (ppy / n) - 1 if n > 0 else 0
        dd = (1 + strat_ret).cumprod()
        running_max = dd.cummax()
        drawdown = (dd - running_max) / running_max
        max_dd = drawdown.min()
        mar = cagr / abs(max_dd) if max_dd < 0 else np.inf

        # BH
        bh_mu = bh_ret.mean()
        bh_std = bh_ret.std()
        bh_sharpe = bh_mu / bh_std * np.sqrt(ppy) if bh_std > 0 else 0
        bh_cum = (1 + bh_ret).prod()
        bh_cagr = bh_cum ** (ppy / len(bh_ret)) - 1
        bh_dd = (1 + bh_ret).cumprod()
        bh_running_max = bh_dd.cummax()
        bh_drawdown = (bh_dd - bh_running_max) / bh_running_max
        bh_max_dd = bh_drawdown.min()
        bh_mar = bh_cagr / abs(bh_max_dd) if bh_max_dd < 0 else np.inf

        strat_results[hname] = {'N': n, 'Ret%': mu * 100, 'Sharpe': sharpe, 'PF': pf,
                                'WR%': wr, 'CAGR%': cagr * 100, 'MaxDD%': max_dd * 100,
                                'MAR': mar, 'BH_Sharpe': bh_sharpe, 'BH_CAGR%': bh_cagr * 100,
                                'BH_MaxDD%': bh_max_dd * 100, 'BH_MAR': bh_mar}

    print(f'\n  {"Horizon":<8s} {"N":<5s} {"Ret%":<8s} {"Sharpe":<8s} {"PF":<8s} {"WR%":<6s} {"CAGR%":<8s} {"MaxDD%":<8s} {"MAR":<8s} {"BH_SR":<8s} {"BH_CAGR%":<8s}')
    print(f'  {"-"*8} {"-"*5} {"-"*8} {"-"*8} {"-"*8} {"-"*6} {"-"*8} {"-"*8} {"-"*8} {"-"*8} {"-"*8}')
    for hname in ['1w', '2w', '4w', '8w']:
        if strat_results[hname] is not None:
            r = strat_results[hname]
            print(f'  {hname:<8s} {r["N"]:<5d} {r["Ret%"]:>7.3f}% {r["Sharpe"]:>7.2f} {r["PF"]:>7.2f} {r["WR%"]:>5.1f}% {r["CAGR%"]:>7.2f}% {r["MaxDD%"]:>7.2f}% {r["MAR"]:>7.2f} {r["BH_Sharpe"]:>7.2f} {r["BH_CAGR%"]:>7.2f}%')

else:
    print('  No candidates to build strategy from.')
    strat_results = {}

# ═══════════════════════════════════════════════════════════════════════════════
# FINAL VERDICT
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# FINAL VERDICT')
print('#' * 70)

# Each candidate gets a score across all tests
verdicts = []
for _, c in candidates.iterrows():
    sig = c['Signal']
    v = {'Signal': sig, 'N': c['N'], 'Mean_Ret%': c['Mean_Ret%'], 'Sharpe': c['Sharpe'],
         'PF': c['PF'], 'WR%': c['WR%'], 'p_val': c['p_val'],
         'T1_Edge': True}

    v['T2_WF'] = wf_results.get(sig, {}).get('PASS', False)
    v['T2_Stability'] = wf_results.get(sig, {}).get('stability', 0)
    v['T3_OOS'] = oos_results.get(sig, {}).get('PASS', False)
    v['T4_Bonferroni'] = c['p_val'] < bonferroni_thresh
    v['T4_BH'] = c['p_val'] <= (bh_thresh if bh_thresh > 0 else 0)
    v['T5_MC'] = mc_results.get(sig, {}).get('PASS', False)
    v['T5_MC_p'] = mc_results.get(sig, {}).get('MC_p', 1)
    v['T6_Alpha'] = drift_results.get(sig, {}).get('PASS', False)
    v['T6_Alpha_Ann%'] = drift_results.get(sig, {}).get('Alpha_Ann%', 0)

    gh = get_group_horizon(sig)
    if gh and gh in mono_results:
        v['T7_Mono_Score'] = mono_results[gh]['Mono_Score']
        v['T7_Spearman_p'] = mono_results[gh]['Spearman_p']
    else:
        v['T7_Mono_Score'] = 0
        v['T7_Spearman_p'] = 1

    test_keys = ['T1_Edge', 'T2_WF', 'T3_OOS', 'T4_Bonferroni', 'T5_MC', 'T6_Alpha']
    test_keys_b = [k for k in test_keys if k in v and isinstance(v[k], bool)]
    v['Total_PASS'] = sum(1 for k in test_keys_b if v[k])
    verdicts.append(v)

vd = pd.DataFrame(verdicts)
if len(vd) > 0:
    vd = vd.sort_values('Total_PASS', ascending=False)

print(f'\n{"Rank":<5s} {"Signal":<50s} {"N":<5s} {"SR":<6s} {"PF":<6s} {"T2_WF":<6s} {"T3_OOS":<6s} {"T4_Bonf":<7s} {"T5_MC":<6s} {"T6_Alpha":<8s} {"T7_Mono":<6s} {"PASS":<5s}')
print(f'{"-"*5} {"-"*50} {"-"*5} {"-"*6} {"-"*6} {"-"*6} {"-"*6} {"-"*7} {"-"*6} {"-"*8} {"-"*6} {"-"*5}')
for i, (_, r) in enumerate(vd.iterrows()):
    print(f'{i+1:<5d} {r["Signal"]:<50s} {r["N"]:<5d} {r["Sharpe"]:>5.2f} {r["PF"]:>5.2f} '
          f'{str(r["T2_WF"]):<6s} {str(r["T3_OOS"]):<6s} {str(r["T4_Bonferroni"]):<7s} '
          f'{str(r["T5_MC"]):<6s} {str(r["T6_Alpha"]):<8s} {r["T7_Mono_Score"]:>5.2f} '
          f'{r["Total_PASS"]:<3d}')

real_edges = vd[vd['Total_PASS'] >= 6] if len(vd) > 0 else pd.DataFrame()
print(f'\n{"="*70}')
print(f'  REAL EDGES (>=6/7 tests passed): {len(real_edges)}')
if len(real_edges) > 0:
    for _, r in real_edges.iterrows():
        print(f'  ✓ {r["Signal"]}')
        print(f'    N={r["N"]}  Ret={r["Mean_Ret%"]:.3f}%  SR={r["Sharpe"]:.2f}  PF={r["PF"]:.2f}  WR={r["WR%"]:.1f}%')
else:
    print(f'  No real edges found.')

print(f'{"="*70}')

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE REPORT
# ═══════════════════════════════════════════════════════════════════════════════

def fmt_row(r):
    return f'{r["Signal"]:<55s} {r["N"]:<5d} {r["Mean_Ret%"]:>7.3f}% {r["Sharpe"]:>6.2f} {r["PF"]:>6.2f} {r["WR%"]:>5.1f}% {r["p_val"]:>7.4f}'

with open(REPORTS_DIR / 'RESEARCH-015_COT_Reality_Check.md', 'w') as f:
    f.write('# RESEARCH-015: COT Edge Validation & Reality Check\n\n')
    f.write(f'Data: {len(merged)} weeks ({merged["Report_Date_as_YYYY-MM-DD"].min().date()} to {merged["Report_Date_as_YYYY-MM-DD"].max().date()})\n')
    f.write(f'Total signals enumerated: {len(sig_df)}\n\n')

    f.write('## Test 1: Edge Selection\n\n')
    f.write(f'Filter: p<0.05, Sharpe>1.0, PF>1.30, N>100\n\n')
    f.write(f'Candidates: {len(candidates)}\n\n')
    if len(candidates) > 0:
        f.write('| Rank | Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |\n')
        f.write('|------|--------|---|-----------|--------|----|-----|-------|\n')
        for i, (_, r) in enumerate(candidates.iterrows()):
            f.write(f'| {i+1} | {r["Signal"]} | {r["N"]} | {r["Mean_Ret%"]:.3f}% | {r["Sharpe"]:.2f} | {r["PF"]:.2f} | {r["WR%"]:.1f}% | {r["p_val"]:.4f} |\n')
    else:
        f.write('No candidates survive Test 1.\n')

    f.write('\n## Test 2: Walk-Forward Validation\n\n')
    f.write(f'Pass: {len(wf_pass)} / {len(candidates)}\n\n')
    if len(candidates) > 0:
        f.write('| Signal | 2006-2011 | 2012-2016 | 2017-2021 | 2022-2026 | Stability | PASS |\n')
        f.write('|--------|-----------|-----------|-----------|-----------|-----------|------|\n')
        for _, c in candidates.iterrows():
            sig = c['Signal']
            wr = wf_results.get(sig, {})
            periods = wr.get('periods', {})
            pstr = []
            for pn in ['2006-2011', '2012-2016', '2017-2021', '2022-2026']:
                if pn in periods:
                    pm = periods[pn]
                    pstr.append(f'{pm["Mean_Ret%"]:.2f}%/{pm["Sharpe"]:.2f}')
                else:
                    pstr.append('N/A')
            f.write(f'| {sig:<45s} | {pstr[0]:<15s} | {pstr[1]:<15s} | {pstr[2]:<15s} | {pstr[3]:<15s} | {wr.get("stability",0):.2f} | {wr.get("PASS",False)} |\n')

    f.write('\n## Test 3: Out-of-Sample Validation\n\n')
    f.write(f'Train: 2006-2020, Test: 2021-2026\n')
    f.write(f'Pass: {len(oos_pass)} / {len(candidates)}\n\n')
    if len(candidates) > 0:
        f.write('| Signal | Train_Ret% | Train_SR | Train_PF | Test_Ret% | Test_SR | Test_PF | Deg_SR | Deg_PF | Deg_WR | PASS |\n')
        f.write('|--------|------------|----------|----------|-----------|---------|---------|--------|--------|--------|------|\n')
        for _, c in candidates.iterrows():
            sig = c['Signal']
            oos = oos_results.get(sig, {})
            tr = oos.get('train', {})
            te = oos.get('test', {})
            dg = oos.get('degradation', {})
            f.write(f'| {sig:<45s} | {tr.get("Mean_Ret%",0):.3f}% | {tr.get("Sharpe",0):.2f} | {tr.get("PF",0):.2f} | {te.get("Mean_Ret%",0):.3f}% | {te.get("Sharpe",0):.2f} | {te.get("PF",0):.2f} | {dg.get("Sharpe",0):.1f}% | {dg.get("PF",0):.1f}% | {dg.get("WR%",0):.1f}% | {oos.get("PASS",False)} |\n')

    f.write('\n## Test 4: Multiple Testing Correction\n\n')
    f.write(f'Total tests: {n_tests}\n')
    f.write(f'Raw significant (p<0.05): {raw_sig}\n')
    f.write(f'Bonferroni threshold: {bonferroni_thresh:.6f}\n')
    f.write(f'Bonferroni survivors: {bonf_sig}\n')
    f.write(f'BH FDR survivors: {bh_sig}\n\n')
    f.write(f'Candidates surviving Bonferroni: {len(candidates_bonf)}\n')
    f.write(f'Candidates surviving FDR: {len(candidates_bh)}\n')

    f.write('\n## Test 5: Monte Carlo Simulation (10,000 permutations)\n\n')
    f.write(f'Pass: {len(mc_pass)} / {len(candidates)}\n\n')
    if len(candidates) > 0:
        f.write('| Signal | Actual_SR | MC_Mean_SR | MC_95th | MC_p | PASS |\n')
        f.write('|--------|-----------|------------|---------|------|------|\n')
        for _, c in candidates.iterrows():
            sig = c['Signal']
            mc = mc_results.get(sig, {})
            f.write(f'| {sig:<45s} | {mc.get("actual_Sharpe",0):.2f} | {mc.get("MC_mean",0):.2f} | {mc.get("MC_95th",0):.2f} | {mc.get("MC_p",1):.4f} | {mc.get("PASS",False)} |\n')

    f.write('\n## Test 6: Gold Drift Neutralization\n\n')
    f.write(f'Pass (positive alpha, p<0.05): {len(drift_pass)} / {len(candidates)}\n\n')
    if len(candidates) > 0:
        f.write('| Signal | Signal_Ret% | BH_Ret% | Alpha_bps | Alpha_Ann% | p_alpha | PASS |\n')
        f.write('|--------|-------------|---------|-----------|------------|---------|------|\n')
        for _, c in candidates.iterrows():
            sig = c['Signal']
            dr = drift_results.get(sig, {})
            f.write(f'| {sig:<45s} | {dr.get("Signal_Ret%",0):.3f}% | {dr.get("BH_Ret%",0):.3f}% | {dr.get("Alpha_bps",0):.1f} | {dr.get("Alpha_Ann%",0):.2f}% | {dr.get("p_alpha",1):.4f} | {dr.get("PASS",False)} |\n')

    f.write('\n## Test 7: Directional Consistency (Quintile Monotonicity)\n\n')
    f.write('| Group_Horizon | Q1% | Q2% | Q3% | Q4% | Q5% | Spearman_r | Spearman_p | Mono_Score |\n')
    f.write('|---------------|-----|-----|-----|-----|-----|------------|------------|------------|\n')
    for key, val in sorted(mono_results.items()):
        f.write(f'| {key} | {val["Q1"]:.3f}% | {val["Q2"]:.3f}% | {val["Q3"]:.3f}% | {val["Q4"]:.3f}% | {val["Q5"]:.3f}% | {val["Spearman_r"]:.3f} | {val["Spearman_p"]:.3f} | {val["Mono_Score"]:.2f} |\n')

    f.write('\n## Test 8: Implementable Strategy\n\n')
    if len(candidates) > 0:
        f.write(f'Composite signal uses {len(active_signals)} survivors\n')
        f.write(f'Weeks with signal active: {n_signal_weeks} / {len(merged)}\n\n')
        f.write('| Horizon | N | Ret% | Sharpe | PF | WR% | CAGR% | MaxDD% | MAR | BH_SR | BH_CAGR% |\n')
        f.write('|---------|---|------|--------|----|-----|-------|--------|-----|-------|----------|\n')
        for hname in ['1w', '2w', '4w', '8w']:
            if strat_results.get(hname) is not None:
                r = strat_results[hname]
                f.write(f'| {hname} | {r["N"]} | {r["Ret%"]:.3f}% | {r["Sharpe"]:.2f} | {r["PF"]:.2f} | {r["WR%"]:.1f}% | {r["CAGR%"]:.2f}% | {r["MaxDD%"]:.2f}% | {r["MAR"]:.2f} | {r["BH_Sharpe"]:.2f} | {r["BH_CAGR%"]:.2f}% |\n')
    else:
        f.write('No candidates to build strategy.\n')

    f.write('\n## Final Verdict\n\n')
    if len(vd) > 0:
        f.write('| Rank | Signal | N | SR | PF | WR% | T2_WF | T3_OOS | T4_Bonf | T5_MC | T6_Alpha | T7_Mono | PASS |\n')
        f.write('|------|--------|---|----|----|-----|-------|--------|---------|-------|----------|---------|------|\n')
        for i, (_, r) in enumerate(vd.iterrows()):
            f.write(f'| {i+1} | {r["Signal"]} | {r["N"]} | {r["Sharpe"]:.2f} | {r["PF"]:.2f} | {r["WR%"]:.1f}% | {r["T2_WF"]} | {r["T3_OOS"]} | {r["T4_Bonferroni"]} | {r["T5_MC"]} | {r["T6_Alpha"]} | {r["T7_Mono_Score"]:.2f} | {r["Total_PASS"]} |\n')

    f.write(f'\n**Surviving Edges (>=6/7): {len(real_edges)}**\n\n')
    if len(real_edges) > 0:
        for _, r in real_edges.iterrows():
            f.write(f'- {r["Signal"]}: N={r["N"]}, Ret={r["Mean_Ret%"]:.3f}%, SR={r["Sharpe"]:.2f}, PF={r["PF"]:.2f}, WR={r["WR%"]:.1f}%\n')
    else:
        f.write('No real edges survive full validation.\n')

    f.write('\n**Failed Edges:**\n')
    failed = vd[vd['Total_PASS'] < 6] if len(vd) > 0 else pd.DataFrame()
    if len(failed) > 0:
        for _, r in failed.iterrows():
            f.write(f'- {r["Signal"]}: {r["Total_PASS"]}/7 tests passed\n')
    else:
        f.write('All edges passed (or no candidates).\n')

    f.write('\n---\n*Generated by scripts/research_015_cot_reality_check.py*\n')

print(f'\nReport saved to {REPORTS_DIR / "RESEARCH-015_COT_Reality_Check.md"}')
