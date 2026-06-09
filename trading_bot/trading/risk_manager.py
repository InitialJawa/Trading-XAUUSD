import json
import os
import math

import pandas as pd

from trading_bot.utils.config_loader import load_settings
from trading_bot.utils.logger import setup_logger

logger = setup_logger("risk_manager")

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def load_latest_atr():
    indicators_path = os.path.join(DATA_DIR, "current", "latest_indicators.json")
    if not os.path.exists(indicators_path):
        return None
    with open(indicators_path) as f:
        data = json.load(f)
    return data.get("atr")


def calculate_lot_size(balance, risk_percent, sl_points, tick_value=0.01):
    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (sl_points * tick_value)
    lot_size = max(0.01, round(lot_size * 100) / 100)
    return lot_size


def calculate_sl_tp(entry_price, atr, direction, sl_mult=2.0, tp_mult=3.0):
    if direction == "buy":
        sl = entry_price - (atr * sl_mult)
        tp = entry_price + (atr * tp_mult)
    else:
        sl = entry_price + (atr * sl_mult)
        tp = entry_price - (atr * tp_mult)
    return round(sl, 2), round(tp, 2)


def get_trade_params(decision, price=None):
    settings = load_settings()
    risk = settings.get("risk", {})

    max_risk = risk.get("max_risk_per_trade", 1.0)
    max_spread = risk.get("max_spread", 30)
    atr_mult_sl = risk.get("atr_multiplier_sl", 2.0)
    atr_mult_tp = risk.get("atr_multiplier_tp", 3.0)

    if decision in ("strong_buy", "buy"):
        direction = "buy"
    elif decision in ("strong_sell", "sell"):
        direction = "sell"
    else:
        return {"action": "hold", "reason": f"Decision: {decision}"}

    if price is None:
        return {"action": "hold", "reason": "No price data"}

    atr = load_latest_atr()
    if atr is None or (isinstance(atr, float) and math.isnan(atr)):
        logger.warning("ATR not available; using fallback SL/TP")
        atr = price * 0.01

    sl, tp = calculate_sl_tp(price, atr, direction, atr_mult_sl, atr_mult_tp)

    try:
        import MetaTrader5 as mt5
        from trading_bot.trading.mt5_connector import get_account_info

        account = get_account_info()
        if account and account.get("balance"):
            balance = account["balance"]
            sl_points = abs(price - sl) / 0.01
            lot = calculate_lot_size(balance, max_risk, sl_points)
            lot = max(0.01, lot)
        else:
            lot = 0.01
    except ImportError:
        lot = 0.01

    spread = abs(price - sl) * 2
    if spread > max_spread * 0.01:
        logger.warning(f"Spread too high: {spread:.2f} > {max_spread * 0.01:.2f}")
        return {"action": "hold", "reason": f"Spread too high: {spread:.2f}"}

    return {
        "action": "open",
        "direction": direction,
        "lot": lot,
        "sl": sl,
        "tp": tp,
        "price": price,
        "risk_percent": max_risk,
        "atr": round(atr, 2)
    }
