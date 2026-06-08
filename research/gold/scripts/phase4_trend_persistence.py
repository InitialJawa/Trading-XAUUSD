"""
RESEARCH-004: Trend Persistence Analysis
XAU/USD Edge Discovery Framework
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

print("Loading cleaned dataset...")
df = pd.read_csv("data/XAUUSD_cleaned.csv", index_col=0, parse_dates=True)
close = df['Close'].dropna()
print(f"Loaded {len(close)} observations, {close.index[0].date()} to {close.index[-1].date()}")

returns = close.pct_change().dropna()
direction = np.sign(returns)  # 1 up, -1 down, 0 flat
# Remove zeros (flat days) - extremely rare but handle
direction = direction[direction != 0]

unconditional_up = (direction > 0).mean()
unconditional_down = (direction < 0).mean()
print(f"Unconditional P(up) = {unconditional_up*100:.2f}%, P(down) = {unconditional_down*100:.2f}%")

# -------------------------------------------------------
# Regime definitions
# -------------------------------------------------------
regimes = {
    '2000-2008': ('2000-01-01', '2008-12-31'),
    '2009-2015': ('2009-01-01', '2015-12-31'),
    '2016-2020': ('2016-01-01', '2020-12-31'),
    '2021-present': ('2021-01-01', '2030-12-31')
}

# -------------------------------------------------------
# Helper: compute streak conditional probabilities
# -------------------------------------------------------
def streak_analysis(direction_series, N_max=6):
    """Analyze conditional probabilities after N consecutive same-direction days"""
    results = []
    dir_arr = direction_series.values
    idx_arr = direction_series.index
    
    for n in range(1, N_max + 1):
        next_dirs = []
        streak_dates = []
        
        for i in range(n, len(dir_arr)):
            streak = dir_arr[i-n:i]
            if (streak > 0).all():
                next_dirs.append(dir_arr[i] if i < len(dir_arr) else 0)
                streak_dates.append(idx_arr[i])
        
        next_dirs = np.array(next_dirs)
        n_events = len(next_dirs)
        
        if n_events > 0:
            n_up = np.sum(next_dirs > 0)
            p_up = n_up / n_events
            n_down = np.sum(next_dirs < 0)
            p_down = n_down / n_events
            
            # Binomial test: H0: p(up) = unconditional probability
            binom_up = stats.binomtest(n_up, n_events, p=unconditional_up)
            binom_down = stats.binomtest(n_down, n_events, p=unconditional_down)
            
            # "Fair coin" test: H0: p(up) = 0.5
            binom_50 = stats.binomtest(n_up, n_events, p=0.5)
            
            # Confidence interval (Clopper-Pearson exact)
            ci_low, ci_high = binom_up.proportion_ci(confidence_level=0.95)
            
            results.append({
                'N': n,
                'Direction': 'up_streak',
                'Events': n_events,
                'P(Up)': p_up,
                'P(Down)': p_down,
                'P(Up)%': p_up * 100,
                'P(Down)%': p_down * 100,
                'N_Up': n_up,
                'N_Down': n_down,
                'Deviation%': (p_up - unconditional_up) * 100,
                'Binom_P_vs_Uncond': binom_up.pvalue,
                'Binom_P_vs_50': binom_50.pvalue,
                'CI_Low': ci_low,
                'CI_High': ci_high,
                'Sig_vs_Uncond (0.05)': 'YES' if binom_up.pvalue < 0.05 else 'NO'
            })
        else:
            results.append({
                'N': n, 'Direction': 'up_streak', 'Events': 0,
                'P(Up)': 0, 'P(Down)': 0, 'P(Up)%': 0, 'P(Down)%': 0,
                'Deviation%': 0, 'Binom_P_vs_Uncond': 1.0, 'Binom_P_vs_50': 1.0,
                'CI_Low': 0, 'CI_High': 0, 'Sig_vs_Uncond (0.05)': 'NO'
            })
    
    # Down streaks
    for n in range(1, N_max + 1):
        next_dirs = []
        for i in range(n, len(dir_arr)):
            streak = dir_arr[i-n:i]
            if (streak < 0).all():
                next_dirs.append(dir_arr[i] if i < len(dir_arr) else 0)
        
        next_dirs = np.array(next_dirs)
        n_events = len(next_dirs)
        
        if n_events > 0:
            n_down = np.sum(next_dirs < 0)
            p_down = n_down / n_events
            n_up = np.sum(next_dirs > 0)
            p_up = n_up / n_events
            
            binom_down = stats.binomtest(n_down, n_events, p=unconditional_down)
            binom_up = stats.binomtest(n_up, n_events, p=unconditional_up)
            binom_50 = stats.binomtest(n_down, n_events, p=0.5)
            
            ci_low, ci_high = binom_down.proportion_ci(confidence_level=0.95)
            
            # For down streaks, measure P(down continues) vs P(reversal up)
            results.append({
                'N': n,
                'Direction': 'down_streak',
                'Events': n_events,
                'P(Down)': p_down,
                'P(Up)': p_up,
                'P(Down)%': p_down * 100,
                'P(Up)%': p_up * 100,
                'N_Down': n_down,
                'N_Up': n_up,
                'Deviation%': (p_down - unconditional_down) * 100,
                'Binom_P_vs_Uncond': binom_down.pvalue,
                'Binom_P_vs_50': binom_50.pvalue,
                'CI_Low': ci_low,
                'CI_High': ci_high,
                'Sig_vs_Uncond (0.05)': 'YES' if binom_down.pvalue < 0.05 else 'NO'
            })
        else:
            results.append({
                'N': n, 'Direction': 'down_streak', 'Events': 0,
                'P(Down)': 0, 'P(Up)': 0, 'P(Down)%': 0, 'P(Up)%': 0,
                'Deviation%': 0, 'Binom_P_vs_Uncond': 1.0, 'Binom_P_vs_50': 1.0,
                'CI_Low': 0, 'CI_High': 0, 'Sig_vs_Uncond (0.05)': 'NO'
            })
    
    return results

# -------------------------------------------------------
# Helper: magnitude analysis
# -------------------------------------------------------
def magnitude_analysis(returns_series, direction_series, N_max=4):
    """Analyze whether streak magnitude affects continuation probability"""
    results = []
    
    # Align both series on common index
    common_idx = returns_series.index.intersection(direction_series.index)
    ret = returns_series.loc[common_idx]
    direc = direction_series.loc[common_idx]
    
    ret_abs = ret.abs()
    small_thresh = float(ret_abs.quantile(0.33))
    large_thresh = float(ret_abs.quantile(0.67))
    
    magnitude_labels = {
        'small': (0, small_thresh),
        'medium': (small_thresh, large_thresh),
        'large': (large_thresh, float('inf'))
    }
    
    for n in range(1, N_max + 1):
        for mag_name, (lo, hi) in magnitude_labels.items():
            up_next = []
            down_next = []
            
            for i in range(n, len(ret) - 1):
                streak_rets = ret.iloc[i-n:i]
                streak_dir = direc.iloc[i-n:i]
                
                if (streak_dir > 0).all():
                    if all(float(lo) <= abs(float(r)) <= float(hi) for r in streak_rets):
                        up_next.append(direc.iloc[i])
                
                if (streak_dir < 0).all():
                    if all(float(lo) <= abs(float(r)) <= float(hi) for r in streak_rets):
                        down_next.append(direc.iloc[i])
            
            up_next_arr = np.array(up_next)
            down_next_arr = np.array(down_next)
            
            if len(up_next_arr) > 0:
                n_up = int(np.sum(up_next_arr > 0))
                p_up = n_up / len(up_next_arr)
                bp = stats.binomtest(n_up, len(up_next_arr), p=0.5).pvalue if len(up_next_arr) > 0 else 1.0
                results.append({
                    'N': n, 'Magnitude': mag_name, 'Type': 'up_streak',
                    'Events': len(up_next_arr), 'P_Continue': p_up,
                    'Binom_P': bp
                })
            if len(down_next_arr) > 0:
                n_down = int(np.sum(down_next_arr < 0))
                p_down = n_down / len(down_next_arr)
                bp = stats.binomtest(n_down, len(down_next_arr), p=0.5).pvalue if len(down_next_arr) > 0 else 1.0
                results.append({
                    'N': n, 'Magnitude': mag_name, 'Type': 'down_streak',
                    'Events': len(down_next_arr), 'P_Continue': p_down,
                    'Binom_P': bp
                })
    
    return results, small_thresh, large_thresh

# -------------------------------------------------------
# MAIN ANALYSIS
# -------------------------------------------------------
report = []
report.append("# RESEARCH-004: Trend Persistence Analysis")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Dataset:** XAU/USD Cleaned (GC=F)")
report.append(f"**Period:** {close.index[0].strftime('%Y-%m-%d')} to {close.index[-1].strftime('%Y-%m-%d')}")
report.append(f"**Observations:** {len(close):,}")
report.append(f"**Unconditional P(Up):** {unconditional_up*100:.2f}%")
report.append(f"**Unconditional P(Down):** {unconditional_down*100:.2f}%")
report.append("")

# ============ FULL PERIOD ANALYSIS ============
print("Full period analysis...")
full_results = streak_analysis(direction)

report.append("## 1. Consecutive Up Days — Full Period")
report.append("")
report.append(f"| N | Events | P(Up Next) | P(Down Next) | Uncond P(Up) | Deviation | Binom P | CI (95%) | Significant? |")
report.append("|---|--------|------------|--------------|--------------|-----------|---------|----------|-------------|")
for r in full_results:
    if r['Direction'] == 'up_streak' and r['Events'] > 0:
        report.append(
            f"| {r['N']} | {r['Events']:,} | {r['P(Up)%']:.2f}% | {r['P(Down)%']:.2f}% | "
            f"{unconditional_up*100:.2f}% | {r['Deviation%']:+.2f}% | "
            f"{r['Binom_P_vs_Uncond']:.4f} | [{r['CI_Low']*100:.1f}%, {r['CI_High']*100:.1f}%] | "
            f"{r['Sig_vs_Uncond (0.05)']} |"
        )

report.append("")
report.append("## 2. Consecutive Down Days — Full Period")
report.append("")
report.append(f"| N | Events | P(Down Next) | P(Up Next) | Uncond P(Down) | Deviation | Binom P | CI (95%) | Significant? |")
report.append("|---|--------|--------------|------------|----------------|-----------|---------|----------|-------------|")
for r in full_results:
    if r['Direction'] == 'down_streak' and r['Events'] > 0:
        report.append(
            f"| {r['N']} | {r['Events']:,} | {r['P(Down)%']:.2f}% | {r['P(Up)%']:.2f}% | "
            f"{unconditional_down*100:.2f}% | {r['Deviation%']:+.2f}% | "
            f"{r['Binom_P_vs_Uncond']:.4f} | [{r['CI_Low']*100:.1f}%, {r['CI_High']*100:.1f}%] | "
            f"{r['Sig_vs_Uncond (0.05)']} |"
        )

# ============ MAGNITUDE ANALYSIS ============
print("Magnitude analysis...")
mag_results, small_th, large_th = magnitude_analysis(returns, direction)

report.append("")
report.append("## 3. Magnitude Analysis")
report.append("")
report.append(f"Magnitude thresholds: Small (< {small_th*100:.3f}%), Medium ({small_th*100:.3f}%-{large_th*100:.3f}%), Large (>{large_th*100:.3f}%)")
report.append("")
report.append("| N | Magnitude | Streak Type | Events | P(Continue) | Binom P | Significant? |")
report.append("|---|-----------|-------------|--------|-------------|---------|-------------|")
for r in sorted(mag_results, key=lambda x: (x['N'], x['Magnitude'])):
    sig = 'YES' if r['Binom_P'] < 0.05 else 'NO'
    report.append(f"| {r['N']} | {r['Magnitude']} | {r['Type']} | {r['Events']} | {r['P_Continue']*100:.2f}% | {r['Binom_P']:.4f} | {sig} |")

# ============ REGIME STABILITY ============
print("Regime stability analysis...")
report.append("")
report.append("## 4. Regime Stability Analysis")
report.append("")
report.append("### 4a. Up Streaks by Regime")
report.append("")
report.append("| Regime | N | Events | P(Up Next) | Deviation | Binom P | Significant? |")
report.append("|--------|---|--------|------------|-----------|---------|-------------|")

regime_up_results = []
for regime_name, (start, end) in regimes.items():
    mask = (direction.index >= start) & (direction.index <= end)
    regime_dir = direction[mask]
    regime_uncond_up = (regime_dir > 0).mean()
    
    regime_results = streak_analysis(regime_dir)
    for r in regime_results:
        if r['Direction'] == 'up_streak' and r['Events'] > 0:
            # Recompute deviation vs regime's own unconditional
            dev = r['P(Up)'] - regime_uncond_up
            regime_up_results.append({**r, 'Regime': regime_name, 'Uncond': regime_uncond_up})
            report.append(
                f"| {regime_name} | {r['N']} | {r['Events']} | {r['P(Up)%']:.2f}% | "
                f"{dev*100:+.2f}% | {r['Binom_P_vs_Uncond']:.4f} | {r['Sig_vs_Uncond (0.05)']} |"
            )

report.append("")
report.append("### 4b. Down Streaks by Regime")
report.append("")
report.append("| Regime | N | Events | P(Down Next) | Deviation | Binom P | Significant? |")
report.append("|--------|---|--------|--------------|-----------|---------|-------------|")

for regime_name, (start, end) in regimes.items():
    mask = (direction.index >= start) & (direction.index <= end)
    regime_dir = direction[mask]
    regime_uncond_down = (regime_dir < 0).mean()
    
    regime_results = streak_analysis(regime_dir)
    for r in regime_results:
        if r['Direction'] == 'down_streak' and r['Events'] > 0:
            dev = r['P(Down)'] - regime_uncond_down
            report.append(
                f"| {regime_name} | {r['N']} | {r['Events']} | {r['P(Down)%']:.2f}% | "
                f"{dev*100:+.2f}% | {r['Binom_P_vs_Uncond']:.4f} | {r['Sig_vs_Uncond (0.05)']} |"
            )

# ============ SUCCESS CRITERIA ============
report.append("")
report.append("## 5. Edge Candidate Evaluation")
report.append("")
report.append("### Success Criteria:")
report.append("- Sample Size > 300")
report.append("- P-value < 0.05")
report.append("- Probability deviation > 5% (absolute)")
report.append("- Stable across regimes")
report.append("")

# Evaluate up streak edges
candidates = []
for r in full_results:
    if r['Direction'] == 'up_streak' and r['Events'] > 0:
        meets_n = r['Events'] > 300
        meets_p = r['Binom_P_vs_Uncond'] < 0.05
        meets_dev = abs(r['Deviation%']) > 5
        
        # Check regime stability: was this N significant in every regime?
        stable = True
        for reg_name, (reg_start, reg_end) in regimes.items():
            mask = (direction.index >= reg_start) & (direction.index <= reg_end)
            reg_dir = direction[mask]
            reg_results = streak_analysis(reg_dir)
            for rr in reg_results:
                if rr['Direction'] == 'up_streak' and rr['N'] == r['N'] and rr['Events'] > 0:
                    if rr['Sig_vs_Uncond (0.05)'] != 'YES':
                        stable = False
        
        candidates.append({
            'Type': f'Up Streak N={r["N"]}',
            'Events': r['Events'],
            'P': f"{r['P(Up)%']:.2f}%",
            'Deviation': f"{r['Deviation%']:+.2f}%",
            'Binom P': f"{r['Binom_P_vs_Uncond']:.4f}",
            'Meets N': meets_n,
            'Meets P': meets_p,
            'Meets Dev': meets_dev,
            'Stable': stable,
            'Pass All': meets_n and meets_p and meets_dev and stable
        })

for r in full_results:
    if r['Direction'] == 'down_streak' and r['Events'] > 0:
        meets_n = r['Events'] > 300
        meets_p = r['Binom_P_vs_Uncond'] < 0.05
        meets_dev = abs(r['Deviation%']) > 5
        
        stable = True
        for reg_name, (reg_start, reg_end) in regimes.items():
            mask = (direction.index >= reg_start) & (direction.index <= reg_end)
            reg_dir = direction[mask]
            reg_results = streak_analysis(reg_dir)
            for rr in reg_results:
                if rr['Direction'] == 'down_streak' and rr['N'] == r['N'] and rr['Events'] > 0:
                    if rr['Sig_vs_Uncond (0.05)'] != 'YES':
                        stable = False
        
        candidates.append({
            'Type': f'Down Streak N={r["N"]}',
            'Events': r['Events'],
            'P': f"{r['P(Down)%']:.2f}%",
            'Deviation': f"{r['Deviation%']:+.2f}%",
            'Binom P': f"{r['Binom_P_vs_Uncond']:.4f}",
            'Meets N': meets_n,
            'Meets P': meets_p,
            'Meets Dev': meets_dev,
            'Stable': stable,
            'Pass All': meets_n and meets_p and meets_dev and stable
        })

report.append("| Edge Type | Sample | P(Continue) | Deviation | Binom P | N>300 | P<0.05 | |Dev|>5% | Stable | PASS ALL? |")
report.append("|-----------|--------|-------------|-----------|---------|-------|--------|---------|--------|-----------|")
for c in candidates:
    report.append(
        f"| {c['Type']} | {c['Events']:,} | {c['P']} | {c['Deviation']} | {c['Binom P']} | "
        f"{'YES' if c['Meets N'] else 'no'} | {'YES' if c['Meets P'] else 'no'} | "
        f"{'YES' if c['Meets Dev'] else 'no'} | {'YES' if c['Stable'] else 'no'} | "
        f"{'YES' if c['Pass All'] else 'NO'} |"
    )

pass_all = [c for c in candidates if c['Pass All']]
report.append("")
if pass_all:
    report.append("### EDGE CANDIDATES FOUND:")
    for c in pass_all:
        report.append(f"- **{c['Type']}**: P={c['P']}, Deviation={c['Deviation']}, p={c['Binom P']}, N={c['Events']:,}")
else:
    report.append("### No Edge Candidates Meet All Criteria")
    report.append("")
    # Show closest
    report.append("Closest candidates:")
    report.append("")
    for c in sorted(candidates, key=lambda x: sum([x['Meets N'], x['Meets P'], x['Meets Dev'], x['Stable']]), reverse=True)[:3]:
        report.append(f"- {c['Type']}: {sum([c['Meets N'], c['Meets P'], c['Meets Dev'], c['Stable']])}/4 criteria met")

# ============ CHARTS ============
print("Generating charts...")
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# Chart 1: Up streak continuation probability
ax = axes[0, 0]
up_data = [r for r in full_results if r['Direction'] == 'up_streak' and r['Events'] > 0]
if up_data:
    ns = [r['N'] for r in up_data]
    probs = [r['P(Up)%'] for r in up_data]
    cis_low = [r['CI_Low']*100 for r in up_data]
    cis_high = [r['CI_High']*100 for r in up_data]
    ax.errorbar(ns, probs, yerr=[[p - l for p, l in zip(probs, cis_low)], [h - p for p, h in zip(probs, cis_high)]],
                fmt='o-', capsize=5, color='green', markersize=8)
    ax.axhline(y=unconditional_up*100, color='red', linestyle='--', label=f'Unconditional ({unconditional_up*100:.1f}%)')
    ax.set_xlabel('N (consecutive up days)')
    ax.set_ylabel('P(Up Next Day) %')
    ax.set_title('Up Streak Continuation')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Chart 2: Down streak continuation
ax = axes[0, 1]
down_data = [r for r in full_results if r['Direction'] == 'down_streak' and r['Events'] > 0]
if down_data:
    ns = [r['N'] for r in down_data]
    probs = [r['P(Down)%'] for r in down_data]
    cis_low = [r['CI_Low']*100 for r in down_data]
    cis_high = [r['CI_High']*100 for r in down_data]
    ax.errorbar(ns, probs, yerr=[[p - l for p, l in zip(probs, cis_low)], [h - p for p, h in zip(probs, cis_high)]],
                fmt='o-', capsize=5, color='red', markersize=8)
    ax.axhline(y=unconditional_down*100, color='blue', linestyle='--', label=f'Unconditional ({unconditional_down*100:.1f}%)')
    ax.set_xlabel('N (consecutive down days)')
    ax.set_ylabel('P(Down Next Day) %')
    ax.set_title('Down Streak Continuation')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Chart 3: Magnitude analysis heatmap
ax = axes[0, 2]
if mag_results:
    mag_pivot = {}
    for r in mag_results:
        key = f"{r['Type']}_N{r['N']}_{r['Magnitude']}"
        mag_pivot[key] = r['P_Continue'] * 100
    if mag_pivot:
        # Simple bar chart
        labels = list(mag_pivot.keys())
        values = list(mag_pivot.values())
        colors = ['green' if 'up' in l else 'red' for l in labels]
        ax.bar(range(len(labels)), values, color=colors, alpha=0.7)
        ax.axhline(y=50, color='black', linestyle='--', alpha=0.5)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=7)
        ax.set_ylabel('Continuation Probability %')
        ax.set_title('Magnitude Analysis')
        ax.grid(True, alpha=0.3, axis='y')

# Chart 4: Regime stability - up streaks N=2
ax = axes[1, 0]
regime_n2_up = [r for r in regime_up_results if r['N'] == 2]
if regime_n2_up:
    reg_names = [r['Regime'] for r in regime_n2_up]
    reg_probs = [r['P(Up)%'] for r in regime_n2_up]
    ax.bar(reg_names, reg_probs, color=['gold', 'silver', 'orange', 'lightblue'], alpha=0.7)
    ax.axhline(y=unconditional_up*100, color='red', linestyle='--', label=f'Full period ({unconditional_up*100:.1f}%)')
    ax.set_title('N=2 Up Streak: Stability Across Regimes')
    ax.set_ylabel('P(Up Next) %')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

# Chart 5: Regime stability - down streaks N=2
ax = axes[1, 1]
regime_n2_down_data = [r for r in full_results if r['Direction'] == 'down_streak' and r['Events'] > 0]
# Get per-regime data for N=2 down
for regime_name, (reg_start, reg_end) in regimes.items():
    mask = (direction.index >= reg_start) & (direction.index <= reg_end)
    reg_dir = direction[mask]
    reg_results = streak_analysis(reg_dir)
    for rr in reg_results:
        if rr['Direction'] == 'down_streak' and rr['N'] == 2:
            regime_n2_down_data = [{'Regime': regime_name, 'P(Down)%': rr['P(Down)%']}]

if isinstance(regime_n2_down_data, list) and len(regime_n2_down_data) > 0 and isinstance(regime_n2_down_data[0], dict) and 'Regime' in regime_n2_down_data[0]:
    reg_names = [r['Regime'] for r in regime_n2_down_data]
    reg_probs = [r['P(Down)%'] for r in regime_n2_down_data]
    ax.bar(reg_names, reg_probs, color=['gold', 'silver', 'orange', 'lightblue'], alpha=0.7)
    ax.axhline(y=unconditional_down*100, color='red', linestyle='--', label=f'Full period ({unconditional_down*100:.1f}%)')
    ax.set_title('N=2 Down Streak: Stability Across Regimes')
    ax.set_ylabel('P(Down Next) %')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

# Chart 6: Sample sizes
ax = axes[1, 2]
all_labels = []
all_sizes = []
all_colors = []
for r in full_results:
    if r['Events'] > 0:
        all_labels.append(f"{r['Direction'][0].upper()}N={r['N']}")
        all_sizes.append(r['Events'])
        all_colors.append('green' if 'up' in r['Direction'] else 'red')
ax.barh(range(len(all_labels)), all_sizes, color=all_colors, alpha=0.7)
ax.axvline(x=300, color='black', linestyle='--', alpha=0.5, label='Min threshold (300)')
ax.set_yticks(range(len(all_labels)))
ax.set_yticklabels(all_labels, fontsize=8)
ax.set_xlabel('Sample Size')
ax.set_title('Sample Sizes by Streak Type')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig("charts/trend_persistence_enhanced.png", dpi=150)
plt.close()
print("Chart saved: charts/trend_persistence_enhanced.png")

report.append("")
report.append("## 6. Charts")
report.append("")
report.append("![Trend Persistence Analysis](../charts/trend_persistence_enhanced.png)")
report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

# Write report
with open("reports/RESEARCH-004_Trend_Persistence.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

# Print summary
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"Unconditional P(Up) = {unconditional_up*100:.2f}%, P(Down) = {unconditional_down*100:.2f}%")
print()
for c in candidates:
    status = 'PASS' if c['Pass All'] else 'FAIL'
    print(f"  {c['Type']}: P={c['P']}, Dev={c['Deviation']}, p={c['Binom P']}, N={c['Events']:,} -> {status}")
print()
print(f"Report: reports/RESEARCH-004_Trend_Persistence.md")
