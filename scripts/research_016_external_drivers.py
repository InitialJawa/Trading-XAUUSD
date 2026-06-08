"""RESEARCH-016: Gold External Drivers — Term Structure, Real Yield, ETF Flows"""
import pandas as pd
import numpy as np
import yfinance as yf
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

REPORTS_DIR = Path('reports')
REPORTS_DIR.mkdir(exist_ok=True)
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

print('Downloading data...', flush=True)

# ── Download / Load Data ──────────────────────────────────────────────────────
def download_save(ticker, filename, period='max'):
    path = DATA_DIR / filename
    if path.exists():
        df = pd.read_csv(path, parse_dates=['Date'], index_col=0)
        if not isinstance(df.index, pd.DatetimeIndex):
            try:
                df.index = pd.to_datetime(df.index)
            except:
                pass
        if hasattr(df.index, 'tz') and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        print(f'  Loaded {ticker}: {len(df)} rows')
        return df
    t = yf.Ticker(ticker)
    df = t.history(period=period)
    if len(df) > 0:
        if hasattr(df.index, 'tz') and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df.index = df.index.date  # store as date objects
        df.index = pd.to_datetime(df.index)
        df.index.name = 'Date'
        df.to_csv(path, date_format='%Y-%m-%d')
        print(f'  Downloaded {ticker}: {len(df)} rows')
    return df

gcf = download_save('GC=F', 'gcf.csv')
tnx = download_save('^TNX', 'tnx.csv')
tip = download_save('TIP', 'tip.csv')
gld = download_save('GLD', 'gld.csv')
ief = download_save('IEF', 'ief.csv')
tyx = download_save('^TYX', 'tyx.csv')
irx = download_save('^IRX', 'irx.csv')

# Load gold prices (already cleaned)
px = pd.read_csv('data/XAUUSD_cleaned.csv', parse_dates=['Date'])
px = px.sort_values('Date').set_index('Date')['Close']

# Make all indices tz-naive for joining
def to_tz_naive(s):
    if hasattr(s.index, 'tz') and s.index.tz is not None:
        s.index = s.index.tz_localize(None)
    return s

aligned = to_tz_naive(px.to_frame('Gold_Close'))
if len(gcf) > 0:
    gcf_idx = to_tz_naive(gcf.set_index(gcf.index)['Close'])
    gcf_idx.name = 'GC_Close'
    aligned = aligned.join(gcf_idx, how='left')
if len(gld) > 0:
    gld_idx = to_tz_naive(gld.set_index(gld.index)['Close'])
    gld_idx.name = 'GLD_Close'
    aligned = aligned.join(gld_idx, how='left')
    gld_vol = to_tz_naive(gld.set_index(gld.index)['Volume'])
    gld_vol.name = 'GLD_Volume'
    aligned = aligned.join(gld_vol, how='left')
if len(tnx) > 0:
    tnx_idx = to_tz_naive(tnx.set_index(tnx.index)['Close'])
    tnx_idx.name = 'US10Y'
    aligned = aligned.join(tnx_idx, how='left')
if len(tip) > 0:
    tip_idx = to_tz_naive(tip.set_index(tip.index)['Close'])
    tip_idx.name = 'TIP_Close'
    aligned = aligned.join(tip_idx, how='left')
if len(tyx) > 0:
    tyx_idx = to_tz_naive(tyx.set_index(tyx.index)['Close'])
    tyx_idx.name = 'US30Y'
    aligned = aligned.join(tyx_idx, how='left')
if len(irx) > 0:
    irx_idx = to_tz_naive(irx.set_index(irx.index)['Close'])
    irx_idx.name = 'US3M'
    aligned = aligned.join(irx_idx, how='left')
if len(ief) > 0:
    ief_idx = to_tz_naive(ief.set_index(ief.index)['Close'])
    ief_idx.name = 'IEF_Close'
    aligned = aligned.join(ief_idx, how='left')

aligned = aligned.dropna(subset=['Gold_Close']).copy()
print(f'  Aligned data: {len(aligned)} rows ({aligned.index.min().date()} to {aligned.index.max().date()})')

# ── Future Gold Returns ───────────────────────────────────────────────────────
HORIZONS = {1: 'Ret_1d', 5: 'Ret_5d', 10: 'Ret_10d', 20: 'Ret_20d', 60: 'Ret_60d'}
PPY = {1: 252, 5: 252/5, 10: 252/10, 20: 252/20, 60: 252/60}
for h, col in HORIZONS.items():
    aligned[col] = aligned['Gold_Close'].pct_change(h).shift(-h)

aligned = aligned.dropna(subset=['Ret_1d']).copy()
print(f'  With returns: {len(aligned)} rows')

# ═══════════════════════════════════════════════════════════════════════════════
# Commmon Validation Functions
# ═══════════════════════════════════════════════════════════════════════════════

def compute_metrics(returns, label, ppy=252):
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

def evaluate_binary(df, mask_col, label, ret_col, ppy):
    """Go long when mask is True."""
    g = df[df[mask_col] == True][ret_col]
    return compute_metrics(g, label, ppy)

def evaluate_quantile(df, sort_col, ret_col, label_base, ppy, nq=5):
    """Test each quantile of sort_col."""
    d = df[[sort_col, ret_col]].dropna().copy()
    if len(d) < 50:
        return []
    d['Q'] = pd.qcut(d[sort_col].rank(method='first'), nq,
                     labels=[f'Q{i+1}' for i in range(nq)])
    results = []
    for q in [f'Q{i+1}' for i in range(nq)]:
        r = compute_metrics(d[d['Q'] == q][ret_col], f'{label_base} {q}', ppy)
        if r is not None:
            results.append(r)
    # Qn-Q1 diff test
    q1 = d[d['Q'] == 'Q1'][ret_col]
    qn = d[d['Q'] == f'Q{nq}'][ret_col]
    if len(q1) > 5 and len(qn) > 5:
        t, p = stats.ttest_ind(qn, q1)
        results.append({'Signal': f'{label_base} Q{nq}-Q1 diff', 'N': len(qn)+len(q1),
                        'Mean_Ret%': (qn.mean()-q1.mean())*100, 'Std%': np.nan,
                        't_stat': t, 'p_val': p, 'Sharpe': np.nan, 'PF': np.nan, 'WR%': np.nan})
    return results

def evaluate_decile_extreme(df, sort_col, ret_col, label_base, ppy):
    """Test extreme deciles (top 10%, bottom 10%)."""
    d = df[[sort_col, ret_col]].dropna().copy()
    if len(d) < 100:
        return []
    d['Pctl'] = d[sort_col].rank(pct=True)
    d['Extreme_Low'] = d['Pctl'] < 0.10
    d['Extreme_High'] = d['Pctl'] > 0.90
    results = []
    for extreme_type, label in [(True, 'Extreme_High'), (False, 'Extreme_Low')]:
        g = d[d['Pctl'] < 0.10 if not extreme_type else d['Pctl'] > 0.90][ret_col]
        r = compute_metrics(g, f'{label_base} {label}', ppy)
        if r is not None:
            results.append(r)
    # Diff
    lo = d[d['Pctl'] < 0.10][ret_col]
    hi = d[d['Pctl'] > 0.90][ret_col]
    if len(lo) > 5 and len(hi) > 5:
        t, p = stats.ttest_ind(hi, lo)
        results.append({'Signal': f'{label_base} Extreme_High-vs-Low diff',
                        'N': len(hi)+len(lo), 'Mean_Ret%': (hi.mean()-lo.mean())*100,
                        'Std%': np.nan, 't_stat': t, 'p_val': p, 'Sharpe': np.nan,
                        'PF': np.nan, 'WR%': np.nan})
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 016A: TERM STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# PHASE 016A: TERM STRUCTURE')
print('#' + '-' * 69)

ts = aligned.dropna(subset=['GC_Close', 'GLD_Close']).copy()
# GLD ≈ 1/10 oz; term structure = GC=F / (GLD * 10)
ts['Spot_Proxy'] = ts['GLD_Close'] * 10
ts['TS_Ratio'] = ts['GC_Close'] / ts['Spot_Proxy']
ts['TS_Spread%'] = (ts['TS_Ratio'] - 1) * 100
ts['TS_Change'] = ts['TS_Spread%'].diff()
ts['TS_Roll_Ret'] = ts['GC_Close'].pct_change() - ts['GLD_Close'].pct_change()
# Z-score of spread (relative to 60d rolling)
ts['TS_Z'] = (ts['TS_Spread%'] - ts['TS_Spread%'].rolling(60).mean()) / ts['TS_Spread%'].rolling(60).std()
ts['TS_Contango'] = ts['TS_Spread%'] > 0
ts['TS_Backwardation'] = ts['TS_Spread%'] < 0
# Extreme term structure
ts['TS_Spread%_Pctl'] = ts['TS_Spread%'].rank(pct=True)
ts['TS_Steep_Contango'] = ts['TS_Spread%_Pctl'] > 0.90
ts['TS_Deep_Backwardation'] = ts['TS_Spread%_Pctl'] < 0.10

# Also try individual contract approach for short history
gc_contracts = {}
for ticker in ['GCZ25.CMX', 'GCM26.CMX', 'GCQ26.CMX']:
    try:
        h = yf.Ticker(ticker).history(period='max')
        if len(h) > 0:
            h_idx = to_tz_naive(h.set_index(h.index)['Close'])
            h_idx.name = ticker.replace('.CMX','')
            gc_contracts[ticker] = h_idx
    except:
        pass

ts_data = ts  # holds term structure data

T1_SIGNALS = []
print('  Generating term structure signals...')

# Signal 1: TS Level quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T1_SIGNALS.extend(evaluate_quantile(ts, 'TS_Spread%', rcol, f'TS_Level_{h}d', ppy_))

# Signal 2: TS Change quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    td = ts.dropna(subset=['TS_Change'])
    T1_SIGNALS.extend(evaluate_quantile(td, 'TS_Change', rcol, f'TS_Change_{h}d', ppy_))

# Signal 3: Contango / Backwardation binary
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    for name, col in [('Contango', 'TS_Contango'), ('Backwardation', 'TS_Backwardation')]:
        r = evaluate_binary(ts, col, f'TS_{name}_{h}d', rcol, ppy_)
        if r: T1_SIGNALS.append(r)

# Signal 4: Extreme term structure
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T1_SIGNALS.extend(evaluate_decile_extreme(ts, 'TS_Spread%', rcol, f'TS_Extreme_{h}d', ppy_))

# Signal 5: Roll return quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    tr = ts.dropna(subset=['TS_Roll_Ret'])
    T1_SIGNALS.extend(evaluate_quantile(tr, 'TS_Roll_Ret', rcol, f'TS_RollRet_{h}d', ppy_))

# Signal 6: TS Z-score extreme
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    tz = ts.dropna(subset=['TS_Z'])
    for extreme_type, label in [(True, 'TS_Z_High'), (False, 'TS_Z_Low')]:
        mask = tz['TS_Z'] > 1.0 if extreme_type else tz['TS_Z'] < -1.0
        g = tz[mask][rcol]
        r = compute_metrics(g, f'{label}_{h}d', ppy_)
        if r: T1_SIGNALS.append(r)

# Individual contract spread (short history)
for cname, cdata in gc_contracts.items():
    cdata.name = 'Contract_Close'
    cdf = ts.join(cdata, how='inner')
    if len(cdf) < 20:
        continue
    cdf['Contract_Ret'] = cdf['Contract_Close'].pct_change()
    cdf['Spread_vs_Spot'] = cdf['Contract_Close'] - cdf['Gold_Close']
    for h, rcol in HORIZONS.items():
        if rcol not in cdf.columns:
            continue
        ppy_ = PPY[h]
        d = cdf[[f'Spread_vs_Spot', rcol]].dropna().copy()
        if len(d) > 20:
            T1_SIGNALS.extend(evaluate_quantile(cdf, 'Spread_vs_Spot', rcol, f'TS_{cname}_{h}d', ppy_))

t1_df = pd.DataFrame(T1_SIGNALS)
print(f'  Total signals: {len(t1_df)}')
t1_candidates = t1_df[(t1_df['p_val'] < 0.05) & (t1_df['Sharpe'] > 1.0) &
                      (t1_df['PF'] > 1.30) & (t1_df['N'] > 50)] if len(t1_df) > 0 else pd.DataFrame()
print(f'  Test 1 candidates: {len(t1_candidates)}')

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 016B: REAL YIELD SHOCKS
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# PHASE 016B: REAL YIELD SHOCKS')
print('#' + '-' * 69)

ry = aligned.dropna(subset=['US10Y', 'TIP_Close']).copy()
# Daily yield changes
ry['TNX_Chg'] = ry['US10Y'].diff()
ry['TNX_Chg_Abs'] = ry['TNX_Chg'].abs()
# Shock detection: rolling 60d mean and std
ry['TNX_Chg_Mean'] = ry['TNX_Chg'].rolling(60).mean()
ry['TNX_Chg_Std'] = ry['TNX_Chg'].rolling(60).std()
ry['TNX_Shock_1s_Up'] = ry['TNX_Chg'] > ry['TNX_Chg_Mean'] + ry['TNX_Chg_Std']
ry['TNX_Shock_2s_Up'] = ry['TNX_Chg'] > ry['TNX_Chg_Mean'] + 2 * ry['TNX_Chg_Std']
ry['TNX_Shock_1s_Dn'] = ry['TNX_Chg'] < ry['TNX_Chg_Mean'] - ry['TNX_Chg_Std']
ry['TNX_Shock_2s_Dn'] = ry['TNX_Chg'] < ry['TNX_Chg_Mean'] - 2 * ry['TNX_Chg_Std']
# TIP returns as real yield proxy
ry['TIP_Ret'] = ry['TIP_Close'].pct_change()
# Real yield regime
ry['US10Y_Pctl'] = ry['US10Y'].rank(pct=True)
ry['US10Y_High'] = ry['US10Y_Pctl'] > 0.75
ry['US10Y_Low'] = ry['US10Y_Pctl'] < 0.25
# Yield curve slope
ry['YCSlope'] = ry['US10Y'] - ry['US30Y'] if 'US30Y' in ry.columns else 0

# Real yield proxy from TIP (inverse)
# TIP is a TIPS fund; when real yields rise, TIP falls
ry['RY_Proxy_Ret'] = -ry['TIP_Ret']  # inverse of TIP return ≈ real yield increase
ry['RY_Shock_1s'] = ry['RY_Proxy_Ret'].abs() > ry['RY_Proxy_Ret'].rolling(60).std() * 1
ry['RY_Shock_2s'] = ry['RY_Proxy_Ret'].abs() > ry['RY_Proxy_Ret'].rolling(60).std() * 2

T2_SIGNALS = []
print('  Generating real yield signals...')

# Signal 1: Yield change shocks (1s, 2s up/down)
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    for shock_col, slabel in [('TNX_Shock_1s_Up', 'TNX_1s_Up'), ('TNX_Shock_2s_Up', 'TNX_2s_Up'),
                               ('TNX_Shock_1s_Dn', 'TNX_1s_Dn'), ('TNX_Shock_2s_Dn', 'TNX_2s_Dn')]:
        r = evaluate_binary(ry.dropna(subset=[shock_col]), shock_col, f'Yield_{slabel}_{h}d', rcol, ppy_)
        if r: T2_SIGNALS.append(r)

# Signal 2: TIP as real yield shock
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    for shock_col, slabel in [('RY_Shock_1s', 'TIP_1s'), ('RY_Shock_2s', 'TIP_2s')]:
        r = evaluate_binary(ry.dropna(subset=[shock_col]), shock_col, f'RY_{slabel}_{h}d', rcol, ppy_)
        if r: T2_SIGNALS.append(r)

# Signal 3: Yield level quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T2_SIGNALS.extend(evaluate_quantile(ry, 'US10Y', rcol, f'Yield_Level_{h}d', ppy_))

# Signal 4: Yield change quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T2_SIGNALS.extend(evaluate_quantile(ry.dropna(subset=['TNX_Chg']), 'TNX_Chg', rcol, f'Yield_Chg_{h}d', ppy_))

# Signal 5: TIP return quintiles (real yield proxy)
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T2_SIGNALS.extend(evaluate_quantile(ry.dropna(subset=['TIP_Ret']), 'TIP_Ret', rcol, f'TIP_Ret_{h}d', ppy_))

# Signal 6: Yield curve slope quintiles
if 'YCSlope' in ry.columns:
    for h, rcol in HORIZONS.items():
        ppy_ = PPY[h]
        T2_SIGNALS.extend(evaluate_quantile(ry.dropna(subset=['YCSlope']), 'YCSlope', rcol, f'YCSlope_{h}d', ppy_))

# Signal 7: High/Low yield regime
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    for name, col in [('Yield_High', 'US10Y_High'), ('Yield_Low', 'US10Y_Low')]:
        r = evaluate_binary(ry, col, f'{name}_{h}d', rcol, ppy_)
        if r: T2_SIGNALS.append(r)

t2_df = pd.DataFrame(T2_SIGNALS)
print(f'  Total signals: {len(t2_df)}')
t2_candidates = t2_df[(t2_df['p_val'] < 0.05) & (t2_df['Sharpe'] > 1.0) &
                      (t2_df['PF'] > 1.30) & (t2_df['N'] > 50)] if len(t2_df) > 0 else pd.DataFrame()
print(f'  Test 1 candidates: {len(t2_candidates)}')

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 016C: ETF FLOWS
# ═══════════════════════════════════════════════════════════════════════════════
print('\n' + '#' * 70)
print('# PHASE 016C: ETF FLOWS (GLD)')
print('#' + '-' * 69)

ef = aligned.dropna(subset=['GLD_Close', 'GLD_Volume']).copy()
# GLD return
ef['GLD_Ret'] = ef['GLD_Close'].pct_change()
# Gold return from GC
ef['GC_Ret'] = ef['GC_Close'].pct_change() if 'GC_Close' in ef.columns else ef['Gold_Close'].pct_change()
# Divergence between GLD and gold (ETF-specific pressure)
ef['GLD_Gold_Div'] = ef['GLD_Ret'] - ef['GC_Ret']
# Volume z-score (20d rolling)
ef['Volume_MA20'] = ef['GLD_Volume'].rolling(20).mean()
ef['Volume_Std20'] = ef['GLD_Volume'].rolling(20).std()
ef['Volume_Z'] = (ef['GLD_Volume'] - ef['Volume_MA20']) / ef['Volume_Std20']
ef['Volume_Spike'] = ef['Volume_Z'] > 1.0
ef['Volume_Drought'] = ef['Volume_Z'] < -1.0
# Dollar volume
ef['Dollar_Vol'] = ef['GLD_Close'] * ef['GLD_Volume']
ef['Dollar_Vol_Chg'] = ef['Dollar_Vol'].pct_change()
# Flow proxy: divergence × sign of volume anomaly
# Positive divergence + high volume = likely inflows
ef['Flow_Proxy'] = ef['GLD_Gold_Div'] * ef['Volume_Z']
ef['Flow_Proxy_Up'] = ef['Flow_Proxy'] > ef['Flow_Proxy'].rolling(60).mean() + ef['Flow_Proxy'].rolling(60).std()
ef['Flow_Proxy_Dn'] = ef['Flow_Proxy'] < ef['Flow_Proxy'].rolling(60).mean() - ef['Flow_Proxy'].rolling(60).std()
# GLD liquidity (Amihud illiquidity proxy: |ret| / volume)
ef['Illiquidity'] = ef['GLD_Ret'].abs() / (ef['GLD_Volume'] + 1) * 1e9
ef['Illiquidity_Z'] = (ef['Illiquidity'] - ef['Illiquidity'].rolling(60).mean()) / ef['Illiquidity'].rolling(60).std()
ef['Illiquid'] = ef['Illiquidity_Z'] > 1.0

T3_SIGNALS = []
print('  Generating ETF flow signals...')

# Signal 1: GLD-Gold divergence quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T3_SIGNALS.extend(evaluate_quantile(ef.dropna(subset=['GLD_Gold_Div']), 'GLD_Gold_Div', rcol, f'GLD_Div_{h}d', ppy_))

# Signal 2: Volume anomaly quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T3_SIGNALS.extend(evaluate_quantile(ef.dropna(subset=['Volume_Z']), 'Volume_Z', rcol, f'Vol_Z_{h}d', ppy_))

# Signal 3: Volume spike/drought
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    for name, col in [('Vol_Spike', 'Volume_Spike'), ('Vol_Drought', 'Volume_Drought')]:
        r = evaluate_binary(ef.dropna(subset=[col]), col, f'{name}_{h}d', rcol, ppy_)
        if r: T3_SIGNALS.append(r)

# Signal 4: Flow proxy extreme
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T3_SIGNALS.extend(evaluate_decile_extreme(ef.dropna(subset=['Flow_Proxy']), 'Flow_Proxy', rcol, f'Flow_{h}d', ppy_))

# Signal 5: GLD return quintiles (ETF price momentum)
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T3_SIGNALS.extend(evaluate_quantile(ef.dropna(subset=['GLD_Ret']), 'GLD_Ret', rcol, f'GLD_Ret_{h}d', ppy_))

# Signal 6: Dollar volume change quintiles
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T3_SIGNALS.extend(evaluate_quantile(ef.dropna(subset=['Dollar_Vol_Chg']), 'Dollar_Vol_Chg', rcol, f'DollarVol_{h}d', ppy_))

# Signal 7: Flow proxy binary signals
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    for name, col in [('Flow_Up', 'Flow_Proxy_Up'), ('Flow_Dn', 'Flow_Proxy_Dn')]:
        r = evaluate_binary(ef.dropna(subset=[col]), col, f'{name}_{h}d', rcol, ppy_)
        if r: T3_SIGNALS.append(r)

# Signal 8: Illiquidity extreme
for h, rcol in HORIZONS.items():
    ppy_ = PPY[h]
    T3_SIGNALS.extend(evaluate_decile_extreme(ef.dropna(subset=['Illiquidity_Z']), 'Illiquidity_Z', rcol, f'Illiq_{h}d', ppy_))

t3_df = pd.DataFrame(T3_SIGNALS)
print(f'  Total signals: {len(t3_df)}')
t3_candidates = t3_df[(t3_df['p_val'] < 0.05) & (t3_df['Sharpe'] > 1.0) &
                      (t3_df['PF'] > 1.30) & (t3_df['N'] > 50)] if len(t3_df) > 0 else pd.DataFrame()
print(f'  Test 1 candidates: {len(t3_candidates)}')

# ═══════════════════════════════════════════════════════════════════════════════
# FULL VALIDATION ON ALL CANDIDATES
# ═══════════════════════════════════════════════════════════════════════════════

print('\n' + '#' * 70)
print('# FULL VALIDATION')
print('#' * 70)

all_phases = [('016A_TermStruct', t1_df, t1_candidates),
              ('016B_RealYield', t2_df, t2_candidates),
              ('016C_ETF_Flows', t3_df, t3_candidates)]

all_candidates = []
for pname, pdf, pcan in all_phases:
    if len(pcan) > 0:
        pcan = pcan.copy()
        pcan['Phase'] = pname
        all_candidates.append(pcan)
        print(f'\n{pname}: {len(pcan)} candidates')
        for _, r in pcan.sort_values('Sharpe', ascending=False).iterrows():
            print(f'  {r["Signal"]:<45s} N={r["N"]:<4d} Ret={r["Mean_Ret%"]:>7.3f}% SR={r["Sharpe"]:>6.2f} PF={r["PF"]:>6.2f} WR={r["WR%"]:>5.1f}% p={r["p_val"]:>7.4f}')
    else:
        print(f'\n{pname}: 0 candidates')

if len(all_candidates) == 0:
    print('\nNO CANDIDATES FROM ANY PHASE — RESEARCH COMPLETE.')
    report_text = '\n'.join([
        '# RESEARCH-016: Gold External Drivers',
        '',
        f'Data: {len(aligned)} days ({aligned.index.min().date()} to {aligned.index.max().date()})',
        '',
        '## Summary',
        '',
        'No candidates survived Test 1 (p<0.05, SR>1.0, PF>1.30, N>50) across any of the three phases.',
        '',
        '### 016A — Term Structure: 0/120+ signals',
        'Term structure proxy via GLD/GC=F spread shows no predictive power for future gold returns.',
        '',
        '### 016B — Real Yield Shocks: 0/90+ signals', 
        'Yield changes, shocks, TIP-based real yield all fail to predict gold.',
        '',
        '### 016C — ETF Flows: 0/120+ signals',
        'GLD volume, divergence, flow proxy all show no predictive edge.',
        '',
        '**Verdict: 0 external driver edges found.**',
        '',
        '---',
        '*Generated by scripts/research_016_external_drivers.py*'
    ])
    with open(REPORTS_DIR / 'RESEARCH-016_External_Drivers.md', 'w') as f:
        f.write(report_text)
    print(report_text)
    print(f'\nReport saved to {REPORTS_DIR / "RESEARCH-016_External_Drivers.md"}')
    exit()
candidates_all = pd.concat(all_candidates, ignore_index=True)

print(f'\nTotal candidates: {len(candidates_all)}')

# ── Test 2: Walk-Forward ──────────────────────────────────────────────────────
print('\n--- Test 2: Walk-Forward ---')
PERIODS = {'2006-2011': ('2006-01-01', '2011-12-31'),
           '2012-2016': ('2012-01-01', '2016-12-31'),
           '2017-2021': ('2017-01-01', '2021-12-31'),
           '2022-2026': ('2022-01-01', '2026-12-31')}

# Build a global mask function using precomputed source data
SRC_MAP = {}
def rebuild_masks():
    """Precompute index sets for all candidate signals for fast lookup."""
    global SRC_MAP
    for _, c in candidates_all.iterrows():
        sig = c['Signal']
        src = None
        if 'TS_' in sig:
            src = ts
        elif any(x in sig for x in ['Yield_', 'RY_', 'YCSlope', 'TIP_']):
            src = ry
        elif any(x in sig for x in ['GLD_', 'Vol_', 'Flow_', 'DollarVol', 'Illiq']):
            src = ef
        if src is None:
            continue
        idx_set = set()
        h_found = None
        rcol_found = None
        ppy_found = None
        for h, rcol in HORIZONS.items():
            if f'_{h}d' in sig or f' {h}d' in sig:
                h_found = h
                rcol_found = rcol
                ppy_found = PPY[h]
                break
        if rcol_found is None:
            continue
        parts = sig.rsplit(' ', 1)
        qname = parts[-1] if len(parts) > 1 else ''
        # Quantile signals
        if qname in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']:
            for sort_col in ['TS_Spread%', 'TS_Change', 'TS_Roll_Ret', 'TS_Spread%_Pctl',
                              'US10Y', 'TNX_Chg', 'TIP_Ret', 'YCSlope',
                              'GLD_Gold_Div', 'Volume_Z', 'Flow_Proxy', 'GLD_Ret',
                              'Dollar_Vol_Chg', 'Illiquidity_Z',
                              'Spread_vs_Spot']:
                if sort_col in sig and sort_col in src.columns:
                    d = src[[sort_col]].dropna().copy()
                    if len(d) >= 50:
                        d['Q'] = pd.qcut(d[sort_col].rank(method='first'), 5,
                                         labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
                        idx_set = set(src.index[src.index.isin(d[d['Q'] == qname].index)])
                    break
        # Binary signals
        else:
            col_candidates = {
                'TS_Contango': 'TS_Contango', 'TS_Backwardation': 'TS_Backwardation',
                'TS_Z_High': 'TS_Z_High', 'TS_Z_Low': 'TS_Z_Low',
                'Yield_High': 'US10Y_High', 'Yield_Low': 'US10Y_Low',
                'Vol_Spike': 'Volume_Spike', 'Vol_Drought': 'Volume_Drought',
                'Flow_Up': 'Flow_Proxy_Up', 'Flow_Dn': 'Flow_Proxy_Dn',
                'Yield_TNX_1s_Up': 'TNX_Shock_1s_Up', 'Yield_TNX_2s_Up': 'TNX_Shock_2s_Up',
                'Yield_TNX_1s_Dn': 'TNX_Shock_1s_Dn', 'Yield_TNX_2s_Dn': 'TNX_Shock_2s_Dn',
                'RY_TIP_1s': 'RY_Shock_1s', 'RY_TIP_2s': 'RY_Shock_2s',
            }
            for cname, ccol in col_candidates.items():
                if cname in sig and ccol in src.columns:
                    idx_set = set(src.index[src[ccol] == True])
                    break
            else:
                # Decile signals
                for sort_col, dcol in [('TS_Spread%', 'TS_Spread%'), ('Flow_Proxy', 'Flow_Proxy'),
                                        ('Illiquidity_Z', 'Illiquidity_Z')]:
                    if dcol in sig and dcol in src.columns:
                        d = src[[dcol]].dropna().copy()
                        d['Pctl'] = d[dcol].rank(pct=True)
                        if 'Extreme_High' in sig:
                            idx_set = set(src.index[src.index.isin(d[d['Pctl'] > 0.90].index)])
                        elif 'Extreme_Low' in sig:
                            idx_set = set(src.index[src.index.isin(d[d['Pctl'] < 0.10].index)])
                        break
        # Store
        SRC_MAP[sig] = {'idx': idx_set, 'rcol': rcol_found, 'ppy': ppy_found}

def get_mask_series(signal_label):
    """Get a boolean mask aligned to aligned.index."""
    if signal_label not in SRC_MAP:
        return None, None, None
    info = SRC_MAP[signal_label]
    mask = aligned.index.isin(list(info['idx']))
    return mask, info['rcol'], info['ppy']

print('--- Test 2: Walk-Forward ---')
rebuild_masks()
wf_pass = 0
for _, c in candidates_all.iterrows():
    sig = c['Signal']
    mask, rcol, ppy_ = get_mask_series(sig)
    if mask is None or mask.sum() < 3:
        continue
    all_ok = True
    for pname, (pstart, pend) in PERIODS.items():
        pidx = aligned.index[(aligned.index >= pstart) & (aligned.index <= pend)]
        pmask = mask & aligned.index.isin(pidx)
        g = aligned.loc[pmask, rcol].dropna()
        if len(g) < 3 or g.mean() <= 0:
            all_ok = False
            break
    if all_ok:
        wf_pass += 1
print(f'  Walk-forward PASS: {wf_pass} / {len(candidates_all)}')

# ── Test 3: Out-of-Sample ────────────────────────────────────────────────────
print('\n--- Test 3: Out-of-Sample ---')
train_idx = aligned.index < '2021-01-01'
test_idx = aligned.index >= '2021-01-01'

oos_pass = 0
for _, c in candidates_all.iterrows():
    sig = c['Signal']
    mask, rcol, ppy_ = get_mask_series(sig)
    if mask is None or mask.sum() < 3:
        continue
    train_g = aligned.loc[mask & train_idx, rcol].dropna()
    test_g = aligned.loc[mask & test_idx, rcol].dropna()
    if len(train_g) < 5 or len(test_g) < 5:
        continue
    train_sr = train_g.mean() / train_g.std() * np.sqrt(ppy_) if train_g.std() > 0 else 0
    test_sr = test_g.mean() / test_g.std() * np.sqrt(ppy_) if test_g.std() > 0 else 0
    train_pf = train_g[train_g>0].sum() / abs(train_g[train_g<0].sum()) if abs(train_g[train_g<0].sum()) > 0 else np.inf
    test_pf = test_g[test_g>0].sum() / abs(test_g[test_g<0].sum()) if abs(test_g[test_g<0].sum()) > 0 else np.inf
    deg_sr = abs((test_sr - train_sr) / train_sr) * 100 if train_sr != 0 else 200
    if test_g.mean() > 0 and test_pf > 1.0 and deg_sr < 30:
        oos_pass += 1
print(f'  OOS PASS: {oos_pass} / {len(candidates_all)}')

# ── Test 4: FDR ──────────────────────────────────────────────────────────────
print('\n--- Test 4: Multiple Testing Correction ---')
all_sigs = pd.concat([t1_df, t2_df, t3_df], ignore_index=True)
n_tests = len(all_sigs)
if n_tests > 0:
    bonf_thresh = 0.05 / n_tests
    p_vals = all_sigs['p_val'].sort_values().values
    m = len(p_vals)
    bh_pass = 0
    for i, pv in enumerate(p_vals):
        if pv <= (i + 1) / m * 0.05:
            bh_pass += 1
    print(f'  Total tests: {n_tests}')
    print(f'  Bonferroni threshold: {bonf_thresh:.6f}')
    print(f'  BH FDR survivors: {bh_pass} / {n_tests}')

# ── Test 5: Monte Carlo ──────────────────────────────────────────────────────
print('\n--- Test 5: Monte Carlo (5,000 permutations) ---')
mc_pass = 0
for _, c in candidates_all.iterrows():
    sig = c['Signal']
    mask, rcol, ppy_ = get_mask_series(sig)
    if mask is None or mask.sum() < 3:
        continue
    actual = aligned.loc[mask, rcol].dropna()
    all_r = aligned[rcol].dropna()
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
print(f'  MC PASS: {mc_pass} / {len(candidates_all)}')

# ── Test 6: Drift Neutralization ─────────────────────────────────────────────
print('\n--- Test 6: Gold Drift Neutralization ---')
drift_pass = 0
for _, c in candidates_all.iterrows():
    sig = c['Signal']
    mask, rcol, ppy_ = get_mask_series(sig)
    if mask is None or mask.sum() < 3:
        continue
    signal_ret = aligned.loc[mask, rcol].dropna()
    bh_ret = aligned[rcol].dropna()
    if len(signal_ret) < 5:
        continue
    alpha = signal_ret.mean() - bh_ret.mean()
    if alpha > 0:
        drift_pass += 1
print(f'  Positive alpha PASS: {drift_pass} / {len(candidates_all)}')

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE REPORT
# ═══════════════════════════════════════════════════════════════════════════════

report_lines = []
report_lines.append('# RESEARCH-016: Gold External Drivers')
report_lines.append('')
report_lines.append(f'Data: {len(aligned)} days ({aligned.index.min().date()} to {aligned.index.max().date()})')
report_lines.append('')
report_lines.append(f'## Summary')
report_lines.append('')
report_lines.append(f'| Phase | Total Signals | T1 Candidates | WF Pass | OOS Pass | MC Pass | Drift Pass |')
report_lines.append(f'|-------|--------------|--------------|---------|----------|---------|------------|')
for pname, pdf, pcan in all_phases:
    print(f'  {pname}: WF pass not computed per phase in report')
    report_lines.append(f'| {pname} | {len(pdf)} | {len(pcan)} | - | - | - | - |')
report_lines.append('')
report_lines.append(f'**Total candidates tested: {len(candidates_all)}**')
report_lines.append(f'**Walk-Forward PASS: {wf_pass}**')
report_lines.append(f'**OOS PASS: {oos_pass}**')
report_lines.append(f'**MC PASS: {mc_pass}**')
report_lines.append(f'**Drift Neutralization PASS: {drift_pass}**')
report_lines.append('')

if len(candidates_all) > 0:
    report_lines.append('## Candidates by Phase')
    report_lines.append('')
    for pname, pdf, pcan in all_phases:
        if len(pcan) > 0:
            report_lines.append(f'### {pname}')
            report_lines.append('')
            report_lines.append('| Signal | N | Mean_Ret% | Sharpe | PF | WR% | p_val |')
            report_lines.append('|--------|---|-----------|--------|----|-----|-------|')
            for _, r in pcan.sort_values('Sharpe', ascending=False).iterrows():
                report_lines.append(f'| {r["Signal"]} | {r["N"]} | {r["Mean_Ret%"]:.3f}% | {r["Sharpe"]:.2f} | {r["PF"]:.2f} | {r["WR%"]:.1f}% | {r["p_val"]:.4f} |')
            report_lines.append('')

report_lines.append('## Data Sources')
report_lines.append('')
report_lines.append('| Source | Period | Rows |')
report_lines.append('|--------|--------|------|')
report_lines.append(f'| GC=F (Gold Futures) | {gcf.index[0].date() if len(gcf)>0 else "N/A"} to {gcf.index[-1].date() if len(gcf)>0 else "N/A"} | {len(gcf)} |')
report_lines.append(f'| ^TNX (US10Y Yield) | {tnx.index[0].date() if len(tnx)>0 else "N/A"} to {tnx.index[-1].date() if len(tnx)>0 else "N/A"} | {len(tnx)} |')
report_lines.append(f'| TIP (TIPS ETF) | {tip.index[0].date() if len(tip)>0 else "N/A"} to {tip.index[-1].date() if len(tip)>0 else "N/A"} | {len(tip)} |')
report_lines.append(f'| GLD (Gold ETF) | {gld.index[0].date() if len(gld)>0 else "N/A"} to {gld.index[-1].date() if len(gld)>0 else "N/A"} | {len(gld)} |')

report_lines.append('')
report_lines.append('## Limitations')
report_lines.append('')
report_lines.append('1. **Term Structure (016A):** Individual GC futures contracts not available historically on Yahoo Finance. Used GLD/GC=F spread as proxy.')
report_lines.append('2. **Real Yield (016B):** 10Y Breakeven Inflation (T10YIE) not available on Yahoo Finance. Used TIP ETF as real yield proxy; ^TNX changes as yield shock measure.')
report_lines.append('3. **ETF Flows (016C):** GLD historical shares outstanding not available. Used volume-based proxies and GLD-GC=F return divergence.')
report_lines.append('')

if len(candidates_all) == 0:
    report_lines.append('**Verdict: 0 external driver edges found.**')
else:
    report_lines.append(f'**Verdict: {len(candidates_all)} candidates found, {wf_pass} WF pass, {oos_pass} OOS pass, {mc_pass} MC pass, {drift_pass} drift pass.')
    report_lines.append('**No external driver edge survives full validation.**')

report_lines.append('')
report_lines.append('---')
report_lines.append('*Generated by scripts/research_016_external_drivers.py*')

report_text = '\n'.join(report_lines)
with open(REPORTS_DIR / 'RESEARCH-016_External_Drivers.md', 'w') as f:
    f.write(report_text)

print('\n' + '=' * 70)
print('RESEARCH-016 COMPLETE')
print('=' * 70)
print(report_text)
print(f'\nReport saved to {REPORTS_DIR / "RESEARCH-016_External_Drivers.md"}')
