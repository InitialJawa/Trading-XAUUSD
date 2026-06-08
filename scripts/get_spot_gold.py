"""
Try to find XAU/USD spot data from various sources
"""
import pandas as pd
import requests
import json
import os

os.makedirs("data", exist_ok=True)

print("Attempting to get spot gold data from multiple sources...")
print()

# 1. FRED Gold Fixing Price
print("[1] FRED - Gold Fixing Price in London...")
series_ids = ['GOLDAMGBD228NLBM', 'GOLDPMGBD228NLBM']
for sid in series_ids:
    try:
        url = f"https://fred.stlouisfed.org/data/{sid}.txt"
        resp = requests.get(url)
        if resp.status_code == 200:
            lines = resp.text.strip().split("\n")
            # Skip header lines starting with #
            data_lines = [l for l in lines if not l.startswith("#") and l.strip()]
            if len(data_lines) > 1:
                # Parse the VALUE column header line and data
                header = data_lines[0].strip().split()
                records = []
                for line in data_lines[1:]:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        records.append((parts[0], float(parts[1])))
                df = pd.DataFrame(records, columns=['Date', 'Value'])
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.set_index('Date').sort_index()
                print(f"  {sid}: {len(df)} rows, {df.index.min().date()} to {df.index.max().date()}")
                print(f"  Last value: ${df['Value'].iloc[-1]:.2f}")
                df.to_csv(f"data/{sid}.csv")
                print(f"  Saved to data/{sid}.csv")
        else:
            print(f"  {sid}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"  {sid}: {e}")

# 2. Try alternative Yahoo Finance symbols for spot gold
print()
print("[2] Trying alternative Yahoo Finance symbols...")
alt_symbols = ['GLD', 'IAU', 'SGOL', 'PHYS', 'GTU']
for sym in alt_symbols:
    try:
        import yfinance as yf
        df = yf.download(sym, period="max", auto_adjust=True)
        if len(df) > 0:
            close = df['Close'].dropna()
            print(f"  {sym}: {len(close)} rows, {close.index.min().date()} to {close.index.max().date()}")
        else:
            print(f"  {sym}: no data")
    except Exception as e:
        print(f"  {sym}: {e}")

# 3. Try OANDA API
print()
print("[3] OANDA...")
try:
    url = "https://www.oanda.com/rates/api/v2/rates/spot.json?api_key=demo&base=XAU&quote=USD"
    # OANDA requires API key, this likely won't work
    print("  Requires API key - skipped")
except:
    pass

print()
print("=== SEARCH COMPLETE ===")
