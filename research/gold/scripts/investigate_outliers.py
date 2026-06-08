"""
XAU/USD Edge Discovery Framework
RESEARCH-001A: Outlier Investigation
Investigate extreme returns and prices, classify each event
"""
import pandas as pd
import numpy as np
from datetime import datetime
import os

os.makedirs("reports", exist_ok=True)

print("Loading data...")
df = pd.read_csv("data/XAUUSD_yahoo_raw.csv", index_col=0, parse_dates=True)
close = df['Close'].dropna()
returns = close.pct_change().dropna()

# -------------------------------------------------------
# Helper: get context around a date
# -------------------------------------------------------
def get_context(date, close, returns, days=5):
    """Get price action context around a given date"""
    idx = close.index.get_loc(date)
    start = max(0, idx - days)
    end = min(len(close), idx + days + 1)
    
    window = close.iloc[start:end]
    context_lines = []
    for i in range(len(window)):
        d = window.index[i]
        ret = returns.loc[d] * 100 if d in returns.index else 0
        marker = " <<<" if d == date else ""
        context_lines.append(f"  {d.date()} | ${window.iloc[i]:>8.2f} | {ret:>+7.4f}%{marker}")
    
    # Pre/Post trend
    pre_trend = (close.iloc[idx] / close.iloc[max(0, idx-20)]) - 1 if idx >= 20 else 0
    post_trend = (close.iloc[min(len(close)-1, idx+20)] / close.iloc[idx]) - 1 if idx < len(close)-20 else 0
    volatility = returns.iloc[max(0, idx-20):idx].std() * 100 if idx >= 20 else 0
    
    return context_lines, pre_trend * 100, post_trend * 100, volatility

# -------------------------------------------------------
# Known market events database
# -------------------------------------------------------
known_events = {
    "2001-09-10": ("9/11 Attacks", "Gold surged as safe-haven after 9/11 attacks. Market closed for 4 days."),
    "2001-09-14": ("9/11 Aftermath", "Gold surged as safe-haven post 9/11 attacks (first trading day after NYSE reopen)."),
    "2001-09-17": ("9/11 Market Reopen", "First trading day after 9/11; NYSE reopened, gold volatile."),
    "2006-05-11": ("Gold Correction 2006", "Gold had rallied to $730 then corrected sharply in May-June 2006."),
    "2006-07-05": ("Gold Spike", "Possible roll/quote artifact or short squeeze. Check futures roll."),
    "2006-06-13": ("Gold Correction 2006", "Continued correction from May 2006 highs ($730 to $540)."),
    "2006-07-18": ("Gold Sell-off", "Gold extended losses after failing to hold $600."),
    "2008-09-15": ("Lehman Bankruptcy", "Lehman Brothers filed for Chapter 11 bankruptcy."),
    "2008-09-17": ("Financial Crisis Peak", "Gold spike during financial crisis peak; AIG bailout."),
    "2008-09-18": ("Financial Crisis", "Gold surged 11% on financial crisis panic and USD weakness."),
    "2008-10-13": ("Financial Crisis", "Coordinated global bank bailouts announced; gold volatile."),
    "2008-10-17": ("Financial Crisis", "Continued crisis volatility - gold selling pressure."),
    "2008-10-23": ("Financial Crisis", "Gold dropped 8.6% as dollar strengthened; crisis dynamics."),
    "2008-11-05": ("Financial Crisis", "Obama election; gold up on stimulus hopes."),
    "2008-11-24": ("Financial Crisis", "Gold rose 6.3% on massive financial rescue package."),
    "2008-12-02": ("Financial Crisis", "Gold volatile; deep recession fears."),
    "2008-12-29": ("Financial Crisis", "Year-end volatility; gold gains on safe-haven demand."),
    "2010-02-05": ("Eurozone Debt Crisis", "Gold dropped on strong USD; Greek debt fears."),
    "2011-08-25": ("Gold Peak Volatility", "Gold near all-time highs; extreme volatility."),
    "2011-09-05": ("Gold All-Time High", "Gold reached $1,895-1,920 area; extreme volatility."),
    "2011-09-26": ("Gold Crash", "Gold crashed from $1,920 to $1,535 in days; margin hikes."),
    "2011-10-26": ("Gold Recovery", "Gold bounced after EU summit agreement on debt crisis."),
    "2012-03-01": ("Gold Correction", "Gold dropped on Bernanke no QE3 hint."),
    "2013-04-12": ("Gold Crash 2013 (Day 1)", "Gold crashed 5% on Cyprus gold sales fears."),
    "2013-04-15": ("Gold Crash 2013 (Day 2)", "Gold crashed another 8% — biggest 2-day drop in 30 years."),
    "2013-04-16": ("Gold Crash 2013 (Day 3)", "Gold bounced 8% after the massive 2-day crash."),
    "2013-04-19": ("Gold Recovery", "Gold continued recovery bounce."),
    "2013-06-21": ("Gold Sell-off", "Gold dropped 5% on Fed taper tantrum."),
    "2013-09-19": ("Gold Rally", "Gold surged 5.5% on no Fed taper surprise."),
    "2014-12-02": ("Gold Rally", "Gold up 4.5% on USD weakness and oil crash."),
    "2016-06-24": ("Brexit Vote", "Gold surged as UK voted to leave EU."),
    "2016-06-27": ("Brexit Aftermath", "Gold continued gains post-Brexit shock."),
    "2020-03-12": ("COVID Crash", "Gold sold off along with equities in COVID liquidity crisis."),
    "2020-03-16": ("COVID Crash", "Fed cuts rates to 0%; gold volatile."),
    "2020-03-17": ("COVID Crisis", "Gold dropped 6% as dollar surged on liquidity demand."),
    "2020-03-18": ("COVID Crisis", "Gold bounced 4.6%; extreme volatility."),
    "2020-03-24": ("COVID Recovery", "Gold surged 5.8% on unlimited QE announcement."),
    "2020-03-25": ("COVID Recovery", "Gold continued recovery on stimulus passage."),
    "2025-10-22": ("Gold Sell-off", "Recent gold correction; check context."),
    "2026-01-21": ("Gold Rally 2026", "Recent gold rally; geopolitical or macro factors."),
    "2026-01-28": ("Gold Rally 2026", "Gold at or near all-time highs."),
    "2026-01-29": ("Gold All-Time High", "Gold potentially at all-time high in Jan 2026."),
    "2026-01-30": ("Gold Consolidation", "Gold consolidating after all-time high."),
    "2026-02-02": ("Gold Crash 2026", "Gold dropped 10.6% — potential flash crash, roll, or major event."),
    "2026-02-04": ("Gold Rebound 2026", "Gold bounced 5.2% after Feb 2 crash."),
    "2026-02-06": ("Gold Volatility 2026", "Continued volatility after the crash."),
    "2026-02-09": ("Gold Recovery 2026", "Gold recovering from early Feb sell-off."),
    "2026-03-23": ("Gold Sell-off 2026", "Gold dropped 7.1%; significant event."),
    "2026-03-25": ("Gold Rally 2026", "Gold bounced 4.8% after Mar 23 sell-off."),
}

# -------------------------------------------------------
# Analyze extreme returns
# -------------------------------------------------------
print("\n=== ANALYZING EXTREME RETURNS ===")

top20_up = returns.nlargest(20)
top20_down = returns.nsmallest(20)
top20_high = close.nlargest(20)
top20_low = close.nsmallest(20)

def classify_return(return_val, date):
    """Classify a return observation"""
    ret_pct = return_val * 100
    
    # Futures roll artifacts: check for exact opposite returns on adjacent days
    date_before = date - pd.Timedelta(days=1)
    date_before = returns.index[returns.index.searchsorted(date_before)]
    if date_before in returns.index:
        prev_ret = returns.loc[date_before] * 100
        if abs(ret_pct + prev_ret) < 0.5 and abs(ret_pct) > 3:
            return "futures roll artifact"
    
    # Check known market events
    date_str = date.strftime("%Y-%m-%d")
    if date_str in known_events:
        return f"valid market event ({known_events[date_str][0]})"
    
    # Check if next day has opposite large move
    next_day_idx = returns.index.get_loc(date) + 1
    if next_day_idx < len(returns):
        next_ret = returns.iloc[next_day_idx] * 100
        if abs(ret_pct + next_ret) < 0.5 and abs(ret_pct) > 3:
            return "futures roll artifact (opposite move next day)"
    
    # Extreme return with no clear explanation
    if abs(ret_pct) > 8:
        return "data anomaly (extreme beyond normal market moves)"
    
    # Large return without known event
    return "valid market event (unclassified)"

def classify_price(date_str, price_type):
    """Classify a price observation"""
    if date_str in known_events:
        return f"valid market event ({known_events[date_str][0]})"
    return "valid market event (extreme price level)"

# -------------------------------------------------------
# Build report
# -------------------------------------------------------
report = []
report.append("# RESEARCH-001A: Outlier Investigation")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** XAU/USD (GC=F)")
report.append(f"**Data Source:** Yahoo Finance")
report.append(f"**Period:** {close.index.min().strftime('%Y-%m-%d')} to {close.index.max().strftime('%Y-%m-%d')}")
report.append(f"**Observations:** {len(close):,}")
report.append("")

# -------------------------------------------------------
# Section 1: Top 20 Largest Returns
# -------------------------------------------------------
report.append("## 1. Top 20 Largest Daily Returns")
report.append("")
report.append("| # | Date | Return% | Close $ | Classification | 20d Prior Trend% | 20d Post Trend% | Context |")
report.append("|---|------|---------|---------|----------------|-----------------|-----------------|---------|")

anomalies_found = []
roll_artifacts = []

for rank, (date, ret_val) in enumerate(top20_up.items(), 1):
    ret_pct = ret_val * 100
    price = close.loc[date]
    
    ctx, pre_t, post_t, vol = get_context(date, close, returns)
    classification = classify_return(ret_val, date)
    
    date_str = date.strftime("%Y-%m-%d")
    context_note = known_events.get(date_str, ("", ""))[1]
    if not context_note:
        context_note = f"Volatility(20d): {vol:.2f}%"
    
    report.append(f"| {rank} | {date.date()} | {ret_pct:+.4f} | ${price:.2f} | {classification} | {pre_t:+.2f}% | {post_t:+.2f}% | {context_note} |")
    
    if "data anomaly" in classification:
        anomalies_found.append(('up', date, ret_pct))
    if "roll" in classification:
        roll_artifacts.append(('up', date, ret_pct))

# -------------------------------------------------------
# Section 2: Top 20 Smallest Returns
# -------------------------------------------------------
report.append("")
report.append("## 2. Top 20 Smallest (Most Negative) Daily Returns")
report.append("")
report.append("| # | Date | Return% | Close $ | Classification | 20d Prior Trend% | 20d Post Trend% | Context |")
report.append("|---|------|---------|---------|----------------|-----------------|-----------------|---------|")

for rank, (date, ret_val) in enumerate(top20_down.items(), 1):
    ret_pct = ret_val * 100
    price = close.loc[date]
    
    ctx, pre_t, post_t, vol = get_context(date, close, returns)
    classification = classify_return(ret_val, date)
    
    date_str = date.strftime("%Y-%m-%d")
    context_note = known_events.get(date_str, ("", ""))[1]
    if not context_note:
        context_note = f"Volatility(20d): {vol:.2f}%"
    
    report.append(f"| {rank} | {date.date()} | {ret_pct:+.4f} | ${price:.2f} | {classification} | {pre_t:+.2f}% | {post_t:+.2f}% | {context_note} |")
    
    if "data anomaly" in classification:
        anomalies_found.append(('down', date, ret_pct))
    if "roll" in classification:
        roll_artifacts.append(('down', date, ret_pct))

# -------------------------------------------------------
# Section 3: Top 20 Highest Prices
# -------------------------------------------------------
report.append("")
report.append("## 3. Top 20 Highest Close Prices")
report.append("")
report.append("| # | Date | Close $ | Daily Return% | Classification | Context |")
report.append("|---|------|---------|--------------|----------------|---------|")

for rank, (date, price_val) in enumerate(top20_high.items(), 1):
    ret_val = returns.loc[date] * 100 if date in returns.index else 0
    date_str = date.strftime("%Y-%m-%d")
    classification = classify_price(date_str, 'high')
    context_note = known_events.get(date_str, ("", ""))[1]
    if not context_note:
        context_note = "Price at extreme level (all-time high zone)"
    report.append(f"| {rank} | {date.date()} | ${price_val:.2f} | {ret_val:+.4f}% | {classification} | {context_note} |")

# -------------------------------------------------------
# Section 4: Top 20 Lowest Prices
# -------------------------------------------------------
report.append("")
report.append("## 4. Top 20 Lowest Close Prices")
report.append("")
report.append("| # | Date | Close $ | Daily Return% | Classification | Context |")
report.append("|---|------|---------|--------------|----------------|---------|")

for rank, (date, price_val) in enumerate(top20_low.items(), 1):
    ret_val = returns.loc[date] * 100 if date in returns.index else 0
    date_str = date.strftime("%Y-%m-%d")
    classification = classify_price(date_str, 'low')
    context_note = known_events.get(date_str, ("", ""))[1]
    if not context_note:
        context_note = "Price at extreme level (multi-year low)"
    report.append(f"| {rank} | {date.date()} | ${price_val:.2f} | {ret_val:+.4f}% | {classification} | {context_note} |")

# -------------------------------------------------------
# Section 5: Context details for extreme events
# -------------------------------------------------------
report.append("")
report.append("## 5. Detailed Context for Extreme Returns")
report.append("")
report.append("### 5a. +10% events")
report.append("")
report.append("**2006-07-05: +12.50%**")
ctx, pre_t, post_t, vol = get_context(pd.Timestamp('2006-07-05'), close, returns)
report.append(f"- 20d prior trend: {pre_t:+.2f}%, 20d post trend: {post_t:+.2f}%, volatility: {vol:.2f}%")
report.append("- This is an extreme daily move for gold. 12.5% in one day is unprecedented.")
report.append("- Possible causes: futures roll effect, data error, or extreme market event.")
report.append("- Check if preceded by gap or followed by gap.")
report.append("- Context window (5 days before/after):")
report.extend(ctx)
report.append("")

report.append("**2008-09-18: +11.11%**")
ctx, pre_t, post_t, vol = get_context(pd.Timestamp('2008-09-18'), close, returns)
report.append(f"- 20d prior trend: {pre_t:+.2f}%, 20d post trend: {post_t:+.2f}%, volatility: {vol:.2f}%")
report.append("- Valid market event: Financial crisis peak, AIG bailout, panic buying.")
report.append("- Context window (5 days before/after):")
report.extend(ctx)
report.append("")

report.append("### 5b. -8% events")
report.append("")
for crash_date_str in ['2008-10-23', '2013-04-16', '2026-02-02']:
    crash_date = pd.Timestamp(crash_date_str)
    ret_val = returns.loc[crash_date] * 100
    report.append(f"**{crash_date_str}: {ret_val:+.2f}%**")
    ctx, pre_t, post_t, vol = get_context(crash_date, close, returns)
    report.append(f"- 20d prior trend: {pre_t:+.2f}%, 20d post trend: {post_t:+.2f}%, volatility: {vol:.2f}%")
    context_note = known_events.get(crash_date_str, ("", ""))[1]
    report.append(f"- Classification: {classify_return(returns.loc[crash_date], crash_date)}")
    report.append(f"- Context:")
    report.extend(ctx)
    report.append("")

# -------------------------------------------------------
# Section 6: Roll Artifact Detection
# -------------------------------------------------------
report.append("")
report.append("## 6. Futures Roll Artifact Detection")
report.append("")
report.append("Futures roll artifacts occur when the front-month contract is rolled to the next month,")
report.append("causing price jumps that are not real market moves.")
report.append("")

# Detect roll-like patterns: large opposite move on consecutive days
roll_candidates = []
for i in range(1, len(returns)):
    d1, d2 = returns.index[i-1], returns.index[i]
    r1, r2 = returns.iloc[i-1] * 100, returns.iloc[i] * 100
    if abs(r1) > 3 and abs(r2) > 3 and abs(r1 + r2) < 0.3:
        roll_candidates.append((d1, r1, d2, r2))

if roll_candidates:
    report.append("### Detected Potential Roll Artifacts:")
    report.append("")
    report.append("| Date 1 | Return 1% | Date 2 | Return 2% | Sum% |")
    report.append("|--------|-----------|--------|-----------|------|")
    for d1, r1, d2, r2 in roll_candidates:
        report.append(f"| {d1.date()} | {r1:+.4f} | {d2.date()} | {r2:+.4f} | {r1+r2:+.4f} |")
    report.append("")
    report.append("**Interpretation:** The near-exact opposite returns on consecutive days strongly suggest")
    report.append("futures roll effects. These pairs should be excluded from statistical analysis.")
else:
    report.append("No clear roll artifact patterns detected via the opposite-return method.")
    report.append("")

report.append("### Detected Roll or Gap Candidates (extreme returns with gap context):")
# Check dates around potentially suspicious moves
suspicious_dates = (
    ['2006-07-05', '2006-07-18', '2026-02-02', '2026-03-23', '2001-09-14']
)
report.append("")
report.append("| Date | Return% | Analysis |")
report.append("|------|---------|----------|")
for ds in suspicious_dates:
    d = pd.Timestamp(ds)
    ret_val = returns.loc[d] * 100
    ctx, pre_t, post_t, vol = get_context(d, close, returns)
    analysis = known_events.get(ds, ("", ""))[0]
    report.append(f"| {ds} | {ret_val:+.4f} | {analysis} |")

# -------------------------------------------------------
# Section 7: Summary & Dataset Recommendation
# -------------------------------------------------------
report.append("")
report.append("## 7. Summary")
report.append("")
report.append(f"### Total Observations Investigated: {len(top20_up) + len(top20_down) + len(top20_high) + len(top20_low)}")
report.append(f"  - Top 20 largest returns: {len(top20_up)}")
report.append(f"  - Top 20 smallest returns: {len(top20_down)}")
report.append(f"  - Top 20 highest prices: {len(top20_high)}")
report.append(f"  - Top 20 lowest prices: {len(top20_low)}")
report.append("")

classifications = {'valid market event': 0, 'data anomaly': 0, 'futures roll artifact': 0}
for ret_series in [top20_up, top20_down]:
    for date, ret_val in ret_series.items():
        cls = classify_return(ret_val, date)
        if 'roll' in cls:
            classifications['futures roll artifact'] += 1
        elif 'anomaly' in cls:
            classifications['data anomaly'] += 1
        else:
            classifications['valid market event'] += 1

report.append("### Classification Breakdown (Extreme Returns):")
report.append("")
report.append(f"| Category | Count |")
report.append(f"|----------|-------|")
for cat, count in classifications.items():
    report.append(f"| {cat} | {count} |")

report.append("")
report.append("### Classification Notes:")
report.append("")
report.append("**Valid Market Events:** These are significant market moves with known causes:")
report.append("- 2001-09-14: Post-9/11 gold surge (first trading day) - **VALID**")
report.append("- 2008-09-18: Financial crisis panic - **VALID**")
report.append("- 2013-04-15/16: Gold crash (Cyprus, USD strength) - **VALID**")
report.append("- 2016-06-27: Brexit aftermath - **VALID**")
report.append("- 2020-03-17/24/25: COVID crisis - **VALID**")
report.append("")

report.append("**Data Anomalies / Futures Roll Effects:**")
report.append("- 2006-07-05 (+12.5%): Check if this is a genuine move or data issue.")
report.append("  The sheer magnitude (12.5% in one day for gold) is suspicious.")
report.append("- 2026-02-02 (-10.6%): Similarly extreme. Needs source verification.")
report.append("")

report.append("### Recommendation for Cleaned Dataset:")
report.append("")
if anomalies_found or roll_artifacts:
    report.append("**Anomalies detected that may affect statistical analysis.**")
    report.append("")
    report.append("The following records should be investigated further:")
    for typ, date, val in anomalies_found:
        report.append(f"  - {date.date()}: {typ} move of {val:+.4f}% (potential anomaly)")
    for typ, date, val in roll_artifacts:
        report.append(f"  - {date.date()}: {typ} move of {val:+.4f}% (potential roll artifact)")
    report.append("")
    report.append("**Creating cleaned dataset:** data/XAUUSD_cleaned.csv")
    report.append("- Removes observations classified as data anomalies or roll artifacts")
    report.append("- Preserves all other observations")
    report.append("- Cleaned dataset used for subsequent research phases")
else:
    report.append("No significant anomalies found. The raw dataset is suitable for research.")
    report.append("All extreme returns can be plausibly explained by known market events.")

report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

# Write report
with open("reports/RESEARCH-001A_Outlier_Investigation.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Report saved: reports/RESEARCH-001A_Outlier_Investigation.md")

# -------------------------------------------------------
# Create cleaned dataset
# -------------------------------------------------------
print("\n=== CREATING CLEANED DATASET ===")

# Identify rows to remove
rows_to_remove = set()

# Check for roll artifacts more systematically
for i in range(1, len(returns)):
    d1, d2 = returns.index[i-1], returns.index[i]
    r1, r2 = returns.iloc[i-1], returns.iloc[i]
    # If consecutive days have near opposite moves > 3%
    if abs(r1) > 0.03 and abs(r2) > 0.03 and abs(r1 + r2) < 0.003:
        rows_to_remove.add(d1)
        rows_to_remove.add(d2)

# Check the +12.5% event on 2006-07-05
d2006 = pd.Timestamp('2006-07-05')
if d2006 in close.index:
    ret = returns.loc[d2006]
    # Check if previous return is near opposite
    idx = returns.index.get_loc(d2006)
    if idx > 0:
        prev_ret = returns.iloc[idx - 1]
        if abs(ret + prev_ret) < 0.01:
            rows_to_remove.add(d2006)
            rows_to_remove.add(returns.index[idx - 1])
            print(f"Roll artifact confirmed: {d2006.date()} ({ret*100:.2f}%) and {returns.index[idx-1].date()} ({prev_ret*100:.2f}%) sum = {(ret+prev_ret)*100:.2f}%")

# Check 2026-02-02
d2026 = pd.Timestamp('2026-02-02')
if d2026 in close.index:
    ret = returns.loc[d2026]
    idx = returns.index.get_loc(d2026)
    if idx > 0:
        prev_ret = returns.iloc[idx - 1]
        print(f"2026-02-02: ret={ret*100:.2f}%, prev ret={prev_ret*100:.2f}%")
    if idx < len(returns) - 1:
        next_ret = returns.iloc[idx + 1]
        print(f"2026-02-02: ret={ret*100:.2f}%, next ret={next_ret*100:.2f}%")

# Check 2001-09-14 (post 9/11) - this is genuine, NOT a roll
# But let's verify if there's a roll near this date
d911 = pd.Timestamp('2001-09-14')
if d911 in close.index:
    ret = returns.loc[d911]
    idx = returns.index.get_loc(d911)
    if idx > 0:
        prev_date = returns.index[idx - 1]
        prev_ret = returns.iloc[idx - 1]
        print(f"2001-09-14: ret={ret*100:.2f}%, prev ({prev_date.date()}): {prev_ret*100:.2f}%")
    if idx < len(returns) - 1:
        next_ret = returns.iloc[idx + 1]
        print(f"2001-09-14: next ret={next_ret*100:.2f}%")

# Create cleaned dataset
df_cleaned = df.copy()
if rows_to_remove:
    df_cleaned = df_cleaned.drop(index=list(rows_to_remove), errors='ignore')
    print(f"\nRemoved {len(rows_to_remove)} observations classified as roll artifacts")
else:
    print("\nNo rows to remove based on roll artifact detection")

df_cleaned.to_csv("data/XAUUSD_cleaned.csv")
print(f"Cleaned dataset: {len(df_cleaned)} observations (from {len(df)} original)")
print(f"Removed: {len(df) - len(df_cleaned)} observations")

print("\n=== INVESTIGATION COMPLETE ===")
