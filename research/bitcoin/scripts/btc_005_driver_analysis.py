"""
BTC-005: Cross-Asset Driver Analysis
Bitcoin vs equities, DXY, gold, yields, etc.
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
DATA_DIR = Path('data')
BTC_DIR = Path('data/bitcoin')
REPORTS_DIR = Path('reports/bitcoin')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

print("Loading data...")

# Bitcoin
btc_df = pd.read_csv(BTC_DIR / 'BTCUSD_cleaned.csv', parse_dates=['Date'], index_col='Date')
btc_close = btc_df['Close'].dropna()
btc_ret = btc_close.pct_change().dropna()
print(f"Bitcoin: {len(btc_close):,} obs, {btc_close.index[0].date()} to {btc_close.index[-1].date()}")

# Gold
try:
    gold = pd.read_csv(DATA_DIR / 'XAUUSD_cleaned.csv', index_col=0, parse_dates=True)
    gold_close = gold['Close'].dropna()
    gold_ret = gold_close.pct_change().dropna()
    print(f"Gold: {len(gold_close):,} obs")
except:
    gold_ret = pd.Series(dtype=float)
    print("Gold data not found")

# Related instruments
drivers_df = pd.read_csv(DATA_DIR / 'related_instruments.csv', index_col=0, parse_dates=True)

all_series = {'BTC': btc_ret}

try:
    if 'DXY' in drivers_df.columns:
        dxy = drivers_df['DXY'].dropna()
        all_series['DXY'] = dxy.pct_change().dropna()
        print(f"DXY: {len(dxy)} obs")
except: pass

try:
    if 'SP500' in drivers_df.columns:
        spx = drivers_df['SP500'].dropna()
        all_series['SP500'] = spx.pct_change().dropna()
except: pass

try:
    if 'VIX' in drivers_df.columns:
        vix = drivers_df['VIX'].dropna()
        all_series['VIX'] = vix  # level
        all_series['VIX_Chg'] = vix.diff()
except: pass

try:
    if 'Crude Oil' in drivers_df.columns:
        oil = drivers_df['Crude Oil'].dropna()
        all_series['Crude_Oil'] = oil.pct_change().dropna()
except: pass

try:
    if 'Silver' in drivers_df.columns:
        silver = drivers_df['Silver'].dropna()
        all_series['Silver'] = silver.pct_change().dropna()
except: pass

try:
    tnx = pd.read_csv(DATA_DIR / 'tnx.csv', parse_dates=['Date'], index_col='Date')
    if 'Close' in tnx.columns:
        tnx_s = tnx['Close'].dropna()
        all_series['US10Y'] = tnx_s  # level
        all_series['US10Y_Chg'] = tnx_s.diff()
except: pass

try:
    gld = pd.read_csv(DATA_DIR / 'gld.csv', parse_dates=['Date'], index_col='Date')
    if 'Close' in gld.columns:
        all_series['GLD'] = gld['Close'].dropna().pct_change().dropna()
except: pass

try:
    ief = pd.read_csv(DATA_DIR / 'ief.csv', parse_dates=['Date'], index_col='Date')
    if 'Close' in ief.columns:
        all_series['IEF'] = ief['Close'].dropna().pct_change().dropna()
except: pass

# Add gold return as driver
if len(gold_ret) > 0:
    all_series['Gold'] = gold_ret

# Align all to common index
aligned = pd.DataFrame()
for name, series in all_series.items():
    aligned[name] = series

aligned = aligned.replace([np.inf, -np.inf], np.nan).dropna()
print(f"Aligned: {len(aligned):,} obs")
print(f"Drivers: {[c for c in aligned.columns if c != 'BTC']}")

core_drivers = [c for c in aligned.columns if c != 'BTC']
report = []
report.append("# BTC-005: Cross-Asset Driver Analysis")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Period:** {aligned.index[0].strftime('%Y-%m-%d')} to {aligned.index[-1].strftime('%Y-%m-%d')}")
report.append(f"**Aligned Observations:** {len(aligned):,}")
report.append(f"**Drivers:** {', '.join(core_drivers)}")
report.append("")

# === TEST 1: CONTEMPORANEOUS CORRELATION ===
print("\nTEST 1: Contemporaneous correlation...")
report.append("## TEST 1: Contemporaneous Return Correlation")
report.append("")

for freq_name, freq_ret in [
    ('Daily', aligned['BTC']),
    ('Weekly', aligned['BTC'].resample('W').apply(lambda x: np.prod(1+x)-1)),
]:
    report.append(f"### {freq_name}")
    report.append("")
    report.append("| Driver | Correlation | R² | P-value |")
    report.append("|--------|-------------|-----|---------|")
    corr_list = []
    for d in core_drivers:
        if d == 'BTC': continue
        common = freq_ret.index.intersection(aligned[d].dropna().index)
        b = freq_ret.loc[common]
        x = aligned[d].loc[common]
        if len(b) > 30:
            r, p = stats.pearsonr(b, x)
            corr_list.append((d, r, p))
            report.append(f"| {d} | {r:+.4f} | {r**2:.4f} | {p:.4e} |")
    if corr_list:
        best = max(corr_list, key=lambda x: abs(x[1]))
        report.append(f"\n**Strongest: {best[0]} (r={best[1]:+.4f})**")
    report.append("")

# === TEST 2: LEAD-LAG ===
print("TEST 2: Lead-lag analysis...")
report.append("## TEST 2: Lead-Lag Analysis")
report.append("")
lags = [-20, -10, -5, -2, -1, 0, 1, 2, 5, 10, 20]
for d in core_drivers:
    if d == 'BTC': continue
    report.append(f"### {d}")
    report.append("")
    report.append("| Lag | Cross-Corr | Interpretation |")
    report.append("|-----|------------|----------------|")
    x_s = aligned[d].dropna()
    b_s = aligned['BTC']
    best_lag, best_c = 0, 0
    for lag in lags:
        if lag < 0:
            sx = x_s.shift(abs(lag))
            v = pd.concat([b_s, sx], axis=1).dropna()
            interp = f"{d} leads {abs(lag)}d"
        elif lag == 0:
            v = pd.concat([b_s, x_s], axis=1).dropna()
            interp = "Same day"
        else:
            sx = x_s.shift(-lag)
            v = pd.concat([b_s, sx], axis=1).dropna()
            interp = f"BTC leads {lag}d"
        if len(v) > 30:
            r, p = stats.pearsonr(v.iloc[:,0], v.iloc[:,1])
            sig = '*' if p<0.05 else ''
            report.append(f"| {lag:+3d} | {r:+.4f}{sig} | {interp} |")
            if abs(r) > abs(best_c):
                best_c, best_lag = r, lag
    report.append(f"\n**Best: lag={best_lag}, r={best_c:+.4f}**")
    report.append("")

# === TEST 3: PREDICTIVE POWER ===
print("TEST 3: Predictive power...")
report.append("## TEST 3: Predictive Power (Univariate)")
report.append("")

for h_days, h_lbl in [(1, '1-Day'), (5, '5-Day'), (20, '20-Day')]:
    report.append(f"### {h_lbl}")
    report.append("")
    report.append("| Driver | R² | Correlation | P-value | Sig? |")
    report.append("|--------|-----|-------------|---------|------|")
    fwd = aligned['BTC'].shift(-h_days)
    sig_drivers = []
    for d in core_drivers:
        if d == 'BTC': continue
        x = aligned[d].dropna()
        y = fwd.loc[x.index]
        v = pd.concat([x, y], axis=1).dropna()
        if len(v) > 60:
            lr = LinearRegression().fit(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)
            r2 = lr.score(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)
            corr, p = stats.pearsonr(v.iloc[:,0], v.iloc[:,1])
            sig = 'YES' if p<0.05 else 'no'
            report.append(f"| {d} | {r2:.6f} | {corr:+.4f} | {p:.4e} | {sig} |")
            if p<0.05: sig_drivers.append((d, r2, corr, p))
    if sig_drivers:
        report.append(f"\n**Significant at {h_lbl}:**")
        for d, r2, c, p in sorted(sig_drivers, key=lambda x: -abs(x[2]))[:3]:
            report.append(f"- {d}: r={c:+.4f}, p={p:.4e}")
    report.append("")

# === TEST 4: CONDITIONAL ===
print("TEST 4: Conditional returns after extreme driver moves...")
report.append("## TEST 4: Conditional Returns After Extreme Driver Moves")
report.append("")

for d in core_drivers:
    if d == 'BTC': continue
    x = aligned[d].dropna()
    for dir_lbl, mask, extreme_lbl in [
        ('Up', x > x.quantile(0.90), 'Top 10% increase'),
        ('Down', x < x.quantile(0.10), 'Top 10% decrease')
    ]:
        dates = x[mask].index
        n = len(dates)
        if n < 20: continue
        report.append(f"### {d} — {extreme_lbl} ({n:,} events)")
        report.append("")
        report.append("| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |")
        report.append("|---------|-----------|----------|----------|------|")
        for h in [1, 5, 20]:
            fwd = aligned['BTC'].shift(-h).loc[dates].dropna()
            if len(fwd) < 10: continue
            mn = fwd.mean() * 100
            wr = (fwd > 0).mean() * 100
            _, tp = stats.ttest_1samp(fwd, 0)
            sig = 'YES' if tp < 0.05 else 'NO'
            report.append(f"| {h}d | {mn:.4f} | {wr:.1f}% | {tp:.4e} | {sig} |")
        report.append("")

# === TEST 5: REGIME ===
print("TEST 5: Regime dependence...")
report.append("## TEST 5: Regime Dependence")
report.append("")
btc_regime = pd.Series('neutral', index=aligned.index)
btc_ma = aligned['BTC'].rolling(252).mean()
btc_regime[aligned['BTC'] > btc_ma] = 'bull'
btc_regime[aligned['BTC'] < btc_ma] = 'bear'
vol = aligned['BTC'].rolling(60).std()
vol_high = vol.quantile(0.67) if len(vol) > 0 else 0
vol_low = vol.quantile(0.33) if len(vol) > 0 else 0

regimes = {
    'Bull BTC (>200d MA)': btc_regime == 'bull',
    'Bear BTC (<200d MA)': btc_regime == 'bear',
}
for r_name, r_mask in regimes.items():
    subset = aligned[r_mask]
    if len(subset) < 60: continue
    report.append(f"### {r_name}  (N={len(subset):,})")
    report.append("")
    report.append("| Driver | Correlation (Regime) | Correlation (Full) | Difference |")
    report.append("|--------|---------------------|--------------------|------------|")
    for d in core_drivers:
        if d == 'BTC': continue
        if d not in subset.columns: continue
        rr, _ = stats.pearsonr(subset['BTC'], subset[d])
        rf, _ = stats.pearsonr(aligned['BTC'], aligned[d])
        report.append(f"| {d} | {rr:+.4f} | {rf:+.4f} | {rr-rf:+.4f} |")
    report.append("")

# === TEST 6: MULTIVARIATE ===
print("TEST 6: Multivariate models...")
report.append("## TEST 6: Multivariate Models (Walk-Forward)")
report.append("")

feature_cols = [d for d in core_drivers if d != 'BTC' and d in aligned.columns]
all_data = aligned[['BTC'] + feature_cols].dropna()
print(f"Model data: {len(all_data):,} obs, {len(feature_cols)} features")

for h_days, h_lbl in [(1, '1-Day'), (5, '5-Day')]:
    report.append(f"### {h_lbl}")
    report.append("")
    target = all_data['BTC'].shift(-h_days)
    data = pd.concat([all_data[feature_cols], target.rename('target')], axis=1).dropna()
    if len(data) < 500:
        report.append("Insufficient data.")
        report.append("")
        continue

    n = len(data)
    train_size = min(1000, n // 2)
    step = max(1, (n - train_size) // 500)

    oos_preds_lr, oos_preds_rf, oos_actuals = [], [], []

    for i in range(train_size, n, step):
        train = data.iloc[:i]
        test = data.iloc[i:i+1]
        if len(test) == 0: continue
        Xtr, ytr = train[feature_cols].values, train['target'].values
        Xte = test[feature_cols].values

        lr = LinearRegression().fit(Xtr, ytr)
        rf = RandomForestRegressor(n_estimators=20, max_depth=4, random_state=42, n_jobs=-1)
        rf.fit(Xtr, ytr)

        oos_preds_lr.append(lr.predict(Xte)[0])
        oos_preds_rf.append(rf.predict(Xte)[0])
        oos_actuals.append(test['target'].values[0])

    oos_a = np.array(oos_actuals)
    oos_lr = np.array(oos_preds_lr)
    oos_rf = np.array(oos_preds_rf)
    n_oos = len(oos_a)

    r2_lr = r2_score(oos_a, oos_lr) if n_oos > 2 else 0
    mae_lr = mean_absolute_error(oos_a, oos_lr)
    dir_lr = np.mean((oos_lr > 0) == (oos_a > 0)) * 100 if n_oos > 0 else 0
    r2_rf = r2_score(oos_a, oos_rf) if n_oos > 2 else 0
    mae_rf = mean_absolute_error(oos_a, oos_rf)
    dir_rf = np.mean((oos_rf > 0) == (oos_a > 0)) * 100 if n_oos > 0 else 0
    base_mae = mean_absolute_error(oos_a, np.zeros_like(oos_a))
    base_dir = np.mean(oos_a > 0) * 100

    report.append("| Metric | Linear Reg | Random Forest | Baseline |")
    report.append("|--------|-----------|---------------|----------|")
    report.append(f"| OOS R² | {r2_lr:.4f} | {r2_rf:.4f} | 0.0 |")
    report.append(f"| OOS MAE | {mae_lr:.6f} | {mae_rf:.6f} | {base_mae:.6f} |")
    report.append(f"| Dir Acc | {dir_lr:.1f}% | {dir_rf:.1f}% | {base_dir:.1f}% |")
    report.append(f"| Samples | {n_oos:,} | {n_oos:,} | {n_oos:,} |")

    verdict = 'NO predictive ability' if r2_lr < 0.001 and dir_lr < base_dir + 1 else 'MARGINAL'
    report.append(f"\n**Verdict: {verdict}**")
    report.append("")

# Ranking
print("Driver ranking...")
report.append("## Driver Ranking Summary")
report.append("")
report.append("| Rank | Driver | Avg |r| | Best Lag | 1d R² | 5d R² | 20d R² | Cond Edge? |")
report.append("|------|--------|---------|----------|--------|-------|--------|------------|")

ranks = []
for d in core_drivers:
    if d == 'BTC': continue
    corrs = []
    for f in [aligned['BTC'], aligned['BTC'].resample('W').apply(lambda x: np.prod(1+x)-1)]:
        c = f.index.intersection(aligned[d].dropna().index)
        if len(c) > 30:
            r, _ = stats.pearsonr(f.loc[c], aligned[d].loc[c])
            corrs.append(abs(r))
    avg_c = np.mean(corrs) if corrs else 0

    pr2 = []
    for h in [1, 5, 20]:
        fwd = aligned['BTC'].shift(-h)
        x = aligned[d].dropna()
        y = fwd.loc[x.index]
        v = pd.concat([x, y], axis=1).dropna()
        if len(v) > 60:
            lr = LinearRegression().fit(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)
            pr2.append(max(0, lr.score(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)))
        else:
            pr2.append(0)

    has_edge = False
    x = aligned[d].dropna()
    for mask in [x > x.quantile(0.90), x < x.quantile(0.10)]:
        dates = x[mask].index
        for h in [1, 5]:
            fwd = aligned['BTC'].shift(-h).loc[dates].dropna()
            if len(fwd) > 20 and stats.ttest_1samp(fwd, 0)[1] < 0.05:
                has_edge = True
    ranks.append((d, avg_c, pr2, has_edge))

for rank, (d, avg_c, pr2, has_edge) in enumerate(sorted(ranks, key=lambda x: -x[1]), 1):
    report.append(f"| {rank} | {d} | {avg_c:.3f} | — | {pr2[0]:.4f} | {pr2[1]:.4f} | {pr2[2]:.4f} | {'YES' if has_edge else 'no'} |")

report.append("")
report.append("---")
report.append("*Generated by research/bitcoin/scripts/btc_005_driver_analysis.py*")

with open(REPORTS_DIR / 'BTC-005_Driver_Analysis.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nReport saved: {REPORTS_DIR / 'BTC-005_Driver_Analysis.md'}")
print("BTC-005 COMPLETE")
