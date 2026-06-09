import json
import os
from datetime import datetime

from trading_bot.utils.logger import setup_logger

logger = setup_logger("archive")

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def archive_current_state():
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "price": None,
        "composite_signal": None,
        "indicators": None,
        "positions": None,
    }

    latest_price_path = os.path.join(DATA_DIR, "current", "latest_price.json")
    if os.path.exists(latest_price_path):
        with open(latest_price_path) as f:
            snapshot["price"] = json.load(f)

    composite_path = os.path.join(DATA_DIR, "signals", "latest_composite.json")
    if os.path.exists(composite_path):
        with open(composite_path) as f:
            snapshot["composite_signal"] = json.load(f)

    indicators_path = os.path.join(DATA_DIR, "current", "latest_indicators.json")
    if os.path.exists(indicators_path):
        with open(indicators_path) as f:
            ind = json.load(f)
            snapshot["indicators"] = {
                "rsi": ind.get("rsi"),
                "atr": ind.get("atr"),
                "macd_histogram": ind.get("macd_histogram"),
                "bb_position": ind.get("bb_position"),
            }

    archive_dir = os.path.join(DATA_DIR, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m")
    filename = f"{date_str}.json"
    filepath = os.path.join(archive_dir, filename)

    if os.path.exists(filepath):
        with open(filepath) as f:
            archive = json.load(f)
    else:
        archive = []

    archive.append(snapshot)
    with open(filepath, "w") as f:
        json.dump(archive, f, indent=4)

    logger.info(f"Archived snapshot -> {filepath}")
    return snapshot


if __name__ == "__main__":
    archive_current_state()
