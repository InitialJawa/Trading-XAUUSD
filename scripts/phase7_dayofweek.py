"""
XAU/USD Edge Discovery Framework
Phase 7: Day of Week Effect
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

returns = close.pct_change().dropna()
df_ret = returns.to_frame('return')
df_ret['day'] = df_ret.index.dayofweek
df_ret['day_name'] = df_ret.index.strftime('%A')

day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

report = []
report.append("# RESEARCH-007: Day of Week Effect")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** XAU/USD (GC=F)")
report.append(f"**Period:** {close.index.min().strftime('%Y-%m-%d')} to {close.index.max().strftime('%Y-%m-%d')}")
report.append(f"**Observations:** {len(returns):,}")
report.append("")

# 1. Day of week statistics
report.append("## 1. Daily Return by Day of Week")
report.append("")
report.append("| Day | Count | Mean Ret% | Median Ret% | Std% | Win Rate% | Avg Win% | Avg Loss% | PF | Sharpe (ann) |")
report.append("|-----|-------|-----------|-------------|------|-----------|----------|-----------|----|-------------|")

day_stats = {}
all_day_data = []
for day_num, day_name in day_map.items():
    data = df_ret[df_ret['day'] == day_num]['return']
    all_day_data.append(data.values)
    n = len(data)
    mean_r = data.mean() * 100
    med_r = data.median() * 100
    std_r = data.std() * 100
    n_up = (data > 0).sum()
    wr = n_up / n * 100
    avg_win = data[data > 0].mean() * 100 if (data > 0).any() else 0
    avg_loss = data[data < 0].mean() * 100 if (data < 0).any() else 0
    gross_win = data[data > 0].sum()
    gross_loss = abs(data[data < 0].sum())
    pf = gross_win / gross_loss if gross_loss > 0 else np.inf
    sharpe = (data.mean() / data.std() * np.sqrt(252)) if data.std() > 0 else 0
    
    day_stats[day_name] = {
        'data': data, 'n': n, 'mean_r': mean_r, 'med_r': med_r,
        'std_r': std_r, 'wr': wr, 'avg_win': avg_win,
        'avg_loss': avg_loss, 'pf': pf, 'sharpe': sharpe,
        'n_up': n_up
    }
    report.append(f"| {day_name} | {n:,} | {mean_r:.4f} | {med_r:.4f} | {std_r:.4f} | {wr:.2f} | {avg_win:.4f} | {avg_loss:.4f} | {pf:.4f} | {sharpe:.4f} |")

# 2. Significance testing
report.append("")
report.append("## 2. Statistical Significance Tests")
report.append("")

# ANOVA: are mean returns different across days?
f_stat, anova_p = stats.f_oneway(*all_day_data)
report.append("### ANOVA: Are mean returns equal across all days?")
report.append("")
report.append(f"| Statistic | Value |")
report.append(f"|-----------|-------|")
report.append(f"| F-statistic | {f_stat:.4f} |")
report.append(f"| P-value | {anova_p:.6f} |")
report.append(f"| Significant difference? | {'YES' if anova_p < 0.05 else 'NO'} |")
report.append("")

# Kruskal-Wallis (non-parametric alternative)
h_stat, kw_p = stats.kruskal(*all_day_data)
report.append("### Kruskal-Wallis: Non-parametric test")
report.append("")
report.append(f"| Statistic | Value |")
report.append(f"|-----------|-------|")
report.append(f"| H-statistic | {h_stat:.4f} |")
report.append(f"| P-value | {kw_p:.6f} |")
report.append(f"| Significant difference? | {'YES' if kw_p < 0.05 else 'NO'} |")
report.append("")

# Individual day tests: is each day's mean return different from 0?
report.append("### T-test: Is each day's mean return different from zero?")
report.append("")
report.append("| Day | T-stat | P-value | Significant? |")
report.append("|-----|--------|---------|--------------|")
for day_name in day_order:
    data = day_stats[day_name]['data']
    t, p = stats.ttest_1samp(data, 0)
    report.append(f"| {day_name} | {t:.4f} | {p:.6f} | {'YES' if p < 0.05 else 'NO'} |")

# Binomial test for each day
report.append("")
report.append("### Binomial Test: Is win rate different from 50%?")
report.append("")
report.append("| Day | Win Rate% | N Wins | N Total | Binom P | Significant? |")
report.append("|-----|-----------|--------|---------|---------|--------------|")
for day_name in day_order:
    s = day_stats[day_name]
    binom_p = stats.binomtest(s['n_up'], s['n'], p=0.5).pvalue
    report.append(f"| {day_name} | {s['wr']:.2f} | {s['n_up']} | {s['n']} | {binom_p:.6f} | {'YES' if binom_p < 0.05 else 'NO'} |")

# 3. Best/Worst days
report.append("")
report.append("## 3. Day Ranking")
report.append("")
sorted_by_mean = sorted(day_order, key=lambda d: day_stats[d]['mean_r'], reverse=True)
report.append("**By Mean Return:**")
for i, d in enumerate(sorted_by_mean, 1):
    s = day_stats[d]
    report.append(f"  {i}. {d}: {s['mean_r']:.4f}% (WR: {s['wr']:.2f}%, PF: {s['pf']:.4f})")

sorted_by_sharpe = sorted(day_order, key=lambda d: day_stats[d]['sharpe'], reverse=True)
report.append("")
report.append("**By Sharpe Ratio:**")
for i, d in enumerate(sorted_by_sharpe, 1):
    s = day_stats[d]
    report.append(f"  {i}. {d}: {s['sharpe']:.4f} (Ret: {s['mean_r']:.4f}%, WR: {s['wr']:.2f}%)")

# 4. Chart
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Mean return by day
days_list = list(day_order)
means = [day_stats[d]['mean_r'] for d in days_list]
colors = ['green' if m > 0 else 'red' for m in means]
axes[0, 0].bar(days_list, means, color=colors, alpha=0.7, edgecolor='black')
axes[0, 0].axhline(y=0, color='black', lw=0.5)
axes[0, 0].set_title('Mean Daily Return by Day of Week')
axes[0, 0].set_ylabel('Mean Return (%)')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Win rate by day
wrs = [day_stats[d]['wr'] for d in days_list]
axes[0, 1].bar(days_list, wrs, color='steelblue', alpha=0.7, edgecolor='black')
axes[0, 1].axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50%')
axes[0, 1].set_title('Win Rate by Day of Week')
axes[0, 1].set_ylabel('Win Rate (%)')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Sharpe by day
sharpe_vals = [day_stats[d]['sharpe'] for d in days_list]
colors_s = ['green' if s > 0 else 'red' for s in sharpe_vals]
axes[1, 0].bar(days_list, sharpe_vals, color=colors_s, alpha=0.7, edgecolor='black')
axes[1, 0].axhline(y=0, color='black', lw=0.5)
axes[1, 0].set_title('Sharpe Ratio by Day of Week')
axes[1, 0].set_ylabel('Sharpe (annualized)')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Box plot
bp_data = [day_stats[d]['data'] for d in days_list]
bp = axes[1, 1].boxplot(bp_data, labels=days_list, patch_artist=True)
for patch, color in zip(bp['boxes'], ['gold', 'silver', 'orange', 'lightblue', 'lightgreen']):
    patch.set_facecolor(color)
axes[1, 1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
axes[1, 1].set_title('Return Distribution by Day of Week')
axes[1, 1].set_ylabel('Return')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig("charts/day_of_week.png", dpi=150)
plt.close()
print("Chart saved: charts/day_of_week.png")

report.append("")
report.append("## Charts")
report.append("")
report.append("![Day of Week Effect](../charts/day_of_week.png)")

report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

with open("reports/RESEARCH-007_Day_Of_Week.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("\nReport saved: reports/RESEARCH-007_Day_Of_Week.md")
print(f"ANOVA p-value: {anova_p:.6f}")
print(f"Best day (mean): {sorted_by_mean[0]} ({day_stats[sorted_by_mean[0]]['mean_r']:.4f}%)")
print(f"Worst day (mean): {sorted_by_mean[-1]} ({day_stats[sorted_by_mean[-1]]['mean_r']:.4f}%)")
