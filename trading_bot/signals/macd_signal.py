import json
import os
import numpy as np

from trading_bot.utils.logger import setup_logger

logger = setup_logger("macd_signal")

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def generate():
    indicators_path = os.path.join(DATA_DIR, "current", "latest_indicators.json")
    if not os.path.exists(indicators_path):
        logger.error("No indicators data found.")
        return None

    with open(indicators_path) as f:
        data = json.load(f)

    macd_line = data.get("macd_line")
    signal_line = data.get("macd_signal")
    histogram = data.get("macd_histogram")

    if any(v is None or (isinstance(v, float) and np.isnan(v))
           for v in [macd_line, signal_line, histogram]):
        logger.warning("MACD data not available")
        return {"signal": 50, "value": None, "type": "neutral"}

    histogram = float(histogram)
    crossover = macd_line - signal_line

    if crossover > 0 and histogram > 0:
        score = 80
        signal_type = "buy"
        if histogram > crossover * 0.5:
            score = 90
            signal_type = "strong_buy"
    elif crossover > 0 and histogram < 0:
        score = 60
        signal_type = "weak_buy"
    elif crossover < 0 and histogram < 0:
        score = 20
        signal_type = "sell"
        if abs(histogram) > abs(crossover) * 0.5:
            score = 10
            signal_type = "strong_sell"
    else:
        score = 40
        signal_type = "weak_sell"

    result = {
        "signal": score,
        "macd_histogram": round(histogram, 2),
        "macd_crossover": round(float(crossover), 2),
        "type": signal_type
    }

    logger.info(f"MACD -> Signal: {score} ({signal_type})")
    return result


if __name__ == "__main__":
    generate()
