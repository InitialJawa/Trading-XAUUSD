"""Quick data availability check v2"""
import yfinance as yf

# Check yield tickers
tickers = ['^TNX', '^TYX', '^IRX', '^FVX', 'TIP', 'GLD', 'GC=F', 'IEF', 'TLT', 'SHY']
for t in tickers:
    try:
        tk = yf.Ticker(t)
        h = tk.history(period='max')
        if len(h) > 0:
            print(f'{t}: {len(h)} rows, {h.index[0].date()} to {h.index[-1].date()}')
        else:
            print(f'{t}: No data')
    except Exception as e:
        print(f'{t}: ERROR {e}')

print()

# Check GLD info
gld = yf.Ticker('GLD')
info = gld.info
for k in ['sharesOutstanding', 'netAssets', 'navPrice', 'category', 'fundFamily', 'yield', 'ytdReturn', 'beta3Year', 'fundInceptionDate']:
    print(f'GLD info[{k}] = {info.get(str(k), "N/A")}')

# Try to get GC individual contract data for recent history
# Yahoo Finance might have them with different suffixes
for year in range(2022, 2027):
    for mcode in ['G', 'J', 'M', 'Q', 'V', 'Z']:
        t = f'GC{mcode}{str(year)[-2:]}.CMX'
        try:
            tk = yf.Ticker(t)
            h = tk.history(period='1y')
            if len(h) > 5:
                print(f'{t}: {len(h)} rows, {h.index[0].date()} to {h.index[-1].date()}')
        except:
            pass

# Try GLD holdings from different source
print("\n--- Trying to get GLD shares outstanding historically ---")
try:
    gld_hist = yf.download('GLD', period='5y', actions=True)
    print(f'GLD columns: {list(gld_hist.columns)}')
    print(f'GLD head:\n{gld_hist.head()}')
except Exception as e:
    print(f'Error: {e}')
