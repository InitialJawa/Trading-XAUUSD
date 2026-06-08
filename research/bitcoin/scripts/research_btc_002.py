"""BTC-002: Funding Rate Research — Do perpetual swap funding rates predict BTC returns?"""
import json
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path('data/bitcoin')
REPORTS_DIR = Path('reports/bitcoin')
REPORTS_DIR.mkdir(exist_ok=True)

print('=' * 70)
print('BTC-002: FUNDING RATE RESEARCH')
print('=' * 70)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════

# BTC-USD daily prices
csv_path = DATA_DIR / 'BTCUSD_cleaned.csv'
df_btc = pd.read_csv(csv_path, parse_dates=['Date'], index_col=0)
print(f'BTC data: {len(df_btc)} rows ({df_btc.index.min().date()} to {df_btc.index.max().date()})')

# Funding rates
fr_path = DATA_DIR / 'BTC_USDT_funding_rates_gateio.json'
with open(fr_path) as f:
    fr_data = json.load(f)

df_fr = pd.DataFrame(fr_data)
df_fr['datetime'] = pd.to_datetime(df_fr['t'], unit='s')
df_fr['rate'] = df_fr['r'].astype(float)
df_fr = df_fr.set_index('datetime').sort_index()

print(f'Funding rate data: {len(df_fr)} records ({df_fr.index.min().date()} to {df_fr.index.max().date()})')

# Resample funding rates to daily (mean per day)
df_fr_daily = df_fr['rate'].resample('D').mean().to_frame('FundingRate')
# Also compute daily sum, max, min, last
df_fr_daily['FundingRate_Sum'] = df_fr['rate'].resample('D').sum()
df_fr_daily['FundingRate_Max'] = df_fr['rate'].resample('D').max()
df_fr_daily['FundingRate_Min'] = df_fr['rate'].resample('D').min()
df_fr_daily['FundingRate_Last'] = df_fr['rate'].resample('D').last()
df_fr_daily['FundingRate_Count'] = df_fr['rate'].resample('D').count()

print(f'Daily funding rate: {len(df_fr_daily)} days')

# Merge with BTC prices
df = df_btc.join(df_fr_daily, how='inner')
# Drop rows with NaN funding
df = df.dropna(subset=['FundingRate']).copy()
print(f'Merged data: {len(df)} rows ({df.index.min().date()} to {df.index.max().date()})')

# Forward returns
HORIZONS = {1: 'Ret_1d', 2: 'Ret_2d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 365, 2: 365/2, 5: 365/5, 10: 365/10, 20: 365/20, 60: 365/60}
for h, col in HORIZONS.items():
    df[col] = df['Close'].pct_change(h).shift(-h)
df = df.dropna(subset=['Ret_1d']).copy()
print(f'With returns: {len(df)} rows')

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def compute_metrics(g, label, ppy):
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

def evaluate_quantile(d, sort_col, rcol, label_base, ppy, nq=5):
    d = d[[sort_col, rcol]].dropna().copy()
    if len(d) < 50:
        return [], {}
    d['Q'] = pd.qcut(d[sort_col].rank(method='first'), nq,
                     labels=[f'Q{i+1}' for i in range(nq)])
    results = []
    q_means = {}
    for q in [f'Q{i+1}' for i in range(nq)]:
        r = compute_metrics(d[d['Q'] == q][rcol], f'{label_base} {q}', ppy)
        if r:
            results.append(r)
            q_means[q] = d[d['Q'] == q][rcol].mean()
    q1 = d[d['Q'] == 'Q1'][rcol]
    qn = d[d['Q'] == f'Q{nq}'][rcol]
    if len(q1) > 5 and len(qn) > 5:
        t, p = stats.ttest_ind(qn, q1)
        results.append({'Signal': f'{label_base} Q{nq}-Q1 diff', 'N': len(qn)+len(q1),
                        'Mean_Ret%': (qn.mean()-q1.mean())*100, 'Std%': np.nan,
                        't_stat': t, 'p_val': p, 'Sharpe': np.nan, 'PF': np.nan, 'WR%': np.nan})
    return results, q_means

def evaluate_binary(df, mask, label, rcol, ppy):
    g = df[mask][rcol].dropna()
    if len(g) < 5:
        return None
    return compute_metrics(g, label, ppy)

def t1_pass(r):
    return r is not None and r['p_val'] < 0.05 and r['Sharpe'] > 1.0 and r['PF'] > 1.30 and r['N'] > 50

ALL_SIGNALS = []
ALL_CANDIDATES = []

def collect(phase_name, signals, candidates):
    global ALL_SIGNALS, ALL_CANDIDATES
    if len(signals) > 0:
        ALL_SIGNALS.append(pd.DataFrame(signals))
    if len(candidates) > 0:
        ALL_CANDIDATES.append(pd.DataFrame(candidates))
    print(f'  {phase_name}: {len(signals)} signals, {len(candidates)} T1 pass')

# ═══════════════════════════════════════════════════════════════════════════════
# H1: FUNDING RATE EXTREMES
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# H1: FUNDING RATE EXTREMES')
print('#' + '-' * 69)

signals_h1 = []
candidates_h1 = []

h1_holdings = [1, 2, 5, 10, 20]

# Top/Bottom 5% and 1% funding extremes
for pct, label_pct in [(0.05, 'P5'), (0.01, 'P1')]:
    hi_thresh = df['FundingRate'].quantile(1 - pct)
    lo_thresh = df['FundingRate'].quantile(pct)
    hi_mask = df['FundingRate'] >= hi_thresh
    lo_mask = df['FundingRate'] <= lo_thresh

    for h, rcol in HORIZONS.items():
        if h not in h1_holdings:
            continue
        ppy_ = PPY[h]
        for direction, mask, dlabel in [('High', hi_mask, 'HighFR'), ('Low', lo_mask, 'LowFR')]:
            label = f'H1_FR_extreme_{label_pct}_{dlabel}_{h}d'
            r = evaluate_binary(df, mask, label, rcol, ppy_)
            if r:
                signals_h1.append(r)
                if t1_pass(r):
                    candidates_h1.append(r)

collect('H1_FR_extremes', signals_h1, candidates_h1)

# ═══════════════════════════════════════════════════════════════════════════════
# H2: FUNDING RATE LEVEL QUINTILES
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# H2: FUNDING RATE LEVEL QUINTILES')
print('#' + '-' * 69)

signals_h2 = []
candidates_h2 = []

for h, rcol in HORIZONS.items():
    if h not in h1_holdings:
        continue
    ppy_ = PPY[h]

    # Quintile analysis on FundingRate level
    q_results, _ = evaluate_quantile(df, 'FundingRate', rcol, 'H2_FR_Level_Q_', ppy_)
    for r in q_results:
        signals_h2.append(r)
        if t1_pass(r):
            candidates_h2.append(r)

    # Also test FundingRate_Last (last 8h rate of the day)
    q_results, _ = evaluate_quantile(df, 'FundingRate_Last', rcol, 'H2_FR_Last_Q_', ppy_)
    for r in q_results:
        signals_h2.append(r)
        if t1_pass(r):
            candidates_h2.append(r)

collect('H2_FR_level', signals_h2, candidates_h2)

# ═══════════════════════════════════════════════════════════════════════════════
# H3: FUNDING RATE CHANGE (DELTA)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# H3: FUNDING RATE CHANGE')
print('#' + '-' * 69)

signals_h3 = []
candidates_h3 = []

h3_holdings = [1, 2, 5]

# 1-day and 3-day funding rate changes
for delta_days, dlabel in [(1, '1d'), (3, '3d')]:
    delta_col = f'FundingRate_Delta_{dlabel}'
    df[delta_col] = df['FundingRate'].diff(delta_days)

    for h, rcol in HORIZONS.items():
        if h not in h3_holdings:
            continue
        ppy_ = PPY[h]
        d = df[[delta_col, rcol]].dropna().copy()
        if len(d) < 100:
            continue

        # Quintile analysis
        q_results, _ = evaluate_quantile(d, delta_col, rcol, f'H3_FR_delta_{dlabel}_Q_', ppy_)
        for r in q_results:
            signals_h3.append(r)
            if t1_pass(r):
                candidates_h3.append(r)

        # Binary: large positive/negative changes
        hi_thresh = d[delta_col].quantile(0.80)
        lo_thresh = d[delta_col].quantile(0.20)
        hi_mask = df[delta_col] >= hi_thresh if delta_col in df.columns else pd.Series(False, index=df.index)
        lo_mask = df[delta_col] <= lo_thresh if delta_col in df.columns else pd.Series(False, index=df.index)

        for direction, mask, d2 in [('Pos', hi_mask, 'PosDelta'), ('Neg', lo_mask, 'NegDelta')]:
            label = f'H3_FR_delta_{dlabel}_{d2}_{h}d'
            r = evaluate_binary(df, mask, label, rcol, ppy_)
            if r:
                signals_h3.append(r)
                if t1_pass(r):
                    candidates_h3.append(r)

collect('H3_FR_delta', signals_h3, candidates_h3)

# ═══════════════════════════════════════════════════════════════════════════════
# H4: CUMULATIVE FUNDING PRESSURE
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# H4: CUMULATIVE FUNDING PRESSURE')
print('#' + '-' * 69)

signals_h4 = []
candidates_h4 = []

h4_windows = [5, 10, 20, 60]
h4_holdings = [1, 5, 10, 20]

for w in h4_windows:
    cum_col = f'FundingRate_Cum_{w}d'
    df[cum_col] = df['FundingRate'].rolling(w).sum()

    for h, rcol in HORIZONS.items():
        if h not in h4_holdings:
            continue
        ppy_ = PPY[h]
        d = df[[cum_col, rcol]].dropna().copy()
        if len(d) < 100:
            continue

        q_results, _ = evaluate_quantile(d, cum_col, rcol, f'H4_FR_cum_{w}d_Q_', ppy_)
        for r in q_results:
            signals_h4.append(r)
            if t1_pass(r):
                candidates_h4.append(r)

        # Binary: extreme cumulative funding
        hi_thresh = d[cum_col].quantile(0.80)
        lo_thresh = d[cum_col].quantile(0.20)
        hi_mask = df[cum_col] >= hi_thresh if cum_col in df.columns else pd.Series(False, index=df.index)
        lo_mask = df[cum_col] <= lo_thresh if cum_col in df.columns else pd.Series(False, index=df.index)

        for direction, mask, d2 in [('Pos', hi_mask, 'HighCum'), ('Neg', lo_mask, 'LowCum')]:
            label = f'H4_FR_cum_{w}d_{d2}_{h}d'
            r = evaluate_binary(df, mask, label, rcol, ppy_)
            if r:
                signals_h4.append(r)
                if t1_pass(r):
                    candidates_h4.append(r)

collect('H4_FR_cumulative', signals_h4, candidates_h4)

# ═══════════════════════════════════════════════════════════════════════════════
# H5: FUNDING REGIME PERSISTENCE
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# H5: FUNDING REGIME PERSISTENCE')
print('#' + '-' * 69)

signals_h5 = []
candidates_h5 = []

h5_holdings = [1, 5, 10]
streak_lengths = [3, 5, 7, 10]

# Positive funding streaks (longs paying shorts for N consecutive days)
pos_streak = (df['FundingRate'] > 0).astype(int)
df['PosStreak'] = pos_streak.groupby((pos_streak != pos_streak.shift()).cumsum()).cumsum()

# Negative funding streaks (shorts paying longs)
neg_streak = (df['FundingRate'] < 0).astype(int)
df['NegStreak'] = neg_streak.groupby((neg_streak != neg_streak.shift()).cumsum()).cumsum()

for n in streak_lengths:
    for direction, streak_col, dlabel in [('Pos', 'PosStreak', 'PosFR'), ('Neg', 'NegStreak', 'NegFR')]:
        streak_mask = df[streak_col] >= n
        for h, rcol in HORIZONS.items():
            if h not in h5_holdings:
                continue
            ppy_ = PPY[h]
            label = f'H5_FR_streak_{dlabel}_{n}d_{h}d'
            r = evaluate_binary(df, streak_mask.shift(1).fillna(False), label, rcol, ppy_)
            if r:
                signals_h5.append(r)
                if t1_pass(r):
                    candidates_h5.append(r)

collect('H5_FR_streaks', signals_h5, candidates_h5)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSOLIDATE & VALIDATE
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# FULL VALIDATION')
print('#' + '-' * 69)

all_candidates = pd.concat(ALL_CANDIDATES, ignore_index=True) if ALL_CANDIDATES else pd.DataFrame()
all_signals = pd.concat(ALL_SIGNALS, ignore_index=True) if ALL_SIGNALS else pd.DataFrame()
print(f'\nTotal signals tested: {len(all_signals)}')
print(f'Total T1 candidates: {len(all_candidates)}')

if len(all_candidates) == 0:
    print('\nNO CANDIDATES SURVIVE T1 SCREENING.')
    print('Verdict: Bitcoin funding rates contain no predictive information.')
    exit(0)

# Build signal masks
def parse_signal(signal_label):
    rcol, ppy_ = None, None
    for h, col in HORIZONS.items():
        if f'_{h}d' in signal_label or f' {h}d' in signal_label:
            rcol = col; ppy_ = PPY[h]; break
    if rcol is None:
        return None, None, None

    mask = pd.Series(False, index=df.index)

    # H1: Funding extremes
    if 'H1_FR_extreme_' in signal_label:
        parts = signal_label.split('_')
        pct_label = parts[3]  # P5 or P1
        direction = parts[4]  # HighFR or LowFR
        pct = 0.05 if pct_label == 'P5' else 0.01
        if direction == 'HighFR':
            thresh = df['FundingRate'].quantile(1 - pct)
            mask = df['FundingRate'] >= thresh
        else:
            thresh = df['FundingRate'].quantile(pct)
            mask = df['FundingRate'] <= thresh

    # H2: Funding level quintiles
    elif 'H2_FR_Level_Q_' in signal_label or 'H2_FR_Last_Q_' in signal_label:
        parts = signal_label.split('_')
        if 'Last' in signal_label:
            col_name = 'FundingRate_Last'
        else:
            col_name = 'FundingRate'
        qname = parts[-1]
        d = df[[col_name]].dropna()
        if len(d) >= 50:
            d['Q'] = pd.qcut(d[col_name].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
            mask = df.index.isin(d[d['Q'] == qname].index)

    # H3: Funding delta
    elif 'H3_FR_delta_' in signal_label:
        parts = signal_label.split('_')
        dlabel = parts[3]  # 1d or 3d
        delta_col = f'FundingRate_Delta_{dlabel}'
        if 'Q_' in signal_label:
            qname = parts[-1]
            d = df[[delta_col]].dropna()
            if len(d) >= 50:
                d['Q'] = pd.qcut(d[delta_col].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
                mask = df.index.isin(d[d['Q'] == qname].index)
        elif 'PosDelta' in signal_label:
            d = df[[delta_col]].dropna()
            thresh = d[delta_col].quantile(0.80)
            mask = df[delta_col] >= thresh if delta_col in df.columns else pd.Series(False, index=df.index)
        elif 'NegDelta' in signal_label:
            d = df[[delta_col]].dropna()
            thresh = d[delta_col].quantile(0.20)
            mask = df[delta_col] <= thresh if delta_col in df.columns else pd.Series(False, index=df.index)

    # H4: Cumulative funding
    elif 'H4_FR_cum_' in signal_label:
        parts = signal_label.split('_')
        w = int(parts[3].replace('d', ''))
        cum_col = f'FundingRate_Cum_{w}d'
        if 'Q_' in signal_label:
            qname = parts[-1]
            d = df[[cum_col]].dropna()
            if len(d) >= 50:
                d['Q'] = pd.qcut(d[cum_col].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
                mask = df.index.isin(d[d['Q'] == qname].index)
        elif 'HighCum' in signal_label:
            d = df[[cum_col]].dropna()
            thresh = d[cum_col].quantile(0.80)
            mask = df[cum_col] >= thresh if cum_col in df.columns else pd.Series(False, index=df.index)
        elif 'LowCum' in signal_label:
            d = df[[cum_col]].dropna()
            thresh = d[cum_col].quantile(0.20)
            mask = df[cum_col] <= thresh if cum_col in df.columns else pd.Series(False, index=df.index)

    # H5: Funding streaks
    elif 'H5_FR_streak_' in signal_label:
        parts = signal_label.split('_')
        direction = parts[3]  # PosFR or NegFR
        n = int(parts[4].replace('d', ''))
        streak_col = 'PosStreak' if direction == 'PosFR' else 'NegStreak'
        mask = df[streak_col] >= n

    return mask, rcol, ppy_

signal_map = {}
for _, c in all_candidates.iterrows():
    sig = c['Signal']
    mask, rcol, ppy_ = parse_signal(sig)
    if mask is not None and mask.sum() > 3:
        signal_map[sig] = {'mask': mask, 'rcol': rcol, 'ppy': ppy_}

n_candidates = len(signal_map)
print(f'\nCandidates with valid masks: {n_candidates}')

# Walk-Forward
total_days = len(df)
period_size = total_days // 4
PERIODS = {
    'P1': (df.index[0], df.index[period_size]),
    'P2': (df.index[period_size], df.index[2 * period_size]),
    'P3': (df.index[2 * period_size], df.index[3 * period_size]),
    'P4': (df.index[3 * period_size], df.index[-1]),
}

wf_pass = 0; wf_detail = {}
for sig, info in signal_map.items():
    mask = info['mask']; rcol = info['rcol']
    all_ok = True
    for pname, (pstart, pend) in PERIODS.items():
        pidx = df.index[(df.index >= pstart) & (df.index <= pend)]
        pmask = mask & df.index.isin(pidx)
        g = df.loc[pmask, rcol].dropna()
        if len(g) < 3 or g.mean() <= 0:
            all_ok = False; break
    if all_ok:
        wf_pass += 1
        wf_detail[sig] = True
print(f'Walk-Forward PASS: {wf_pass} / {n_candidates}')

# OOS
cutoff = '2023-06-01'
train_idx = df.index < cutoff
test_idx = df.index >= cutoff
oos_pass = 0
for sig, info in signal_map.items():
    mask = info['mask']; rcol = info['rcol']; ppy_ = info['ppy']
    train_g = df.loc[mask & train_idx, rcol].dropna()
    test_g = df.loc[mask & test_idx, rcol].dropna()
    if len(train_g) < 5 or len(test_g) < 5: continue
    train_sr = train_g.mean() / train_g.std() * np.sqrt(ppy_) if train_g.std() > 0 else 0
    test_sr = test_g.mean() / test_g.std() * np.sqrt(ppy_) if test_g.std() > 0 else 0
    test_pf = test_g[test_g>0].sum() / abs(test_g[test_g<0].sum()) if abs(test_g[test_g<0].sum()) > 0 else np.inf
    deg_sr = abs((test_sr - train_sr) / train_sr) * 100 if train_sr != 0 else 200
    if test_g.mean() > 0 and test_pf > 1.0 and deg_sr < 30:
        oos_pass += 1
print(f'OOS PASS: {oos_pass} / {n_candidates}')

# Monte Carlo
mc_pass = 0
np.random.seed(42)
for sig, info in signal_map.items():
    mask = info['mask']; rcol = info['rcol']; ppy_ = info['ppy']
    actual = df.loc[mask, rcol].dropna()
    all_r = df[rcol].dropna()
    if len(actual) < 5 or len(all_r) < 10: continue
    actual_sr = actual.mean() / actual.std() * np.sqrt(ppy_) if actual.std() > 0 else 0
    n_perm = 5000
    perm_srs = np.zeros(n_perm)
    for i in range(n_perm):
        perm = np.random.choice(all_r, size=len(actual), replace=False)
        perm_srs[i] = perm.mean() / perm.std() * np.sqrt(ppy_) if perm.std() > 0 else 0
    mc_p = np.mean(perm_srs >= actual_sr)
    if mc_p < 0.05:
        mc_pass += 1
print(f'MC PASS: {mc_pass} / {n_candidates}')

# Drift
drift_pass = 0
for sig, info in signal_map.items():
    mask = info['mask']; rcol = info['rcol']
    signal_ret = df.loc[mask, rcol].dropna()
    bh_ret = df[rcol].dropna()
    if len(signal_ret) < 5: continue
    alpha = signal_ret.mean() - bh_ret.mean()
    if alpha > 0:
        drift_pass += 1
print(f'Drift PASS: {drift_pass} / {n_candidates}')

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE REPORT
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('BTC-002 COMPLETE')
print('=' * 70)

ann_vol = df['Close'].pct_change().std() * np.sqrt(365) * 100
ann_sr = df['Close'].pct_change().mean() / df['Close'].pct_change().std() * np.sqrt(365)

report_lines = []
report_lines.append('# BTC-002: Funding Rate Research Results')
report_lines.append('')
report_lines.append(f'**Data:** {len(df)} days ({df.index.min().date()} to {df.index.max().date()})')
report_lines.append(f'**Instrument:** BTC-USD (Bitcoin) with Gate.io BTC_USDT perpetual funding rates')
report_lines.append(f'**Funding rate source:** Gate.io API (8h frequency, resampled to daily)')
report_lines.append(f'**Ann. Volatility:** {ann_vol:.1f}%')
report_lines.append(f'**Ann. Sharpe:** {ann_sr:.4f}')
report_lines.append('')
report_lines.append('## Summary')
report_lines.append('')
report_lines.append('| Hypothesis | Description | Total Signals | T1 Candidates |')
report_lines.append('|-----------|------------|--------------|--------------|')
phase_names = [('H1_FR_extremes', 'Funding Extremes'),
               ('H2_FR_level', 'Funding Level'),
               ('H3_FR_delta', 'Funding Change'),
               ('H4_FR_cumulative', 'Cumulative Funding'),
               ('H5_FR_streaks', 'Funding Streaks')]
for phase_name, _ in phase_names:
    pass
report_lines.append('')
report_lines.append(f'**Total signals tested:** {len(all_signals)}')
report_lines.append(f'**T1 candidates:** {len(all_candidates)}')
report_lines.append(f'**Valid masks:** {n_candidates}')
report_lines.append(f'**Walk-Forward PASS:** {wf_pass}')
report_lines.append(f'**OOS PASS:** {oos_pass}')
report_lines.append(f'**MC PASS:** {mc_pass}')
report_lines.append(f'**Drift Neutralization PASS:** {drift_pass}')
report_lines.append('')
report_lines.append('## Verdict')
report_lines.append('')

if wf_pass > 0 and mc_pass > 0 and drift_pass > 0:
    report_lines.append('**Funding rates show potential predictive power requiring replication.**')
else:
    report_lines.append('**No funding rate edge survives full validation.**')
    report_lines.append('')
    report_lines.append('Bitcoin funding rates, like price structure, show no robust predictive')

if len(all_candidates) > 0:
    report_lines.append('')
    report_lines.append('## T1 Candidates')
    report_lines.append('')
    report_lines.append('| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |')
    report_lines.append('|--------|---|-----------|--------|----|-----|-------|')
    for _, c in all_candidates.iterrows():
        report_lines.append(f'| {c["Signal"]} | {c["N"]} | {c["Mean_Ret%"]:.3f}% | {c["Sharpe"]:.2f} | {c["PF"]:.2f} | {c["WR%"]:.1f}% | {c["p_val"]:.4f} |')

report_lines.append('')
report_lines.append('---')
report_lines.append(f'*Generated by research/bitcoin/scripts/research_btc_002.py*')

report_path = REPORTS_DIR / 'BTC_002_RESULTS.md'
with open(report_path, 'w') as f:
    f.write('\n'.join(report_lines))
print(f'\nReport saved to {report_path}')
print(f'\nFinal: T1={len(all_candidates)}, WF={wf_pass}, OOS={oos_pass}, MC={mc_pass}, Drift={drift_pass}')
