"""
BTC-006: Intraday Session Analysis for Bitcoin (24/7 market)
"""
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

REPORTS_DIR = Path('reports/bitcoin')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("BTC-006: Intraday Session Analysis")
print("=" * 60)

print("\nDownloading BTC-USD H1 data from Yahoo Finance...")
import yfinance as yf
btc = yf.Ticker('BTC-USD')
raw = btc.history(period='max', interval='1h')
if len(raw) == 0:
    print("ERROR: No H1 data available")
    exit()

if hasattr(raw.index, 'tz') and raw.index.tz is not None:
    raw.index = raw.index.tz_localize(None)

print(f"Loaded {len(raw):,} hourly bars")
print(f"Period: {raw.index[0]} to {raw.index[-1]}")

close = raw['Close'].dropna()
ret = close.pct_change().dropna()
high = raw['High']
low = raw['Low']

hourly_rets = ret.copy()

report = []
report.append("# BTC-006: Intraday Session Analysis")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** BTC-USD (H1)")
report.append(f"**Period:** {raw.index[0]} to {raw.index[-1]}")
report.append(f"**Observations:** {len(hourly_rets):,} hourly bars")
report.append("")

# Since Bitcoin trades 24/7, sessions are different from traditional markets
# We define:
# - Asia Night: 0:00-8:00 UTC
# - Europe/London: 8:00-16:00 UTC
# - US/NY: 16:00-0:00 UTC
# - Overlap (Europe+US): 12:00-16:00 UTC

print("\n--- Session Effect ---")
report.append("## 1. Session Effect (24/7 Bitcoin Market)")
report.append("")
report.append("Sessions defined as UTC hours:")
report.append("- Asia Night: 0:00-8:00 UTC")
report.append("- Europe/London: 8:00-16:00 UTC")
report.append("- US/NY: 16:00-0:00 UTC")
report.append("- Europe-US Overlap: 12:00-16:00 UTC")
report.append("")

sessions = {
    'Asia Night (0-8 UTC)': (0, 8),
    'Europe (8-16 UTC)': (8, 16),
    'US (16-0 UTC)': (16, 24),
    'EU-US Overlap (12-16 UTC)': (12, 16),
}
pf_threshold = 1.30

report.append("| Session | Hours | N Hours | Mean Ret% | Win Rate% | PF | Sharpe (ann) | T-test P | PF>1.30? |")
report.append("|---------|-------|---------|-----------|-----------|----|-------------|----------|----------|")
session_edges = []
for sname, (sh, eh) in sessions.items():
    if eh > sh:
        mask = (hourly_rets.index.hour >= sh) & (hourly_rets.index.hour < eh)
    else:
        mask = (hourly_rets.index.hour >= sh) | (hourly_rets.index.hour < eh)
    data = hourly_rets[mask]
    n = len(data)
    if n < 50: continue
    mu = data.mean() * 100
    wr = (data > 0).mean() * 100
    pos = data[data > 0].sum()
    neg = abs(data[data < 0].sum())
    pf = pos / neg if neg > 0 else np.inf
    sh_ann = data.mean() / data.std() * np.sqrt(365*24) if data.std() > 0 else 0
    t, p = stats.ttest_1samp(data, 0)
    pf_pass = "✅" if pf > pf_threshold else "❌"
    report.append(f"| {sname} | {sh}-{eh} | {n:,} | {mu:.4f} | {wr:.2f} | {pf:.4f} | {sh_ann:.4f} | {p:.4e} | {pf_pass} |")
    if pf > pf_threshold and p < 0.05:
        session_edges.append((sname, mu, wr, pf, sh_ann, p))

report.append("")
if session_edges:
    report.append("**Potential session edges:**")
    for s, mu, wr, pf, sh, p in session_edges:
        report.append(f"- {s}: Ret={mu:.4f}%, WR={wr:.1f}%, PF={pf:.2f}, Sharpe={sh:.2f}, p={p:.4f}")
else:
    report.append("No session passes PF>1.30 threshold.")
report.append("")
report.append("---")
report.append("")

print("--- Hour of Day ---")
report.append("## 2. Hour of Day Effect")
report.append("")
report.append("| Hour (UTC) | N | Mean Ret% | WR% | PF | Sharpe (ann) | T-test P |")
report.append("|------------|----|-----------|-----|----|-------------|----------|")

hour_edges = []
for h in range(24):
    data = hourly_rets[hourly_rets.index.hour == h]
    n = len(data)
    if n < 50: continue
    mu = data.mean() * 100
    wr = (data > 0).mean() * 100
    pos = data[data > 0].sum()
    neg = abs(data[data < 0].sum())
    pf = pos / neg if neg > 0 else np.inf
    sh = data.mean() / data.std() * np.sqrt(365*24) if data.std() > 0 else 0
    t, p = stats.ttest_1samp(data, 0)
    report.append(f"| {h:02d}:00 | {n:,} | {mu:.4f} | {wr:.2f} | {pf:.4f} | {sh:.4f} | {p:.4e} |")
    if pf > pf_threshold and p < 0.05:
        hour_edges.append((h, mu, wr, pf, sh, p))

report.append("")
if hour_edges:
    report.append("**Best hours (PF>1.30, p<0.05):**")
    for h, mu, wr, pf, sh, p in sorted(hour_edges, key=lambda x: -x[3])[:5]:
        report.append(f"- Hour {h:02d}:00 UTC: Ret={mu:.4f}%, WR={wr:.1f}%, PF={pf:.2f}, Sharpe={sh:.2f}")
else:
    report.append("No hour passes PF>1.30 and p<0.05 simultaneously.")
report.append("")
report.append("---")
report.append("")

print("--- Volatility Profile ---")
report.append("## 3. Intraday Volatility Profile")
report.append("")
report.append("| Session | Mean Hourly Vol% (ATR-1) | Relative to Avg |")
report.append("|---------|--------------------------|-----------------|")
abs_rets = hourly_rets.abs() * 100
overall_avg_vol = abs_rets.mean()
for sname, (sh, eh) in sessions.items():
    if eh > sh:
        mask = (hourly_rets.index.hour >= sh) & (hourly_rets.index.hour < eh)
    else:
        mask = (hourly_rets.index.hour >= sh) | (hourly_rets.index.hour < eh)
    vol = abs_rets[mask].mean()
    rel = vol / overall_avg_vol if overall_avg_vol > 0 else 1
    report.append(f"| {sname} | {vol:.4f}% | {rel:.2f}x |")
report.append("")

# Volatility by hour
report.append("| Hour (UTC) | Mean |Ret|% | Relative to Avg |")
report.append("|------------|------------------|-----------------|")
for h in range(24):
    vol = abs_rets[hourly_rets.index.hour == h].mean()
    rel = vol / overall_avg_vol if overall_avg_vol > 0 else 1
    report.append(f"| {h:02d}:00 | {vol:.4f}% | {rel:.2f}x |")
report.append("")
report.append("---")
report.append("")

print("--- Opening Range Breakout ---")
report.append("## 4. Opening Range Breakout")
report.append("")
report.append("Test: After a 1h opening range, does breakout beyond it predict continuation?")
report.append("")

# We need to define daily opens for 24/7 market
daily_data = raw.resample('D').agg({
    'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'
}).dropna()
daily_ret = daily_data['Close'].pct_change().dropna()

# ORB 1h: First hour range
for orb_window in [1, 2, 4]:
    orb_results = []
    for direction, mult, label in [('Long', 1, 'Long'), ('Short', -1, 'Short')]:
        try:
            first_h = raw.groupby(raw.index.date).head(orb_window)
            orb_high = first_h.groupby(first_h.index.date)['High'].max()
            orb_low = first_h.groupby(first_h.index.date)['Low'].min()
            
            # Get the next candle after the ORB period
            daily_close = daily_data['Close']
            daily_close_idx = pd.Series(daily_close.index, index=daily_close.index.date)
            
            dates = orb_high.index.intersection(daily_close.index.date)
            signals = []
            for d in dates:
                if d not in daily_close_idx.index: continue
                day_close = daily_data.loc[daily_close_idx[d], 'Close']
                if direction == 'Long':
                    signal_price = orb_high.loc[d]
                    if day_close > signal_price:
                        signals.append(d)
                else:
                    signal_price = orb_low.loc[d]
                    if day_close < signal_price:
                        signals.append(d)
            
            signal_dates = pd.DatetimeIndex([daily_close_idx[d] for d in signals if d in daily_close_idx.index])
            fwd_ret = daily_ret.shift(-1).loc[signal_dates].dropna()
            
            if len(fwd_ret) > 10:
                mu = fwd_ret.mean() * 100
                wr = (fwd_ret > 0).mean() * 100
                pos = fwd_ret[fwd_ret > 0].sum()
                neg = abs(fwd_ret[fwd_ret < 0].sum())
                pf = pos / neg if neg > 0 else np.inf
                _, p = stats.ttest_1samp(fwd_ret, 0)
                orb_results.append({
                    'Label': f'{label} ({orb_window}h ORB)',
                    'N': len(fwd_ret),
                    'Ret%': mu,
                    'WR%': wr,
                    'PF': pf,
                    'P': p
                })
        except: pass
    
    if orb_results:
        report.append(f"### {orb_window}h Opening Range")
        report.append("")
        report.append("| Signal | N | Mean Ret% | WR% | PF | P-value |")
        report.append("|--------|----|-----------|-----|----|---------|")
        for r in orb_results:
            report.append(f"| {r['Label']} | {r['N']} | {r['Ret%']:.4f} | {r['WR%']:.1f} | {r['PF']:.4f} | {r['P']:.4e} |")
        report.append("")

report.append("---")
report.append("")

print("--- Volatility Regime ---")
report.append("## 5. Volatility Regime (H1)")
report.append("")
atr_h1 = close.rolling(24).std()  # ~1 day ATR
vol_regime = pd.qcut(atr_h1.rank(method='first'), 3, labels=['Low', 'Med', 'High'])

report.append("| Vol Regime | N Hours | Mean Ret% | WR% | PF | Sharpe (ann) |")
report.append("|------------|---------|-----------|-----|----|-------------|")
vol_edges = []
for regime in ['Low', 'Med', 'High']:
    data = hourly_rets[vol_regime == regime]
    n = len(data)
    if n < 50: continue
    mu = data.mean() * 100
    wr = (data > 0).mean() * 100
    pos = data[data > 0].sum()
    neg = abs(data[data < 0].sum())
    pf = pos / neg if neg > 0 else np.inf
    sh = data.mean() / data.std() * np.sqrt(365*24) if data.std() > 0 else 0
    report.append(f"| {regime} | {n:,} | {mu:.4f} | {wr:.2f} | {pf:.4f} | {sh:.4f} |")
    if pf > pf_threshold:
        vol_edges.append((regime, mu, wr, pf, sh))

report.append("")
report.append("---")
report.append("")

print("--- Final Summary ---")
report.append("## Summary")
report.append("")
all_edges = []
if session_edges:
    for s, mu, wr, pf, sh, p in session_edges:
        all_edges.append({'Type': 'Session', 'Name': s, 'WR%': wr, 'PF': pf, 'Sharpe': sh, 'P': p})
if hour_edges:
    for h, mu, wr, pf, sh, p in hour_edges:
        all_edges.append({'Type': 'Hour', 'Name': f'H{h:02d}', 'WR%': wr, 'PF': pf, 'Sharpe': sh, 'P': p})
if vol_edges:
    for r, mu, wr, pf, sh in vol_edges:
        all_edges.append({'Type': 'VolRegime', 'Name': r, 'WR%': wr, 'PF': pf, 'Sharpe': sh, 'P': 'N/A'})

if all_edges:
    report.append("| Type | Name | WR% | PF | Sharpe | P-value |")
    report.append("|------|------|-----|----|--------|---------|")
    for e in all_edges:
        report.append(f"| {e['Type']} | {e['Name']} | {e['WR%']:.1f} | {e['PF']:.2f} | {e['Sharpe']:.2f} | {e['P']} |")
    report.append("")
    report.append("**Note:** Intraday edges require Monte Carlo validation before confirmation (same as Gold H1-002).")
else:
    report.append("No intraday edges found at PF>1.30 threshold.")

report.append("")
report.append("---")
report.append("*Generated by research/bitcoin/scripts/btc_006_intraday.py*")

with open(REPORTS_DIR / 'BTC-006_Intraday_Analysis.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nReport saved: {REPORTS_DIR / 'BTC-006_Intraday_Analysis.md'}")
print("BTC-006 COMPLETE")
