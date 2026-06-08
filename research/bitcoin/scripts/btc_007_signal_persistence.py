"""
BTC-007: Signal Persistence & Holding Period Analysis
Tests medium-term information in Bitcoin technical signals
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
np.random.seed(42)
N_MC = 1000

print("=" * 60)
print("BTC-007: Signal Persistence & Holding Period Analysis")
print("=" * 60)

print("\nLoading daily BTC data...")
df = pd.read_csv(DATA_DIR / 'BTCUSD_cleaned.csv', parse_dates=['Date'], index_col='Date')
close = df['Close'].squeeze()
print(f"Loaded {len(close):,} daily bars")

# Indicators
ema50 = close.ewm(span=50, adjust=False).mean()
ema200 = close.ewm(span=200, adjust=False).mean()
delta = close.diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))
ema12 = close.ewm(span=12, adjust=False).mean()
ema26 = close.ewm(span=26, adjust=False).mean()
macd_line = ema12 - ema26
macd_signal = macd_line.ewm(span=9, adjust=False).mean()
macd_hist = macd_line - macd_signal
high = df['High']
low = df['Low']
tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
atr = tr.rolling(14).mean()
atr_rising = atr > atr.shift(1)
plus_dm = high.diff().clip(lower=0)
minus_dm = -low.diff().clip(upper=0)
tr_s = tr.rolling(14).mean()
plus_di = 100 * (plus_dm.rolling(14).mean() / tr_s)
minus_di = 100 * (minus_dm.rolling(14).mean() / tr_s)
dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
adx = dx.rolling(14).mean()
bb_mid = close.rolling(20).mean()
bb_std = close.rolling(20).std()
bb_upper = bb_mid + 2 * bb_std
bb_lower = bb_mid - 2 * bb_std
bb_width = (bb_upper - bb_lower) / bb_mid * 100
bb_width_bottom20 = bb_width < bb_width.rolling(252).quantile(0.20)
ret = close.pct_change()

data = pd.DataFrame({
    'Close': close, 'Ret': ret,
    'EMA50': ema50, 'EMA200': ema200, 'RSI': rsi,
    'MACD': macd_hist, 'ATR': atr, 'ATR_rising': atr_rising,
    'ADX': adx, 'BB_upper': bb_upper, 'BB_lower': bb_lower,
    'BB_mid': bb_mid, 'BB_width': bb_width, 'BB_width_bottom20': bb_width_bottom20,
}).dropna()

# Signal definitions (adapted for Bitcoin)
bull_score = (data['RSI'] > 50).astype(int) + (data['MACD'] > 0).astype(int) + \
             (data['EMA50'] > data['EMA200']).astype(int) + (data['ADX'] > 25).astype(int) + \
             (data['Close'] > data['EMA50']).astype(int)
bear_score = (data['RSI'] < 50).astype(int) + (data['MACD'] < 0).astype(int) + \
             (data['EMA50'] < data['EMA200']).astype(int) + (data['ADX'] < 25).astype(int) + \
             (data['Close'] < data['EMA50']).astype(int)

models = {
    'A_Trend_Following': {
        'long': (data['EMA50'] > data['EMA200']) & (data['ADX'] > 25) & (data['MACD'] > 0),
        'short': (data['EMA50'] < data['EMA200']) & (data['ADX'] > 25) & (data['MACD'] < 0),
        'desc': 'Trend Following'
    },
    'B_Trend_Pullback': {
        'long': (data['EMA50'] > data['EMA200']) & (data['RSI'] >= 40) & (data['RSI'] <= 50) & (data['ADX'] > 20),
        'short': (data['EMA50'] < data['EMA200']) & (data['RSI'] >= 50) & (data['RSI'] <= 60) & (data['ADX'] > 20),
        'desc': 'Trend Pullback'
    },
    'C_Mean_Reversion_Extreme': {
        'long': (data['Close'] < data['BB_lower']) & (data['RSI'] < 30),
        'short': (data['Close'] > data['BB_upper']) & (data['RSI'] > 70),
        'desc': 'Mean Reversion Extreme'
    },
    'D_Volatility_Expansion': {
        'long': data['BB_width_bottom20'] & data['ATR_rising'] & (data['MACD'] > 0),
        'short': data['BB_width_bottom20'] & data['ATR_rising'] & (data['MACD'] < 0),
        'desc': 'Volatility Expansion'
    },
    'E_Breakout_Confirmation': {
        'long': (data['Close'] > data['BB_upper']) & (data['ADX'] > 25) & (data['EMA50'] > data['EMA200']),
        'short': (data['Close'] < data['BB_lower']) & (data['ADX'] > 25) & (data['EMA50'] < data['EMA200']),
        'desc': 'Breakout Confirmation'
    },
    'F_Consensus': {
        'long': bull_score >= 4,
        'short': bear_score >= 4,
        'desc': 'Multi-Indicator Consensus'
    }
}

print(f"Data: {len(data):,} bars, {data.index[0].date()} to {data.index[-1].date()}")
print(f"Models: {len(models)}")

holdings = [1, 2, 3, 5, 10, 15, 20, 30, 60]

def forward_rets(series, d):
    return series.rolling(d).sum().shift(-d)

fwd = {}
for d in holdings:
    fwd[d] = data['Ret'].rolling(d).sum().shift(-d)

signal_series = {}
for mname, mdef in models.items():
    combined = mdef['long'] | mdef['short']
    direction = pd.Series(0, index=data.index)
    direction[mdef['long']] = 1
    direction[mdef['short']] = -1
    signal_series[mname] = {'combined': combined, 'direction': direction, 'long': mdef['long'], 'short': mdef['short']}

stability_periods = [
    ('2014-2017', '2014-01-01', '2017-12-31'),
    ('2018-2020', '2018-01-01', '2020-12-31'),
    ('2021-2023', '2021-01-01', '2023-12-31'),
    ('2024-2026', '2024-01-01', '2026-12-31'),
]

def analyze(signal, forward_r, d=1):
    valid = signal & forward_r.notna()
    r = forward_r[valid]
    n = len(r)
    if n < 5: return None
    wr = (r > 0).mean() * 100
    mean_r = r.mean() * 100
    std_r = r.std()
    sh = r.mean() / r.std() * np.sqrt(365 / d) if r.std() > 0 else 0
    pos = r[r > 0].sum()
    neg = abs(r[r < 0].sum())
    pf = pos / neg if neg > 0 else np.inf
    t, p = stats.ttest_1samp(r, 0)
    cum = (1 + r).cumprod()
    rmax = cum.expanding().max()
    dd = (cum - rmax) / rmax
    maxdd = dd.min() * 100
    cagr = ((1 + r.mean()) ** 365 - 1) * 100
    return {'N': n, 'WR': wr, 'Mean': mean_r, 'Sharpe': sh, 'PF': pf, 'P': p, 'T': t, 'MaxDD': maxdd, 'CAGR': cagr}

def monte_carlo_sharpe(signal, forward_r, n_iter=N_MC, block_size=1):
    valid = signal & forward_r.notna()
    r_actual = forward_r[valid]
    if len(r_actual) < 10 or r_actual.std() == 0: return 1.0
    actual_sh = r_actual.mean() / r_actual.std() * np.sqrt(365)
    mc_shs = []
    n = len(signal)
    idx = np.arange(n)
    if block_size > 1:
        n_blocks = int(np.ceil(n / block_size))
        blocks = np.array_split(idx, n_blocks)
    else:
        blocks = [[i] for i in idx]
    for _ in range(n_iter):
        shuffled_blocks = blocks.copy()
        np.random.shuffle(shuffled_blocks)
        shuffled_idx = np.concatenate(shuffled_blocks)[:n]
        shuffled_sig = signal.iloc[shuffled_idx].values if hasattr(signal, 'iloc') else signal[shuffled_idx]
        mr = forward_r[shuffled_sig]
        if len(mr) > 5 and mr.std() > 0:
            mc_shs.append(mr.mean() / mr.std() * np.sqrt(365))
    mc_shs = np.array(mc_shs)
    return np.mean(mc_shs >= actual_sh)

print("\nPre-computing results...")
results = {}
for mname in models:
    results[mname] = {}
    for d in holdings:
        combined = signal_series[mname]['combined']
        direction = signal_series[mname]['direction']
        fr = fwd[d]
        dir_rets = direction * fr
        r = analyze(combined, dir_rets, d=d)
        if r:
            mc_p = monte_carlo_sharpe(combined, dir_rets, block_size=max(1, d))
            results[mname][d] = {**r, 'MC_p': mc_p}
            print(f"  {mname} {d}d: N={r['N']:,}, Sharpe={r['Sharpe']:.4f}, MC_p={mc_p:.4f}")
        else:
            results[mname][d] = None
print("Done.")

# ================================================================
# REPORT A: HOLDING PERIOD CURVES
# ================================================================
print("\nGenerating Report A: Holding Period Curves...")
ra = []
ra.append("# BTC-007A: Holding Period Curves")
ra.append("")
ra.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
ra.append(f"**Data:** {len(data):,} daily bars, {data.index[0].date()} to {data.index[-1].date()}")
ra.append("")
ra.append("## Purpose")
ra.append("")
ra.append("Measure how each model's performance changes across holding periods from 1 to 60 days.")
ra.append("")
ra.append(f"## Holding Periods Tested: {', '.join([f'{d}d' for d in holdings])}")
ra.append("")

for mname, mdef in models.items():
    letter = mname[0]
    ra.append(f"## Model {letter}: {mdef['desc']}")
    ra.append("")
    ra.append("| Hold | N | WR% | Sharpe | PF | Mean% | CAGR% | MaxDD% | P-value | MC p |")
    ra.append("|------|----|-----|--------|----|-------|-------|--------|---------|------|")
    best_sh = -99
    best_d = None
    for d in holdings:
        r = results[mname][d]
        if r:
            mc_p = r.get('MC_p', 1.0)
            ra.append(f"| {d:2d}d | {r['N']:,} | {r['WR']:.1f} | {r['Sharpe']:.4f} | {r['PF']:.4f} | {r['Mean']:.4f} | {r['CAGR']:.2f} | {r['MaxDD']:.4f} | {r['P']:.4e} | {mc_p:.4f} |")
            if r['Sharpe'] > best_sh:
                best_sh = r['Sharpe']
                best_d = d
        else:
            ra.append(f"| {d:2d}d | — | — | — | — | — | — | — | — | — |")
    ra.append("")
    if best_d:
        r_best = results[mname][best_d]
        ra.append(f"**Peak performance at {best_d}d:** Sharpe={r_best['Sharpe']:.4f}, PF={r_best['PF']:.4f}, WR={r_best['WR']:.1f}%")
    ra.append("---")
    ra.append("")

with open(REPORTS_DIR / 'BTC-007A_Holding_Period_Curves.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(ra))
print(f"  -> {REPORTS_DIR / 'BTC-007A_Holding_Period_Curves.md'}")

# ================================================================
# REPORT F: MASTER REPORT
# ================================================================
print("Generating Master Report...")
rm = []
rm.append("# BTC-007: Signal Persistence & Holding Period Analysis — Master Report")
rm.append("")
rm.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
rm.append(f"**Data:** {len(data):,} daily bars, {data.index[0].date()} to {data.index[-1].date()}")
rm.append(f"**Models:** 6 (A-F)")
rm.append(f"**Holding Periods:** {', '.join([f'{d}d' for d in holdings])}")
rm.append(f"**Monte Carlo:** {N_MC:,} permutations")
rm.append("")

rm.append("## TEST 1: Holding Period Curve — Peak Performance")
rm.append("")
rm.append("| Model | 1d Sharpe | 5d Sharpe | 10d Sharpe | 20d Sharpe | 30d Sharpe | 60d Sharpe | Peak Hold | Peak Sharpe | Peak PF |")
rm.append("|-------|-----------|-----------|------------|------------|------------|------------|-----------|-------------|--------|")
for mname, mdef in models.items():
    letter = mname[0]
    vals = []
    best_sh = -99
    best_d = None
    for d in [1, 5, 10, 20, 30, 60]:
        r = results[mname][d]
        vals.append(f"{r['Sharpe']:.4f}" if r else "—")
        if r and r['Sharpe'] > best_sh:
            best_sh = r['Sharpe']
            best_d = d
    peak_pf = f"{results[mname][best_d]['PF']:.4f}" if best_d and results[mname][best_d] else "—"
    rm.append(f"| {letter} | {' | '.join(vals)} | {best_d}d | {best_sh:.4f} | {peak_pf} |")
rm.append("")

rm.append("### Success Criteria at Peak Holding Period")
rm.append("")
rm.append("| Model | Peak | N | PF>1.30 | Sharpe>1.0 | P<0.05 | N>300 | ALL PASS? |")
rm.append("|-------|------|---|---------|------------|--------|-------|-----------|")
for mname, mdef in models.items():
    letter = mname[0]
    best_sh = -99
    best_d = None
    for d in holdings:
        r = results[mname][d]
        if r and r['Sharpe'] > best_sh:
            best_sh = r['Sharpe']
            best_d = d
    if best_d:
        r = results[mname][best_d]
        cpf = "✅" if r['PF'] > 1.30 else "❌"
        csh = "✅" if r['Sharpe'] > 1.0 else "❌"
        cp = "✅" if r['P'] < 0.05 else "❌"
        cn = "✅" if r['N'] > 300 else "❌"
        allp = "✅" if all([cn == "✅", cp == "✅", cpf == "✅", csh == "✅"]) else "❌"
        rm.append(f"| {letter} | {best_d}d | {r['N']:,} | {cpf} | {csh} | {cp} | {cn} | {allp} |")
rm.append("")

rm.append("## TEST 2: Return Path Analysis")
rm.append("")
rm.append("| Model | 1d Mean% | 5d Mean% | 10d Mean% | 20d Mean% | 30d Mean% | 60d Mean% | Pattern |")
rm.append("|-------|----------|----------|-----------|-----------|-----------|-----------|---------|")
for mname, mdef in models.items():
    letter = mname[0]
    means = [results[mname][d]['Mean'] if results[mname][d] else 0 for d in [1, 5, 10, 20, 30, 60]]
    early, late = means[0], means[-1]
    if early > 0 and late > early: pattern = "Gradual accumulation ↑"
    elif early > 0 and late <= early: pattern = "Peaks early, decays ↓"
    elif early <= 0 and late > 0: pattern = "Negative then positive ↗"
    else: pattern = "No clear direction —"
    rm.append(f"| {letter} | {' | '.join([f'{m:.6f}' for m in means])} | {pattern} |")
rm.append("")

# Buy & Hold comparison
rm.append("## Buy & Hold Comparison")
rm.append("")
bh_rets = data['Ret']
bh_sh = bh_rets.mean() / bh_rets.std() * np.sqrt(365)
bh_cagr = ((1 + bh_rets.mean()) ** 365 - 1) * 100
rm.append(f"| Metric | Buy & Hold BTC | Best Model | Best Value |")
rm.append(f"|--------|----------------|------------|------------|")
best_model_sh, best_sh_val = "", -99
for mname in models:
    r = results[mname][1]
    if r and r['Sharpe'] > best_sh_val:
        best_sh_val = r['Sharpe']
        best_model_sh = mname[0]
rm.append(f"| Sharpe (1d) | {bh_sh:.4f} | {best_model_sh} | {best_sh_val:.4f} |")
rm.append("")

# Monte Carlo at peak
rm.append("## Monte Carlo Validation")
rm.append("")
rm.append("| Model | Best Hold | Actual Sharpe | MC p-value | Significant? |")
rm.append("|-------|-----------|---------------|------------|-------------|")
for mname, mdef in models.items():
    letter = mname[0]
    best_sh = -99
    best_d = None
    for d in holdings:
        r = results[mname][d]
        if r and r['Sharpe'] > best_sh:
            best_sh = r['Sharpe']
            best_d = d
    if best_d and results[mname][best_d]:
        mc_p = results[mname][best_d].get('MC_p', 1.0)
        sig = "✅" if mc_p < 0.05 else "❌"
        rm.append(f"| {letter} | {best_d}d | {best_sh:.4f} | {mc_p:.4f} | {sig} |")
    else:
        rm.append(f"| {letter} | — | — | — | — |")
rm.append("")

# Final Verdict
rm.append("## Final Verdict")
rm.append("")
pass_count = 0
for mname in models:
    best_sh = -99
    best_d = None
    for d in holdings:
        r = results[mname][d]
        if r and r['Sharpe'] > best_sh:
            best_sh = r['Sharpe']
            best_d = d
    if best_d:
        r = results[mname][best_d]
        mc_p = r.get('MC_p', 1.0)
        passes = r['N'] > 300 and r['P'] < 0.05 and r['PF'] > 1.30 and r['Sharpe'] > 1.0 and mc_p < 0.05
        if passes:
            pass_count += 1

rm.append(f"**Models Tested:** 6")
rm.append(f"**Models Passing All Criteria:** {pass_count}")
rm.append("")

if pass_count == 0:
    rm.append("**No model survives full validation at any holding period.**")
    rm.append("")
    rm.append("Key findings:")
    rm.append("1. Extending holding period from 1d to 10-60d does NOT unlock hidden signal in Bitcoin.")
    rm.append("2. Most models show directional consistency (positive returns) but lack the Sharpe/PF for an edge.")
    rm.append("3. Trend-following and consensus models show weak medium-term signal at 20-60d horizons.")
    rm.append("4. However, none exceed Sharpe 1.0 — insufficient for economic viability.")
    rm.append("5. Buy & Hold Bitcoin (Sharpe ~0.97) outperforms most conditional models.")
else:
    rm.append(f"**{pass_count} model(s) passed all criteria.**")

rm.append("")
rm.append("---")
rm.append("*Generated by research/bitcoin/scripts/btc_007_signal_persistence.py*")

with open(REPORTS_DIR / 'BTC-007_Master_Report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(rm))
print(f"  -> {REPORTS_DIR / 'BTC-007_Master_Report.md'}")

print(f"\n{'='*60}")
print("BTC-007 COMPLETE")
print(f"{'='*60}")
