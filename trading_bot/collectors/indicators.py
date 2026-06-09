import json
import os

import numpy as np
import pandas as pd

from trading_bot.utils.logger import setup_logger

logger = setup_logger("indicators")

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    for i in range(period, len(avg_gain)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(series, period=20, std_dev=2):
    middle = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return upper, middle, lower


def calculate_atr(df, period=14):
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr


def calculate_all(df):
    close = df["close"]
    high_low = df["high"] - df["low"]

    df["rsi"] = calculate_rsi(close, 14)

    macd_line, signal_line, histogram = calculate_macd(close)
    df["macd_line"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_histogram"] = histogram

    df["ema_9"] = close.ewm(span=9, adjust=False).mean()
    df["ema_21"] = close.ewm(span=21, adjust=False).mean()
    df["sma_50"] = close.rolling(window=50).mean()
    df["sma_200"] = close.rolling(window=200).mean()

    bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(close)
    df["bb_upper"] = bb_upper
    df["bb_middle"] = bb_middle
    df["bb_lower"] = bb_lower
    df["bb_width"] = (bb_upper - bb_lower) / bb_middle
    df["bb_position"] = (close - bb_lower) / (bb_upper - bb_lower)

    df["atr"] = calculate_atr(df, 14)

    df["volume_sma"] = df["volume"].rolling(window=20).mean()
    df["volume_ratio"] = df["volume"] / df["volume_sma"]

    return df


def process():
    csv_path = os.path.join(DATA_DIR, "historical", "XAUUSD.csv")
    if not os.path.exists(csv_path):
        logger.error(f"Historical data not found: {csv_path}")
        return None

    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]

    date_cols = [c for c in ["datetime", "date", "timestamp"] if c in df.columns]
    if date_cols:
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
        df.set_index(date_cols[0], inplace=True)

    df = calculate_all(df)

    output_path = os.path.join(DATA_DIR, "indicators", "XAUUSD_indicators.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    logger.info(f"Indicators saved -> {output_path}")

    latest = df.iloc[-1].to_dict()
    latest = {k: float(v) if isinstance(v, (np.integer, np.floating)) else v
              for k, v in latest.items()}

    json_path = os.path.join(DATA_DIR, "current", "latest_indicators.json")
    with open(json_path, "w") as f:
        json.dump(latest, f, indent=4, default=str)

    logger.info(f"Latest indicators -> {json_path}")
    return df


if __name__ == "__main__":
    process()
