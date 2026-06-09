import json
import os
from datetime import datetime

import pandas as pd
import yfinance as yf

from trading_bot.utils.config_loader import load_settings
from trading_bot.utils.logger import setup_logger

logger = setup_logger("prices")

SYMBOL_YAHOO = "GC=F"
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def fetch_latest():
    settings = load_settings()
    symbol = settings.get("symbol", "XAUUSD")

    logger.info(f"Fetching {symbol} ({SYMBOL_YAHOO})...")

    stock = yf.Ticker(SYMBOL_YAHOO)
    hist = stock.history(period="5d")

    if hist.empty:
        logger.error("No data received from Yahoo Finance")
        return None

    latest = hist.iloc[-1]
    result = {
        "timestamp": datetime.now().isoformat(),
        "symbol": symbol,
        "close": float(latest["Close"]),
        "open": float(latest["Open"]),
        "high": float(latest["High"]),
        "low": float(latest["Low"]),
        "volume": int(latest["Volume"]),
        "source": "yahoo"
    }

    os.makedirs(os.path.join(DATA_DIR, "current"), exist_ok=True)
    output_path = os.path.join(DATA_DIR, "current", "latest_price.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)

    logger.info(f"{symbol} = {result['close']:.2f}")
    return result


def fetch_history(period="6mo", interval="1h"):
    logger.info(f"Fetching {SYMBOL_YAHOO} history ({period}, {interval})...")

    stock = yf.Ticker(SYMBOL_YAHOO)
    hist = stock.history(period=period, interval=interval)

    if hist.empty:
        logger.error("No historical data received")
        return None

    hist.index = hist.index.tz_localize(None)
    hist.reset_index(inplace=True)

    os.makedirs(os.path.join(DATA_DIR, "historical"), exist_ok=True)
    output_path = os.path.join(DATA_DIR, "historical", "XAUUSD.csv")
    hist.to_csv(output_path, index=False)

    logger.info(f"Saved {len(hist)} rows -> {output_path}")
    return hist


if __name__ == "__main__":
    fetch_latest()
