"""
XAU/USD Edge Discovery Framework
Phase 1: Data Audit
"""
import pandas as pd
import numpy as np
import os

os.makedirs("reports", exist_ok=True)

# Load data
print("Loading XAU/USD data...")
df = pd.read_csv("data/XAUUSD_yahoo_raw.csv", index_col=0, parse_dates=True)
print(f"Loaded {len(df)} rows")

# Basic info
report = []
report.append("# RESEARCH-001: Data Audit Report")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Source:** Yahoo Finance (GC=F)")
report.append("")
report.append("## 1. Data Overview")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| Total Observations | {len(df):,} |")
report.append(f"| Start Date | {df.index.min().strftime('%Y-%m-%d')} |")
report.append(f"| End Date | {df.index.max().strftime('%Y-%m-%d')} |")
report.append(f"| Coverage (years) | {(df.index.max() - df.index.min()).days / 365.25:.1f} |")
report.append(f"| Columns | {', '.join(df.columns)} |")

# 2. Missing values
report.append("")
report.append("## 2. Missing Values")
report.append("")
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100)
report.append(f"| Column | Missing | % Missing |")
report.append(f"|--------|---------|-----------|")
for col in df.columns:
    report.append(f"| {col} | {missing[col]:,} | {missing_pct[col]:.2f}% |")

# Check for NaN in Close specifically
close_nan = df['Close'].isnull().sum()
report.append("")
report.append(f"**Close column missing values:** {close_nan} ({close_nan/len(df)*100:.2f}%)")

# 3. Gap analysis
report.append("")
report.append("## 3. Gap Analysis")
report.append("")
dates = df.index.sort_values()
date_diffs = pd.Series(dates[1:]) - pd.Series(dates[:-1])
gaps = date_diffs[date_diffs > pd.Timedelta(days=1)]
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| Expected interval | 1 business day |")
report.append(f"| Total gaps (>1 day) | {len(gaps):,} |")
report.append(f"| Max gap | {gaps.max()} |")
report.append(f"| Mean gap | {gaps.mean()} |")
report.append(f"| Median gap | {gaps.median()} |")
if len(gaps) > 0:
    report.append("")
    report.append("### Largest gaps:")
    report.append("")
    report.append("| Gap Start | Gap End | Gap Size |")
    report.append("|-----------|---------|----------|")
    for i in gaps.nlargest(10).index:
        report.append(f"| {dates[i].strftime('%Y-%m-%d')} | {dates[i+1].strftime('%Y-%m-%d')} | {gaps[i]} |")

# 4. Outlier detection (using IQR on Close)
report.append("")
report.append("## 4. Outlier Detection")
report.append("")
Q1 = df['Close'].quantile(0.25)
Q3 = df['Close'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 3 * IQR
upper = Q3 + 3 * IQR
outliers = df[(df['Close'] < lower) | (df['Close'] > upper)]
report.append(f"| Method | Value |")
report.append(f"|--------|-------|")
report.append(f"| Lower bound (Q1 - 3*IQR) | {lower:.2f} |")
report.append(f"| Upper bound (Q3 + 3*IQR) | {upper:.2f} |")
report.append(f"| Outlier count | {len(outliers):,} ({len(outliers)/len(df)*100:.2f}%) |")
report.append(f"| Min Close | {df['Close'].min():.2f} |")
report.append(f"| Max Close | {df['Close'].max():.2f} |")

# Z-score method for daily returns
daily_returns = df['Close'].pct_change().dropna()
z_scores = np.abs((daily_returns - daily_returns.mean()) / daily_returns.std())
return_outliers = (z_scores > 4).sum()
report.append(f"| Return outliers (|z|>4) | {return_outliers:,} ({return_outliers/len(daily_returns)*100:.2f}%) |")

# 5. Data quality assessment
report.append("")
report.append("## 5. Data Quality Score")
report.append("")
score = 100
deductions = []

# Completeness
completeness = 100 - close_nan / len(df) * 100
if completeness < 99:
    d = (99 - completeness) * 2
    deductions.append(f"Missing data: -{d:.1f}")
    score -= d

# Gap regularity
gap_ratio = len(gaps) / len(df) * 100
if gap_ratio > 1:
    d = min(gap_ratio * 2, 10)
    deductions.append(f"Excessive gaps: -{d:.1f}")
    score -= d

# Outlier ratio
outlier_ratio = len(outliers) / len(df) * 100
if outlier_ratio > 1:
    d = min((outlier_ratio - 1) * 2, 5)
    deductions.append(f"Excessive outliers: -{d:.1f}")
    score -= d

# Coverage length
coverage_years = (df.index.max() - df.index.min()).days / 365.25
if coverage_years < 5:
    deductions.append(f"Short coverage: -10")
    score -= 10
elif coverage_years < 10:
    deductions.append(f"Moderate coverage: -5")
    score -= 5

# Recent data check
days_since_last = (pd.Timestamp.now() - df.index.max()).days
if days_since_last > 30:
    d = min(days_since_last / 10, 10)
    deductions.append(f"Stale data ({days_since_last}d stale): -{d:.1f}")
    score -= d

report.append(f"**Overall Score: {max(score, 0):.1f}/100**")
report.append("")
report.append("### Deductions:")
for d in deductions:
    report.append(f"- {d}")
if not deductions:
    report.append("- None")
report.append("")
report.append("### Quality Rating:")
if score >= 90:
    report.append("**Excellent** - Data is suitable for all research phases.")
elif score >= 70:
    report.append("**Good** - Data is suitable with minor caveats.")
elif score >= 50:
    report.append("**Fair** - Data may have limitations. Proceed with caution.")
else:
    report.append("**Poor** - Data quality issues may affect results.")

# 6. Summary statistics
report.append("")
report.append("## 6. Price Summary Statistics")
report.append("")
report.append("| Statistic | Open | High | Low | Close | Volume |")
report.append("|-----------|------|------|-----|-------|--------|")
for stat in ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']:
    vals = df.describe().loc[stat]
    report.append(f"| {stat} | {vals['Open']:,.2f} | {vals['High']:,.2f} | {vals['Low']:,.2f} | {vals['Close']:,.2f} | {vals['Volume']:,.0f} |")

report.append("")
report.append("---")
report.append("*Generated automatically by XAU/USD Edge Discovery Framework*")

# Write report
with open("reports/RESEARCH-001_Data_Audit.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print("Report saved: reports/RESEARCH-001_Data_Audit.md")
print(f"\nKey findings:")
print(f"  Observations: {len(df):,}")
print(f"  Date range: {df.index.min().date()} to {df.index.max().date()}")
print(f"  Missing values: {close_nan}")
print(f"  Gaps (>1 day): {len(gaps)}")
print(f"  Outliers (price): {len(outliers)}")
print(f"  Quality score: {max(score, 0):.1f}/100")
