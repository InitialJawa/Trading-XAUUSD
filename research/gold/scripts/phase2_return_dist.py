"""
XAU/USD Edge Discovery Framework
Phase 2: Return Distribution Analysis
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

# Calculate returns
daily_return = close.pct_change().dropna()
log_return = np.log(close / close.shift(1)).dropna()

report = []
report.append("# RESEARCH-002: Return Distribution Analysis")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** XAU/USD (GC=F)")
report.append(f"**Period:** {close.index.min().strftime('%Y-%m-%d')} to {close.index.max().strftime('%Y-%m-%d')}")
report.append(f"**Observations:** {len(daily_return):,}")
report.append("")

# 1. Summary statistics
report.append("## 1. Summary Statistics")
report.append("")
report.append("| Statistic | Daily Return | Log Return |")
report.append("|-----------|-------------|------------|")
report.append(f"| Mean | {daily_return.mean():.8f} | {log_return.mean():.8f} |")
report.append(f"| Median | {daily_return.median():.8f} | {log_return.median():.8f} |")
report.append(f"| Std Dev | {daily_return.std():.6f} | {log_return.std():.6f} |")
report.append(f"| Variance | {daily_return.var():.8f} | {log_return.var():.8f} |")
report.append(f"| Skewness | {daily_return.skew():.4f} | {log_return.skew():.4f} |")
report.append(f"| Kurtosis | {daily_return.kurtosis():.4f} | {log_return.kurtosis():.4f} |")
report.append(f"| Min | {daily_return.min():.6f} | {log_return.min():.6f} |")
report.append(f"| Max | {daily_return.max():.6f} | {log_return.max():.6f} |")
report.append(f"| Range | {daily_return.max() - daily_return.min():.6f} | {log_return.max() - log_return.min():.6f} |")

# 2. Normality tests
report.append("")
report.append("## 2. Normality Tests")
report.append("")

# Jarque-Bera
jb_stat, jb_p = stats.jarque_bera(daily_return)
report.append("### Jarque-Bera Test (Daily Return)")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| JB Statistic | {jb_stat:.4f} |")
report.append(f"| P-value | {jb_p:.6e} |")
report.append(f"| Normal at α=0.05? | {'No' if jb_p < 0.05 else 'Yes'} |")

jb_stat_l, jb_p_l = stats.jarque_bera(log_return)
report.append("")
report.append("### Jarque-Bera Test (Log Return)")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| JB Statistic | {jb_stat_l:.4f} |")
report.append(f"| P-value | {jb_p_l:.6e} |")
report.append(f"| Normal at α=0.05? | {'No' if jb_p_l < 0.05 else 'Yes'} |")

# Shapiro-Wilk (limit to 5000 samples)
report.append("")
report.append("### Shapiro-Wilk Test (Daily Return, max 5000 samples)")
report.append("")
sw_sample = daily_return.sample(min(5000, len(daily_return)), random_state=42)
sw_stat, sw_p = stats.shapiro(sw_sample)
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| W Statistic | {sw_stat:.6f} |")
report.append(f"| P-value | {sw_p:.6e} |")
report.append(f"| Normal at α=0.05? | {'No' if sw_p < 0.05 else 'Yes'} |")

# D'Agostino-Pearson
dp_stat, dp_p = stats.normaltest(daily_return)
report.append("")
report.append("### D'Agostino-Pearson Test (Daily Return)")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| K² Statistic | {dp_stat:.4f} |")
report.append(f"| P-value | {dp_p:.6e} |")
report.append(f"| Normal at α=0.05? | {'No' if dp_p < 0.05 else 'Yes'} |")

# 3. Interpretation
report.append("")
report.append("## 3. Findings")
report.append("")
mean_ann = daily_return.mean() * 252
std_ann = daily_return.std() * np.sqrt(252)
report.append(f"- Annualized mean return: {mean_ann*100:.2f}%")
report.append(f"- Annualized volatility: {std_ann*100:.2f}%")
report.append(f"- Sharpe ratio (0% risk-free): {mean_ann/std_ann:.4f}" if std_ann > 0 else "- Sharpe ratio: N/A (zero vol)")

# Check if normal
all_tests_pass = True
for p in [jb_p, sw_p, dp_p]:
    if p >= 0.05:
        all_tests_pass = False
        break

if all_tests_pass:
    report.append("\n**Conclusion: Daily returns DO follow a normal distribution** (all normality tests fail to reject H0 at α=0.05)")
else:
    report.append("\n**Conclusion: Daily returns do NOT follow a normal distribution** (normality tests reject H0 at α=0.05)")

report.append(f"- Skewness ({daily_return.skew():.4f}) indicates a {'symmetric' if abs(daily_return.skew()) < 0.1 else 'asymmetric'} distribution")
report.append(f"- Kurtosis ({daily_return.kurtosis():.4f}) indicates a {'normal' if abs(daily_return.kurtosis()) < 0.5 else 'fat-tailed' if daily_return.kurtosis() > 0 else 'thin-tailed'} distribution")

# 4. Generate chart
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Histogram of daily returns
axes[0, 0].hist(daily_return, bins=100, density=True, alpha=0.7, color='gold', edgecolor='black')
x = np.linspace(daily_return.min(), daily_return.max(), 100)
axes[0, 0].plot(x, stats.norm.pdf(x, daily_return.mean(), daily_return.std()),
         'r-', lw=2, label='Normal PDF')
axes[0, 0].set_title(f'Daily Return Distribution (N={len(daily_return):,})')
axes[0, 0].set_xlabel('Daily Return')
axes[0, 0].set_ylabel('Density')
axes[0, 0].legend()

# Q-Q plot
stats.probplot(daily_return, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Q-Q Plot (Daily Return)')

# Histogram of log returns
axes[1, 0].hist(log_return, bins=100, density=True, alpha=0.7, color='orange', edgecolor='black')
axes[1, 0].plot(x, stats.norm.pdf(x, log_return.mean(), log_return.std()),
         'r-', lw=2, label='Normal PDF')
axes[1, 0].set_title(f'Log Return Distribution (N={len(log_return):,})')
axes[1, 0].set_xlabel('Log Return')
axes[1, 0].set_ylabel('Density')
axes[1, 0].legend()

# Box plot
axes[1, 1].boxplot([daily_return, log_return], labels=['Daily Return', 'Log Return'])
axes[1, 1].set_title('Return Distribution - Box Plot')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("charts/return_distribution.png", dpi=150)
plt.close()
print("Chart saved: charts/return_distribution.png")

# Also produce rolling statistics chart
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
axes[0].plot(close.index, close, color='gold', lw=1)
axes[0].set_title('XAU/USD Price')
axes[0].set_ylabel('Price ($)')
axes[0].grid(True, alpha=0.3)

axes[1].plot(daily_return.index, daily_return, color='blue', lw=0.5, alpha=0.6)
axes[1].axhline(y=0, color='red', linestyle='--', lw=0.5)
axes[1].set_title('Daily Returns')
axes[1].set_ylabel('Return')
axes[1].grid(True, alpha=0.3)

# Rolling mean + std
rolling_mean = daily_return.rolling(252).mean()
rolling_std = daily_return.rolling(252).std()
axes[2].plot(rolling_mean.index, rolling_mean, label='252d Rolling Mean', color='green', lw=1)
axes[2].plot(rolling_std.index, rolling_std, label='252d Rolling Std', color='red', lw=1)
axes[2].axhline(y=0, color='black', linestyle='--', lw=0.5)
axes[2].set_title('Rolling Statistics (252-day window)')
axes[2].set_ylabel('Value')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("charts/price_returns_rolling.png", dpi=150)
plt.close()
print("Chart saved: charts/price_returns_rolling.png")

report.append("")
report.append("## 5. Charts")
report.append("")
report.append("![Return Distribution](../charts/return_distribution.png)")
report.append("")
report.append("![Price and Rolling Stats](../charts/price_returns_rolling.png)")

report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

with open("reports/RESEARCH-002_Return_Distribution.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Report saved: reports/RESEARCH-002_Return_Distribution.md")
print(f"\nKey findings:")
print(f"  Mean daily return: {daily_return.mean()*100:.4f}%")
print(f"  Daily std dev: {daily_return.std()*100:.2f}%")
print(f"  Skewness: {daily_return.skew():.4f}")
print(f"  Kurtosis: {daily_return.kurtosis():.4f}")
print(f"  JB p-value: {jb_p:.6e}")
print(f"  Normally distributed? {'YES' if jb_p >= 0.05 else 'NO'}")
