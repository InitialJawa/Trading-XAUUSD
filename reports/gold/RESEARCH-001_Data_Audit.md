# RESEARCH-001: Data Audit Report

**Date:** 2026-06-08 16:56
**Source:** Yahoo Finance (GC=F)

## 1. Data Overview

| Metric | Value |
|--------|-------|
| Total Observations | 6,466 |
| Start Date | 2000-08-30 |
| End Date | 2026-06-08 |
| Coverage (years) | 25.8 |
| Columns | Open, High, Low, Close, Volume |

## 2. Missing Values

| Column | Missing | % Missing |
|--------|---------|-----------|
| Open | 0 | 0.00% |
| High | 0 | 0.00% |
| Low | 0 | 0.00% |
| Close | 0 | 0.00% |
| Volume | 0 | 0.00% |

**Close column missing values:** 0 (0.00%)

## 3. Gap Analysis

| Metric | Value |
|--------|-------|
| Expected interval | 1 business day |
| Total gaps (>1 day) | 1,402 |
| Max gap | 5 days 00:00:00 |
| Mean gap | 3 days 02:27:54.179743 |
| Median gap | 3 days 00:00:00 |

### Largest gaps:

| Gap Start | Gap End | Gap Size |
|-----------|---------|----------|
| 2000-11-22 | 2000-11-27 | 5 days 00:00:00 |
| 2001-11-21 | 2001-11-26 | 5 days 00:00:00 |
| 2001-12-21 | 2001-12-26 | 5 days 00:00:00 |
| 2002-07-03 | 2002-07-08 | 5 days 00:00:00 |
| 2002-11-27 | 2002-12-02 | 5 days 00:00:00 |
| 2003-11-26 | 2003-12-01 | 5 days 00:00:00 |
| 2003-12-24 | 2003-12-29 | 5 days 00:00:00 |
| 2003-12-31 | 2004-01-05 | 5 days 00:00:00 |
| 2004-11-24 | 2004-11-29 | 5 days 00:00:00 |
| 2005-11-23 | 2005-11-28 | 5 days 00:00:00 |

## 4. Outlier Detection

| Method | Value |
|--------|-------|
| Lower bound (Q1 - 3*IQR) | -2507.42 |
| Upper bound (Q3 + 3*IQR) | 4873.20 |
| Outlier count | 34 (0.53%) |
| Min Close | 255.00 |
| Max Close | 5415.70 |
| Return outliers (|z|>4) | 34 (0.53%) |

## 5. Data Quality Score

**Overall Score: 90.0/100**

### Deductions:
- Excessive gaps: -10.0

### Quality Rating:
**Excellent** - Data is suitable for all research phases.

## 6. Price Summary Statistics

| Statistic | Open | High | Low | Close | Volume |
|-----------|------|------|-----|-------|--------|
| count | 6,466.00 | 6,466.00 | 6,466.00 | 6,466.00 | 6,466 |
| mean | 1,310.26 | 1,317.39 | 1,302.90 | 1,310.32 | 4,280 |
| std | 852.27 | 858.88 | 845.59 | 852.59 | 23,975 |
| min | 255.10 | 256.10 | 255.00 | 255.00 | 0 |
| 25% | 655.27 | 657.93 | 653.02 | 655.70 | 23 |
| 50% | 1,254.25 | 1,260.20 | 1,249.85 | 1,255.25 | 119 |
| 75% | 1,711.30 | 1,720.00 | 1,701.98 | 1,710.07 | 459 |
| max | 5,318.40 | 5,586.20 | 5,301.60 | 5,415.70 | 386,334 |

---
*Generated automatically by XAU/USD Edge Discovery Framework*