import json
import os
import time

from trading_bot.signals import rsi_signal, macd_signal, ma_signal, momentum_signal
from trading_bot.utils.config_loader import load_signal_weights
from trading_bot.utils.logger import setup_logger

logger = setup_logger("composite_signal")

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "signals"
)


def generate():
    weights = load_signal_weights()

    signal_generators = {
        "rsi": rsi_signal.generate,
        "macd": macd_signal.generate,
        "ma_crossover": ma_signal.generate,
        "momentum": momentum_signal.generate,
    }

    signals = {}
    total_score = 0
    total_weight = 0

    for name, generator in signal_generators.items():
        try:
            result = generator()
            if result and "signal" in result:
                signals[name] = result
                weight = weights.get(name, 0.20)
                total_score += result["signal"] * weight
                total_weight += weight
                logger.info(f"{name}: {result['signal']} (w={weight})")
            else:
                logger.warning(f"{name}: no signal generated")
        except Exception as e:
            logger.error(f"{name}: error -> {e}")

    if total_weight == 0:
        logger.error("No signals generated")
        return None

    final_score = round(total_score / total_weight, 2)

    if final_score >= 80:
        decision = "strong_buy"
    elif final_score >= 60:
        decision = "buy"
    elif final_score >= 45:
        decision = "hold"
    elif final_score >= 30:
        decision = "sell"
    else:
        decision = "strong_sell"

    composite = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "final_score": final_score,
        "decision": decision,
        "signals": signals,
        "weights": weights
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "latest_composite.json")
    with open(output_path, "w") as f:
        json.dump(composite, f, indent=4)

    logger.info(f"=== COMPOSITE SIGNAL: {final_score} -> {decision.upper()} ===")
    return composite


if __name__ == "__main__":
    generate()
