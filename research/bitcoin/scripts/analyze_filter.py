"""Analyze BTC-001A: filter VolPersist and compute genuine survivor counts."""
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

DATA_DIR = Path('data/bitcoin')
REPORT = Path('reports/bitcoin/BTC_001A_RESULTS.md')
csv_path = DATA_DIR / 'BTCUSD_cleaned.csv'
df = pd.read_csv(csv_path, parse_dates=['Date'], index_col=0)

HORIZONS = {1: 'Ret_1d', 2: 'Ret_2d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 365, 2: 365/2, 5: 365/5, 10: 365/10, 20: 365/20, 60: 365/60}
for h, col in HORIZONS.items():
    df[col] = df['Close'].pct_change(h).shift(-h)

df['TR'] = pd.concat([(df['High'] - df['Low']).abs(),
                       (df['High'] - df['Close'].shift(1)).abs(),
                       (df['Low'] - df['Close'].shift(1)).abs()], axis=1).max(axis=1)
for w in [5, 10, 20, 60]:
    df[f'ATR_{w}'] = df['TR'].rolling(w).mean() / df['Close'] * 100
    df[f'RollStd_{w}'] = df['Close'].pct_change().rolling(w).std() * np.sqrt(365 / w) * 100
    df[f'RealVol_{w}'] = (df['Close'].pct_change() ** 2).rolling(w).mean().apply(np.sqrt) * np.sqrt(365 / w) * 100

df['Vol_20d'] = df['Close'].pct_change().rolling(20).std() * np.sqrt(365) * 100
dvol = df['Vol_20d'].dropna()
dvol_q = pd.qcut(dvol.rank(method='first'), 3, labels=['LowVol', 'MedVol', 'HighVol'])
df['Vol_Regime'] = pd.Series(dvol_q.values, index=dvol.index, dtype=object).reindex(df.index, fill_value=None).values
df['Trend_60d'] = df['Close'].pct_change(60)
dtrend = df['Trend_60d'].dropna()
dtrend_q = pd.qcut(dtrend.rank(method='first'), 3, labels=['Bear', 'Sideways', 'Bull'])
df['Trend_Regime'] = pd.Series(dtrend_q.values, index=dtrend.index, dtype=object).reindex(df.index, fill_value=None).values

# Read T1 candidates from report
lines = REPORT.read_text().split('\n')
sig_names = []
in_table = False
for line in lines:
    if line.startswith('| Signal | N | Mean_Ret%'):
        in_table = True
        continue
    if in_table and line.startswith('|---'):
        continue
    if in_table:
        if line.startswith('---') or line.startswith('*Generated'):
            break
        if line.startswith('| '):
            parts = line.split('|')
            if len(parts) >= 2:
                sig = parts[1].strip()
                if sig and sig.startswith('H'):
                    sig_names.append(sig)

print(f'Read {len(sig_names)} T1 candidate entries')

# Debug: check raw signal names
for s in sig_names[:5]:
    print(f'  [{s}]')
print('  ...')
# Check if VolPersist signals have a specific pattern issue
vp_in_list = [s for s in sig_names if 'VolPersist' in s]
print(f'VolPersist in list: {len(vp_in_list)}')
if vp_in_list:
    print(f'  First VP: [{vp_in_list[0]}]')

def parse_signal(signal_label):
    """Return (mask_series, ret_col, ppy) for a signal label."""
    rcol, ppy_ = None, None
    for h, col in HORIZONS.items():
        if f'_{h}d' in signal_label or f' {h}d' in signal_label:
            rcol = col
            ppy_ = PPY[h]
            break
    if rcol is None:
        return None, None, None

    mask = pd.Series(False, index=df.index)

    if 'H1_Trend_' in signal_label:
        parts = signal_label.split('_')
        direction = parts[2]
        n = int([p for p in parts if p.endswith('d')][0].replace('d', ''))
        ret_d = df['Close'].pct_change()
        if direction == 'Up':
            streak_label = (ret_d.rolling(n).apply(lambda x: all(x > 0)) == 1.0)
        else:
            streak_label = (ret_d.rolling(n).apply(lambda x: all(x < 0)) == 1.0)
        mask = streak_label.shift(1).fillna(False)

    elif 'H2_MeanRev_' in signal_label:
        parts = signal_label.split('_')
        ret_p = int(parts[2].replace('d', ''))
        ret_lookback = df['Close'].pct_change(ret_p)
        if 'Top5' in signal_label:
            thresh = ret_lookback.quantile(0.95)
            mask = ret_lookback >= thresh
        elif 'Bot5' in signal_label:
            thresh = ret_lookback.quantile(0.05)
            mask = ret_lookback <= thresh
        elif 'Q_' in signal_label:
            qname = signal_label.split('_')[-1]
            d = ret_lookback.to_frame('Ret').dropna()
            if len(d) >= 50:
                d['Q'] = pd.qcut(d['Ret'].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
                mask = df.index.isin(d[d['Q'] == qname].index)

    elif 'H3_' in signal_label:
        parts = signal_label.split('_')
        vol_type = parts[1]
        w = int(parts[2].replace('d', ''))
        if vol_type == 'ATR':
            col_name = f'ATR_{w}'
        elif vol_type == 'RollStd':
            col_name = f'RollStd_{w}'
        elif vol_type == 'RealVol':
            col_name = f'RealVol_{w}'
        
        if col_name not in df.columns:
            return None, None, None

        if 'Q_' in signal_label:
            qname = signal_label.split('_')[-1]
            d = df[[col_name]].dropna()
            if len(d) >= 50:
                d['Q'] = pd.qcut(d[col_name].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
                mask = df.index.isin(d[d['Q'] == qname].index)
        elif 'HighVol' in signal_label:
            d = df[[col_name]].dropna()
            thresh = d[col_name].quantile(0.80)
            mask = df[col_name] >= thresh if col_name in df.columns else pd.Series(False, index=df.index)
        elif 'LowVol' in signal_label:
            d = df[[col_name]].dropna()
            thresh = d[col_name].quantile(0.20)
            mask = df[col_name] <= thresh if col_name in df.columns else pd.Series(False, index=df.index)

    elif 'H4_' in signal_label:
        if 'VolRegime' in signal_label:
            regime = signal_label.split('_')[2]
            mask = df['Vol_Regime'] == regime
        elif 'TrendRegime' in signal_label:
            regime = signal_label.split('_')[2]
            mask = df['Trend_Regime'] == regime
        elif 'Combined' in signal_label:
            parts = signal_label.split('_')
            v_reg = parts[2]
            t_reg = parts[3]
            mask = (df['Vol_Regime'] == v_reg) & (df['Trend_Regime'] == t_reg)

    return mask, rcol, ppy_

# Count valid masks for each group
vp_valid = 0
nonvp_valid = 0
vp_mask_count = 0
for sig in sig_names:
    m, r, p = parse_signal(sig)
    valid = m is not None and m.sum() > 3
    if 'VolPersist' in sig:
        vp_mask_count += 1
        if valid:
            vp_valid += 1
    else:
        if valid:
            nonvp_valid += 1

print(f'\n=== MASK ANALYSIS ===')
print(f'VolPersist signals examined: {vp_mask_count}')
print(f'VolPersist with valid mask: {vp_valid}')
print(f'Non-VolPersist with valid mask: {nonvp_valid}')
print(f'Total valid masks: {vp_valid + nonvp_valid}')

# Run validation on non-VolPersists only
nonvp_sigs = [s for s in sig_names if 'VolPersist' not in s]
signal_map = {}
for sig in nonvp_sigs:
    mask, rcol, ppy_ = parse_signal(sig)
    if mask is not None and mask.sum() > 3:
        signal_map[sig] = {'mask': mask, 'rcol': rcol, 'ppy': ppy_}

n = len(signal_map)
print(f'\nNon-VolPersist valid masks for validation: {n}')

# Walk-Forward
total_days = len(df)
period_size = total_days // 4
PERIODS = {
    'P1': (df.index[0], df.index[period_size]),
    'P2': (df.index[period_size], df.index[2 * period_size]),
    'P3': (df.index[2 * period_size], df.index[3 * period_size]),
    'P4': (df.index[3 * period_size], df.index[-1]),
}
wf_pass = 0
wf_detail = {}
for sig, info in signal_map.items():
    mask = info['mask']
    rcol = info['rcol']
    all_ok = True
    for pname, (pstart, pend) in PERIODS.items():
        pidx = df.index[(df.index >= pstart) & (df.index <= pend)]
        pmask = mask & df.index.isin(pidx)
        g = df.loc[pmask, rcol].dropna()
        if len(g) < 3 or g.mean() <= 0:
            all_ok = False
            break
    if all_ok:
        wf_pass += 1
        wf_detail[sig] = True
print(f'Walk-Forward PASS: {wf_pass} / {n}')

# OOS
cutoff = '2021-01-01'
train_idx = df.index < cutoff
test_idx = df.index >= cutoff
oos_pass = 0
for sig, info in signal_map.items():
    mask = info['mask']
    rcol = info['rcol']
    ppy_ = info['ppy']
    train_g = df.loc[mask & train_idx, rcol].dropna()
    test_g = df.loc[mask & test_idx, rcol].dropna()
    if len(train_g) < 5 or len(test_g) < 5:
        continue
    train_sr = train_g.mean() / train_g.std() * np.sqrt(ppy_) if train_g.std() > 0 else 0
    test_sr = test_g.mean() / test_g.std() * np.sqrt(ppy_) if test_g.std() > 0 else 0
    test_pf = test_g[test_g > 0].sum() / abs(test_g[test_g < 0].sum()) if abs(test_g[test_g < 0].sum()) > 0 else np.inf
    deg_sr = abs((test_sr - train_sr) / train_sr) * 100 if train_sr != 0 else 200
    if test_g.mean() > 0 and test_pf > 1.0 and deg_sr < 30:
        oos_pass += 1
print(f'OOS PASS: {oos_pass} / {n}')

# Monte Carlo
mc_pass = 0
np.random.seed(42)
for sig, info in signal_map.items():
    mask = info['mask']
    rcol = info['rcol']
    ppy_ = info['ppy']
    actual = df.loc[mask, rcol].dropna()
    all_r = df[rcol].dropna()
    if len(actual) < 5 or len(all_r) < 10:
        continue
    actual_sr = actual.mean() / actual.std() * np.sqrt(ppy_) if actual.std() > 0 else 0
    n_perm = 5000
    perm_srs = np.zeros(n_perm)
    for i in range(n_perm):
        perm = np.random.choice(all_r, size=len(actual), replace=False)
        perm_srs[i] = perm.mean() / perm.std() * np.sqrt(ppy_) if perm.std() > 0 else 0
    mc_p = np.mean(perm_srs >= actual_sr)
    if mc_p < 0.05:
        mc_pass += 1
print(f'MC PASS: {mc_pass} / {n}')

# Drift
drift_pass = 0
for sig, info in signal_map.items():
    mask = info['mask']
    rcol = info['rcol']
    signal_ret = df.loc[mask, rcol].dropna()
    bh_ret = df[rcol].dropna()
    if len(signal_ret) < 5:
        continue
    alpha = signal_ret.mean() - bh_ret.mean()
    if alpha > 0:
        drift_pass += 1
print(f'Drift PASS: {drift_pass} / {n}')

print(f'\n=== FINAL VERDICT ===')
print(f'Non-VolPersist T1 candidates: {len(nonvp_sigs)}')
print(f'Valid masks: {n}')
print(f'WF: {wf_pass}, OOS: {oos_pass}, MC: {mc_pass}, Drift: {drift_pass}')
print(f'All four tests pass: 0 (by design - no single signal tracked)')

# Count full survivors (pass all 4)
# Check which signals pass ALL validation stages
all_pass = []
for sig, info in signal_map.items():
    mask = info['mask']
    rcol = info['rcol']
    ppy_ = info['ppy']
    
    # WF
    wf_ok = True
    for pname, (pstart, pend) in PERIODS.items():
        pidx = df.index[(df.index >= pstart) & (df.index <= pend)]
        pmask = mask & df.index.isin(pidx)
        g = df.loc[pmask, rcol].dropna()
        if len(g) < 3 or g.mean() <= 0:
            wf_ok = False
            break
    
    # OOS
    train_g = df.loc[mask & train_idx, rcol].dropna()
    test_g = df.loc[mask & test_idx, rcol].dropna()
    oos_ok = False
    if len(train_g) >= 5 and len(test_g) >= 5:
        train_sr = train_g.mean() / train_g.std() * np.sqrt(ppy_) if train_g.std() > 0 else 0
        test_sr = test_g.mean() / test_g.std() * np.sqrt(ppy_) if test_g.std() > 0 else 0
        test_pf = test_g[test_g > 0].sum() / abs(test_g[test_g < 0].sum()) if abs(test_g[test_g < 0].sum()) > 0 else np.inf
        deg_sr = abs((test_sr - train_sr) / train_sr) * 100 if train_sr != 0 else 200
        if test_g.mean() > 0 and test_pf > 1.0 and deg_sr < 30:
            oos_ok = True
    
    # MC
    actual = df.loc[mask, rcol].dropna()
    all_r = df[rcol].dropna()
    mc_ok = False
    if len(actual) >= 5 and len(all_r) >= 10:
        actual_sr = actual.mean() / actual.std() * np.sqrt(ppy_) if actual.std() > 0 else 0
        n_perm = 5000
        perm_srs = np.zeros(n_perm)
        for i in range(n_perm):
            perm = np.random.choice(all_r, size=len(actual), replace=False)
            perm_srs[i] = perm.mean() / perm.std() * np.sqrt(ppy_) if perm.std() > 0 else 0
        mc_p = np.mean(perm_srs >= actual_sr)
        if mc_p < 0.05:
            mc_ok = True
    
    # Drift
    signal_ret = df.loc[mask, rcol].dropna()
    bh_ret = df[rcol].dropna()
    drift_ok = False
    if len(signal_ret) >= 5:
        alpha = signal_ret.mean() - bh_ret.mean()
        if alpha > 0:
            drift_ok = True
    
    passes = sum([wf_ok, oos_ok, mc_ok, drift_ok])
    all_pass.append((sig, passes, wf_ok, oos_ok, mc_ok, drift_ok))

# How many pass all 4?
n_all4 = sum(1 for x in all_pass if x[1] >= 4)
print(f'\nPass ALL 4 validation tests: {n_all4} / {n}')
# How many pass 3+?
n_3plus = sum(1 for x in all_pass if x[1] >= 3)
print(f'Pass 3+ validation tests: {n_3plus} / {n}')

if n_all4 > 0:
    print('\nSignals passing ALL 4:')
    for sig, passes, wf, oos, mc, drift in all_pass:
        if passes >= 4:
            print(f'  {sig} (WF={wf} OOS={oos} MC={mc} Drift={drift})')
else:
    print('\nNO non-VolPersist signal passes all validation tests.')

# Also check for H2 MeanReversion candidates specifically
h2_pass_all = sum(1 for x in all_pass if x[0].startswith('H2') and x[1] >= 4)
h3_pass_all = sum(1 for x in all_pass if x[0].startswith('H3') and x[1] >= 4 and 'VolPersist' not in x[0])
h4_pass_all = sum(1 for x in all_pass if x[0].startswith('H4') and x[1] >= 4)
print(f'\nBy hypothesis (pass all 4):')
print(f'  H2_MeanRev: {h2_pass_all}')
print(f'  H3_VolClust (excl VolPersist): {h3_pass_all}')
print(f'  H4_Regime: {h4_pass_all}')
