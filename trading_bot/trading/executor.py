import json
import os
import time

from trading_bot.trading.mt5_connector import connect, disconnect, get_positions
from trading_bot.trading.risk_manager import get_trade_params
from trading_bot.utils.config_loader import load_settings
from trading_bot.utils.logger import setup_logger

logger = setup_logger("executor")

SYMBOL = "XAUUSD"
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)


def get_current_price():
    latest_path = os.path.join(DATA_DIR, "current", "latest_price.json")
    if not os.path.exists(latest_path):
        logger.error("No price data available")
        return None
    with open(latest_path) as f:
        data = json.load(f)
    return data.get("close")


def has_open_position(symbol=SYMBOL):
    positions = get_positions(symbol)
    return len(positions) > 0, positions


def execute(decision, force_open=False):
    price = get_current_price()
    if price is None:
        logger.error("Cannot execute trade: no price")
        return {"status": "error", "message": "No price available"}

    has_pos, positions = has_open_position()

    if decision in ("hold",):
        if has_pos:
            logger.info("HOLD signal, but position open. No action.")
        else:
            logger.info("HOLD signal. No action.")
        return {
            "status": "hold",
            "decision": decision,
            "price": price,
            "positions_open": len(positions)
        }

    if has_pos and not force_open:
        for pos in positions:
            pos_type = "buy" if pos["type"] == 0 else "sell"
            if ((decision == "buy" or decision == "strong_buy") and pos_type == "buy") or \
               ((decision == "sell" or decision == "strong_sell") and pos_type == "sell"):
                logger.info(f"Position already open in {pos_type} direction. Skip.")
                return {
                    "status": "skipped",
                    "reason": f"Already in {pos_type} position",
                    "positions_open": len(positions)
                }

    if has_pos and not force_open:
        logger.info("Closing existing positions before new trade")
        close_all_positions()

    trade_params = get_trade_params(decision, price)

    if trade_params["action"] == "hold":
        return {"status": "hold", "reason": trade_params["reason"]}

    return place_order(trade_params)


def place_order(params):
    try:
        import MetaTrader5 as mt5
    except ImportError:
        logger.error("MetaTrader5 package not installed")
        return {"status": "error", "message": "MetaTrader5 not installed"}

    connected = connect()
    if not connected:
        return {"status": "error", "message": "Cannot connect to MT5"}

    order_type = mt5.ORDER_TYPE_BUY if params["direction"] == "buy" else mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": params["lot"],
        "type": order_type,
        "price": params["price"],
        "sl": params["sl"],
        "tp": params["tp"],
        "deviation": 20,
        "magic": 202406,
        "comment": "XAUUSD_BOT",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    logger.info(f"Placing {params['direction'].upper()} order:")
    logger.info(f"  Lot: {params['lot']} | Price: {params['price']} | SL: {params['sl']} | TP: {params['tp']}")

    result = mt5.order_send(request)

    if result is None:
        logger.error(f"Order send failed: {mt5.last_error()}")
        return {"status": "error", "message": str(mt5.last_error())}

    result_dict = {
        "retcode": result.retcode,
        "comment": result.comment,
        "order": result.order,
        "volume": result.volume,
        "price": result.price,
    }

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logger.error(f"Order rejected: {result.comment} (code: {result.retcode})")
        return {"status": "rejected", "message": result.comment, "details": result_dict}

    logger.info(f"Order filled: {result.order} @ {result.price}")
    return {"status": "executed", "order_id": result.order, "details": result_dict}


def close_all_positions(symbol=SYMBOL):
    try:
        import MetaTrader5 as mt5
    except ImportError:
        return

    positions = get_positions(symbol)
    if not positions:
        logger.info("No positions to close")
        return

    for pos in positions:
        order_type = mt5.ORDER_TYPE_SELL if pos["type"] == 0 else mt5.ORDER_TYPE_BUY
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": pos["volume"],
            "type": order_type,
            "position": pos["ticket"],
            "price": mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).bid,
            "deviation": 20,
            "magic": 202406,
            "comment": "XAUUSD_BOT_CLOSE",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            logger.info(f"Closed position {pos['ticket']}")
        else:
            err = mt5.last_error() if result is None else result.comment
            logger.error(f"Failed to close {pos['ticket']}: {err}")


if __name__ == "__main__":
    pass
