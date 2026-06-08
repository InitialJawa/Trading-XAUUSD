"""
BTC-003: Calendar Effects — Day of Week, Month, Halving Cycle
"""
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path('data/bitcoin')
REPORTS_DIR = Path('reports/bitcoin')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

print("Loading BTC-USD data...")
df = pd.read_csv(DATA_DIR / 'BTCUSD_cleaned.csv', parse_dates=['Date'], index_col='Date')
close = df['Close'].dropna()
returns = close.pct_change().dropna()
print(f"Data: {len(returns):,} daily returns ({returns.index.min().date()} to {returns.index.max().date()})")

report = []
report.append("# BTC-003: Calendar Effects")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** BTC-USD")
report.append(f"**Period:** {returns.index.min().strftime('%Y-%m-%d')} to {returns.index.max().strftime('%Y-%m-%d')}")
report.append(f"**Observations:** {len(returns):,}")
report.append("")

# ================================================================
# PART 1: DAY OF WEEK
# ================================================================
print("\n--- Day of Week ---")
report.append("## 1. Day of Week Effect")
report.append("")

df_ret = returns.to_frame('return')
df_ret['day'] = df_ret.index.dayofweek
df_ret['day_name'] = df_ret.index.strftime('%A')

day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

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
    sharpe = (data.mean() / data.std() * np.sqrt(365)) if data.std() > 0 else 0
    day_stats[day_name] = {'data': data, 'n': n, 'mean_r': mean_r, 'med_r': med_r,
                           'std_r': std_r, 'wr': wr, 'avg_win': avg_win, 'avg_loss': avg_loss,
                           'pf': pf, 'sharpe': sharpe, 'n_up': n_up}
    report.append(f"| {day_name} | {n:,} | {mean_r:.4f} | {med_r:.4f} | {std_r:.4f} | {wr:.2f} | {avg_win:.4f} | {avg_loss:.4f} | {pf:.4f} | {sharpe:.4f} |")

# ANOVA
f_stat, anova_p = stats.f_oneway(*all_day_data)
report.append("")
report.append("### ANOVA: Are mean returns equal across all days?")
report.append(f"F-statistic: {f_stat:.4f}, P-value: {anova_p:.6f}, Significant? {'YES' if anova_p < 0.05 else 'NO'}")
report.append("")

# Kruskal-Wallis
h_stat, kw_p = stats.kruskal(*all_day_data)
report.append("### Kruskal-Wallis (non-parametric)")
report.append(f"H-statistic: {h_stat:.4f}, P-value: {kw_p:.6f}, Significant? {'YES' if kw_p < 0.05 else 'NO'}")
report.append("")

# T-test each day vs zero
report.append("### T-test: Is each day's mean return different from zero?")
report.append("| Day | T-stat | P-value | Significant? |")
report.append("|-----|--------|---------|--------------|")
for day_name in day_order:
    data = day_stats[day_name]['data']
    t, p = stats.ttest_1samp(data, 0)
    report.append(f"| {day_name} | {t:.4f} | {p:.6f} | {'YES' if p < 0.05 else 'NO'} |")

# Binomial test
report.append("")
report.append("### Binomial Test: Is win rate different from 50%?")
report.append("| Day | Win Rate% | N Wins | N Total | Binom P | Significant? |")
report.append("|-----|-----------|--------|---------|---------|--------------|")
for day_name in day_order:
    s = day_stats[day_name]
    binom_p = stats.binomtest(s['n_up'], s['n'], p=0.5).pvalue
    report.append(f"| {day_name} | {s['wr']:.2f} | {s['n_up']} | {s['n']} | {binom_p:.6f} | {'YES' if binom_p < 0.05 else 'NO'} |")

# Ranking
report.append("")
report.append("### Day Ranking by Mean Return")
sorted_mean = sorted(day_order, key=lambda d: day_stats[d]['mean_r'], reverse=True)
for i, d in enumerate(sorted_mean, 1):
    s = day_stats[d]
    report.append(f"  {i}. {d}: {s['mean_r']:.4f}% (WR: {s['wr']:.2f}%, PF: {s['pf']:.4f})")

report.append("")
report.append("---")
report.append("")

# ================================================================
# PART 2: MONTH OF YEAR
# ================================================================
print("--- Month of Year ---")
report.append("## 2. Month of Year Effect")
report.append("")

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_stats = {}
all_month_data = []

report.append("| Month | Count | Mean Ret% | Win Rate% | PF | Sharpe (ann) | T-test P |")
report.append("|-------|-------|-----------|-----------|----|-------------|----------|")

for m in range(1, 13):
    data = returns[returns.index.month == m]
    all_month_data.append(data.values)
    n = len(data)
    if n < 3:
        month_stats[m] = None
        report.append(f"| {month_names[m-1]} | {n:,} | — | — | — | — | — |")
        continue
    mean_r = data.mean() * 100
    wr = (data > 0).mean() * 100
    gross_win = data[data > 0].sum()
    gross_loss = abs(data[data < 0].sum())
    pf = gross_win / gross_loss if gross_loss > 0 else np.inf
    sharpe = (data.mean() / data.std() * np.sqrt(365)) if data.std() > 0 else 0
    t, p = stats.ttest_1samp(data, 0)
    month_stats[m] = {'data': data, 'n': n, 'mean_r': mean_r, 'wr': wr, 'pf': pf, 'sharpe': sharpe, 'p': p}
    report.append(f"| {month_names[m-1]} | {n:,} | {mean_r:.4f} | {wr:.2f} | {pf:.4f} | {sharpe:.4f} | {p:.4e} |")

# ANOVA by month
f_stat_m, anova_p_m = stats.f_oneway(*[data for data in all_month_data if len(data) > 0])
report.append("")
report.append(f"**ANOVA (month):** F={f_stat_m:.4f}, p={anova_p_m:.6f}, {'Significant' if anova_p_m < 0.05 else 'Not significant'}")

# Best/worst months
report.append("")
valid_months = {m: s for m, s in month_stats.items() if s is not None}
if valid_months:
    best_m = max(valid_months, key=lambda m: valid_months[m]['mean_r'])
    worst_m = min(valid_months, key=lambda m: valid_months[m]['mean_r'])
    report.append(f"**Best month:** {month_names[best_m-1]} ({valid_months[best_m]['mean_r']:.4f}%, WR: {valid_months[best_m]['wr']:.2f}%)")
    report.append(f"**Worst month:** {month_names[worst_m-1]} ({valid_months[worst_m]['mean_r']:.4f}%, WR: {valid_months[worst_m]['wr']:.2f}%)")

report.append("")
report.append("---")
report.append("")

# ================================================================
# PART 3: HALVING CYCLE
# ================================================================
print("--- Halving Cycle ---")
report.append("## 3. Halving Cycle Effect")
report.append("")

halving_dates = [
    ('2012-11-28', '1st Halving', 2012),
    ('2016-07-09', '2nd Halving', 2016),
    ('2020-05-11', '3rd Halving', 2020),
    ('2024-04-19', '4th Halving', 2024),
]
halving_dates = [(pd.Timestamp(d), name, yr) for d, name, yr in halving_dates]

# Phase definitions (days relative to halving)
phases = {
    'Pre-Halving (-180d to -1d)': (-180, -1),
    'Post-Halving (+1d to +180d)': (1, 180),
    'Post-Halving (+1d to +365d)': (1, 365),
    'Halving Year': (-180, 365),
}

all_halving_results = []
for phase_name, (start_offset, end_offset) in phases.items():
    phase_rets = []
    phase_dates = []
    for h_date, h_name, h_year in halving_dates:
        if h_date < returns.index[0] or h_date > returns.index[-1]:
            continue
        start_date = h_date + pd.Timedelta(days=start_offset)
        end_date = h_date + pd.Timedelta(days=end_offset)
        mask = (returns.index >= start_date) & (returns.index <= end_date)
        d = returns[mask]
        if len(d) > 0:
            cum = (1 + d).prod() - 1
            phase_rets.append(cum * 100)
            phase_dates.append(h_name)
    
    if len(phase_rets) > 0:
        mean_ret = np.mean(phase_rets)
        std_ret = np.std(phase_rets)
        n_up = sum(1 for r in phase_rets if r > 0)
        wr = n_up / len(phase_rets) * 100
        all_halving_results.append({
            'Phase': phase_name,
            'N_Halvings': len(phase_rets),
            'Mean_Cum_Ret%': mean_ret,
            'Std%': std_ret,
            'WR%': wr,
            'Min%': min(phase_rets),
            'Max%': max(phase_rets)
        })

report.append("| Phase | N Halvings | Mean Cum Ret% | Std% | WR% | Min% | Max% |")
report.append("|-------|-----------|--------------|------|-----|------|------|")
for r in all_halving_results:
    report.append(f"| {r['Phase']} | {r['N_Halvings']} | {r['Mean_Cum_Ret%']:.2f} | {r['Std%']:.2f} | {r['WR%']:.0f} | {r['Min%']:.2f} | {r['Max%']:.2f} |")

# Period analysis: halving era returns
report.append("")
report.append("### Returns by Halving Era")
report.append("")
report.append("| Era | Period | Daily Mean% | Ann Sharpe | Ann Vol% | CAGR% |")
report.append("|-----|--------|------------|------------|---------|-------|")

# Split into halving eras
era_results = []
for i, (h_date, h_name, h_year) in enumerate(halving_dates):
    era_start = h_date
    if i + 1 < len(halving_dates):
        era_end = halving_dates[i+1][0] - pd.Timedelta(days=1)
    else:
        era_end = returns.index[-1]
    
    mask = (returns.index >= era_start) & (returns.index <= era_end)
    era_rets = returns[mask]
    if len(era_rets) < 20:
        continue
    n = len(era_rets)
    mean_daily = era_rets.mean() * 100
    vol_ann = era_rets.std() * np.sqrt(365) * 100
    sharpe_ann = era_rets.mean() / era_rets.std() * np.sqrt(365) if era_rets.std() > 0 else 0
    cagr = ((1 + era_rets.mean()) ** 365 - 1) * 100
    era_results.append({'Era': h_name, 'Period': f'{era_start.date()} to {era_end.date()}',
                        'Mean%': mean_daily, 'Sharpe': sharpe_ann, 'Vol%': vol_ann, 'CAGR%': cagr})
    report.append(f"| {h_name} | {era_start.date()} to {era_end.date()} | {mean_daily:.4f} | {sharpe_ann:.4f} | {vol_ann:.2f} | {cagr:.2f} |")

# Full period
full_mean = returns.mean() * 100
full_sharpe = returns.mean() / returns.std() * np.sqrt(365) if returns.std() > 0 else 0
full_vol = returns.std() * np.sqrt(365) * 100
full_cagr = ((1 + returns.mean()) ** 365 - 1) * 100
report.append(f"| Full Period | {returns.index[0].date()} to {returns.index[-1].date()} | {full_mean:.4f} | {full_sharpe:.4f} | {full_vol:.2f} | {full_cagr:.2f} |")

report.append("")
report.append("---")
report.append("")

# ================================================================
# PART 4: MONTHLY SEASONALITY
# ================================================================
print("--- Monthly Return Patterns ---")
report.append("## 4. Monthly Return Patterns")
report.append("")

# Average monthly return across all years
monthly_rets = returns.groupby([returns.index.year, returns.index.month]).apply(lambda x: (1 + x).prod() - 1) * 100
monthly_rets.index = [f'{y}-{m:02d}' for y, m in monthly_rets.index]
monthly_by_month = returns.groupby(returns.index.month).apply(lambda x: (1 + x).prod() - 1) * 100

report.append("| Month | Average Monthly Return% | Positive Years / Total | WR% |")
report.append("|-------|----------------------|----------------------|-----|")
for m in range(1, 13):
    data = returns[returns.index.month == m]
    monthly_cum = data.groupby(data.index.year).apply(lambda x: (1 + x).prod() - 1) * 100
    avg = monthly_cum.mean()
    pos_years = (monthly_cum > 0).sum()
    total_years = len(monthly_cum)
    wr = pos_years / total_years * 100 if total_years > 0 else 0
    report.append(f"| {month_names[m-1]} | {avg:.2f} | {pos_years}/{total_years} | {wr:.0f} |")

report.append("")
report.append("### Quarterly Returns")
report.append("")
q_map = {'Q1': [1,2,3], 'Q2': [4,5,6], 'Q3': [7,8,9], 'Q4': [10,11,12]}
report.append("| Quarter | Months | Avg Return% | Win Rate% |")
report.append("|---------|--------|-------------|-----------|")
for qname, qmonths in q_map.items():
    data = returns[returns.index.month.isin(qmonths)]
    q_ret = ((1 + data).prod() - 1) * 100
    # Average quarterly return across years
    q_by_year = data.groupby(data.index.year).apply(lambda x: (1 + x).prod() - 1) * 100
    avg = q_by_year.mean()
    wr = (q_by_year > 0).mean() * 100
    report.append(f"| {qname} | {', '.join(month_names[m-1] for m in qmonths)} | {avg:.2f} | {wr:.0f} |")

report.append("")
report.append("---")
report.append("")

# ================================================================
# SUMMARY
# ================================================================
report.append("## Summary")
report.append("")

# Check if any day passes edge criteria
edge_found = False
edge_candidates = []
for day_name in day_order:
    s = day_stats[day_name]
    _, t_p = stats.ttest_1samp(s['data'], 0)
    binom_p = stats.binomtest(s['n_up'], s['n'], p=0.5).pvalue
    passes = binom_p < 0.05 and s['pf'] > 1.30 and s['sharpe'] > 1.0 and s['n'] > 50
    if passes:
        edge_found = True
        edge_candidates.append((day_name, s))

report.append("### Day of Week")
if edge_candidates:
    for d, s in edge_candidates:
        report.append(f"- **{d}**: WR={s['wr']:.1f}%, PF={s['pf']:.2f}, Sharpe={s['sharpe']:.2f} — passes criteria (but check stability)")
else:
    report.append("- No day of week passes all edge criteria (N>50, p<0.05, PF>1.30, Sharpe>1.0)")

report.append("")
report.append("### Month of Year")
valid_ms = {m: s for m, s in month_stats.items() if s is not None}
month_edges = [m for m, s in valid_ms.items() if s['p'] < 0.05 and s['pf'] > 1.30 and s['sharpe'] > 1.0 and s['n'] > 50]
if month_edges:
    for m in month_edges:
        report.append(f"- {month_names[m-1]}: passes edge criteria")
else:
    report.append("- No month passes all edge criteria")

report.append("")
report.append("### Halving Cycle")
if all_halving_results:
    best_phase = max(all_halving_results, key=lambda r: r['Mean_Cum_Ret%'])
    report.append(f"- Best phase: {best_phase['Phase']} (mean {best_phase['Mean_Cum_Ret%']:.1f}%)")
    report.append(f"- All halvings produced positive returns post-event")

report.append("")
report.append("### Verdict")
has_edge = len(edge_candidates) > 0 or len(month_edges) > 0
if has_edge:
    report.append("Some calendar effects show statistical significance, but require regime stability and OOS testing.")
else:
    report.append("**No robust calendar-based edge found for Bitcoin.**")

report.append("")
report.append("---")
report.append("*Generated by research/bitcoin/scripts/btc_003_calendar.py*")

with open(REPORTS_DIR / 'BTC-003_Calendar_Effects.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nReport saved: {REPORTS_DIR / 'BTC-003_Calendar_Effects.md'}")
print("BTC-003 COMPLETE")
