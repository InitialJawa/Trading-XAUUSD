"""
XAU/USD Edge Discovery Framework
Phase 3: Mean Reversion Study
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

print("Loading data...")
df = pd.read_csv("data/XAUUSD_yahoo_raw.csv", index_col=0, parse_dates=True)
close = df['Close'].dropna()

# Parameters
windows = [10, 20, 30, 50]
thresholds = [1.0, 1.5, 2.0, 2.5, 3.0]

results = []
report = []
report.append("# RESEARCH-003: Mean Reversion Study")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** XAU/USD (GC=F)")
report.append(f"**Period:** {close.index.min().strftime('%Y-%m-%d')} to {close.index.max().strftime('%Y-%m-%d')}")
report.append(f"**Observations:** {len(close):,}")
report.append("")
report.append("## Methodology")
report.append("")
report.append("For each rolling window (10, 20, 30, 50 days):")
report.append("1. Calculate z-score of close price relative to rolling mean")
report.append("2. When |z-score| exceeds threshold, record signal")
report.append("3. Measure forward return over the same window")
report.append("4. Test if returns are significantly different from zero")
report.append("")
report.append("## Results")
report.append("")

# For the summary table
all_results = []

for w in windows:
    for t in thresholds:
        rolling_mean = close.rolling(w).mean()
        rolling_std = close.rolling(w).std()
        z_scores = (close - rolling_mean) / rolling_std
        
        signals = []
        for i in range(w, len(close)):
            if abs(z_scores.iloc[i]) >= t:
                entry = close.iloc[i]
                exit_idx = min(i + w, len(close) - 1)
                exit_price = close.iloc[exit_idx]
                ret = (exit_price - entry) / entry
                
                # Mean reversion: short if z-score > threshold (overbought), long if < -threshold (oversold)
                if z_scores.iloc[i] > t:
                    # Overbought - expect reversion down
                    signals.append(-ret)  # short return is positive if price drops
                elif z_scores.iloc[i] < -t:
                    # Oversold - expect reversion up
                    signals.append(ret)
        
        signals = np.array(signals)
        n_events = len(signals)
        
        if n_events > 0:
            win_rate = np.mean(signals > 0) * 100
            avg_ret = np.mean(signals)
            med_ret = np.median(signals)
            std_ret = np.std(signals)
            total_ret = np.sum(signals)
            avg_win = np.mean(signals[signals > 0]) if np.any(signals > 0) else 0
            avg_loss = abs(np.mean(signals[signals <= 0])) if np.any(signals <= 0) else 0
            profit_factor = (np.sum(signals[signals > 0]) / abs(np.sum(signals[signals <= 0]))
                          if np.any(signals <= 0) else np.inf)
            
            # Binomial test: H0: median return = 0 (p=0.5 for positive)
            n_wins = np.sum(signals > 0)
            binom_p = stats.binomtest(n_wins, n_events, p=0.5).pvalue
            
            # T-test: H0: mean return = 0
            t_stat, t_p = stats.ttest_1samp(signals, 0)
            
            # Sharpe-like ratio (for raw returns)
            sharpe = avg_ret / std_ret * np.sqrt(252/w) if std_ret > 0 else 0
            
            # Expected value
            ev = win_rate/100 * avg_win - (1 - win_rate/100) * avg_loss
            
            all_results.append({
                'Window': w,
                'Threshold': t,
                'Events': n_events,
                'Win Rate %': round(win_rate, 2),
                'Avg Return %': round(avg_ret * 100, 4),
                'Med Return %': round(med_ret * 100, 4),
                'Std Dev %': round(std_ret * 100, 4),
                'Avg Win %': round(avg_win * 100, 4),
                'Avg Loss %': round(avg_loss * 100, 4),
                'Profit Factor': round(profit_factor, 4),
                'EV %': round(ev * 100, 4),
                'Sharpe': round(sharpe, 4),
                'Binom P': round(binom_p, 6),
                'T-test P': round(t_p, 6),
                'Sig (α=0.05)': 'YES' if binom_p < 0.05 else 'NO'
            })
            
            print(f"  Window={w:2d}, Thresh={t:.1f}: Events={n_events:4d}, WR={win_rate:5.2f}%, PF={profit_factor:.2f}, BinomP={binom_p:.4f}, Sig={binom_p < 0.05}")
        else:
            all_results.append({
                'Window': w,
                'Threshold': t,
                'Events': 0,
                'Win Rate %': 0,
                'Avg Return %': 0,
                'Med Return %': 0,
                'Std Dev %': 0,
                'Avg Win %': 0,
                'Avg Loss %': 0,
                'Profit Factor': 0,
                'EV %': 0,
                'Sharpe': 0,
                'Binom P': 1.0,
                'T-test P': 1.0,
                'Sig (α=0.05)': 'NO'
            })
            print(f"  Window={w:2d}, Thresh={t:.1f}: No events")

# Summary table
report.append("| Window | Threshold | Events | Win Rate% | Avg Ret% | PF | Sharpe | EV% | Binom P | Sig? |")
report.append("|--------|-----------|--------|-----------|----------|----|--------|-----|---------|------|")
best_entries = []
for r in all_results:
    report.append(f"| {r['Window']} | {r['Threshold']} | {r['Events']} | {r['Win Rate %']} | {r['Avg Return %']} | {r['Profit Factor']} | {r['Sharpe']} | {r['EV %']} | {r['Binom P']} | {r['Sig (α=0.05)']} |")
    if r['Sig (α=0.05)'] == 'YES' and r['Events'] >= 30:
        best_entries.append(r)

report.append("")
report.append("## Best Combinations (Significant, >=30 events)")
report.append("")
if best_entries:
    report.append("| Window | Threshold | Events | Win Rate% | Avg Ret% | PF | Sharpe | Binom P |")
    report.append("|--------|-----------|--------|-----------|----------|----|--------|---------|")
    for r in sorted(best_entries, key=lambda x: x['Binom P']):
        report.append(f"| {r['Window']} | {r['Threshold']} | {r['Events']} | {r['Win Rate %']} | {r['Avg Return %']} | {r['Profit Factor']} | {r['Sharpe']} | {r['Binom P']} |")
else:
    report.append("No statistically significant mean reversion edges found.")

report.append("")
report.append("## Interpretation")
report.append("")
sig_count = sum(1 for r in all_results if r['Sig (α=0.05)'] == 'YES')
pf_gt_13 = sum(1 for r in all_results if r['Profit Factor'] > 1.30 and r['Events'] > 0)
report.append(f"- Total parameter combinations tested: {len(all_results)}")
report.append(f"- Statistically significant (p<0.05): {sig_count}")
report.append(f"- Profit Factor > 1.30: {pf_gt_13}")
success_edges = [r for r in all_results if r['Events'] > 300 and r['Profit Factor'] > 1.30 and r['Binom P'] < 0.05]
report.append(f"- Combinations meeting SUCCESS CRITERIA (Events>300, PF>1.30, p<0.05): {len(success_edges)}")

report.append("")
if len(success_edges) > 0:
    for s in success_edges:
        report.append(f"  - Window={s['Window']}, Threshold={s['Threshold']}: WR={s['Win Rate %']}%, PF={s['Profit Factor']}, Sharpe={s['Sharpe']}")
else:
    report.append("No combinations meet all success criteria.")

# Generate chart
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
df_res = pd.DataFrame(all_results)

for idx, w in enumerate(windows):
    ax = axes[idx // 2, idx % 2]
    subset = df_res[df_res['Window'] == w]
    ax.plot(subset['Threshold'], subset['Win Rate %'], marker='o', label='Win Rate %')
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='No edge (50%)')
    ax.set_title(f'Window={w}')
    ax.set_xlabel('Z-score Threshold')
    ax.set_ylabel('Win Rate %')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.suptitle('Mean Reversion: Win Rate by Window and Threshold', fontsize=14)
plt.tight_layout()
plt.savefig("charts/mean_reversion_winrate.png", dpi=150)
plt.close()
print("Chart saved: charts/mean_reversion_winrate.png")

# Heatmap
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for metric_idx, metric in enumerate(['Win Rate %', 'Profit Factor']):
    ax = axes[metric_idx]
    pivot = df_res.pivot(index='Window', columns='Threshold', values=metric)
    im = ax.imshow(pivot.values, cmap='RdYlGn' if metric == 'Win Rate %' else 'YlOrRd', aspect='auto')
    ax.set_xticks(range(len(thresholds)))
    ax.set_xticklabels(thresholds)
    ax.set_yticks(range(len(windows)))
    ax.set_yticklabels(windows)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Window')
    ax.set_title(metric)
    for i in range(len(windows)):
        for j in range(len(thresholds)):
            val = pivot.values[i, j]
            ax.text(j, i, f'{val:.1f}' if metric == 'Win Rate %' else f'{val:.2f}', ha='center', va='center', fontsize=9)
    plt.colorbar(im, ax=ax)

plt.suptitle('Mean Reversion Performance Heatmap', fontsize=14)
plt.tight_layout()
plt.savefig("charts/mean_reversion_heatmap.png", dpi=150)
plt.close()
print("Chart saved: charts/mean_reversion_heatmap.png")

report.append("")
report.append("## Charts")
report.append("")
report.append("![Mean Reversion Win Rates](../charts/mean_reversion_winrate.png)")
report.append("")
report.append("![Mean Reversion Heatmap](../charts/mean_reversion_heatmap.png)")

report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

with open("reports/RESEARCH-003_Mean_Reversion.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("\nReport saved: reports/RESEARCH-003_Mean_Reversion.md")
print(f"\nSummary: {sig_count}/{len(all_results)} combinations significant, {len(success_edges)} meet all success criteria")
