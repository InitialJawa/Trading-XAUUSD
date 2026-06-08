"""Check availability of funding rate data from various exchanges."""
import ccxt
import pandas as pd
from datetime import datetime

# Try Binance futures funding rate history
try:
    binance = ccxt.binance({"options": {"defaultType": "future"}})
    fr = binance.fetchFundingRateHistory(symbol="BTC/USDT", limit=100)
    if fr:
        print("Binance: Got %d funding rate records" % len(fr))
        print("  Latest: %s rate=%s" % (fr[-1]["datetime"], fr[-1]["fundingRate"]))
        print("  Earliest: %s rate=%s" % (fr[0]["datetime"], fr[0]["fundingRate"]))
except Exception as e:
    print("Binance error: %s" % e)

# Try Gate.io
try:
    gate = ccxt.gate()
    fr = gate.fetchFundingRateHistory(symbol="BTC/USDT", limit=100)
    if fr:
        print("Gate: Got %d funding rate records" % len(fr))
        print("  Latest: %s rate=%s" % (fr[-1]["datetime"], fr[-1]["fundingRate"]))
        print("  Earliest: %s rate=%s" % (fr[0]["datetime"], fr[0]["fundingRate"]))
except Exception as e:
    print("Gate error: %s" % e)

# Try fetching more history from Binance
try:
    binance = ccxt.binance({"options": {"defaultType": "future"}})
    since = int(datetime(2024, 1, 1).timestamp() * 1000)
    fr = binance.fetchFundingRateHistory(symbol="BTC/USDT", since=since, limit=1000)
    if fr:
        print("Binance (since 2024): Got %d funding rate records" % len(fr))
        df = pd.DataFrame(fr)
        print("  Date range: %s to %s" % (df["datetime"].min(), df["datetime"].max()))
        print("  Rate range: %.6f to %.6f" % (df["fundingRate"].min(), df["fundingRate"].max()))
except Exception as e:
    print("Binance (since) error: %s" % e)

# Try Bybit
try:
    bybit = ccxt.bybit()
    fr = bybit.fetchFundingRateHistory(symbol="BTC/USDT", limit=100)
    if fr:
        print("Bybit: Got %d funding rate records" % len(fr))
        print("  Latest: %s rate=%s" % (fr[-1]["datetime"], fr[-1]["fundingRate"]))
        print("  Earliest: %s rate=%s" % (fr[0]["datetime"], fr[0]["fundingRate"]))
except Exception as e:
    print("Bybit error: %s" % e)

# Try OKX
try:
    okx = ccxt.okx()
    fr = okx.fetchFundingRateHistory(symbol="BTC/USDT", limit=100)
    if fr:
        print("OKX: Got %d funding rate records" % len(fr))
        print("  Latest: %s rate=%s" % (fr[-1]["datetime"], fr[-1]["fundingRate"]))
        print("  Earliest: %s rate=%s" % (fr[0]["datetime"], fr[0]["fundingRate"]))
except Exception as e:
    print("OKX error: %s" % e)
