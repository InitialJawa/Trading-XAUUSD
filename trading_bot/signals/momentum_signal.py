import json
import os
import numpy as np

import pandas as pd

from trading_bot.utils.logger import setup_logger

logger = setup_logger("momentum_signal")

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def generate():
    indicators_path = os.path.join(DATA_DIR, "indicators", "XAUUSD_indicators.csv")
    if not os.path.exists(indicators_path):
        logger.error("No indicators CSV found.")
        return None

    df = pd.read_csv(indicators_path)

    if "close" not in df.columns:
        logger.error("No close column in indicators data")
        return None

    close = df["close"]
    if len(close) < 20:
        return {"signal": 50, "type": "neutral"}

    returns_1d = close.pct_change(1).iloc[-1] if len(close) >= 2 else 0
    returns_5d = close.pct_change(5).iloc[-1] if len(close) >= 6 else 0
    returns_10d = close.pct_change(10).iloc[-1] if len(close) >= 11 else 0
    returns_20d = close.pct_change(20).iloc[-1] if len(close) >= 21 else 0

    momentum_1d = max(0, min(100, (returns_1d + 0.05) / 0.10 * 100)) if not np.isnan(returns_1d) else 50
    momentum_5d = max(0, min(100, (returns_5d + 0.10) / 0.20 * 100)) if not np.isnan(returns_5d) else 50
    momentum_10d = max(0, min(100, (returns_10d + 0.15) / 0.30 * 100)) if not np.isnan(returns_10d) else 50
    momentum_20d = max(0, min(100, (returns_20d + 0.20) / 0.40 * 100)) if not np.isnan(returns_20d) else 50

    score = (
        momentum_1d * 0.15 +
        momentum_5d * 0.25 +
        momentum_10d * 0.30 +
        momentum_20d * 0.30
    )

    score = max(0, min(100, score))

    if score >= 65:
        signal_type = "buy"
    elif score <= 35:
        signal_type = "sell"
    else:
        signal_type = "neutral"

    result = {
        "signal": round(score, 2),
        "return_1d": round(float(returns_1d) * 100, 2) if not np.isnan(returns_1d) else 0,
        "return_5d": round(float(returns_5d) * 100, 2) if not np.isnan(returns_5d) else 0,
        "return_20d": round(float(returns_20d) * 100, 2) if not np.isnan(returns_20d) else 0,
        "type": signal_type
    }

    logger.info(f"Momentum -> Signal: {score:.2f} ({signal_type})")
    return result


if __name__ == "__main__":
    generate()
