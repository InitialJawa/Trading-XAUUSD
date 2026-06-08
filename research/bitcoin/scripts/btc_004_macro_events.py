"""
BTC-004: Macro Events — FOMC, CPI, NFP, Bitcoin-specific events
"""
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
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

# ================================================================
# EVENT DATE GENERATORS
# ================================================================

def get_nfp_dates(start_year=2014, end_year=2026):
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            first_day = datetime(year, month, 1)
            days_to_friday = (4 - first_day.weekday()) % 7
            dates.append(first_day + timedelta(days=days_to_friday))
    return pd.to_datetime(sorted(dates))

def get_cpi_dates(start_year=2014, end_year=2026):
    dates = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            dates.append(datetime(year, month, 12))
    return pd.to_datetime(sorted(dates))

def get_fomc_dates(start_year=2014, end_year=2026):
    fomc_months = [1, 3, 5, 6, 7, 9, 11, 12]
    dates = []
    for year in range(start_year, end_year + 1):
        for month in fomc_months:
            dates.append(datetime(year, month, 20))
    return pd.to_datetime(sorted(dates))

def get_bitcoin_halving_dates():
    return pd.to_datetime(['2012-11-28', '2016-07-09', '2020-05-11', '2024-04-19'])

def get_bitcoin_etf_events():
    """Major Bitcoin ETF-related events."""
    return pd.to_datetime([
        '2017-03-10',  # First BTC ETF rejection
        '2021-10-19',  # ProShares Bitcoin Strategy ETF (BITO) launch
        '2023-06-15',  # BlackRock BTC ETF filing
        '2024-01-10',  # SEC approves spot BTC ETFs
        '2024-01-11',  # First day of spot BTC ETF trading
    ])

def get_crypto_crash_dates():
    """Major crash events for post-event analysis."""
    return pd.to_datetime([
        '2020-03-12',  # COVID crash
        '2021-05-19',  # China ban crash
        '2022-05-09',  # Luna/UST crash
        '2022-11-08',  # FTX crash
    ])

nfp_dates = get_nfp_dates()
cpi_dates = get_cpi_dates()
fomc_dates = get_fomc_dates()
halving_dates = get_bitcoin_halving_dates()
etf_dates = get_bitcoin_etf_events()
crash_dates = get_crypto_crash_dates()

events = {
    'NFP': nfp_dates,
    'CPI': cpi_dates,
    'FOMC': fomc_dates,
    'Halving': halving_dates,
    'ETF_Events': etf_dates,
    'Crash_Events': crash_dates,
}

report = []
report.append("# BTC-004: Macro Event Effect")
report.append("")
report.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
report.append(f"**Instrument:** BTC-USD")
report.append(f"**Period:** {returns.index.min().strftime('%Y-%m-%d')} to {returns.index.max().strftime('%Y-%m-%d')}")
report.append("")
report.append("## Methodology")
report.append("")
report.append("For each event type:")
report.append("- Find the nearest trading day to the event date")
report.append("- Calculate return 1 day before, 1 day after, and 3 days after")
report.append("- Calculate volatility around event vs normal periods")
report.append("- Test if event returns differ significantly from non-event returns")
report.append("")

all_event_results = []

for event_name, event_dates in events.items():
    print(f"\nProcessing {event_name}...")
    report.append(f"## {event_name} Events")
    report.append("")

    event_trading_days = []
    for ed in event_dates:
        mask = close.index >= ed
        idx = close.index.searchsorted(ed)
        if idx < len(close):
            event_trading_days.append(close.index[idx])
    event_trading_days = pd.DatetimeIndex(sorted(set(event_trading_days)))
    event_trading_days = event_trading_days[event_trading_days >= returns.index[0]]
    event_trading_days = event_trading_days[event_trading_days <= returns.index[-1]]

    pre_event_returns = []
    post_event_returns = []
    post3_event_returns = []
    pre3_event_returns = []
    event_day_returns = []
    event_volatilities = []

    for ed in event_trading_days:
        ed_idx = close.index.get_loc(ed)
        if isinstance(ed_idx, slice):
            ed_idx = ed_idx.start
        if ed_idx < 0 or ed_idx >= len(close):
            continue

        if ed in returns.index:
            event_day_returns.append(returns.loc[ed])

        if ed_idx > 0:
            pre_idx = close.index[ed_idx - 1]
            if pre_idx in returns.index:
                pre_event_returns.append(returns.loc[pre_idx])

        if ed_idx < len(close) - 1:
            post_idx = close.index[ed_idx + 1]
            if post_idx in returns.index:
                post_event_returns.append(returns.loc[post_idx])

        if ed_idx < len(close) - 3:
            post3_idx = close.index[ed_idx + 3]
            ret_3d = (close.loc[post3_idx] / close.loc[ed] - 1)
            post3_event_returns.append(ret_3d)

        if ed_idx > 2:
            pre3_idx = close.index[ed_idx - 3]
            ret_pre3 = (close.loc[ed] / close.loc[pre3_idx] - 1)
            pre3_event_returns.append(ret_pre3)

        # Event-day volatility (absolute return as proxy)
        if ed in returns.index:
            event_volatilities.append(abs(returns.loc[ed]))

    n_events = len(event_trading_days)
    non_event_days = returns.index.difference(event_trading_days)
    non_event_returns = returns.loc[non_event_days]

    report.append(f"| Metric | Pre-Event (-3d) | Pre-Event (-1d) | Event Day | Post-Event (+1d) | Post-Event (+3d) | Non-Event |")
    report.append(f"|--------|----------------|----------------|-----------|------------------|--------------------|-----------|")

    periods = {
        'Pre-3d': pre3_event_returns,
        'Pre-1d': pre_event_returns,
        'Event Day': event_day_returns,
        'Post+1d': post_event_returns,
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
            binom_p = stats.binomtest(n_up, n, p=0.5).pvalue if n > 0 else 1
            period_stats[period_name] = {'n': n, 'mean': mean_r, 'std': std_r, 'wr': wr, 't_p': t_pval, 'binom_p': binom_p}
        else:
            period_stats[period_name] = {'n': 0, 'mean': 0, 'std': 0, 'wr': 0, 't_p': 1, 'binom_p': 1}

    for stat_name in ['mean', 'std', 'wr']:
        row_name = {'mean': 'Avg Return %', 'std': 'Std Dev %', 'wr': 'Win Rate %'}[stat_name]
        vals = [f"{period_stats[p][stat_name]:.4f}" if period_stats[p]['n'] > 0 else "N/A" for p in periods.keys()]
        report.append(f"| {row_name} | {' | '.join(vals)} |")

    report.append("")
    report.append("### Significance Tests")
    report.append("")

    for period_name in ['Post+1d', 'Post+3d', 'Pre-1d']:
        event_data = periods[period_name]
        if len(event_data) > 0 and len(non_event_returns) > 0:
            t_stat, t_p = stats.ttest_ind(event_data, non_event_returns)
            report.append(f"- **{period_name} vs Non-Event**: t={t_stat:.4f}, p={t_p:.6f} ({'SIGNIFICANT' if t_p < 0.05 else 'Not significant'})")

    if len(pre_event_returns) > 0 and len(post_event_returns) > 0:
        t_stat, t_p = stats.ttest_ind(pre_event_returns, post_event_returns)
        report.append(f"- **Pre-Event vs Post-Event**: t={t_stat:.4f}, p={t_p:.6f} ({'SIGNIFICANT' if t_p < 0.05 else 'Not significant'})")

    volatility_ratio = np.std(event_day_returns) / np.std(non_event_returns) if len(event_day_returns) > 0 and len(non_event_returns) > 0 and np.std(non_event_returns) > 0 else 1
    report.append(f"- **Volatility ratio (event/non-event):** {volatility_ratio:.2f}x")

    # Check for exploitable edge
    for period_name in ['Post+1d', 'Post+3d']:
        ps = period_stats[period_name]
        if ps['n'] > 20:
            if abs(ps['wr'] - 50) > 8 and ps['binom_p'] < 0.05:
                all_event_results.append({
                    'Event': f'{event_name} {period_name}',
                    'N Events': ps['n'],
                    'WR%': round(ps['wr'], 2),
                    'Avg Ret%': round(ps['mean'], 4),
                    'Std%': round(ps['std'], 4),
                    'Binom P': round(ps['binom_p'], 6),
                    'Significant': 'YES'
                })
                report.append(f"\n**Potential edge detected**: {period_name} for {event_name} (WR={ps['wr']:.1f}%, p={ps['binom_p']:.4f})")

    report.append("")
    report.append("---")
    report.append("")

report.append("## Summary")
report.append("")
report.append("| Event Period | N Events | Avg Ret% | WR% | Binom P | Significant? |")
report.append("|-------------|----------|----------|-----|---------|--------------|")
if all_event_results:
    for r in all_event_results:
        report.append(f"| {r['Event']} | {r['N Events']} | {r['Avg Ret%']} | {r['WR%']} | {r['Binom P']} | {r['Significant']} |")
else:
    report.append("| No significant macro event edges found | | | | | |")

report.append("")
report.append("## Conclusion")
report.append("")
if all_event_results:
    report.append(f"- {len(all_event_results)} potential macro event edges identified")
    for r in all_event_results:
        report.append(f"  - {r['Event']}: WR={r['WR%']}%, p={r['Binom P']}")
    report.append("- Note: CPI and FOMC dates are approximate; precise economic calendar data would improve accuracy")
else:
    report.append("- No statistically significant macro event edges detected")
    report.append("- CPI and FOMC dates are approximate; precision would improve with dedicated economic calendar data")
    report.append("- NFP dates (first Friday of month) are more reliable")
    report.append("- Bitcoin-specific events (halving, ETF) limited by small sample size")

report.append("")
report.append("---")
report.append("*Generated by research/bitcoin/scripts/btc_004_macro_events.py*")

with open(REPORTS_DIR / 'BTC-004_Macro_Events.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nReport saved: {REPORTS_DIR / 'BTC-004_Macro_Events.md'}")
if all_event_results:
    for r in all_event_results:
        print(f"Edge: {r['Event']} - WR={r['WR%']}%, p={r['Binom P']}")
else:
    print("No significant macro event edges found")
print("BTC-004 COMPLETE")
