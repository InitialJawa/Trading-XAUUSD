"""
RESEARCH-005A: Overlap Bias Audit
Audit look-ahead and overlap bias in volatility predictability tests.
XAU/USD Edge Discovery Framework
"""
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

print("Loading cleaned data...")
df = pd.read_csv("data/XAUUSD_cleaned.csv", index_col=0, parse_dates=True)
close = df['Close'].dropna()
high = df['High'].dropna()
low = df['Low'].dropna()

print("Calculating ATR(14)...")
tr = pd.DataFrame({
    'hl': high - low,
    'hc': (high - close.shift(1)).abs(),
    'lc': (low - close.shift(1)).abs()
}).max(axis=1)
atr = tr.rolling(14).mean()
atr_pct = atr / close * 100
atr_pct = atr_pct.dropna()

# Align
close = close.loc[atr_pct.index]
print(f"Observations with ATR: {len(atr_pct)}")

report = []
report.append("# RESEARCH-005A: Overlap Bias Audit")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Dataset:** XAU/USD Cleaned (GC=F)")
report.append(f"**ATR Period:** 14 days")
report.append(f"**Observations:** {len(atr_pct):,}")
report.append("")
report.append("## Background")
report.append("")
report.append("The original RESEARCH-005 Test 4 measured: ATR(today) predicting average ATR(next 5 days).")
report.append("This introduces **overlap bias** because ATR is a rolling 14-day average, so the")
report.append("'today' window and 'next 5 days' window share 9 days of overlap (14 - 5 = 9).")
report.append("This artificially inflates the apparent predictability.")
report.append("")
report.append("This audit uses **fully non-overlapping** forward windows:")
report.append("1. ATR today → ATR 20 trading days later (no overlap, ~1 month)")
report.append("2. ATR today → ATR 30 trading days later (no overlap, ~1.5 months)")
report.append("3. ATR today → volatility regime classification 20 days later")
report.append("")

# -------------------------------------------------------
# Helper: ATR at exact future point (no averaging overlap)
# -------------------------------------------------------
def atr_at_future(atr_series, forward_days):
    """Get ATR value forward_days ahead (no overlap with today's window).
    ATR(14) uses days t-13 through t.
    Future ATR at t+forward_days uses days t+forward_days-13 through t+forward_days.
    These windows overlap iff forward_days < 14.
    So for forward_days >= 14, there is ZERO overlap."""
    future_atr = atr_series.shift(-forward_days)
    return future_atr

# -------------------------------------------------------
# TEST 1: ATR Today → ATR 20 Days Later
# -------------------------------------------------------
print("TEST 1: ATR today -> ATR 20 trading days later...")

FWD_20 = 20
pred_20 = atr_at_future(atr_pct, FWD_20)
test1_df = pd.DataFrame({'atr_today': atr_pct, 'atr_fwd': pred_20}).dropna()

report.append("## TEST 1: ATR Today → ATR 20 Trading Days Later")
report.append("")
report.append(f"Forward gap: {FWD_20} trading days (~1 calendar month)")
report.append(f"ATR window overlap: 0 days (fully non-overlapping since {FWD_20} >= 14)")
report.append(f"Sample size: {len(test1_df):,}")
report.append("")

if len(test1_df) > 0:
    r_20, p_20 = pearsonr(test1_df['atr_today'], test1_df['atr_fwd'])
    slope_20, intercept_20, _, _, _ = stats.linregress(test1_df['atr_today'], test1_df['atr_fwd'])
    
    # MAE of naive prediction (use today's ATR as tomorrow's prediction)
    pred_20_naive = test1_df['atr_today']
    mae_20 = (test1_df['atr_fwd'] - pred_20_naive).abs().mean()
    
    # Also compute using linear model
    pred_20_lm = slope_20 * test1_df['atr_today'] + intercept_20
    mae_20_lm = (test1_df['atr_fwd'] - pred_20_lm).abs().mean()
    
    # Relative MAE improvement
    naive_error = (test1_df['atr_fwd'] - test1_df['atr_today'].mean()).abs().mean()
    improvement = (naive_error - mae_20_lm) / naive_error * 100
    
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Pearson Correlation | {r_20:.6f} |")
    report.append(f"| R² | {r_20**2:.6f} |")
    report.append(f"| Regression Slope | {slope_20:.4f} |")
    report.append(f"| Intercept | {intercept_20:.6f} |")
    report.append(f"| P-value | {p_20:.6e} |")
    report.append(f"| Significant? | {'YES' if p_20 < 0.05 else 'NO'} |")
    report.append(f"| MAE (naive: use today's ATR) | {mae_20:.6f}% |")
    report.append(f"| MAE (linear model) | {mae_20_lm:.6f}% |")
    report.append(f"| Improvement vs mean predictor | {improvement:.2f}% |")
    
    # Compare with the original biased result
    report.append("")
    report.append(f"**Comparison with original RESEARCH-005 Test 4 (overlapping windows):**")
    report.append(f"- Original R² (5-day avg forward, overlapping): 0.9092")
    report.append(f"- Clean R² ({FWD_20}-day point forward, no overlap): {r_20**2:.4f}")
    report.append(f"- Degradation: {(0.9092 - r_20**2) / 0.9092 * 100:.1f}% reduction in R²")
    
    # Quintile transition
    report.append("")
    report.append("### Quintile Transition (20-day forward)")
    report.append("")
    q_labels = ['Q1 (Very Low)', 'Q2 (Low)', 'Q3 (Medium)', 'Q4 (High)', 'Q5 (Very High)']
    test1_df['q_today'] = pd.qcut(test1_df['atr_today'], 5, labels=q_labels)
    test1_df['q_fwd'] = pd.qcut(test1_df['atr_fwd'], 5, labels=q_labels)
    
    report.append("| Today \\ 20d Later | Q1 | Q2 | Q3 | Q4 | Q5 |")
    report.append("|------------------|----|----|----|----|----|")
    for i, q in enumerate(q_labels):
        mask = test1_df['q_today'] == q
        subset = test1_df[mask]
        total = len(subset)
        if total > 0:
            pcts = []
            for j, q_fwd in enumerate(q_labels):
                pct = (subset['q_fwd'] == q_fwd).sum() / total * 100
                pcts.append(f"{pct:.0f}%")
            report.append(f"| {q} | {' | '.join(pcts)} |")
    
    # Diagonal persistence
    diag_pct = sum(
        (test1_df['q_today'] == test1_df['q_fwd'])
    ) / len(test1_df) * 100
    report.append("")
    report.append(f"**Overall quintile persistence (stay in same Q): {diag_pct:.1f}%**")
    report.append(f"**Random expectation: 20%**")
    report.append("")
    
    # Binomial test: is persistence > 20%?
    n_same = int(sum(test1_df['q_today'] == test1_df['q_fwd']))
    binom_p_20 = stats.binomtest(n_same, len(test1_df), p=0.20)
    report.append(f"**Binomial test (H0: persistence = 20%): p = {binom_p_20.pvalue:.6e}**")
    report.append(f"**Significant? {'YES' if binom_p_20.pvalue < 0.05 else 'NO'}**")
    
    # Q5->Q5 specific
    q5_mask = test1_df['q_today'] == q_labels[4]
    q5_total = q5_mask.sum()
    q5_same = (test1_df.loc[q5_mask, 'q_fwd'] == q_labels[4]).sum() if q5_total > 0 else 0
    if q5_total > 0:
        q5_pct = q5_same / q5_total * 100
        bp_q5 = stats.binomtest(q5_same, q5_total, p=0.20)
        report.append(f"**Q5 (Very High) → Q5: {q5_same}/{q5_total} ({q5_pct:.1f}%), p={bp_q5.pvalue:.6e}**")
else:
    report.append("Insufficient data for this test.")

# -------------------------------------------------------
# TEST 2: ATR Today → ATR 30 Days Later
# -------------------------------------------------------
print("TEST 2: ATR today -> ATR 30 trading days later...")

FWD_30 = 30
pred_30 = atr_at_future(atr_pct, FWD_30)
test2_df = pd.DataFrame({'atr_today': atr_pct, 'atr_fwd': pred_30}).dropna()

report.append("")
report.append("## TEST 2: ATR Today → ATR 30 Trading Days Later")
report.append("")
report.append(f"Forward gap: {FWD_30} trading days (~1.5 calendar months)")
report.append(f"ATR window overlap: 0 days (fully non-overlapping)")
report.append(f"Sample size: {len(test2_df):,}")
report.append("")

if len(test2_df) > 0:
    r_30, p_30 = pearsonr(test2_df['atr_today'], test2_df['atr_fwd'])
    slope_30, intercept_30, _, _, _ = stats.linregress(test2_df['atr_today'], test2_df['atr_fwd'])
    
    pred_30_lm = slope_30 * test2_df['atr_today'] + intercept_30
    mae_30_lm = (test2_df['atr_fwd'] - pred_30_lm).abs().mean()
    naive_error_30 = (test2_df['atr_fwd'] - test2_df['atr_today'].mean()).abs().mean()
    improvement_30 = (naive_error_30 - mae_30_lm) / naive_error_30 * 100
    
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Pearson Correlation | {r_30:.6f} |")
    report.append(f"| R² | {r_30**2:.6f} |")
    report.append(f"| Regression Slope | {slope_30:.4f} |")
    report.append(f"| Intercept | {intercept_30:.6f} |")
    report.append(f"| P-value | {p_30:.6e} |")
    report.append(f"| Significant? | {'YES' if p_30 < 0.05 else 'NO'} |")
    report.append(f"| MAE (linear model) | {mae_30_lm:.6f}% |")
    report.append(f"| Improvement vs mean predictor | {improvement_30:.2f}% |")
    
    # Compare
    report.append("")
    report.append(f"**Comparison with TEST 1 (20-day forward):**")
    report.append(f"- R² at 20 days: {r_20**2:.4f}")
    report.append(f"- R² at 30 days: {r_30**2:.4f}")
    report.append(f"- Decay rate: {(r_20**2 - r_30**2) / r_20**2 * 100:.1f}% reduction from 20d to 30d")
    
    # Quintile
    report.append("")
    report.append("### Quintile Transition (30-day forward)")
    report.append("")
    test2_df['q_today'] = pd.qcut(test2_df['atr_today'], 5, labels=q_labels)
    test2_df['q_fwd'] = pd.qcut(test2_df['atr_fwd'], 5, labels=q_labels)
    
    report.append("| Today \\ 30d Later | Q1 | Q2 | Q3 | Q4 | Q5 |")
    report.append("|------------------|----|----|----|----|----|")
    for i, q in enumerate(q_labels):
        mask = test2_df['q_today'] == q
        subset = test2_df[mask]
        total = len(subset)
        if total > 0:
            pcts = []
            for j, q_fwd in enumerate(q_labels):
                pct = (subset['q_fwd'] == q_fwd).sum() / total * 100
                pcts.append(f"{pct:.0f}%")
            report.append(f"| {q} | {' | '.join(pcts)} |")
    
    # Q5 persistence
    q5_mask = test2_df['q_today'] == q_labels[4]
    q5_total = q5_mask.sum()
    q5_same_30 = (test2_df.loc[q5_mask, 'q_fwd'] == q_labels[4]).sum() if q5_total > 0 else 0
    if q5_total > 0:
        q5_pct_30 = q5_same_30 / q5_total * 100
        bp_q5_30 = stats.binomtest(q5_same_30, q5_total, p=0.20)
        report.append(f"")
        report.append(f"**Q5 (Very High) → Q5: {q5_same_30}/{q5_total} ({q5_pct_30:.1f}%), p={bp_q5_30.pvalue:.6e}**")
else:
    report.append("Insufficient data for this test.")

# -------------------------------------------------------
# TEST 3: ATR Today → Volatility Regime After 20 Days
# -------------------------------------------------------
print("TEST 3: ATR today -> volatility regime after 20 days...")

report.append("")
report.append("## TEST 3: ATR Today → Volatility Regime After 20 Days")
report.append("")
report.append("Instead of predicting exact ATR value, predict whether the market will be in a")
report.append("Low, Medium, or High volatility regime 20 days later.")
report.append("")

# Define regimes
vol_low_thresh = atr_pct.quantile(0.33)
vol_high_thresh = atr_pct.quantile(0.67)

regime_today = pd.Series(index=atr_pct.index, dtype='object')
regime_today[atr_pct <= vol_low_thresh] = 'Low'
regime_today[(atr_pct > vol_low_thresh) & (atr_pct < vol_high_thresh)] = 'Medium'
regime_today[atr_pct >= vol_high_thresh] = 'High'

regime_fwd_20 = regime_today.shift(-20)

report.append(f"| Regime | Threshold |")
report.append(f"|--------|-----------|")
report.append(f"| Low Vol | ATR ≤ {vol_low_thresh:.4f}% |")
report.append(f"| Medium | {vol_low_thresh:.4f}% < ATR < {vol_high_thresh:.4f}% |")
report.append(f"| High Vol | ATR ≥ {vol_high_thresh:.4f}% |")
report.append("")

test3_df = pd.DataFrame({
    'regime_today': regime_today,
    'regime_fwd': regime_fwd_20,
    'atr_today': atr_pct,
    'atr_fwd': atr_pct.shift(-20)
}).dropna()

report.append(f"Sample size: {len(test3_df):,}")
report.append("")

# 3x3 transition matrix
regime_labels = ['Low', 'Medium', 'High']
report.append("### Regime Transition Matrix (Today → 20 Days Later)")
report.append("")
report.append(f"| Today \\ +20d | Low | Medium | High |")
report.append(f"|-------------|-----|--------|------|")

for r_label in regime_labels:
    mask = test3_df['regime_today'] == r_label
    subset = test3_df[mask]
    total = len(subset)
    if total > 0:
        pcts = []
        for c_label in regime_labels:
            pct = (subset['regime_fwd'] == c_label).sum() / total * 100
            pcts.append(f"{pct:.1f}%")
        report.append(f"| {r_label} | {' | '.join(pcts)} |")

# Accuracy metrics
report.append("")
report.append("### Regime Prediction Accuracy")
report.append("")

# Exact match
exact_match = (test3_df['regime_today'] == test3_df['regime_fwd']).mean() * 100
# Off by 1 (Low→Medium, Medium→High or reverse)
off_by_1 = 0
for idx, row in test3_df.iterrows():
    r_idx_today = regime_labels.index(row['regime_today'])
    r_idx_fwd = regime_labels.index(row['regime_fwd'])
    if abs(r_idx_today - r_idx_fwd) == 1:
        off_by_1 += 1
off_by_1_pct = off_by_1 / len(test3_df) * 100
wrong = 100 - exact_match - off_by_1_pct

# Baseline (random guess: 33.3%)
baseline = 33.33

# Chi-squared test
contingency = np.zeros((3, 3))
for i, r in enumerate(regime_labels):
    for j, c in enumerate(regime_labels):
        contingency[i, j] = ((test3_df['regime_today'] == r) & (test3_df['regime_fwd'] == c)).sum()

chi2, chi2_p, _, _ = stats.chi2_contingency(contingency)

report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| Exact Regime Match | {exact_match:.1f}% |")
report.append(f"| Off by 1 level | {off_by_1_pct:.1f}% |")
report.append(f"| Complete Regime Flip (Low↔High) | {wrong:.1f}% |")
report.append(f"| Random Baseline | {baseline:.1f}% |")
report.append(f"| Improvement vs Random | {exact_match - baseline:.1f}% |")
report.append(f"| Chi-squared | {chi2:.2f} |")
report.append(f"| P-value | {chi2_p:.6e} |")
report.append(f"| Significant? | {'YES' if chi2_p < 0.05 else 'NO'} |")

# Per-regime accuracy
report.append("")
report.append("### Per-Regime Persistence")
report.append("")
report.append("| Current Regime | P(Same in 20d) | P(Switch to Opposite) |")
report.append("|----------------|----------------|-----------------------|")
for r_label in regime_labels:
    mask = test3_df['regime_today'] == r_label
    subset = test3_df[mask]
    total = len(subset)
    if total > 0:
        p_same = (subset['regime_fwd'] == r_label).mean() * 100
        if r_label == 'Low':
            p_opposite = (subset['regime_fwd'] == 'High').mean() * 100
        elif r_label == 'High':
            p_opposite = (subset['regime_fwd'] == 'Low').mean() * 100
        else:
            # Medium - opposite is Low or High
            p_opposite = ((subset['regime_fwd'] == 'Low') | (subset['regime_fwd'] == 'High')).mean() * 100
        
        bp = stats.binomtest(int(subset['regime_fwd'].eq(r_label).sum()), total, p=1/3)
        report.append(f"| {r_label} | {p_same:.1f}% (p={bp.pvalue:.4f}) | {p_opposite:.1f}% |")

# -------------------------------------------------------
# Comparison Summary
# -------------------------------------------------------
report.append("")
report.append("## Summary: Overlap Bias Impact")
report.append("")
report.append("| Test | Forward Gap | R² Original (biased) | R² Clean | Degradation | Significant? |")
report.append("|------|-------------|---------------------|----------|-------------|-------------|")
report.append(f"| Original (RESEARCH-005) | 5d avg (overlapping) | 0.9092 | - | - | YES |")
report.append(f"| Clean Test 1 | {FWD_20}d point | - | {r_20**2:.4f} | {(0.9092 - r_20**2)/0.9092*100:.1f}% | {'YES' if p_20 < 0.05 else 'NO'} |")
report.append(f"| Clean Test 2 | {FWD_30}d point | - | {r_30**2:.4f} | {(0.9092 - r_30**2)/0.9092*100:.1f}% | {'YES' if p_30 < 0.05 else 'NO'} |")

report.append("")
report.append("### Verdict")
report.append("")

degradation_20 = (0.9092 - r_20**2) / 0.9092 * 100 if len(test1_df) > 0 else 0
if r_20**2 > 0.5:
    report.append("**Volatility predictability remains strong after removing overlap bias.**")
    report.append(f"The R² of {r_20**2:.4f} at 20-day forward gap is still economically meaningful.")
elif r_20**2 > 0.2:
    report.append("**Volatility predictability is reduced but still statistically significant.**")
    report.append(f"The R² dropped {degradation_20:.0f}% from the biased estimate, but the correlation")
    report.append("is still non-zero, indicating genuine (though weaker) volatility persistence.")
elif p_20 < 0.05:
    report.append("**Volatility predictability is statistically significant but practically weak.**")
    report.append(f"The R² of {r_20**2:.4f} after removing overlap bias suggests that most of the")
    report.append("apparent predictability in the original test was due to overlapping windows.")
else:
    report.append("**Volatility predictability does NOT survive overlap bias correction.**")
    report.append("The apparent predictability in RESEARCH-005 was entirely due to overlapping ATR windows.")

report.append("")
report.append("### Key Insight")
report.append("")
report.append("ATR(14) as a rolling window creates ~13 days of overlap between consecutive observations.")
report.append("When predicting ATR 20+ days forward, the overlap disappears entirely.")
report.append("The remaining predictability reflects genuine volatility persistence, not statistical artifact.")
report.append("")
report.append("The true R² of ~{:.4f} (at 20-day gap) vs the biased R² of 0.9092 represents a".format(r_20**2 if len(test1_df) > 0 else 0))
report.append(f"{degradation_20:.0f}% reduction — meaning roughly {100-degradation_20:.0f}% of the original")
report.append("'predictability' was genuine, and the rest was overlap bias.")

# -------------------------------------------------------
# Chart
# -------------------------------------------------------
print("Generating charts...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Correlation decay with forward horizon
ax = axes[0, 0]
horizons = []
corrs = []
for h in range(1, 61, 1):
    fwd = atr_at_future(atr_pct, h)
    df_h = pd.DataFrame({'t': atr_pct, 'f': fwd}).dropna()
    if len(df_h) > 30:
        r_h, _ = pearsonr(df_h['t'], df_h['f'])
        horizons.append(h)
        corrs.append(r_h)
ax.plot(horizons, corrs, 'b-', lw=1.5)
ax.axhline(y=0.2, color='green', linestyle='--', alpha=0.5, label='R=0.2')
ax.axhline(y=0, color='black', lw=0.5)
ax.axvline(x=14, color='red', linestyle=':', alpha=0.5, label='ATR window (14d)')
ax.set_xlabel('Forward Horizon (trading days)')
ax.set_ylabel('Pearson Correlation')
ax.set_title('ATR Autocorrelation Decay with Forward Horizon')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Chart 2: 20-day scatter
ax = axes[0, 1]
if len(test1_df) > 0:
    ax.scatter(test1_df['atr_today'], test1_df['atr_fwd'], alpha=0.15, s=2, c='steelblue')
    x_line = np.linspace(test1_df['atr_today'].min(), test1_df['atr_today'].max(), 100)
    y_line = slope_20 * x_line + intercept_20
    ax.plot(x_line, y_line, 'r-', lw=2, label=f'R²={r_20**2:.4f}')
    ax.set_xlabel('ATR% Today')
    ax.set_ylabel(f'ATR% {FWD_20}d Later')
    ax.set_title(f'ATR Predictability ({FWD_20}-day gap, no overlap)')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Chart 3: 30-day scatter
ax = axes[1, 0]
if len(test2_df) > 0:
    ax.scatter(test2_df['atr_today'], test2_df['atr_fwd'], alpha=0.15, s=2, c='orange')
    x_line = np.linspace(test2_df['atr_today'].min(), test2_df['atr_today'].max(), 100)
    y_line = slope_30 * x_line + intercept_30
    ax.plot(x_line, y_line, 'r-', lw=2, label=f'R²={r_30**2:.4f}')
    ax.set_xlabel('ATR% Today')
    ax.set_ylabel(f'ATR% {FWD_30}d Later')
    ax.set_title(f'ATR Predictability ({FWD_30}-day gap, no overlap)')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Chart 4: Regime transition heatmap
ax = axes[1, 1]
regime_matrix = np.zeros((3, 3))
for i, r in enumerate(regime_labels):
    for j, c in enumerate(regime_labels):
        regime_matrix[i, j] = ((test3_df['regime_today'] == r) & (test3_df['regime_fwd'] == c)).sum()
# Normalize rows
for i in range(3):
    row_sum = regime_matrix[i].sum()
    if row_sum > 0:
        regime_matrix[i] = regime_matrix[i] / row_sum * 100

im = ax.imshow(regime_matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=100)
ax.set_xticks(range(3))
ax.set_xticklabels(regime_labels)
ax.set_yticks(range(3))
ax.set_yticklabels(regime_labels)
ax.set_title('Regime Transition (Today -> 20d Later) %')
for i in range(3):
    for j in range(3):
        ax.text(j, i, f'{regime_matrix[i,j]:.0f}%', ha='center', va='center', fontsize=12)
plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.savefig("charts/overlap_bias_audit.png", dpi=150)
plt.close()
print("Chart saved: charts/overlap_bias_audit.png")

report.append("")
report.append("## Charts")
report.append("")
report.append("![Overlap Bias Audit](../charts/overlap_bias_audit.png)")
report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

# Final print
print(f"\n{'='*60}")
print("OVERLAP BIAS AUDIT COMPLETE")
print(f"{'='*60}")
if len(test1_df) > 0:
    print(f"Original R² (biased, 5d avg): 0.9092")
    print(f"Clean R² (20d point, no overlap): {r_20**2:.4f}")
    print(f"Clean R² (30d point, no overlap): {r_30**2:.4f}")
    print(f"Correlation 20d: {r_20:.4f}")
    print(f"Correlation 30d: {r_30:.4f}")
    print(f"Regime exact match: {exact_match:.1f}% (random: {baseline:.1f}%)")
print(f"Report: reports/RESEARCH-005A_Overlap_Bias_Audit.md")

with open("reports/RESEARCH-005A_Overlap_Bias_Audit.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
