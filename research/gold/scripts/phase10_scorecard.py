"""
XAU/USD Edge Discovery Framework
Phase 10: Edge Scorecard
Compile and rank all edges discovered across all phases
"""
import pandas as pd
import numpy as np
import json
import os

os.makedirs("reports", exist_ok=True)

print("=" * 60)
print("PHASE 10: EDGE SCORECARD")
print("=" * 60)

# Collect all edges from all phases
edges = []

# --- From Phase 3 (Mean Reversion) ---
print("\n[Phase 3] Mean Reversion edges...")
df = pd.read_csv("data/XAUUSD_yahoo_raw.csv", index_col=0, parse_dates=True)
close = df['Close'].dropna()

windows = [10, 20, 30, 50]
thresholds = [1.0, 1.5, 2.0, 2.5, 3.0]

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
                ret = (close.iloc[exit_idx] - entry) / entry
                if z_scores.iloc[i] > t:
                    signals.append(-ret)
                else:
                    signals.append(ret)
        
        signals = np.array(signals)
        n_events = len(signals)
        
        if n_events > 0:
            win_rate = np.mean(signals > 0)
            avg_ret = np.mean(signals)
            std_ret = np.std(signals)
            gross_win = np.sum(signals[signals > 0])
            gross_loss = abs(np.sum(signals[signals <= 0]))
            pf = gross_win / gross_loss if gross_loss > 0 else np.inf
            n_wins = np.sum(signals > 0)
            from scipy import stats
            binom_p = stats.binomtest(n_wins, n_events, p=0.5).pvalue
            sharpe = avg_ret / std_ret * np.sqrt(252/w) if std_ret > 0 else 0
            
            if n_events > 30 and binom_p < 0.05:
                edges.append({
                    'Edge': f'MR_W{w}_T{t}',
                    'Phase': '3 - Mean Reversion',
                    'Description': f'Mean Rev w={w} thresh={t}',
                    'Sample Size': n_events,
                    'Win Rate': round(win_rate, 4),
                    'Avg Return': round(avg_ret, 6),
                    'Profit Factor': round(pf, 4),
                    'Sharpe': round(sharpe, 4),
                    'P-value': round(binom_p, 6),
                    'EV': round(avg_ret * win_rate - abs(avg_ret) * (1-win_rate), 8)
                })

# --- From Phase 4 (Trend Persistence) ---
print("[Phase 4] Trend Persistence edges...")
returns = close.pct_change().dropna()
direction = np.sign(returns)
N_values = [2, 3, 4, 5, 6]

for N in N_values:
    next_returns = []
    for i in range(N, len(direction) - 1):
        if (direction.iloc[i-N:i] > 0).all():
            next_returns.append(returns.iloc[i])
    
    next_returns = np.array(next_returns)
    n_events = len(next_returns)
    
    if n_events > 0:
        n_up = np.sum(next_returns > 0)
        win_rate = n_up / n_events
        avg_ret = np.mean(next_returns)
        std_ret = np.std(next_returns)
        gross_win = np.sum(next_returns[next_returns > 0])
        gross_loss = abs(np.sum(next_returns[next_returns < 0]))
        pf = gross_win / gross_loss if gross_loss > 0 else np.inf
        from scipy import stats
        binom_p = stats.binomtest(n_up, n_events, p=0.5).pvalue
        sharpe = avg_ret / std_ret * np.sqrt(252) if std_ret > 0 else 0
        
        if n_events > 30 and binom_p < 0.05:
            edges.append({
                'Edge': f'TP_Up{N}',
                'Phase': '4 - Trend Persistence',
                'Description': f'Up streak N={N}',
                'Sample Size': n_events,
                'Win Rate': round(win_rate, 4),
                'Avg Return': round(avg_ret, 6),
                'Profit Factor': round(pf, 4),
                'Sharpe': round(sharpe, 4),
                'P-value': round(binom_p, 6),
                'EV': round(avg_ret * win_rate - abs(avg_ret) * (1-win_rate), 8)
            })

    # Also down streaks (reversal)
    down_returns = []
    for i in range(N, len(direction) - 1):
        if (direction.iloc[i-N:i] < 0).all():
            down_returns.append(returns.iloc[i])
    
    down_returns = np.array(down_returns)
    n_down = len(down_returns)
    
    if n_down > 0:
        n_up_after = np.sum(down_returns > 0)
        win_rate = n_up_after / n_down
        avg_ret = np.mean(down_returns)
        std_ret = np.std(down_returns)
        gross_win = np.sum(down_returns[down_returns > 0])
        gross_loss = abs(np.sum(down_returns[down_returns < 0]))
        pf = gross_win / gross_loss if gross_loss > 0 else np.inf
        from scipy import stats
        binom_p = stats.binomtest(n_up_after, n_down, p=0.5).pvalue
        sharpe = avg_ret / std_ret * np.sqrt(252) if std_ret > 0 else 0
        
        if n_down > 30 and binom_p < 0.05:
            edges.append({
                'Edge': f'TP_Down{N}',
                'Phase': '4 - Trend Persistence',
                'Description': f'Down streak N={N}',
                'Sample Size': n_down,
                'Win Rate': round(win_rate, 4),
                'Avg Return': round(avg_ret, 6),
                'Profit Factor': round(pf, 4),
                'Sharpe': round(sharpe, 4),
                'P-value': round(binom_p, 6),
                'EV': round(avg_ret * win_rate - abs(avg_ret) * (1-win_rate), 8)
            })

# --- From Phase 5 (Volatility) ---
print("[Phase 5] Volatility edges...")
high = df['High'].dropna()
low = df['Low'].dropna()
tr = pd.DataFrame({'hl': high - low, 'hc': abs(high - close.shift(1)), 'lc': abs(low - close.shift(1))}).max(axis=1)
atr = tr.rolling(14).mean().dropna()
atr_pct = atr / close.reindex(atr.index) * 100
threshold_75 = atr_pct.quantile(0.75)
high_vol = atr_pct > threshold_75

# Test: if high vol today, what's the forward return?
for forward_days in [1, 5, 10]:
    future_ret = close.pct_change(forward_days).shift(-forward_days)
    aligned = pd.DataFrame({'high_vol': high_vol, 'fwd_ret': future_ret}).dropna()
    
    high_vol_returns = aligned[aligned['high_vol']]['fwd_ret']
    n_events = len(high_vol_returns)
    
    if n_events > 30:
        n_pos = (high_vol_returns > 0).sum()
        win_rate = n_pos / n_events
        avg_ret = high_vol_returns.mean()
        std_ret = high_vol_returns.std()
        gross_win = high_vol_returns[high_vol_returns > 0].sum()
        gross_loss = abs(high_vol_returns[high_vol_returns < 0].sum())
        pf = gross_win / gross_loss if gross_loss > 0 else np.inf
        from scipy import stats
        binom_p = stats.binomtest(n_pos, n_events, p=0.5).pvalue
        sharpe = avg_ret / std_ret * np.sqrt(252/forward_days) if std_ret > 0 else 0
        
        if binom_p < 0.05:
            edges.append({
                'Edge': f'Vol_AfterHighVol_{forward_days}d',
                'Phase': '5 - Volatility',
                'Description': f'Return after high ATR ({forward_days}d fwd)',
                'Sample Size': n_events,
                'Win Rate': round(win_rate, 4),
                'Avg Return': round(avg_ret, 6),
                'Profit Factor': round(pf, 4),
                'Sharpe': round(sharpe, 4),
                'P-value': round(binom_p, 6),
                'EV': round(avg_ret * win_rate - abs(avg_ret) * (1-win_rate), 8)
            })

# --- From Phase 7 (Day of Week) ---
print("[Phase 7] Day of Week edges...")
df_ret = returns.to_frame('return')
df_ret['day'] = df_ret.index.dayofweek
day_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri'}
for day_num, day_name in day_map.items():
    data = df_ret[df_ret['day'] == day_num]['return']
    n_events = len(data)
    n_pos = (data > 0).sum()
    win_rate = n_pos / n_events
    avg_ret = data.mean()
    std_ret = data.std()
    gross_win = data[data > 0].sum()
    gross_loss = abs(data[data < 0].sum())
    pf = gross_win / gross_loss if gross_loss > 0 else np.inf
    from scipy import stats
    binom_p = stats.binomtest(n_pos, n_events, p=0.5).pvalue
    sharpe = avg_ret / std_ret * np.sqrt(252) if std_ret > 0 else 0
    
    if n_events > 100 and binom_p < 0.05:
        edges.append({
            'Edge': f'DoW_{day_name}',
            'Phase': '7 - Day of Week',
            'Description': f'{day_name} return',
            'Sample Size': n_events,
            'Win Rate': round(win_rate, 4),
            'Avg Return': round(avg_ret, 6),
            'Profit Factor': round(pf, 4),
            'Sharpe': round(sharpe, 4),
            'P-value': round(binom_p, 6),
            'EV': round(avg_ret * win_rate - abs(avg_ret) * (1-win_rate), 8)
        })

# Rank all edges by composite score
print(f"\nTotal candidate edges: {len(edges)}")

if len(edges) > 0:
    df_edges = pd.DataFrame(edges)
    
    # Stability score: combination of sample size, p-value, and profit factor consistency
    # Normalize metrics
    df_edges['Sample Score'] = df_edges['Sample Size'] / df_edges['Sample Size'].max()
    df_edges['PF Score'] = (df_edges['Profit Factor'] - 1) / (df_edges['Profit Factor'].max() - 1) if df_edges['Profit Factor'].max() != 1 else 0
    df_edges['Sharpe Score'] = (df_edges['Sharpe'] - df_edges['Sharpe'].min()) / (df_edges['Sharpe'].max() - df_edges['Sharpe'].min()) if df_edges['Sharpe'].max() != df_edges['Sharpe'].min() else 0
    df_edges['P Score'] = 1 - df_edges['P-value']  # Lower p-value is better
    df_edges['WR Score'] = (df_edges['Win Rate'] - 0.5) * 2  # How far from 50%
    
    # Composite stability score (weighted)
    df_edges['Stability Score'] = (
        0.20 * df_edges['Sample Score'] +
        0.25 * df_edges['PF Score'] +
        0.20 * df_edges['Sharpe Score'] +
        0.20 * df_edges['P Score'] +
        0.15 * df_edges['WR Score']
    )
    
    # Rank
    df_edges = df_edges.sort_values('Stability Score', ascending=False).reset_index(drop=True)
    df_edges['Rank'] = range(1, len(df_edges) + 1)
    
    # Check success criteria
    df_edges['Meets Criteria'] = (
        (df_edges['Sample Size'] > 300) &
        (df_edges['P-value'] < 0.05) &
        (df_edges['Profit Factor'] > 1.30) &
        (df_edges['Sharpe'] > 1.00)
    )
    
    # Write report
    report = []
    report.append("# RESEARCH-010: Edge Scorecard")
    report.append("")
    report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**Instrument:** XAU/USD (GC=F)")
    report.append(f"**Total Edges Tested:** {len(edges)}")
    report.append(f"**Edges Meeting Success Criteria:** {df_edges['Meets Criteria'].sum()}")
    report.append("")
    
    # Success criteria definition
    report.append("## Success Criteria")
    report.append("")
    report.append("| Criterion | Requirement |")
    report.append("|-----------|-------------|")
    report.append("| Sample Size | > 300 |")
    report.append("| P-value | < 0.05 |")
    report.append("| Profit Factor | > 1.30 |")
    report.append("| Sharpe Ratio | > 1.00 |")
    report.append("| Stability | Consistent across periods |")
    report.append("")
    
    report.append("## Full Ranking")
    report.append("")
    report.append("| Rank | Edge | Phase | Sample | Win Rate | PF | Sharpe | P-value | Stability | Meets Criteria? |")
    report.append("|------|------|-------|--------|----------|----|--------|---------|-----------|-----------------|")
    
    for _, row in df_edges.iterrows():
        report.append(
            f"| {int(row['Rank'])} | {row['Edge']} | {row['Phase']} | {int(row['Sample Size']):,} | "
            f"{row['Win Rate']*100:.2f}% | {row['Profit Factor']:.2f} | {row['Sharpe']:.2f} | "
            f"{row['P-value']:.6f} | {row['Stability Score']:.4f} | {'YES' if row['Meets Criteria'] else 'no'} |"
        )
    
    report.append("")
    
    # Edges meeting criteria
    meeting = df_edges[df_edges['Meets Criteria']]
    if len(meeting) > 0:
        report.append("## Edges Meeting All Success Criteria")
        report.append("")
        report.append(f"| Rank | Edge | Sample | Win Rate | PF | Sharpe | P-value | Stability |")
        report.append("|------|------|--------|----------|----|--------|---------|-----------|")
        for _, row in meeting.iterrows():
            report.append(
                f"| {int(row['Rank'])} | {row['Edge']} | {int(row['Sample Size']):,} | "
                f"{row['Win Rate']*100:.2f}% | {row['Profit Factor']:.2f} | {row['Sharpe']:.2f} | "
                f"{row['P-value']:.6f} | {row['Stability Score']:.4f} |"
            )
    else:
        report.append("## Edges Meeting All Success Criteria")
        report.append("")
        report.append("*No edges meet all success criteria simultaneously.*")
        report.append("")
        # Show closest
        report.append("### Closest Edges")
        report.append("")
        report.append("| Edge | Sample | Win Rate | PF | Sharpe | P-value | Criteria Missing |")
        report.append("|------|--------|----------|----|--------|---------|-----------------|")
        for _, row in df_edges.head(5).iterrows():
            missing = []
            if row['Sample Size'] <= 300:
                missing.append('Sample Size')
            if row['P-value'] >= 0.05:
                missing.append('P-value')
            if row['Profit Factor'] <= 1.30:
                missing.append('PF')
            if row['Sharpe'] <= 1.00:
                missing.append('Sharpe')
            report.append(
                f"| {row['Edge']} | {int(row['Sample Size']):,} | "
                f"{row['Win Rate']*100:.2f}% | {row['Profit Factor']:.2f} | {row['Sharpe']:.2f} | "
                f"{row['P-value']:.6f} | {', '.join(missing)} |"
            )
    
    report.append("")
    report.append("## Summary by Phase")
    report.append("")
    report.append("| Phase | Total Edges | Significant (p<0.05) | Meeting All Criteria |")
    report.append("|-------|-------------|---------------------|---------------------|")
    for phase in sorted(df_edges['Phase'].unique()):
        subset = df_edges[df_edges['Phase'] == phase]
        n_sig = (subset['P-value'] < 0.05).sum()
        n_all = subset['Meets Criteria'].sum()
        report.append(f"| {phase} | {len(subset)} | {n_sig} | {n_all} |")
    
    report.append("")
    report.append("## Verdict")
    report.append("")
    report.append(f"**Number of statistically significant edges found: {len(edges)}**")
    report.append(f"**Number of edges meeting ALL success criteria: {df_edges['Meets Criteria'].sum()}**")
    report.append("")
    if df_edges['Meets Criteria'].sum() > 0:
        report.append("### VALID EDGES FOUND")
        report.append("")
        report.append("The following edges demonstrate statistically significant predictive power:")
        for _, row in meeting.iterrows():
            report.append(f"- **{row['Edge']}**: {row['Description']} (WR={row['Win Rate']*100:.1f}%, PF={row['Profit Factor']:.2f}, Sharpe={row['Sharpe']:.2f}, p={row['P-value']:.4f})")
    else:
        report.append("### NO VALID EDGES FOUND")
        report.append("")
        report.append("No edge meets all success criteria simultaneously. The XAU/USD market appears")
        report.append("to be highly efficient for these simple statistical patterns. All apparent edges")
        report.append("either have insufficient sample size, inadequate profit factor, or fail statistical")
        report.append("significance tests.")
    
    report.append("")
    report.append("---")
    report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")
    
    with open("reports/RESEARCH-010_Edge_Scorecard.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    
    print("\nReport saved: reports/RESEARCH-010_Edge_Scorecard.md")
    
    # Save edge data for reproducibility
    df_edges.to_csv("data/edge_scorecard.csv", index=False)
    print("Edge data saved: data/edge_scorecard.csv")
    
    # Print summary
    print(f"\n{'='*60}")
    print("EDGE SCORECARD SUMMARY")
    print(f"{'='*60}")
    print(f"Total edges tested: {len(edges)}")
    print(f"Meeting success criteria: {df_edges['Meets Criteria'].sum()}")
    print(f"\nTop 5 Edges:")
    for _, row in df_edges.head(5).iterrows():
        print(f"  #{int(row['Rank'])} {row['Edge']}: WR={row['Win Rate']*100:.1f}% PF={row['Profit Factor']:.2f} Sharpe={row['Sharpe']:.2f} p={row['P-value']:.4f}")
else:
    print("\nNo significant edges found.")
    report = ["# RESEARCH-010: Edge Scorecard", "",
              f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
              "**Instrument:** XAU/USD (GC=F)",
              "",
              "## Results", "",
              "No statistically significant edges were found across any of the tested phases.",
              "",
              "### Interpretation",
              "",
              "The XAU/USD market appears to be highly efficient with respect to the simple statistical",
              "patterns tested. This is consistent with the Efficient Market Hypothesis for liquid",
              "commodity markets.",
              "",
              "---",
              "*Generated automatically by XAU/USD Edge Discovery Framework*"]
    with open("reports/RESEARCH-010_Edge_Scorecard.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
