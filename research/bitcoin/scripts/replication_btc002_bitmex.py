"""BTC-002 replication on BitMEX XBTUSD funding rate data.
Runs identical 280 signals as the original Gate.io study for comparison."""
import json, warnings, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings('ignore')

DATA_DIR = Path('data/bitcoin')
REPORT_DIR = Path('reports/bitcoin')
csv_path = DATA_DIR / 'BTCUSD_cleaned.csv'
bitmex_path = DATA_DIR / 'XBTUSD_funding_rates_bitmex.json'

df_btc = pd.read_csv(csv_path, parse_dates=['Date'], index_col=0)
with open(bitmex_path) as f: fr_data = json.load(f)

df_fr = pd.DataFrame(fr_data)
df_fr['timestamp'] = pd.to_datetime(df_fr['timestamp'])
df_fr = df_fr.set_index('timestamp').sort_index()
df_fr.index = df_fr.index.tz_localize(None)
# Resample funding rate to daily mean (same as Gate.io approach)
df_fr_daily = df_fr['fundingRate'].astype(float).resample('D').mean().to_frame('FundingRate')
df_fr_daily['FundingRate_Last'] = df_fr['fundingRate'].astype(float).resample('D').last()
df_fr_daily['FundingRate_Sum'] = df_fr['fundingRate'].astype(float).resample('D').sum()

df = df_btc.join(df_fr_daily, how='inner').dropna(subset=['FundingRate']).copy()
df.index.name = 'Date'

n_total_days = len(df)
print(f'BitMEX merged data: {n_total_days} trading days')
print(f'Date range: {df.index[0].date()} to {df.index[-1].date()}')
print(f'BTC ann vol: {df["Close"].pct_change().std()*np.sqrt(365)*100:.1f}%')
print(f'BTC Sharpe: {df["Close"].pct_change().mean()/df["Close"].pct_change().std()*np.sqrt(365):.4f}')
print(f'Funding rate mean: {df["FundingRate"].mean()*100:.4f}%')
print(f'Funding rate min: {df["FundingRate"].min()*100:.4f}%')
print(f'Funding rate max: {df["FundingRate"].max()*100:.4f}%')

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

def build_signals():
    signals = {}
    # H1: Funding extremes
    for pct, label in [(0.05, 'P5'), (0.01, 'P1')]:
        high_thresh_1d = df['FundingRate'].quantile(1 - pct)
        low_thresh_1d = df['FundingRate'].quantile(pct)
        for h in HORIZONS:
            rcol = HORIZONS[h]
            # HighFR (shorts receiving)
            for suffix, mask in [(f'H1_FR_extreme_{label}_HighFR_{h}d', df['FundingRate'] >= high_thresh_1d),
                                  (f'H1_FR_extreme_{label}_LowFR_{h}d', df['FundingRate'] <= low_thresh_1d)]:
                signals[suffix] = (mask, rcol, PPY[h])
    # H2: Funding level quintiles
    for col_name, col in [('Level', 'FundingRate'), ('Last', 'FundingRate_Last')]:
        if col not in df.columns: continue
        d = df[[col]].dropna()
        if len(d) < 50: continue
        d['Q'] = pd.qcut(d[col].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
        for h in HORIZONS:
            rcol = HORIZONS[h]
            for q in ['Q1','Q2','Q3','Q4','Q5']:
                sig = f'H2_FR_{col_name}_Q_{q}_{h}d'
                mask = df.index.isin(d[d['Q'] == q].index)
                signals[sig] = (mask, rcol, PPY[h])
    # H3: Funding change
    for d in [1, 3]:
        delta_col = f'FundingRate_Delta_{d}d'
        ddf = df[[delta_col]].dropna()
        if len(ddf) < 50: continue
        ddf['Q'] = pd.qcut(ddf[delta_col].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
        high_thresh = ddf[delta_col].quantile(0.80)
        low_thresh = ddf[delta_col].quantile(0.20)
        for h in HORIZONS:
            rcol = HORIZONS[h]
            for q in ['Q1','Q2','Q3','Q4','Q5']:
                sig = f'H3_FR_delta_{d}d_Q_{q}_{h}d'
                signals[sig] = (df.index.isin(ddf[ddf['Q']==q].index), rcol, PPY[h])
            sig_pos = f'H3_FR_delta_{d}d_PosDelta_{h}d'
            sig_neg = f'H3_FR_delta_{d}d_NegDelta_{h}d'
            signals[sig_pos] = (df[delta_col] >= high_thresh, rcol, PPY[h])
            signals[sig_neg] = (df[delta_col] <= low_thresh, rcol, PPY[h])
    # H4: Cumulative funding
    for w in [5, 10, 20, 60]:
        cum_col = f'FundingRate_Cum_{w}d'
        cdf = df[[cum_col]].dropna()
        if len(cdf) < 50: continue
        cdf['Q'] = pd.qcut(cdf[cum_col].rank(method='first'), 5, labels=['Q1','Q2','Q3','Q4','Q5'])
        high_thresh = cdf[cum_col].quantile(0.80)
        low_thresh = cdf[cum_col].quantile(0.20)
        for h in HORIZONS:
            rcol = HORIZONS[h]
            for suffix, mask in [
                (f'H4_FR_cum_{w}d_Q1_{h}d', df.index.isin(cdf[cdf['Q']=='Q1'].index)),
                (f'H4_FR_cum_{w}d_Q2_{h}d', df.index.isin(cdf[cdf['Q']=='Q2'].index)),
                (f'H4_FR_cum_{w}d_Q3_{h}d', df.index.isin(cdf[cdf['Q']=='Q3'].index)),
                (f'H4_FR_cum_{w}d_Q4_{h}d', df.index.isin(cdf[cdf['Q']=='Q4'].index)),
                (f'H4_FR_cum_{w}d_Q5_{h}d', df.index.isin(cdf[cdf['Q']=='Q5'].index)),
                (f'H4_FR_cum_{w}d_HighCum_{h}d', df[cum_col] >= high_thresh),
                (f'H4_FR_cum_{w}d_LowCum_{h}d', df[cum_col] <= low_thresh),
            ]:
                signals[suffix] = (mask, rcol, PPY[h])
    # H5: Funding streaks
    for streak_type, streak_col in [('PosFR', 'PosStreak'), ('NegFR', 'NegStreak')]:
        for n in [2, 3, 4, 5]:
            for h in HORIZONS:
                rcol = HORIZONS[h]
                sig = f'H5_FR_streak_{streak_type}_{n}d_{h}d'
                mask = df[streak_col] >= n
                signals[sig] = (mask, rcol, PPY[h])
    return signals

print('\nBuilding signals...')
signals = build_signals()
print(f'Total signals to test: {len(signals)}')

t1_results = []
valid_signal_map = {}
for sig, (mask, rcol, ppy) in signals.items():
    g = df.loc[mask, rcol].dropna()
    n = len(g)
    if n < 3: continue
    mean_ret = g.mean()
    if mean_ret <= 0: continue
    std_ret = g.std()
    sharpe = mean_ret / std_ret * np.sqrt(ppy) if std_ret > 0 else 0
    wins = (g > 0).sum()
    losses = (g <= 0).sum()
    pf = (g[g>0].sum() / abs(g[g<0].sum())) if abs(g[g<0].sum()) > 0 else np.inf
    wr = wins / n * 100
    t_stat, p_val = stats.ttest_1samp(g, 0) if n >= 3 else (0, 1)
    if p_val < 0.05 and n >= 5:
        t1_results.append({
            'Signal': sig, 'N': n, 'Mean_Ret%': round(mean_ret * 100, 4),
            'Sharpe': round(sharpe, 2), 'PF': round(pf, 2), 'WR%': round(wr, 1),
            'p_val': round(p_val, 4)
        })
        valid_signal_map[sig] = {'mask': mask, 'rcol': rcol, 'ppy': ppy}

print(f'T1 candidates: {len(t1_results)}')
print(f'Valid masks: {len(valid_signal_map)}')

# Validation
n_valid = len(valid_signal_map)
total_days = len(df)
period_size = total_days // 4
PERIODS = {
    'P1': (df.index[0], df.index[period_size]),
    'P2': (df.index[period_size], df.index[2*period_size]),
    'P3': (df.index[2*period_size], df.index[3*period_size]),
    'P4': (df.index[3*period_size], df.index[-1])
}
cutoff = df.index[int(len(df) * 0.5)]
train_idx = df.index < cutoff
test_idx = df.index >= cutoff

print(f'\nOOS cutoff: {cutoff.date()} (train: {train_idx.sum()} days, test: {test_idx.sum()} days)')

wf_pass, oos_pass, mc_pass, drift_pass = 0, 0, 0, 0
for sig, info in valid_signal_map.items():
    mask = info['mask']; rcol = info['rcol']; ppy = info['ppy']

    wf_ok = all(
        len(df.loc[mask & (df.index >= pstart) & (df.index <= pend), rcol].dropna()) >= 3 and
        df.loc[mask & (df.index >= pstart) & (df.index <= pend), rcol].dropna().mean() > 0
        for pname, (pstart, pend) in PERIODS.items()
    )

    train_g = df.loc[mask & train_idx, rcol].dropna()
    test_g = df.loc[mask & test_idx, rcol].dropna()
    oos_ok = False
    if len(train_g) >= 5 and len(test_g) >= 5:
        train_sr = train_g.mean() / train_g.std() * np.sqrt(ppy) if train_g.std() > 0 else 0
        test_sr = test_g.mean() / test_g.std() * np.sqrt(ppy) if test_g.std() > 0 else 0
        test_pf = (test_g[test_g>0].sum() / abs(test_g[test_g<0].sum())) if abs(test_g[test_g<0].sum()) > 0 else np.inf
        deg_sr = abs((test_sr - train_sr) / train_sr) * 100 if train_sr != 0 else 200
        if test_g.mean() > 0 and test_pf > 1.0 and deg_sr < 30:
            oos_ok = True

    actual = df.loc[mask, rcol].dropna()
    all_r = df[rcol].dropna()
    mc_ok = False
    if len(actual) >= 5 and len(all_r) >= 10:
        actual_sr = actual.mean() / actual.std() * np.sqrt(ppy) if actual.std() > 0 else 0
        perm_srs = np.zeros(5000)
        for i in range(5000):
            perm = np.random.choice(all_r, size=len(actual), replace=False)
            perm_srs[i] = perm.mean() / perm.std() * np.sqrt(ppy) if perm.std() > 0 else 0
        if np.mean(perm_srs >= actual_sr) < 0.05:
            mc_ok = True

    drift_ok = actual.mean() > all_r.mean() if len(actual) >= 5 else False

    if wf_ok: wf_pass += 1
    if oos_ok: oos_pass += 1
    if mc_ok: mc_pass += 1
    if drift_ok: drift_pass += 1

print(f'\n=== BitMEX Replication Validation Results ===')
print(f'Walk-Forward PASS: {wf_pass} / {n_valid}')
print(f'OOS PASS: {oos_pass} / {n_valid}')
print(f'MC PASS: {mc_pass} / {n_valid}')
print(f'Drift Neutralization PASS: {drift_pass} / {n_valid}')

# Find signals that pass all 4
print('\n=== Signals Passing ALL 4 ===')
for sig, info in valid_signal_map.items():
    mask = info['mask']; rcol = info['rcol']; ppy = info['ppy']
    wf_ok = all(
        len(df.loc[mask & (df.index >= pstart) & (df.index <= pend), rcol].dropna()) >= 3 and
        df.loc[mask & (df.index >= pstart) & (df.index <= pend), rcol].dropna().mean() > 0
        for pname, (pstart, pend) in PERIODS.items()
    )
    train_g = df.loc[mask & train_idx, rcol].dropna()
    test_g = df.loc[mask & test_idx, rcol].dropna()
    oos_ok = False
    if len(train_g) >= 5 and len(test_g) >= 5:
        train_sr = train_g.mean() / train_g.std() * np.sqrt(ppy) if train_g.std() > 0 else 0
        test_sr = test_g.mean() / test_g.std() * np.sqrt(ppy) if test_g.std() > 0 else 0
        test_pf = (test_g[test_g>0].sum() / abs(test_g[test_g<0].sum())) if abs(test_g[test_g<0].sum()) > 0 else np.inf
        deg_sr = abs((test_sr - train_sr) / train_sr) * 100 if train_sr != 0 else 200
        if test_g.mean() > 0 and test_pf > 1.0 and deg_sr < 30: oos_ok = True
    actual = df.loc[mask, rcol].dropna()
    all_r = df[rcol].dropna()
    mc_ok = False
    if len(actual) >= 5 and len(all_r) >= 10:
        actual_sr = actual.mean() / actual.std() * np.sqrt(ppy) if actual.std() > 0 else 0
        perm_srs = np.zeros(5000)
        for i in range(5000):
            perm = np.random.choice(all_r, size=len(actual), replace=False)
            perm_srs[i] = perm.mean() / perm.std() * np.sqrt(ppy) if perm.std() > 0 else 0
        if np.mean(perm_srs >= actual_sr) < 0.05: mc_ok = True
    drift_ok = actual.mean() > all_r.mean() if len(actual) >= 5 else False
    n_all4 = sum([wf_ok, oos_ok, mc_ok, drift_ok])
    if n_all4 >= 4:
        g = df.loc[mask, rcol].dropna()
        mean_ret = g.mean()
        std_ret = g.std()
        sharpe = mean_ret / std_ret * np.sqrt(ppy) if std_ret > 0 else 0
        pf = (g[g>0].sum() / abs(g[g<0].sum())) if abs(g[g<0].sum()) > 0 else np.inf
        wr = (g>0).sum() / len(g) * 100
        print(f'  {sig}')
        print(f'    N={len(g)}, Ret={mean_ret*100:.2f}%, Sharpe={sharpe:.2f}, PF={pf:.2f}, WR={wr:.1f}%')
        print(f'    WF={wf_ok} OOS={oos_ok} MC={mc_ok} Drift={drift_ok}')

# Comparison summary
print('\n=== Gate.io vs BitMEX Comparison ===')
print('Metric | Gate.io | BitMEX')
print(f'Data range | 2019-2026 | 2016-2026')
print(f'Trading days | 2394 | {n_total_days}')
print(f'Funding records | 7,183 | 10,990')
print(f'T1 candidates | 76 | {len(t1_results)}')
print(f'Valid masks | 25 | {n_valid}')
print(f'WF pass | 13 | {wf_pass}')
print(f'OOS pass | 8 | {oos_pass}')
print(f'MC pass | 15 | {mc_pass}')
print(f'Drift pass | 25 | {drift_pass}')
