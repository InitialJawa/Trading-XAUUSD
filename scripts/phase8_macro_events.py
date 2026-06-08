"""
XAU/USD Edge Discovery Framework
Phase 8: Macro Event Effect
Analyze XAU/USD behavior around CPI, NFP, and FOMC events
"""
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

print("Loading XAU/USD data...")
df = pd.read_csv("data/XAUUSD_yahoo_raw.csv", index_col=0, parse_dates=True)
close = df['Close'].dropna()
returns = close.pct_change().dropna()

# Generate known event dates (2000-2026)
# CPI: Typically 2nd or 3rd week of each month (~12th-15th)
# NFP: First Friday of each month
# FOMC: 8 scheduled meetings per year

def get_nfp_dates(start_year=2000, end_year=2026):
    """Get NFP (Non-Farm Payroll) dates - first Friday of each month"""
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # First day of month
            first_day = datetime(year, month, 1)
            # Find first Friday
            days_to_friday = (4 - first_day.weekday()) % 7
            nfp_date = first_day + timedelta(days=days_to_friday)
            dates.append(nfp_date)
    return pd.to_datetime(sorted(dates))

def get_cpi_dates(start_year=2000, end_year=2026):
    """Approximate CPI release dates - around 12th-15th of each month"""
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            cpi_date = datetime(year, month, 12)  # approximate
            dates.append(cpi_date)
    return pd.to_datetime(sorted(dates))

def get_fomc_dates(start_year=2000, end_year=2026):
    """Known FOMC meeting dates (approximate schedule)"""
    # FOMC typically meets 8 times/year: Jan, Mar, May, Jun, Jul, Sep, Nov, Dec
    # Approximate dates - for precise dates we'd need a data feed
    dates = []
    fomc_months = [1, 3, 5, 6, 7, 9, 11, 12]
    for year in range(start_year, end_year + 1):
        for month in fomc_months:
            # Typically around 3rd week
            fomc_date = datetime(year, month, 20)
            dates.append(fomc_date)
    return pd.to_datetime(sorted(dates))

print("Generating event dates (2000-2026)...")
nfp_dates = get_nfp_dates()
cpi_dates = get_cpi_dates()
fomc_dates = get_fomc_dates()

events = {
    'NFP': nfp_dates,
    'CPI': cpi_dates,
    'FOMC': fomc_dates
}

report = []
report.append("# RESEARCH-008: Macro Event Effect")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** XAU/USD (GC=F)")
report.append(f"**Period:** {close.index.min().strftime('%Y-%m-%d')} to {close.index.max().strftime('%Y-%m-%d')}")
report.append("")
report.append("## Methodology")
report.append("")
report.append("For each event type (CPI, NFP, FOMC):")
report.append("- Find the nearest trading day to the event date")
report.append("- Calculate return 1 day before, 1 day after, and 3 days after")
report.append("- Calculate volatility around event vs normal periods")
report.append("- Test if event returns differ significantly from non-event returns")
report.append("")

all_event_results = []

for event_name, event_dates in events.items():
    report.append(f"## {event_name} Events")
    report.append("")
    
    # Find nearest trading days
    event_trading_days = []
    for ed in event_dates:
        mask = close.index >= ed
        # Find closest trading day on or after
        idx = close.index.searchsorted(ed)
        if idx < len(close):
            event_trading_days.append(close.index[idx])
    
    event_trading_days = pd.DatetimeIndex(sorted(set(event_trading_days)))
    
    # Get returns around events
    pre_event_returns = []
    post_event_returns = []
    post3_event_returns = []
    event_day_returns = []
    
    for ed in event_trading_days:
        ed_idx = close.index.get_loc(ed)
        
        # Event day return
        if ed in returns.index:
            event_day_returns.append(returns.loc[ed])
        
        # Pre-event return (1 day before)
        if ed_idx > 0:
            pre_idx = close.index[ed_idx - 1]
            if pre_idx in returns.index:
                pre_event_returns.append(returns.loc[pre_idx])
        
        # Post-event return (1 day after)
        if ed_idx < len(close) - 1:
            post_idx = close.index[ed_idx + 1]
            if post_idx in returns.index:
                post_event_returns.append(returns.loc[post_idx])
        
        # Post-event return (3 days after)
        if ed_idx < len(close) - 3:
            post3_idx = close.index[ed_idx + 3]
            ret_3d = (close.loc[post3_idx] / close.loc[ed] - 1)
            post3_event_returns.append(ret_3d)
    
    n_events = len(event_trading_days)
    
    # Non-event returns (all other days)
    non_event_days = returns.index.difference(event_trading_days)
    non_event_returns = returns.loc[non_event_days]
    
    report.append(f"| Metric | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |")
    report.append(f"|--------|----------------|-----------|------------------|--------------------|-----------|")
    
    periods = {
        'Pre-Event': pre_event_returns,
        'Event Day': event_day_returns,
        'Post-Event': post_event_returns,
        'Post+3d': post3_event_returns,
        'Non-Event': non_event_returns
    }
    
    period_stats = {}
    for period_name, period_data in periods.items():
        if len(period_data) > 0:
            period_data = np.array(period_data)
            n = len(period_data)
            mean_r = np.mean(period_data) * 100
            std_r = np.std(period_data) * 100
            n_up = np.sum(period_data > 0)
            wr = n_up / n * 100
            t_stat, t_pval = stats.ttest_1samp(period_data, 0)
            binom_p = stats.binomtest(n_up, n, p=0.5).pvalue
            period_stats[period_name] = {
                'n': n, 'mean': mean_r, 'std': std_r,
                'wr': wr, 't_p': t_pval, 'binom_p': binom_p
            }
        else:
            period_stats[period_name] = {'n': 0, 'mean': 0, 'std': 0, 'wr': 0, 't_p': 1, 'binom_p': 1}
    
    for stat_name in ['mean', 'std', 'wr']:
        row_name = f"Avg Return %" if stat_name == 'mean' else f"Std Dev %" if stat_name == 'std' else f"Win Rate %"
        vals = [f"{period_stats[p][stat_name]:.4f}" if period_stats[p]['n'] > 0 else "N/A" for p in periods.keys()]
        report.append(f"| {row_name} | {' | '.join(vals)} |")
    
    # Significance tests
    report.append("")
    report.append("### Significance Tests")
    report.append("")
    
    # Compare event vs non-event returns
    for period_name in ['Post-Event', 'Post+3d']:
        event_data = periods[period_name]
        if len(event_data) > 0 and len(non_event_returns) > 0:
            t_stat, t_p = stats.ttest_ind(event_data, non_event_returns)
            report.append(f"- **{period_name} vs Non-Event**: t={t_stat:.4f}, p={t_p:.6f} ({'SIGNIFICANT' if t_p < 0.05 else 'Not significant'})")
    
    # Pre vs Post comparison
    if len(pre_event_returns) > 0 and len(post_event_returns) > 0:
        t_stat, t_p = stats.ttest_ind(pre_event_returns, post_event_returns)
        report.append(f"- **Pre-Event vs Post-Event**: t={t_stat:.4f}, p={t_p:.6f} ({'SIGNIFICANT' if t_p < 0.05 else 'Not significant'})")
    
    # Check for exploitable edge
    # Long post-NFP or short pre-NFP, etc.
    for period_name in ['Post-Event', 'Post+3d']:
        ps = period_stats[period_name]
        if ps['n'] > 30:
            # Simple directional edge
            if abs(ps['wr'] - 50) > 5 and ps['binom_p'] < 0.05:
                all_event_results.append({
                    'Event': f'{event_name} {period_name}',
                    'N Events': ps['n'],
                    'WR%': round(ps['wr'], 2),
                    'Avg Ret%': round(ps['mean'], 4),
                    'Std%': round(ps['std'], 4),
                    'Binom P': round(ps['binom_p'], 6),
                    'Significant': 'YES' if ps['binom_p'] < 0.05 else 'NO'
                })
                report.append(f"\n**Potential edge detected**: {period_name} for {event_name} (WR={ps['wr']:.1f}%, p={ps['binom_p']:.4f})")
    
    report.append("")
    report.append("---")
    report.append("")

# 4. Combined charts
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
event_colors = {'NFP': 'blue', 'CPI': 'orange', 'FOMC': 'red'}

for idx, (event_name, event_dates_list) in enumerate(events.items()):
    row = idx
    # Find nearest trading days
    event_trading_days = []
    for ed in event_dates_list:
        idx_pos = close.index.searchsorted(ed)
        if idx_pos < len(close):
            event_trading_days.append(close.index[idx_pos])
    event_trading_days = pd.DatetimeIndex(sorted(set(event_trading_days)))
    
    # Map events to valid index positions within range
    valid_positions = []
    for ed in event_trading_days:
        try:
            pos = close.index.get_loc(ed)
            if isinstance(pos, slice):
                pos = pos.start
            valid_positions.append(pos)
        except (KeyError, TypeError):
            continue
    
    # Pre/Post returns
    pre_rets = []
    post_rets = []
    for pos in valid_positions:
        if pos > 0 and pos < len(returns) - 1:
            pre_rets.append(returns.iloc[pos - 1] * 100)
            post_rets.append(returns.iloc[pos + 1] * 100)
    
    # Scatter
    axes[row, 0].scatter(pre_rets, post_rets, alpha=0.5, s=10, color=event_colors[event_name])
    axes[row, 0].axhline(y=0, color='black', lw=0.5)
    axes[row, 0].axvline(x=0, color='black', lw=0.5)
    axes[row, 0].set_title(f'{event_name}: Pre vs Post Return')
    axes[row, 0].set_xlabel('Pre-Event Return (%)')
    axes[row, 0].set_ylabel('Post-Event Return (%)')
    axes[row, 0].grid(True, alpha=0.3)
    
    # Histograms
    axes[row, 1].hist(pre_rets, bins=30, alpha=0.5, label='Pre-Event', color='blue')
    axes[row, 1].hist(post_rets, bins=30, alpha=0.5, label='Post-Event', color='green')
    axes[row, 1].axvline(x=np.mean(pre_rets), color='blue', linestyle='--', lw=2)
    axes[row, 1].axvline(x=np.mean(post_rets), color='green', linestyle='--', lw=2)
    axes[row, 1].set_title(f'{event_name}: Return Distribution')
    axes[row, 1].set_xlabel('Return (%)')
    axes[row, 1].legend()
    axes[row, 1].grid(True, alpha=0.3)
    
    # Cumulative post-event returns
    cum_rets = []
    for pos in valid_positions:
        if pos < len(close) - 5:
            cum_ret = (close.iloc[pos + 5] / close.iloc[pos] - 1) * 100
            cum_rets.append(cum_ret)
    
    axes[row, 2].hist(cum_rets, bins=30, alpha=0.7, color=event_colors[event_name])
    axes[row, 2].axvline(x=np.mean(cum_rets), color='red', linestyle='--', lw=2, label=f'Mean: {np.mean(cum_rets):.2f}%')
    axes[row, 2].axvline(x=0, color='black', lw=0.5)
    axes[row, 2].set_title(f'{event_name}: 5-Day Post-Event Return')
    axes[row, 2].set_xlabel('5-Day Return (%)')
    axes[row, 2].legend()
    axes[row, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("charts/macro_events.png", dpi=150)
plt.close()
print("Chart saved: charts/macro_events.png")

report.append("")
report.append("## Charts")
report.append("")
report.append("![Macro Events](../charts/macro_events.png)")

report.append("")
report.append("## Summary")
report.append("")
report.append("| Event Period | N Events | Avg Ret% | WR% | Binom P | Significant? |")
report.append("|-------------|----------|----------|-----|---------|--------------|")
for r in all_event_results:
    report.append(f"| {r['Event']} | {r['N Events']} | {r['Avg Ret%']} | {r['WR%']} | {r['Binom P']} | {r['Significant']} |")

if not all_event_results:
    report.append("| No significant macro event edges found | | | | | |")

report.append("")
report.append("## Conclusion")
report.append("")
report.append("Based on approximate event dates:")
if all_event_results:
    report.append(f"- {len(all_event_results)} potential macro event edges identified")
    for r in all_event_results:
        report.append(f"  - {r['Event']}: WR={r['WR%']}%, p={r['Binom P']}")
else:
    report.append("- No statistically significant macro event edges detected")
report.append("- Note: CPI and FOMC dates are approximate; precise economic calendar data would improve accuracy")
report.append("- NFP dates (first Friday of month) are more reliable")

report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

with open("reports/RESEARCH-008_Macro_Events.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("\nReport saved: reports/RESEARCH-008_Macro_Events.md")
if all_event_results:
    for r in all_event_results:
        print(f"Edge: {r['Event']} - WR={r['WR%']}%, p={r['Binom P']}")
else:
    print("No significant macro event edges found")
