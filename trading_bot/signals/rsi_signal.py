import json
import os
import numpy as np

from trading_bot.utils.logger import setup_logger

logger = setup_logger("rsi_signal")

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def generate():
    indicators_path = os.path.join(DATA_DIR, "current", "latest_indicators.json")
    if not os.path.exists(indicators_path):
        logger.error("No indicators data found. Run collectors/indicators.py first.")
        return None

    with open(indicators_path) as f:
        data = json.load(f)

    rsi = data.get("rsi")
    if rsi is None or (isinstance(rsi, float) and np.isnan(rsi)):
        logger.warning("RSI not available")
        return {"signal": 50, "value": None, "type": "neutral"}

    if rsi <= 30:
        score = 100
        signal_type = "strong_buy"
    elif rsi <= 40:
        score = 80
        signal_type = "buy"
    elif rsi <= 45:
        score = 65
        signal_type = "weak_buy"
    elif rsi <= 55:
        score = 50
        signal_type = "neutral"
    elif rsi <= 60:
        score = 35
        signal_type = "weak_sell"
    elif rsi <= 70:
        score = 20
        signal_type = "sell"
    else:
        score = 0
        signal_type = "strong_sell"

    result = {
        "signal": score,
        "rsi": round(rsi, 2),
        "type": signal_type
    }

    logger.info(f"RSI = {rsi:.2f} -> Signal: {score} ({signal_type})")
    return result


if __name__ == "__main__":
    generate()
