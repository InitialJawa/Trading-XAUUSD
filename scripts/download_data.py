"""
XAU/USD Edge Discovery Framework
Phase 1: Data Download & Audit
Objective: Download maximum available XAU/USD data, audit quality
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

os.makedirs("reports", exist_ok=True)
os.makedirs("data", exist_ok=True)

print("=" * 60)
print("DOWNLOADING XAU/USD DATA")
print("=" * 60)

# Download from Yahoo Finance (GC=F)
print("\n[1] Downloading GC=F from Yahoo Finance...")
gold = yf.download("GC=F", period="max", auto_adjust=True)
gold.columns = ['Open','High','Low','Close','Volume']
gold.index.name = 'Date'
print(f"    Rows downloaded: {len(gold)}")
print(f"    Date range: {gold.index.min()} to {gold.index.max()}")
gold.to_csv("data/XAUUSD_yahoo_raw.csv")
print("    Saved to data/XAUUSD_yahoo_raw.csv")

# Also try to get additional data via Stooq
print("\n[2] Attempting Stooq download...")
try:
    stooq = pd.read_csv(
        "https://stooq.com/q/d/l/?s=xauusd&i=d",
        parse_dates=['Date'],
        index_col='Date'
    )
    stooq.columns = ['Open','High','Low','Close','Volume']
    stooq.to_csv("data/XAUUSD_stooq_raw.csv")
    print(f"    Rows downloaded: {len(stooq)}")
    print(f"    Date range: {stooq.index.min()} to {stooq.index.max()}")
except Exception as e:
    print(f"    Stooq download failed: {e}")
    stooq = None

# Download related instruments for Phase 9 (Driver Analysis)
print("\n[3] Downloading related instruments...")
symbols = {
    'DX-Y.NYB': 'DXY',
    '^TNX': 'US10Y',
    '^GSPC': 'SP500',
    '^VIX': 'VIX',
    'TLT': 'TLT'
}
related = {}
for sym, name in symbols.items():
    try:
        df = yf.download(sym, period="max", auto_adjust=True)
        df.columns = ['Open','High','Low','Close','Volume']
        related[name] = df['Close'].copy()
        print(f"    {name} ({sym}): {len(df)} rows, {df.index.min()} to {df.index.max()}")
    except Exception as e:
        print(f"    {name} ({sym}) failed: {e}")

if related:
    related_df = pd.DataFrame(related)
    related_df.to_csv("data/related_instruments.csv")
    print("    Saved to data/related_instruments.csv")

print("\n=== DOWNLOAD COMPLETE ===")
