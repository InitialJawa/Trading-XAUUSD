"""RESEARCH-016: Data availability check for external drivers."""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def check_ticker(ticker, period='1mo'):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        info = {}
        try:
            info = t.info
        except:
            pass
        return {
            'available': len(hist) > 0,
            'rows': len(hist),
            'date_range': f"{hist.index[0].date()} to {hist.index[-1].date()}" if len(hist) > 0 else 'N/A',
            'info_keys': list(info.keys())[:5] if info else []
        }
    except Exception as e:
        return {'available': False, 'error': str(e)}

# ── 016A: Term Structure ──
print("=" * 60)
print("016A: TERM STRUCTURE DATA CHECK")
print("=" * 60)

# Check GC=F (front month continuous)
print("\n--- GC=F (Front Month Continuous) ---")
res = check_ticker('GC=F', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Check individual gold futures contracts for the current year
current_year = datetime.now().year
month_codes = {'Feb': 'G', 'Apr': 'J', 'Jun': 'M', 'Aug': 'Q', 'Oct': 'V', 'Dec': 'Z'}
# Check 2026 contracts
for mname, mcode in month_codes.items():
    ticker = f'GC{mcode}{str(current_year)[-2:]}.CMX'
    res = check_ticker(ticker, '3mo')
    print(f"\n  {ticker} ({mname} {current_year}):")
    print(f"    Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Also check 2025 contracts
for mname, mcode in month_codes.items():
    ticker = f'GC{mcode}25.CMX'
    res = check_ticker(ticker, '3mo')
    print(f"\n  {ticker} ({mname} 2025):")
    print(f"    Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# ── 016B: Real Yield Shocks ──
print("\n" + "=" * 60)
print("016B: REAL YIELD DATA CHECK")
print("=" * 60)

# Check US10Y (already have this)
print("\n--- ^TNX (US 10Y Treasury Yield) ---")
res = check_ticker('^TNX', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Check T10YIE (10Y Breakeven Inflation Rate) - try Yahoo Finance
print("\n--- T10YIE (10Y Breakeven) ---")
res = check_ticker('T10YIE', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Check ^TYX (30Y Treasury)
print("\n--- ^TYX (US 30Y Treasury Yield) ---")
res = check_ticker('^TYX', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Check TIPS ETF for real yield proxy
print("\n--- TIP (TIPS ETF) ---")
res = check_ticker('TIP', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Check STIP (Short-Term TIPS ETF)
print("\n--- STIP (Short-Term TIPS ETF) ---")
res = check_ticker('STIP', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Check 10Y TIPS yield directly (ticker: ^TYX?... Actually TIPS yield is different)
# Let's try ^10YTIPS or similar
print("\n--- DGS10 (FRED via Yahoo) ---")
res = check_ticker('DGS10', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# Check DFII10 (10-Year TIPS yield from FRED)
print("\n--- DFII10 (10Y TIPS Yield) ---")
res = check_ticker('DFII10', '1y')
print(f"  Available: {res['available']}, Rows: {res['rows']}, Range: {res['date_range']}")

# ── 016C: ETF Flows ──
print("\n" + "=" * 60)
print("016C: GLD ETF DATA CHECK")
print("=" * 60)

print("\n--- GLD (SPDR Gold Trust ETF) ---")
t = yf.Ticker('GLD')
hist = t.history(period='1y')
info = {}
try:
    info = t.info
except:
    pass
print(f"  Available: {len(hist) > 0}, Rows: {len(hist)}, Range: {hist.index[0].date()} to {hist.index[-1].date()}")
print(f"  Info keys available: {list(info.keys())[:20]}")

# Check specific GLD info fields
for field in ['sharesOutstanding', 'totalNetAssets', 'netAssets', 'aum', 'navPrice', 'holdings']:
    val = info.get(field, 'NOT FOUND')
    print(f"  info['{field}']: {val}")

# Check if GLD has balance sheet or financials for shares outstanding
try:
    bs = t.balance_sheet
    print(f"\n  Balance sheet columns: {list(bs.columns) if bs is not None else 'None'}")
except:
    print(f"\n  Balance sheet: Not available")

try:
    # Try to get historical shares outstanding via actions
    actions = t.actions
    print(f"  Actions: {list(actions.columns) if actions is not None else 'None'}")
    if actions is not None and len(actions) > 0:
        print(f"  Actions sample:\n{actions.tail()}")
except:
    print(f"  Actions: Not available")

print("\n" + "=" * 60)
print("DATA CHECK COMPLETE")
print("=" * 60)
