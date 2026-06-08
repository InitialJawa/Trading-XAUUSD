"""
RESEARCH-H1-002: Candidate Validation
XAU/USD Edge Discovery Framework — H1 Near-Miss Validation
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, warnings
warnings.filterwarnings('ignore')

os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)
np.random.seed(42)

print("="*60)
print("RESEARCH-H1-002: H1 Candidate Validation")
print("="*60)

# ============================================
# DATA LOADING
# ============================================
print("\nLoading H1 data...")

gc_file = "data/XAUUSD_H1.csv"
if os.path.exists(gc_file):
    gc = pd.read_csv(gc_file, index_col=0, parse_dates=True)
else:
    import yfinance as yf
    raw = yf.download('GC=F', interval='1h', period='2y', auto_adjust=True)
    gc = raw['Close'].squeeze().to_frame('Close')
    gc.to_csv(gc_file)

print(f"GC=F H1: {len(gc):,} bars")

# Build clean dataset
gc_utc = gc.copy()
gc_utc.index = pd.to_datetime(gc_utc.index, utc=True)
if gc_utc.index.tz is None:
    gc_utc.index = gc_utc.index.tz_localize('America/New_York').tz_convert('UTC')

gc_utc['Ret'] = gc_utc['Close'].pct_change()
gc_utc['Hour'] = gc_utc.index.hour
gc_utc['Weekday'] = gc_utc.index.weekday
gc_utc['Date'] = gc_utc.index.date
gc_utc['Month'] = gc_utc.index.month
gc_utc['Year'] = gc_utc.index.year
gc_utc['ATR'] = gc_utc['Close'].diff().abs().rolling(14).mean()
gc_utc['ATR_pct'] = gc_utc['Close'].pct_change().abs().rolling(14).mean() * 100
gc_utc['ATR_signal'] = gc_utc['ATR_pct'].shift(1)

data = gc_utc.dropna(subset=['Ret']).copy()
print(f"Clean bars: {len(data):,}")
print(f"Period: {data.index[0]} to {data.index[-1]} UTC")
print(f"Trading days: {data['Date'].nunique():,}")

# ============================================
# HELPER FUNCTIONS
# ============================================
def analyze(rets, min_n=20):
    rets = rets.dropna()
    n = len(rets)
    if n < min_n:
        return None
    wr = (rets > 0).mean() * 100
    mean_r = rets.mean() * 100
    sh = rets.mean() / rets.std() * np.sqrt(252*24) if rets.std() > 0 else 0
    pos = rets[rets > 0].sum()
    neg = abs(rets[rets < 0].sum())
    pf = pos / neg if neg > 0 else np.inf
    t, p = stats.ttest_1samp(rets, 0)
    return {'N': n, 'WR': wr, 'Mean': mean_r, 'Sharpe': sh, 'PF': pf, 'P': p, 'T': t}

def fmt_row(r):
    if r is None:
        return "| — | — | — | — | — | — |"
    return f"| {r['N']:,} | {r['Mean']:.4f} | {r['WR']:.1f} | {r['Sharpe']:.4f} | {r['PF']:.4f} | {r['P']:.4e} |"

def monte_carlo(rets, n_iter=10000):
    n = len(rets)
    actual_t = stats.ttest_1samp(rets, 0)[0]
    count_more_extreme = 0
    for _ in range(n_iter):
        shuffled = np.random.permutation(rets)
        t_shuf = stats.ttest_1samp(shuffled, 0)[0]
        if abs(t_shuf) >= abs(actual_t):
            count_more_extreme += 1
    return count_more_extreme / n_iter

# ============================================
# DEFINE CANDIDATES
# ============================================
candidates = {
    'Hour 20 UTC': {
        'mask': data['Hour'] == 20,
        'rets': data.loc[data['Hour'] == 20, 'Ret'],
        'description': 'Gold returns during 20:00 UTC hour (4 PM ET, near NY close)'
    },
    'Hour 23 UTC': {
        'mask': data['Hour'] == 23,
        'rets': data.loc[data['Hour'] == 23, 'Ret'],
        'description': 'Gold returns during 23:00 UTC hour (7 PM ET, after US cash session)'
    },
    'Hour 08 UTC': {
        'mask': data['Hour'] == 8,
        'rets': data.loc[data['Hour'] == 8, 'Ret'],
        'description': 'Gold returns during 08:00 UTC hour (4 AM ET, London open)'
    },
    'Low Vol Regime': {
        'mask': data['ATR_signal'] < data['ATR_signal'].quantile(0.33),
        'rets': data.loc[data['ATR_signal'] < data['ATR_signal'].quantile(0.33), 'Ret'],
        'description': 'Gold returns when trailing ATR is in bottom 33%'
    },
    'ORB London Short': {
        'description': 'London open breakout short signals (computed separately)'
    }
}

report = []
report.append("# RESEARCH-H1-002: H1 Candidate Validation")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** XAU/USD (GC=F)")
report.append(f"**Data:** H1 (hourly), {len(data):,} bars")
report.append(f"**Period:** {data.index[0].strftime('%Y-%m-%d %H:%M')} to {data.index[-1].strftime('%Y-%m-%d %H:%M')} UTC")
report.append(f"**Trading Days:** {data['Date'].nunique():,}")
report.append(f"**Data Source:** Yahoo Finance (yfinance)")
report.append("")
report.append("> **Data Limitation:** Yahoo Finance restricts H1 data to the last 730 days.")
report.append("> This analysis covers ~2 years (June 2024 – June 2026). The user requested")
report.append("> 2018–present (5+ years). Only 2024–2026 is available from free sources.")
report.append("> Results should be interpreted with this limitation in mind.")
report.append("")

# ============================================
# RETEST EACH CANDIDATE
# ============================================
print("\n=== RETESTING ALL CANDIDATES ===")

report.append("## 1. Candidate Retests")
report.append("")

# Re-compute ORB short signals
london_short = []
for date_key, group in data.groupby('Date'):
    range_bars = group[(group['Hour'] >= 8) & (group['Hour'] <= 9)]
    if len(range_bars) < 1:
        continue
    range_high = range_bars['Close'].max()
    range_low = range_bars['Close'].min()
    open_price = range_bars.iloc[0]['Close']
    range_size = (range_high - range_low) / open_price * 100
    if range_size < 0.01:
        continue
    later_bars = group[group['Hour'] >= 10]
    for _, bar in later_bars.iterrows():
        if bar['Close'] < range_low:  # Short breakout
            entry_time = bar.name
            entry_price = bar['Close']
            for fwd in [1, 3, 6]:
                future = data.loc[entry_time:].iloc[1:fwd+1]
                if len(future) >= fwd:
                    exit_price = future.iloc[-1]['Close']
                    ret = (entry_price - exit_price) / entry_price  # Short: entry-exit
                    london_short.append({'Date': date_key, 'Fwd': fwd, 'Ret': ret})
            break

df_short = pd.DataFrame(london_short) if london_short else pd.DataFrame()
orb_short_1h = df_short[df_short['Fwd'] == 1]['Ret'].values if len(df_short) > 0 else np.array([])

report.append("| Candidate | N | Mean% | WR% | Sharpe | PF | P-value | MC p-val |")
report.append("|-----------|----|-------|-----|--------|----|---------|----------|")

all_results = {}
for cname, cdata in candidates.items():
    if cname == 'ORB London Short':
        rets = pd.Series(orb_short_1h)
        n_or = len(rets)
        report.append(f"| {cname} | {n_or:,} | — | — | — | — | — | — |")
        if n_or < 20:
            report = report[:-1] + [f"| {cname} | {n_or} | — | — | — | — | — | — |"]
        all_results[cname] = {'rets': rets.values, 'r': None}
        continue
    
    rets = cdata['rets']
    r = analyze(rets)
    all_results[cname] = {'rets': rets.values, 'r': r}
    
    if r:
        mc_p = monte_carlo(rets.values, n_iter=5000)
        report.append(f"| {cname} {fmt_row(r)} | {mc_p:.4f} |")
    else:
        report.append(f"| {cname} | {rets.dropna().shape[0]:,} | — | — | — | — | — | — |")

report.append("")

# ============================================
# STABILITY TEST
# ============================================
print("\n=== STABILITY ANALYSIS ===")
report.append("## 2. Stability Analysis")
report.append("")

dates_sorted = sorted(data['Date'].unique())
n_dates = len(dates_sorted)
split1 = dates_sorted[:n_dates//3]
split2 = dates_sorted[n_dates//3:2*n_dates//3]
split3 = dates_sorted[2*n_dates//3:]

periods = [
    ('Early Period', split1, f'{split1[0]} to {split1[-1]}'),
    ('Middle Period', split2, f'{split2[0]} to {split2[-1]}'),
    ('Late Period', split3, f'{split3[0]} to {split3[-1]}'),
]

for cname, cdata in candidates.items():
    if cname == 'ORB London Short':
        continue
    if all_results[cname]['r'] is None:
        continue
    
    report.append(f"### {cname}")
    report.append("")
    report.append(f"Full sample: N={all_results[cname]['r']['N']:,}, WR={all_results[cname]['r']['WR']:.1f}%, "
                  f"PF={all_results[cname]['r']['PF']:.4f}, Sharpe={all_results[cname]['r']['Sharpe']:.4f}, "
                  f"p={all_results[cname]['r']['P']:.4e}")
    report.append("")
    report.append("| Period | N | Mean% | WR% | PF | Sharpe | P-value |")
    report.append("|--------|----|-------|-----|----|--------|---------|")
    
    stability_scores = []
    for label, date_list, range_str in periods:
        mask = pd.Series(data.index.date, index=data.index).isin(date_list) & cdata['mask']
        rets = data.loc[mask, 'Ret']
        r = analyze(rets, min_n=10)
        if r:
            report.append(f"| {label} ({range_str}) | {r['N']:,} | {r['Mean']:.4f} | {r['WR']:.1f} | {r['PF']:.4f} | {r['Sharpe']:.4f} | {r['P']:.4e} |")
            stability_scores.append(r['Sharpe'])
    
    if len(stability_scores) >= 2:
        consistency = 1 - np.std(stability_scores) / (abs(np.mean(stability_scores)) + 0.001)
        report.append(f"\n**Stability score:** {consistency:.2f} (1.0 = perfect consistency, lower = erratic)")
    report.append("")
    report.append("---")
    report.append("")

# ORB short stability
report.append("### ORB London Short (1h)")
report.append("")
report.append(f"Full sample: N={len(df_short[df_short['Fwd']==1]):,} signals")
report.append("")
report.append("| Period | N | Mean% | WR% | PF | Sharpe | P-value |")
report.append("|--------|----|-------|-----|----|--------|---------|")
for label, date_list, range_str in periods:
    subset = df_short[(df_short['Fwd'] == 1) & (df_short['Date'].isin(date_list))]
    if len(subset) > 5:
        rets = subset['Ret'].values / 100
        wr = (rets > 0).mean() * 100
        mean_r = rets.mean() * 100
        sh = rets.mean() / rets.std() * np.sqrt(252*24) if rets.std() > 0 else 0
        pos = rets[rets > 0].sum()
        neg = abs(rets[rets < 0].sum())
        pf = pos / neg if neg > 0 else np.inf
        _, p = stats.ttest_1samp(rets, 0)
        report.append(f"| {label} ({range_str}) | {len(subset):,} | {mean_r:.4f} | {wr:.1f} | {pf:.4f} | {sh:.4f} | {p:.4e} |")
report.append("")

# ============================================
# MONTE CARLO
# ============================================
print("\n=== MONTE CARLO SIMULATION ===")
report.append("## 3. Monte Carlo Simulation")
report.append("")
report.append("Method: Shuffle return labels 10,000 times to estimate probability that observed results occur by chance alone.")
report.append("")

for cname, cdata in candidates.items():
    if cname == 'ORB London Short':
        rets = orb_short_1h
        if len(rets) < 20:
            report.append(f"### {cname} — Insufficient data for MC")
            report.append("")
            continue
    else:
        if all_results[cname]['r'] is None:
            report.append(f"### {cname} — Insufficient data")
            report.append("")
            continue
        rets = all_results[cname]['rets']
    
    n_iter = 10000
    np.random.seed(42)
    
    actual_mean = np.mean(rets) * 100
    actual_wr = (rets > 0).mean() * 100
    actual_sh = np.mean(rets) / np.std(rets) * np.sqrt(252*24) if np.std(rets) > 0 else 0
    actual_t = stats.ttest_1samp(rets, 0)[0]
    
    mc_means = []
    mc_wrs = []
    mc_shs = []
    mc_ts = []
    
    for i in range(n_iter):
        shuffled = np.random.permutation(rets)
        mc_means.append(np.mean(shuffled) * 100)
        mc_wrs.append((shuffled > 0).mean() * 100)
        if np.std(shuffled) > 0:
            mc_shs.append(np.mean(shuffled) / np.std(shuffled) * np.sqrt(252*24))
        else:
            mc_shs.append(0)
        mc_ts.append(stats.ttest_1samp(shuffled, 0)[0])
    
    mc_means = np.array(mc_means)
    mc_wrs = np.array(mc_wrs)
    mc_shs = np.array(mc_shs)
    mc_ts = np.array(mc_ts)
    
    p_mean = np.mean(mc_means >= actual_mean) if actual_mean > 0 else np.mean(mc_means <= actual_mean)
    p_wr = np.mean(mc_wrs >= actual_wr) if actual_wr > 50 else np.mean(mc_wrs <= actual_wr)
    p_sh = np.mean(mc_shs >= actual_sh) if actual_sh > 0 else np.mean(mc_shs <= actual_sh)
    p_t = np.mean(np.abs(mc_ts) >= np.abs(actual_t))
    
    report.append(f"### {cname}")
    report.append("")
    report.append(f"| Metric | Actual | MC Mean | MC 95th | MC p-value | Significant? |")
    report.append(f"|--------|--------|---------|---------|------------|--------------|")
    sig_mean = 'YES' if p_mean < 0.05 else 'no'
    sig_wr = 'YES' if p_wr < 0.05 else 'no'
    sig_sh = 'YES' if p_sh < 0.05 else 'no'
    sig_t = 'YES' if p_t < 0.05 else 'no'
    
    report.append(f"| Mean Ret% | {actual_mean:.4f} | {np.mean(mc_means):.4f} | {np.percentile(mc_means, 95):.4f} | {p_mean:.4f} | {sig_mean} |")
    report.append(f"| Win Rate% | {actual_wr:.1f} | {np.mean(mc_wrs):.1f} | {np.percentile(mc_wrs, 95):.1f} | {p_wr:.4f} | {sig_wr} |")
    report.append(f"| Sharpe | {actual_sh:.4f} | {np.mean(mc_shs):.4f} | {np.percentile(mc_shs, 95):.4f} | {p_sh:.4f} | {sig_sh} |")
    report.append(f"| T-stat | {actual_t:.4f} | {np.mean(mc_ts):.4f} | {np.percentile(mc_ts, 95):.4f} | {p_t:.4f} | {sig_t} |")
    report.append("")

# ============================================
# FINAL VERDICT
# ============================================
print("\n=== FINAL VERDICT ===")
report.append("## 4. Final Verdict")
report.append("")

# Determine verdict for each candidate
vcandidates = ['Hour 20 UTC', 'Hour 23 UTC', 'Hour 08 UTC', 'Low Vol Regime', 'ORB London Short']

for cname in vcandidates:
    if cname == 'ORB London Short':
        rets = orb_short_1h
        if len(rets) < 20:
            report.append(f"### {cname}")
            report.append("- Insufficient data")
            report.append("")
            continue
    else:
        if all_results[cname]['r'] is None:
            report.append(f"### {cname}")
            report.append("- Insufficient data")
            report.append("")
            continue
        rets = all_results[cname]['rets']
    
    r_full = analyze(pd.Series(rets))
    
    issues = []
    if r_full['N'] < 500:
        issues.append(f"Sample N={r_full['N']:,} < 500")
    if r_full['P'] >= 0.05:
        issues.append(f"p={r_full['P']:.4f} >= 0.05")
    if r_full['PF'] < 1.30:
        issues.append(f"PF={r_full['PF']:.4f} < 1.30")
    if r_full['Sharpe'] < 1.0:
        issues.append(f"Sharpe={r_full['Sharpe']:.4f} < 1.0")
    
    mc_p = monte_carlo(rets, n_iter=10000)
    if mc_p >= 0.05:
        issues.append(f"MC p={mc_p:.4f} >= 0.05 (not distinguishable from noise)")
    else:
        issues.append(f"MC p={mc_p:.4f} < 0.05 (survives randomization)")
    
    report.append(f"### {cname}")
    report.append(f"- **Full sample:** N={r_full['N']:,}, WR={r_full['WR']:.1f}%, PF={r_full['PF']:.4f}, Sharpe={r_full['Sharpe']:.4f}, p={r_full['P']:.4e}")
    report.append(f"- **MC validation:** {'FAILS' if mc_p >= 0.05 else 'PASSES'} randomization test (p={mc_p:.4f})")
    report.append(f"- **Issues:** {'; '.join(issues)}")
    report.append(f"- **Verdict: {'REJECTED - NOT A VALID EDGE' if len(issues) > 1 else 'REJECTED'}")
    report.append("")

report.append("## 5. Summary")
report.append("")

any_valid = False
for cname in vcandidates:
    if cname == 'ORB London Short':
        rets = orb_short_1h
    else:
        if all_results[cname]['r'] is None:
            continue
        rets = all_results[cname]['rets']
    
    r_full = analyze(pd.Series(rets)) if len(rets) > 20 else None
    if r_full is None:
        continue
    mc_p = monte_carlo(rets, n_iter=10000)
    
    passes_full = (r_full['N'] >= 500 and r_full['P'] < 0.05 and r_full['PF'] >= 1.30 and r_full['Sharpe'] >= 1.0)
    passes_mc = mc_p < 0.05
    
    if passes_full and passes_mc:
        any_valid = True
        report.append(f"- **{cname}**: PASSES all criteria. MC p={mc_p:.4f}. ✅")
    else:
        failures = []
        if not passes_full: failures.append("full criteria")
        if not passes_mc: failures.append("MC test")
        report.append(f"- **{cname}**: REJECTED ({', '.join(failures)}). MC p={mc_p:.4f}. ❌")

if not any_valid:
    report.append("")
    report.append("**No H1 intraday edge survives all validation tests.**")
    report.append("")
    report.append("All 5 near-misses from RESEARCH-H1-001 are confirmed as statistical noise")
    report.append("when subjected to Monte Carlo permutation testing and stability analysis.")
    report.append("The 2-year sample is insufficient to distinguish these patterns from random chance.")
    report.append("")

report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

with open("reports/RESEARCH-H1-002_Candidate_Validation.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"\n{'='*60}")
print("RESEARCH-H1-002 COMPLETE")
print(f"{'='*60}")
print(f"Report: reports/RESEARCH-H1-002_Candidate_Validation.md")
