"""Compute per-signal all-4 pass rate for BTC-002."""
import json
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

DATA_DIR = Path('data/bitcoin')
REPORT = Path('reports/bitcoin/BTC_002_RESULTS.md')
csv_path = DATA_DIR / 'BTCUSD_cleaned.csv'
fr_path = DATA_DIR / 'BTC_USDT_funding_rates_gateio.json'

df_btc = pd.read_csv(csv_path, parse_dates=['Date'], index_col=0)
with open(fr_path) as f: fr_data = json.load(f)
df_fr = pd.DataFrame(fr_data)
df_fr['datetime'] = pd.to_datetime(df_fr['t'], unit='s')
df_fr['rate'] = df_fr['r'].astype(float)
df_fr = df_fr.set_index('datetime').sort_index()
df_fr_daily = df_fr['rate'].resample('D').mean().to_frame('FundingRate')
df_fr_daily['FundingRate_Last'] = df_fr['rate'].resample('D').last()
df_fr_daily['FundingRate_Sum'] = df_fr['rate'].resample('D').sum()
df = df_btc.join(df_fr_daily, how='inner').dropna(subset=['FundingRate']).copy()

HORIZONS = {1: 'Ret_1d', 2: 'Ret_2d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 365, 2: 365/2, 5: 365/5, 10: 365/10, 20: 365/20, 60: 365/60}
for h, col in HORIZONS.items():
    df[col] = df['Close'].pct_change(h).shift(-h)

# Derived columns
for d in [1, 3]:
    df[f'FundingRate_Delta_{d}d'] = df['FundingRate'].diff(d)
for w in [5, 10, 20, 60]:
    df[f'FundingRate_Cum_{w}d'] = df['FundingRate'].rolling(w).sum()
pos_streak = (df['FundingRate'] > 0).astype(int)
df['PosStreak'] = pos_streak.groupby((pos_streak != pos_streak.shift()).cumsum()).cumsum()
neg_streak = (df['FundingRate'] < 0).astype(int)
df['NegStreak'] = neg_streak.groupby((neg_streak != neg_streak.shift()).cumsum()).cumsum()

# Parse signals
def parse_signal(signal_label):
    rcol, ppy_ = None, None
    for h, col in HORIZONS.items():
        if f'_{h}d' in signal_label or f' {h}d' in signal_label:
            rcol = col; ppy_ = PPY[h]; break
    if rcol is None: return None, None, None
    mask = pd.Series(False, index=df.index)
    if 'H1_FR_extreme_' in signal_label:
        parts = signal_label.split('_')
        pct_label = parts[3]; direction = parts[4]
        pct = 0.05 if pct_label == 'P5' else 0.01
        if direction == 'HighFR':
            mask = df['FundingRate'] >= df['FundingRate'].quantile(1 - pct)
        else:
            mask = df['FundingRate'] <= df['FundingRate'].quantile(pct)
    elif 'H2_FR_Level_Q_' in signal_label or 'H2_FR_Last_Q_' in signal_label:
        col_name = 'FundingRate_Last' if 'Last' in signal_label else 'FundingRate'
        qname = signal_label.split('_')[-1]
        d = df[[col_name]].dropna()
        if len(d) >= 50:
            d['Q'] = pd.qcut(d[col_name].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
            mask = df.index.isin(d[d['Q'] == qname].index)
    elif 'H3_FR_delta_' in signal_label:
        parts = signal_label.split('_')
        dlabel = parts[3]
        delta_col = f'FundingRate_Delta_{dlabel}'
        if 'Q_' in signal_label:
            qname = parts[-1]
            d = df[[delta_col]].dropna()
            if len(d) >= 50:
                d['Q'] = pd.qcut(d[delta_col].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
                mask = df.index.isin(d[d['Q'] == qname].index)
        elif 'PosDelta' in signal_label:
            d = df[[delta_col]].dropna(); thresh = d[delta_col].quantile(0.80)
            mask = df[delta_col] >= thresh
        elif 'NegDelta' in signal_label:
            d = df[[delta_col]].dropna(); thresh = d[delta_col].quantile(0.20)
            mask = df[delta_col] <= thresh
    elif 'H4_FR_cum_' in signal_label:
        parts = signal_label.split('_')
        w = int(parts[3].replace('d',''))
        cum_col = f'FundingRate_Cum_{w}d'
        if 'Q_' in signal_label:
            qname = parts[-1]; d = df[[cum_col]].dropna()
            if len(d) >= 50:
                d['Q'] = pd.qcut(d[cum_col].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
                mask = df.index.isin(d[d['Q'] == qname].index)
        elif 'HighCum' in signal_label:
            d = df[[cum_col]].dropna(); thresh = d[cum_col].quantile(0.80)
            mask = df[cum_col] >= thresh
        elif 'LowCum' in signal_label:
            d = df[[cum_col]].dropna(); thresh = d[cum_col].quantile(0.20)
            mask = df[cum_col] <= thresh
    elif 'H5_FR_streak_' in signal_label:
        parts = signal_label.split('_')
        direction = parts[3]; n = int(parts[4].replace('d',''))
        streak_col = 'PosStreak' if direction == 'PosFR' else 'NegStreak'
        mask = df[streak_col] >= n
    return mask, rcol, ppy_

# Read T1 candidates from report
lines = REPORT.read_text().split('\n')
sig_names = []; in_table = False
for line in lines:
    if line.startswith('| Signal | N | Mean_Ret%'): in_table = True; continue
    if in_table and line.startswith('|---'): continue
    if in_table:
        if line.startswith('---') or line.startswith('*Generated'): break
        if line.startswith('| '):
            parts = line.split('|')
            if len(parts) >= 2:
                sig = parts[1].strip()
                if sig and sig.startswith('H'): sig_names.append(sig)

# Build signal map
signal_map = {}
for sig in sig_names:
    mask, rcol, ppy_ = parse_signal(sig)
    if mask is not None and mask.sum() > 3:
        signal_map[sig] = {'mask': mask, 'rcol': rcol, 'ppy': ppy_}

n = len(signal_map)
print(f'Valid masks: {n}')

# Walk Forward periods
total_days = len(df); period_size = total_days // 4
PERIODS = {'P1': (df.index[0], df.index[period_size]), 'P2': (df.index[period_size], df.index[2*period_size]),
           'P3': (df.index[2*period_size], df.index[3*period_size]), 'P4': (df.index[3*period_size], df.index[-1])}
cutoff = '2023-06-01'
train_idx = df.index < cutoff; test_idx = df.index >= cutoff

all_pass = []
for sig, info in signal_map.items():
    mask = info['mask']; rcol = info['rcol']; ppy_ = info['ppy']

    # WF
    wf_ok = True
    for pname, (pstart, pend) in PERIODS.items():
        pidx = df.index[(df.index >= pstart) & (df.index <= pend)]
        g = df.loc[mask & df.index.isin(pidx), rcol].dropna()
        if len(g) < 3 or g.mean() <= 0: wf_ok = False; break

    # OOS
    train_g = df.loc[mask & train_idx, rcol].dropna()
    test_g = df.loc[mask & test_idx, rcol].dropna()
    oos_ok = False
    if len(train_g) >= 5 and len(test_g) >= 5:
        train_sr = train_g.mean()/train_g.std()*np.sqrt(ppy_) if train_g.std()>0 else 0
        test_sr = test_g.mean()/test_g.std()*np.sqrt(ppy_) if test_g.std()>0 else 0
        test_pf = test_g[test_g>0].sum()/abs(test_g[test_g<0].sum()) if abs(test_g[test_g<0].sum())>0 else np.inf
        deg_sr = abs((test_sr-train_sr)/train_sr)*100 if train_sr!=0 else 200
        if test_g.mean()>0 and test_pf>1.0 and deg_sr<30: oos_ok = True

    # MC
    actual = df.loc[mask, rcol].dropna()
    all_r = df[rcol].dropna()
    mc_ok = False
    if len(actual) >= 5 and len(all_r) >= 10:
        actual_sr = actual.mean()/actual.std()*np.sqrt(ppy_) if actual.std()>0 else 0
        perm_srs = np.zeros(5000)
        for i in range(5000):
            perm = np.random.choice(all_r, size=len(actual), replace=False)
            perm_srs[i] = perm.mean()/perm.std()*np.sqrt(ppy_) if perm.std()>0 else 0
        if np.mean(perm_srs >= actual_sr) < 0.05: mc_ok = True

    # Drift
    signal_ret = df.loc[mask, rcol].dropna()
    bh_ret = df[rcol].dropna()
    drift_ok = signal_ret.mean() > bh_ret.mean() if len(signal_ret) >= 5 else False

    passes = sum([wf_ok, oos_ok, mc_ok, drift_ok])
    all_pass.append((sig, passes, wf_ok, oos_ok, mc_ok, drift_ok))

n_all4 = sum(1 for x in all_pass if x[1] >= 4)
print(f'Pass ALL 4 validation tests: {n_all4} / {n}')
n_all3 = sum(1 for x in all_pass if x[1] >= 3)
print(f'Pass 3+ tests: {n_all3} / {n}')

if n_all4 > 0:
    print('\n=== PASS ALL 4 ===')
    for sig, passes, wf, oos, mc, drift in all_pass:
        if passes >= 4:
            print(f'  {sig}')
else:
    print('\nNO signal passes all 4 tests.')
