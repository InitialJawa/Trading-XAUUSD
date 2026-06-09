import json
import os
import numpy as np

from trading_bot.utils.logger import setup_logger

logger = setup_logger("ma_signal")

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

    close = data.get("close")
    ema_9 = data.get("ema_9")
    ema_21 = data.get("ema_21")
    sma_50 = data.get("sma_50")
    sma_200 = data.get("sma_200")

    if any(v is None or (isinstance(v, float) and np.isnan(v))
           for v in [close, ema_9, ema_21, sma_50]):
        return {"signal": 50, "type": "neutral"}

    signals = []

    if ema_9 > ema_21:
        signals.append(70)
    else:
        signals.append(30)

    if close > sma_50:
        signals.append(65)
    else:
        signals.append(35)

    if sma_50 > sma_200 if not (np.isnan(sma_200) if isinstance(sma_200, float) else False) else True:
        pass
    elif isinstance(sma_200, float) and not np.isnan(sma_200):
        if sma_50 > sma_200:
            signals.append(70)
        else:
            signals.append(30)

    score = sum(signals) / len(signals) if signals else 50

    if score >= 65:
        signal_type = "buy"
    elif score <= 35:
        signal_type = "sell"
    else:
        signal_type = "neutral"

    result = {
        "signal": round(score, 2),
        "ema_9": round(float(ema_9), 2),
        "ema_21": round(float(ema_21), 2),
        "sma_50": round(float(sma_50), 2),
        "type": signal_type
    }

    logger.info(f"MA Crossover -> Signal: {score:.2f} ({signal_type})")
    return result


if __name__ == "__main__":
    generate()
