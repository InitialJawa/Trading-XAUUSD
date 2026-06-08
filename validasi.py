import yfinance as yf
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("Downloading data...")
raw = yf.download("GC=F", start="2010-01-01", end="2026-01-01", interval="1d")
raw.columns = raw.columns.get_level_values(0)
df = raw[['Open','High','Low','Close']].copy().dropna()

# =====================
# HELPER FUNCTIONS
# =====================
def hitung_adx(df, period=14):
    high, low, close = df['High'], df['Low'], df['Close']
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    dm_pos = (high - high.shift()).clip(lower=0)
    dm_neg = (low.shift() - low).clip(lower=0)
    dm_pos[dm_pos < dm_neg] = 0
    dm_neg[dm_neg < dm_pos] = 0
    di_pos = 100 * dm_pos.rolling(period).mean() / atr
    di_neg = 100 * dm_neg.rolling(period).mean() / atr
    dx     = 100 * (di_pos - di_neg).abs() / (di_pos + di_neg)
    return dx.rolling(period).mean()

def hitung_rsi(close, period=14):
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss
    return 100 - (100 / (1 + rs))

def validasi(label, events_df, harga_10_col='Harga10', close_col='Close', event_col='Event'):
    ev = events_df.dropna(subset=[harga_10_col])
    ev = ev[ev[event_col] != '']
    if len(ev) < 30:
        print(f"\n{'='*45}")
        print(f"  {label}")
        print(f"  Sample terlalu kecil ({len(ev)}) — skip")
        return

    balik = np.where(
        ev[event_col] == 'OVERSOLD',   ev[harga_10_col] > ev[close_col],
        np.where(
        ev[event_col] == 'OVERBOUGHT', ev[harga_10_col] < ev[close_col],
        np.nan))
    balik = pd.Series(balik, dtype=float).dropna()

    total    = len(balik)
    total_ya = int(balik.sum())
    wr       = total_ya / total
    pval     = stats.binomtest(total_ya, total, 0.5, alternative='greater').pvalue

    print(f"\n{'='*45}")
    print(f"  {label}")
    print(f"  Total event : {total}")
    print(f"  Win Rate    : {wr:.1%}")
    print(f"  P-Value     : {pval:.4f}")
    print(f"  Signifikan  : {'YA ✅' if pval < 0.05 else 'TIDAK ❌'}")
    print(f"  {'>>> EDGE DITEMUKAN! <<<' if pval < 0.05 and wr > 0.55 else ''}")

# =====================
# INDIKATOR DASAR
# =====================
df['ADX'] = hitung_adx(df)
df['RSI'] = hitung_rsi(df['Close'])
df['EMA9']  = df['Close'].ewm(span=9).mean()
df['EMA21'] = df['Close'].ewm(span=21).mean()
df['EMA50'] = df['Close'].ewm(span=50).mean()
df['Harga10'] = df['Close'].shift(-10)

print("Indikator siap. Mulai pengujian...\n")

# =====================
# BLOK A — Z-SCORE BERBAGAI PARAMETER
# =====================
print("\n" + "="*45)
print("  BLOK A: Z-SCORE BERBAGAI PARAMETER")
print("="*45)

for window in [10, 20, 30]:
    for threshold in [1.5, 2.0, 2.5]:
        df['Mean']   = df['Close'].rolling(window).mean()
        df['Std']    = df['Close'].rolling(window).std()
        df['ZScore'] = (df['Close'] - df['Mean']) / df['Std']
        df['Event']  = np.where(df['ZScore'] >  threshold, 'OVERBOUGHT',
                       np.where(df['ZScore'] < -threshold, 'OVERSOLD', ''))
        label = f"Z-Score window={window} threshold=±{threshold}"
        validasi(label, df)

# =====================
# BLOK B — Z-SCORE + ADX FILTER
# =====================
print("\n" + "="*45)
print("  BLOK B: Z-SCORE + ADX FILTER")
print("="*45)

for adx_thresh in [20, 25, 30]:
    df['Mean']   = df['Close'].rolling(20).mean()
    df['Std']    = df['Close'].rolling(20).std()
    df['ZScore'] = (df['Close'] - df['Mean']) / df['Std']
    df['Event']  = np.where(
        (df['ZScore'] >  2) & (df['ADX'] < adx_thresh), 'OVERBOUGHT',
        np.where(
        (df['ZScore'] < -2) & (df['ADX'] < adx_thresh), 'OVERSOLD', ''))
    label = f"Z-Score ±2 + ADX < {adx_thresh}"
    validasi(label, df)

# =====================
# BLOK C — Z-SCORE + RSI KONFIRMASI
# =====================
print("\n" + "="*45)
print("  BLOK C: Z-SCORE + RSI KONFIRMASI")
print("="*45)

df['Mean']   = df['Close'].rolling(20).mean()
df['Std']    = df['Close'].rolling(20).std()
df['ZScore'] = (df['Close'] - df['Mean']) / df['Std']

for rsi_os, rsi_ob in [(40, 60), (35, 65), (30, 70)]:
    df['Event'] = np.where(
        (df['ZScore'] < -2) & (df['RSI'] < rsi_os), 'OVERSOLD',
        np.where(
        (df['ZScore'] >  2) & (df['RSI'] > rsi_ob), 'OVERBOUGHT', ''))
    label = f"Z-Score ±2 + RSI (OS<{rsi_os}, OB>{rsi_ob})"
    validasi(label, df)

# =====================
# BLOK D — EMA CROSSOVER (TREND FOLLOWING)
# =====================
print("\n" + "="*45)
print("  BLOK D: EMA CROSSOVER TREND FOLLOWING")
print("="*45)

# Sinyal EMA crossover
df['CrossUp']   = (df['EMA9'] > df['EMA21']) & (df['EMA9'].shift() <= df['EMA21'].shift())
df['CrossDown'] = (df['EMA9'] < df['EMA21']) & (df['EMA9'].shift() >= df['EMA21'].shift())

df['Event'] = np.where(df['CrossUp'],   'BUY',
              np.where(df['CrossDown'], 'SELL', ''))

# Untuk EMA: BUY berhasil kalau harga naik, SELL berhasil kalau harga turun
ev = df[df['Event'] != ''].dropna(subset=['Harga10'])
balik = np.where(
    ev['Event'] == 'BUY',  ev['Harga10'] > ev['Close'],
    np.where(
    ev['Event'] == 'SELL', ev['Harga10'] < ev['Close'],
    np.nan))
balik = pd.Series(balik, dtype=float).dropna()
total = len(balik)
total_ya = int(balik.sum())
wr = total_ya / total
pval = stats.binomtest(total_ya, total, 0.5, alternative='greater').pvalue
print(f"\n  EMA9 x EMA21 Crossover")
print(f"  Total event : {total}")
print(f"  Win Rate    : {wr:.1%}")
print(f"  P-Value     : {pval:.4f}")
print(f"  Signifikan  : {'YA ✅' if pval < 0.05 else 'TIDAK ❌'}")

# EMA Crossover + ADX > 25 (konfirmasi tren kuat)
df['Event'] = np.where(
    df['CrossUp']   & (df['ADX'] > 25), 'BUY',
    np.where(
    df['CrossDown'] & (df['ADX'] > 25), 'SELL', ''))
ev = df[df['Event'] != ''].dropna(subset=['Harga10'])
balik = np.where(
    ev['Event'] == 'BUY',  ev['Harga10'] > ev['Close'],
    np.where(
    ev['Event'] == 'SELL', ev['Harga10'] < ev['Close'],
    np.nan))
balik = pd.Series(balik, dtype=float).dropna()
total = len(balik)
total_ya = int(balik.sum())
wr = total_ya / total
pval = stats.binomtest(total_ya, total, 0.5, alternative='greater').pvalue
print(f"\n  EMA9 x EMA21 + ADX > 25")
print(f"  Total event : {total}")
print(f"  Win Rate    : {wr:.1%}")
print(f"  P-Value     : {pval:.4f}")
print(f"  Signifikan  : {'YA ✅' if pval < 0.05 else 'TIDAK ❌'}")
print(f"  {'>>> EDGE DITEMUKAN! <<<' if pval < 0.05 and wr > 0.55 else ''}")

print("\n\nSelesai. Cari baris yang ada EDGE DITEMUKAN!")