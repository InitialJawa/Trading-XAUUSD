"""Check if Gate.io BTC-002 survivors replicate on BitMEX data."""
import json, warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')

DATA_DIR = Path('data/bitcoin')
csv_path = DATA_DIR / 'BTCUSD_cleaned.csv'
bitmex_path = DATA_DIR / 'XBTUSD_funding_rates_bitmex.json'

df_btc = pd.read_csv(csv_path, parse_dates=['Date'], index_col=0)
with open(bitmex_path) as f: fr_data = json.load(f)

df_fr = pd.DataFrame(fr_data)
df_fr['timestamp'] = pd.to_datetime(df_fr['timestamp'])
df_fr = df_fr.set_index('timestamp').sort_index()
df_fr.index = df_fr.index.tz_localize(None)
df_fr_daily = df_fr['fundingRate'].astype(float).resample('D').mean().to_frame('FundingRate')
df_fr_daily['FundingRate_Last'] = df_fr['fundingRate'].astype(float).resample('D').last()
df_fr_daily['FundingRate_Sum'] = df_fr['fundingRate'].astype(float).resample('D').sum()

df = df_btc.join(df_fr_daily, how='inner').dropna(subset=['FundingRate']).copy()
print(f'Data: {len(df)} days ({df.index[0].date()} to {df.index[-1].date()})')

HORIZONS = {1: 'Ret_1d', 2: 'Ret_2d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 365, 2: 365/2, 5: 365/5, 10: 365/10, 20: 365/20, 60: 365/60}
for h, col in HORIZONS.items():
    df[col] = df['Close'].pct_change(h).shift(-h)
for w in [5, 10, 20, 60]:
    df[f'FundingRate_Cum_{w}d'] = df['FundingRate'].rolling(w).sum()

# The 3 Gate.io survivors
GATE_SURVIVORS = [
    ('H1_FR_extreme_P5_LowFR_10d', lambda df: df['FundingRate'] <= df['FundingRate'].quantile(0.05), HORIZONS[10], PPY[10]),
    ('H1_FR_extreme_P5_LowFR_20d', lambda df: df['FundingRate'] <= df['FundingRate'].quantile(0.05), HORIZONS[20], PPY[20]),
    ('H4_FR_cum_5d_LowCum_1d', lambda df: df['FundingRate_Cum_5d'] <= df['FundingRate_Cum_5d'].quantile(0.20), HORIZONS[1], PPY[1]),
]

# Validation setup
total_days = len(df)
period_size = total_days // 4
PERIODS = {
    'P1': (df.index[0], df.index[period_size]),
    'P2': (df.index[period_size], df.index[2*period_size]),
    'P3': (df.index[2*period_size], df.index[3*period_size]),
    'P4': (df.index[3*period_size], df.index[-1])
}

# Use same OOS split as original Gate.io study
cutoff = pd.Timestamp('2023-06-01')
train_idx = df.index < cutoff
test_idx = df.index >= cutoff
print(f'OOS cutoff: 2023-06-01 (train: {train_idx.sum()}, test: {test_idx.sum()})')

print('\n=== Gate.io Survivors on BitMEX Data ===')
print(f'{"Signal":40s} {"N":6s} {"Ret%":8s} {"Sharpe":8s} {"PF":8s} {"WR%":6s} {"WF":5s} {"OOS":5s} {"MC":5s} {"Drift":5s} {"Pass":5s}')
print('-'*105)

for name, mask_fn, rcol, ppy in GATE_SURVIVORS:
    mask = mask_fn(df)
    g = df.loc[mask, rcol].dropna()
    n = len(g)
    if n < 3:
        print(f'{name:40s} {str(n):6s} {"N/A":>8s}')
        continue
    mean_ret = g.mean()
    std_ret = g.std()
    sharpe = mean_ret / std_ret * np.sqrt(ppy) if std_ret > 0 else 0
    pf = (g[g>0].sum() / abs(g[g<0].sum())) if abs(g[g<0].sum()) > 0 else np.inf
    wr = (g>0).sum() / n * 100

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
    actual = g
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
    n_pass = sum([wf_ok, oos_ok, mc_ok, drift_ok])

    print(f'{name:40s} {n:<6d} {mean_ret*100:<8.2f} {sharpe:<8.2f} {pf:<8.2f} {wr:<6.1f} {str(wf_ok):5s} {str(oos_ok):5s} {str(mc_ok):5s} {str(drift_ok):5s} {n_pass}/4')
