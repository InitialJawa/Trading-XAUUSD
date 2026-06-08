"""
OIL-007: Signal Persistence & Holding Period Analysis
"""
import pandas as pd, numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path('data/oil'); REPORTS_DIR = Path('reports/oil')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(DATA_DIR / 'CLF_cleaned.csv', parse_dates=['Date'], index_col='Date')
close = df['Close'].dropna(); high = df['High']; low = df['Low']; vol = df['Volume']

holding_periods = {'1d': 1, '2d': 2, '3d': 3, '5d': 5, '10d': 10, '15d': 15, '20d': 20, '30d': 30, '60d': 60}
forward = {k: close.pct_change(v).shift(-v).dropna() for k, v in holding_periods.items()}
PPY = {'1d': 252, '2d': 126, '3d': 84, '5d': 50.4, '10d': 25.2, '15d': 16.8, '20d': 12.6, '30d': 8.4, '60d': 4.2}

# Technical models (same as BTC/Gold)
def model_A(idx):  # Trend Following
    s = pd.Series(0.0, index=idx)
    ema50 = close.rolling(50).mean(); ema200 = close.rolling(200).mean()
    adx = (high - low).rolling(14).mean()
    macd = close.ewm(12).mean() - close.ewm(26).mean()
    cond = (ema50 > ema200) & (adx > close.rolling(50).std()*0.5) & (macd > 0)
    s[cond] = 1.0; return s

def model_B(idx):  # Trend Pullback
    s = pd.Series(0.0, index=idx)
    ema50 = close.rolling(50).mean(); ema200 = close.rolling(200).mean()
    rsi14 = 100 - 100 / (1 + (close.diff().clip(lower=0).rolling(14).mean() / close.diff().clip(upper=0).abs().rolling(14).mean()))
    cond = (ema50 > ema200) & (rsi14 < 40) & (rsi14 > 20)
    s[cond] = 1.0; return s

def model_C(idx):  # Mean Reversion Extreme
    s = pd.Series(0.0, index=idx)
    rsi14 = 100 - 100 / (1 + (close.diff().clip(lower=0).rolling(14).mean() / close.diff().clip(upper=0).abs().rolling(14).mean()))
    s[rsi14 > 80] = -1.0; s[rsi14 < 20] = 1.0; return s

def model_D(idx):  # Volatility Expansion
    s = pd.Series(0.0, index=idx)
    atr14 = (high - low).rolling(14).mean(); atr50 = (high - low).rolling(50).mean()
    cond = (atr14 > 1.5 * atr50) & (close > close.shift(1))
    s[cond] = 1.0; return s

def model_E(idx):  # Breakout
    s = pd.Series(0.0, index=idx)
    h20 = high.rolling(20).max().shift(1); l20 = low.rolling(20).min().shift(1)
    s[close > h20] = 1.0; s[close < l20] = -1.0; return s

def model_F(idx):  # Consensus
    a = model_A(idx); b = model_B(idx); c = model_C(idx); d = model_D(idx); e = model_E(idx)
    s = pd.Series(0.0, index=idx)
    agree = ((a==1).astype(int) + (b==1).astype(int) + (c==1).astype(int) + (d==1).astype(int) + (e==1).astype(int))
    s[agree >= 4] = 1.0; s[agree <= -4] = -1.0; return s

models = {'A_TrendFollowing': model_A, 'B_TrendPullback': model_B, 'C_MeanReversion': model_C,
          'D_VolatilityExpansion': model_D, 'E_Breakout': model_E, 'F_Consensus': model_F}

report = []
report.append("# OIL-007: Signal Persistence & Holding Period")
report.append("")

def mc_test(actual, n_perm=1000):
    actual = actual.dropna()
    if len(actual) < 10: return 1.0
    actual_sharpe = actual.mean() / actual.std() * np.sqrt(252) if actual.std() > 0 else 0
    count = 0
    for _ in range(n_perm):
        perm = np.random.permutation(actual)
        s = perm.mean() / perm.std() * np.sqrt(252) if perm.std() > 0 else 0
        if s >= actual_sharpe: count += 1
    return count / n_perm

idx = close.index
all_data = {}
for mname, mfunc in models.items():
    sig = mfunc(idx)
    all_data[mname] = sig

report.append("| Model | Best Hold | Sharpe | PF | MC p | N | |")
report.append("|-------|-----------|--------|----|-------|---|-|")
for mname in ['A_TrendFollowing', 'B_TrendPullback', 'C_MeanReversion', 'D_VolatilityExpansion', 'E_Breakout', 'F_Consensus']:
    sig = all_data[mname]
    label = mname.replace('_', ' ')
    results = []
    for hp_name, hp_days in holding_periods.items():
        fwd = forward[hp_name]
        common = sig.dropna().index.intersection(fwd.index)
        aligned = fwd.loc[common] * np.sign(sig.loc[common])
        n = len(aligned.dropna())
        if n < 20: continue
        m = aligned.mean(); s = aligned.std()
        sh = m / s * np.sqrt(PPY[hp_name]) if s > 0 else 0
        pos = aligned[aligned>0].sum(); neg = abs(aligned[aligned<0].sum())
        pf = pos/neg if neg>0 else np.inf
        results.append((hp_name, sh, pf, n))
    
    if results:
        best = max(results, key=lambda x: x[1])
        mc_p = mc_test(forward[best[0]].loc[sig.dropna().index.intersection(forward[best[0]].index)] * np.sign(sig.loc[sig.dropna().index.intersection(forward[best[0]].index)]))
        pf_pass = "PASS" if best[2] > 1.30 else "FAIL"
        sr_pass = "PASS" if best[1] > 1.0 else "FAIL"
        mc_pass = "PASS" if mc_p < 0.05 else "FAIL"
        n_pass = "PASS" if best[3] > 300 else "FAIL"
        all_pass = "PASS" if pf_pass=="PASS" and sr_pass=="PASS" and mc_pass=="PASS" and n_pass=="PASS" else "FAIL"
        report.append(f"| {label} | {best[0]} | {best[1]:.4f} | {best[2]:.4f} | {mc_p:.4f} | {best[3]:,} | {all_pass} |")
        for hp, sh, pf, n in results:
            report.append(f"  | {hp} | Sharpe={sh:.4f} | PF={pf:.4f} | N={n} |")
report.append("")

report.append("---")
report.append("*Generated by research/oil/scripts/oil_007_signal_persistence.py*")
with open(REPORTS_DIR / 'OIL-007_Signal_Persistence.md', 'w') as f:
    f.write('\n'.join(report))
print("OIL-007 COMPLETE")
