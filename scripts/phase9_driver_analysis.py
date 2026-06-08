"""
RESEARCH-009: Cross-Asset Driver Analysis
XAU/USD Edge Discovery Framework
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
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
print(f"Gold: {len(gold_close)} obs, {gold_close.index[0].date()} to {gold_close.index[-1].date()}")

rel = pd.read_csv("data/related_instruments.csv", index_col=0, parse_dates=True)
drivers = {}
for col in rel.columns:
    s = rel[col].dropna()
    drivers[col] = s
drivers['TLT_close'] = drivers.pop('TLT')

add = pd.read_csv("data/drivers_additional.csv", index_col=0, parse_dates=True)
for col in add.columns:
    s = add[col].dropna()
    k = col.replace('_', ' ')
    drivers[k] = s
drivers['TLT_ret'] = drivers['TLT_close'].pct_change()

all_rets = pd.DataFrame({'Gold': gold_ret})
for name, series in drivers.items():
    if name in ['US10Y', 'DXY', 'SP500', 'VIX', 'Crude Oil', 'Silver', 'TLT_close']:
        s_ret = series.pct_change().dropna()
        all_rets[name] = s_ret
    elif name == 'TLT_ret':
        all_rets[name] = series
drivers['US10Y_chg'] = drivers['US10Y'].diff()
all_rets['US10Y_chg'] = drivers['US10Y_chg']
all_rets['VIX_level'] = drivers['VIX']
all_rets = all_rets.replace([np.inf, -np.inf], np.nan).dropna()
print(f"Aligned: {len(all_rets)} obs")

core_drivers = ['DXY', 'US10Y', 'US10Y_chg', 'SP500', 'VIX', 'Crude Oil', 'Silver', 'TLT_ret']

report = []
report.append("# RESEARCH-009: Cross-Asset Driver Analysis")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Period:** {all_rets.index[0].strftime('%Y-%m-%d')} to {all_rets.index[-1].strftime('%Y-%m-%d')}")
report.append(f"**Aligned Observations:** {len(all_rets):,}")
report.append(f"**Drivers:** {', '.join(core_drivers)}")
report.append("")

# === TEST 1: CONTEMPORANEOUS CORRELATION ===
print("TEST 1: Contemporaneous correlation...")
report.append("## TEST 1: Contemporaneous Return Correlation")

for freq_name, gold_freq, label in [
    ('Daily', gold_ret, 'Daily'),
    ('Weekly', gold_ret.resample('W').apply(lambda x: np.prod(1+x)-1), 'Weekly'),
    ('Monthly', gold_ret.resample('ME').apply(lambda x: np.prod(1+x)-1), 'Monthly')
]:
    report.append(f"\n### {freq_name}\n")
    report.append("| Driver | Correlation | R² | P-value |")
    report.append("|--------|-------------|-----|---------|")
    corr_list = []
    for d in core_drivers:
        if d not in all_rets.columns: continue
        common = gold_freq.index.intersection(all_rets[d].dropna().index)
        g = gold_freq.loc[common]
        x = all_rets[d].loc[common]
        if len(g) > 30:
            r, p = stats.pearsonr(g, x)
            corr_list.append((d, r, p))
            report.append(f"| {d} | {r:+.4f} | {r**2:.4f} | {p:.4e} |")
    if corr_list:
        best = max(corr_list, key=lambda x: abs(x[1]))
        report.append(f"\n**Strongest: {best[0]} (r={best[1]:+.4f})**")

# === TEST 2: LEAD-LAG ===
print("TEST 2: Lead-lag...")
report.append("\n## TEST 2: Lead-Lag Analysis\n")
lags = [-20, -10, -5, -2, -1, 0, 1, 2, 5, 10, 20]
for d in core_drivers:
    if d not in all_rets.columns: continue
    report.append(f"### {d}\n| Lag | Cross-Corr | Interpretation |")
    report.append("|-----|------------|----------------|")
    x_s = all_rets[d].dropna()
    g_s = all_rets['Gold']
    best_lag, best_c = 0, 0
    for lag in lags:
        if lag < 0:
            sx = x_s.shift(abs(lag))
            v = pd.concat([g_s, sx], axis=1).dropna()
            interp = f"{d} leads {abs(lag)}d"
        elif lag == 0:
            v = pd.concat([g_s, x_s], axis=1).dropna()
            interp = "Same day"
        else:
            sx = x_s.shift(-lag)
            v = pd.concat([g_s, sx], axis=1).dropna()
            interp = f"Gold leads {lag}d"
        if len(v) > 30:
            r, p = stats.pearsonr(v.iloc[:,0], v.iloc[:,1])
            sig = '*' if p<0.05 else ''
            report.append(f"| {lag:+3d} | {r:+.4f}{sig} | {interp} |")
            if abs(r) > abs(best_c):
                best_c, best_lag = r, lag
    report.append(f"\n**Best: lag={best_lag}, r={best_c:+.4f}**\n")

# === TEST 3: PREDICTIVE POWER ===
print("TEST 3: Predictive power...")
report.append("\n## TEST 3: Predictive Power (Univariate)\n")

for h_days, h_lbl in [(1, '1-Day'), (5, '5-Day'), (20, '20-Day')]:
    report.append(f"### {h_lbl}\n| Driver | R² | Correlation | P-value | Sig? |")
    report.append("|--------|-----|-------------|---------|------|")
    fwd = gold_ret.shift(-h_days)
    sig_drivers = []
    for d in core_drivers:
        if d not in all_rets.columns: continue
        x = all_rets[d].dropna()
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
        for d,r2,c,p in sorted(sig_drivers, key=lambda x: -abs(x[2]))[:3]:
            report.append(f"- {d}: r={c:+.4f}, p={p:.4e}")

# === TEST 4: CONDITIONAL ===
print("TEST 4: Conditional returns...")
report.append("\n## TEST 4: Conditional Returns After Extreme Driver Moves\n")

for d in core_drivers:
    if d not in all_rets.columns: continue
    x = all_rets[d].dropna()
    for dir_lbl, mask, extreme_lbl in [
        ('Up', x > x.quantile(0.90), 'Top 10% increase'),
        ('Down', x < x.quantile(0.10), 'Top 10% decrease')
    ]:
        dates = x[mask].index
        n = len(dates)
        if n < 20: continue
        report.append(f"### {d} — {extreme_lbl} ({n:,} events)\n")
        report.append("| Horizon | Mean Ret% | Win Rate | T-test P | Sig? |")
        report.append("|---------|-----------|----------|----------|------|")
        for h in [1, 5, 20]:
            fwd = gold_ret.shift(-h).loc[dates].dropna()
            if len(fwd) < 10: continue
            mn = fwd.mean() * 100
            wr = (fwd > 0).mean() * 100
            _, tp = stats.ttest_1samp(fwd, 0)
            sig = 'YES' if tp < 0.05 else 'NO'
            report.append(f"| {h}d | {mn:.4f} | {wr:.1f}% | {tp:.4e} | {sig} |")
        report.append("")

# === TEST 5: REGIME ===
print("TEST 5: Regime dependence...")
report.append("\n## TEST 5: Regime Dependence\n")
gold_regime = pd.Series('neutral', index=gold_close.index)
gold_ma = gold_close.rolling(252).mean()
gold_regime[gold_close > gold_ma] = 'bull'
gold_regime[gold_close < gold_ma] = 'bear'

# Align regime to gold_ret index (previous day's regime)
gold_regime_ret = gold_regime.reindex(gold_ret.index).ffill()

vol = gold_ret.rolling(60).std()
vol_high = vol.quantile(0.67)
vol_low = vol.quantile(0.33)

regimes = {
    'Bull Gold (>200d MA)': all_rets.index.isin(gold_ret.index[gold_regime_ret == 'bull']),
    'Bear Gold (<200d MA)': all_rets.index.isin(gold_ret.index[gold_regime_ret == 'bear']),
}
for r_name, r_mask in regimes.items():
    subset = all_rets[r_mask]
    if len(subset) < 60: continue
    report.append(f"### {r_name}  (N={len(subset):,})\n")
    report.append("| Driver | Correlation | Full Period | Difference |")
    report.append("|--------|-------------|-------------|------------|")
    for d in core_drivers:
        if d not in subset.columns: continue
        rr, _ = stats.pearsonr(subset['Gold'], subset[d])
        rf, _ = stats.pearsonr(all_rets['Gold'], all_rets[d])
        report.append(f"| {d} | {rr:+.4f} | {rf:+.4f} | {rr-rf:+.4f} |")
    report.append("")

# === TEST 6: MULTIVARIATE (OPTIMIZED) ===
print("TEST 6: Multivariate models...")
report.append("\n## TEST 6: Multivariate Models (Walk-Forward)\n")

feature_cols = [d for d in core_drivers if d in all_rets.columns]
all_data = all_rets[['Gold'] + feature_cols].dropna()
print(f"Model data: {len(all_data)} obs, {len(feature_cols)} features")

for h_days, h_lbl in [(1, '1-Day'), (5, '5-Day'), (20, '20-Day')]:
    report.append(f"### {h_lbl}\n")
    target = all_data['Gold'].shift(-h_days)
    data = pd.concat([all_data[feature_cols], target.rename('target')], axis=1).dropna()
    if len(data) < 500:
        report.append("Insufficient data.\n")
        continue

    n = len(data)
    train_size = min(1000, n // 2)
    step = max(1, (n - train_size) // 500)  # ~500 validation points

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

    r2_lr = r2_score(oos_a, oos_lr)
    mae_lr = mean_absolute_error(oos_a, oos_lr)
    dir_lr = np.mean((oos_lr > 0) == (oos_a > 0)) * 100
    r2_rf = r2_score(oos_a, oos_rf)
    mae_rf = mean_absolute_error(oos_a, oos_rf)
    dir_rf = np.mean((oos_rf > 0) == (oos_a > 0)) * 100
    base_mae = mean_absolute_error(oos_a, np.zeros_like(oos_a))
    base_dir = np.mean(oos_a > 0) * 100

    report.append(f"| Metric | Linear Reg | Random Forest | Baseline |")
    report.append(f"|--------|-----------|---------------|----------|")
    report.append(f"| OOS R² | {r2_lr:.4f} | {r2_rf:.4f} | 0.0 |")
    report.append(f"| OOS MAE | {mae_lr:.6f} | {mae_rf:.6f} | {base_mae:.6f} |")
    report.append(f"| Dir Acc | {dir_lr:.1f}% | {dir_rf:.1f}% | {base_dir:.1f}% |")
    report.append(f"| Samples | {n_oos:,} | {n_oos:,} | {n_oos:,} |")

    lr_full = LinearRegression().fit(data[feature_cols].values, data['target'].values)
    coefs = pd.DataFrame({'feature': feature_cols, 'coef': lr_full.coef_}).sort_values('coef', key=abs, ascending=False)
    rf_full = RandomForestRegressor(n_estimators=20, max_depth=4, random_state=42, n_jobs=-1)
    rf_full.fit(data[feature_cols].values, data['target'].values)
    rf_imp = pd.DataFrame({'feature': feature_cols, 'importance': rf_full.feature_importances_}).sort_values('importance', ascending=False)

    report.append(f"\n**Top LR features:** {', '.join(f'{r.feature}({r.coef:+.4f})' for _, r in coefs.head(3).iterrows())}")
    report.append(f"\n**Top RF features:** {', '.join(f'{r.feature}({r.importance:.3f})' for _, r in rf_imp.head(3).iterrows())}")

    verdict = 'NO predictive ability' if r2_lr < 0.001 and dir_lr < base_dir + 1 else 'MARGINAL predictive ability'
    report.append(f"\n**Verdict: {verdict}**\n")

# === RANKING ===
print("Driver ranking...")
report.append("\n## Driver Ranking Summary\n")
report.append("| Rank | Driver | Avg |r| | Best Lag | 1d R² | 5d R² | 20d R² | Cond Edge? |")
report.append("|------|--------|---------|----------|--------|-------|--------|------------|")

ranks = []
for d in core_drivers:
    if d not in all_rets.columns: continue
    corrs = []
    for f in [gold_ret, gold_ret.resample('W').apply(lambda x: np.prod(1+x)-1)]:
        c = f.index.intersection(all_rets[d].dropna().index)
        if len(c) > 30:
            r, _ = stats.pearsonr(f.loc[c], all_rets[d].loc[c])
            corrs.append(abs(r))
    avg_c = np.mean(corrs) if corrs else 0

    # Pred R²
    pr2 = []
    for h in [1,5,20]:
        fwd = gold_ret.shift(-h)
        x = all_rets[d].dropna()
        y = fwd.loc[x.index]
        v = pd.concat([x, y], axis=1).dropna()
        if len(v) > 60:
            lr = LinearRegression().fit(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)
            pr2.append(max(0, lr.score(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)))
        else:
            pr2.append(0)

    # Conditional edge
    has_edge = False
    x = all_rets[d].dropna()
    for mask in [x > x.quantile(0.90), x < x.quantile(0.10)]:
        dates = x[mask].index
        for h in [1,5]:
            fwd = gold_ret.shift(-h).loc[dates].dropna()
            if len(fwd) > 20 and stats.ttest_1samp(fwd, 0)[1] < 0.05:
                has_edge = True

    ranks.append((d, avg_c, pr2, has_edge))

for rank, (d, avg_c, pr2, has_edge) in enumerate(sorted(ranks, key=lambda x: -x[1]), 1):
    report.append(f"| {rank} | {d} | {avg_c:.3f} | — | {pr2[0]:.4f} | {pr2[1]:.4f} | {pr2[2]:.4f} | {'YES' if has_edge else 'no'} |")

# === CHARTS ===
print("Generating charts...")
fig, axes = plt.subplots(3, 3, figsize=(16, 14))

# 1: Correlation matrix
cm = all_rets[['Gold']+core_drivers].corr()
ax = axes[0,0]
im = ax.imshow(cm.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax.set_xticks(range(len(cm.columns)))
ax.set_xticklabels(cm.columns, rotation=45, ha='right', fontsize=7)
ax.set_yticks(range(len(cm.columns)))
ax.set_yticklabels(cm.columns, fontsize=7)
for i in range(len(cm.columns)):
    for j in range(len(cm.columns)):
        ax.text(j,i,f'{cm.values[i,j]:.2f}', ha='center', va='center', fontsize=6)
ax.set_title('Return Correlation Matrix')
plt.colorbar(im, ax=ax)

# 2: DXY scatter
ax = axes[0,1]
if 'DXY' in all_rets.columns:
    ax.scatter(all_rets['DXY']*100, all_rets['Gold']*100, alpha=0.2, s=2, c='steelblue')
    z = np.polyfit(all_rets['DXY']*100, all_rets['Gold']*100, 1)
    xl = np.linspace(all_rets['DXY'].min()*100, all_rets['DXY'].max()*100, 100)
    ax.plot(xl, np.poly1d(z)(xl), 'r-', lw=2)
    r_d, _ = stats.pearsonr(all_rets['DXY'], all_rets['Gold'])
    ax.set_title(f'Gold vs DXY (r={r_d:.3f})')
    ax.set_xlabel('DXY Return %')
    ax.set_ylabel('Gold Return %')
    ax.grid(True, alpha=0.3)

# 3: Lead-lag heatmap
ax = axes[0,2]
llm = np.zeros((len(core_drivers), len(lags)))
for i, d in enumerate(core_drivers):
    if d not in all_rets.columns: continue
    x_s, g_s = all_rets[d].dropna(), all_rets['Gold']
    for j, lag in enumerate(lags):
        if lag < 0: v = pd.concat([g_s, x_s.shift(abs(lag))], axis=1).dropna()
        elif lag == 0: v = pd.concat([g_s, x_s], axis=1).dropna()
        else: v = pd.concat([g_s, x_s.shift(-lag)], axis=1).dropna()
        if len(v) > 30:
            llm[i,j], _ = stats.pearsonr(v.iloc[:,0], v.iloc[:,1])
valid_d = [d for d in core_drivers if d in all_rets.columns]
im = ax.imshow(llm, cmap='RdBu_r', vmin=-0.5, vmax=0.5, aspect='auto')
ax.set_yticks(range(len(valid_d))); ax.set_yticklabels(valid_d, fontsize=8)
ax.set_xticks(range(len(lags))); ax.set_xticklabels(lags, fontsize=7)
ax.set_title('Lead-Lag Cross-Correlation')

# 4: Rolling DXY corr
ax = axes[1,0]
if 'DXY' in all_rets.columns:
    rc = all_rets['Gold'].rolling(60).corr(all_rets['DXY']).dropna()
    ax.plot(rc.index, rc.values, 'b-', lw=0.8)
    ax.axhline(y=rc.mean(), color='red', ls='--', label=f'Mean: {rc.mean():.3f}')
    ax.axhline(y=0, color='black', lw=0.5)
    ax.set_title('60d Rolling Gold-DXY Correlation')
    ax.legend(); ax.grid(True, alpha=0.3)

# 5: Rolling SP500 corr
ax = axes[1,1]
if 'SP500' in all_rets.columns:
    rc = all_rets['Gold'].rolling(60).corr(all_rets['SP500']).dropna()
    ax.plot(rc.index, rc.values, 'g-', lw=0.8)
    ax.axhline(y=rc.mean(), color='red', ls='--', label=f'Mean: {rc.mean():.3f}')
    ax.axhline(y=0, color='black', lw=0.5)
    ax.set_title('60d Rolling Gold-SP500 Correlation')
    ax.legend(); ax.grid(True, alpha=0.3)

# 6: Silver scatter
ax = axes[1,2]
if 'Silver' in all_rets.columns:
    ax.scatter(all_rets['Silver']*100, all_rets['Gold']*100, alpha=0.2, s=2, c='orange')
    z = np.polyfit(all_rets['Silver']*100, all_rets['Gold']*100, 1)
    xl = np.linspace(all_rets['Silver'].min()*100, all_rets['Silver'].max()*100, 100)
    ax.plot(xl, np.poly1d(z)(xl), 'r-', lw=2)
    r_s, _ = stats.pearsonr(all_rets['Silver'], all_rets['Gold'])
    ax.set_title(f'Gold vs Silver (r={r_s:.3f})')
    ax.set_xlabel('Silver Return %'); ax.set_ylabel('Gold Return %')
    ax.grid(True, alpha=0.3)

# 7: Predictive R² bar chart
ax = axes[2,0]
bw = 0.25
for h_idx, (h, lbl) in enumerate([(1,'1d'),(5,'5d'),(20,'20d')]):
    r2s, labs = [], []
    for d in core_drivers:
        if d not in all_rets.columns: continue
        fwd = gold_ret.shift(-h)
        x = all_rets[d].dropna()
        v = pd.concat([x, fwd.loc[x.index]], axis=1).dropna()
        if len(v) > 60:
            lr = LinearRegression().fit(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)
            r2s.append(max(0, lr.score(v.iloc[:,0].values.reshape(-1,1), v.iloc[:,1].values)))
            labs.append(d)
    if r2s:
        xp = np.arange(len(labs)) + h_idx * bw
        ax.bar(xp, r2s, bw, alpha=0.7, label=lbl)
        if h_idx == 0:
            ax.set_xticks(np.arange(len(labs)) + bw)
            ax.set_xticklabels(labs, rotation=45, ha='right', fontsize=7)
ax.set_title('Predictive R² by Driver & Horizon')
ax.legend(fontsize=8); ax.grid(True, alpha=0.3, axis='y')

# 8: OOS comparison
ax = axes[2,1]
ax.axis('off')
ax.text(0.5, 0.5, 'OOS Model Results\nSee report tables', ha='center', va='center', transform=ax.transAxes, fontsize=12)
ax.set_title('OOS Model Performance')

# 9: VIX scatter
ax = axes[2,2]
if 'VIX' in all_rets.columns:
    ax.scatter(all_rets['VIX_level'], all_rets['Gold']*100, alpha=0.15, s=2, c='purple')
    r_v, _ = stats.pearsonr(all_rets['VIX_level'].dropna(), all_rets['Gold'].loc[all_rets['VIX_level'].dropna().index])
    ax.set_title(f'Gold vs VIX Level (r={r_v:.3f})')
    ax.set_xlabel('VIX Level'); ax.set_ylabel('Gold Return %')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("charts/driver_analysis_comprehensive.png", dpi=150)
plt.close()
print("Chart saved.")

report.append("\n---\n*Generated by XAU/USD Edge Discovery Framework*")

with open("reports/RESEARCH-009_Driver_Analysis.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"\n{'='*60}")
print("DRIVER ANALYSIS COMPLETE")
print(f"{'='*60}")
print(f"Top drivers:")
for d, av, pr2, _ in sorted(ranks, key=lambda x: -x[1])[:5]:
    r,_ = stats.pearsonr(all_rets['Gold'], all_rets[d])
    print(f"  {d}: r={r:+.4f}, avg|r|={av:.3f}")
print(f"Report: reports/RESEARCH-009_Driver_Analysis.md")
