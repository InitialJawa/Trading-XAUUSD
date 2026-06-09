import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trading_bot.utils.logger import setup_logger
from trading_bot.utils.config_loader import load_settings

logger = setup_logger("pipeline")

PIPELINE = [
    ("Data Collection", [
        "trading_bot.collectors.prices",
        "trading_bot.collectors.indicators",
    ]),
    ("Signal Generation", [
        "trading_bot.signals.rsi_signal",
        "trading_bot.signals.macd_signal",
        "trading_bot.signals.ma_signal",
        "trading_bot.signals.momentum_signal",
        "trading_bot.signals.composite_signal",
    ]),
    ("Archive", [
        "trading_bot.backtesting.archive",
    ]),
    ("Dashboard", [
        "trading_bot.dashboard.generate_dashboard",
    ]),
]


def run_module(module_name):
    logger.info(f"Running: {module_name}")
    result = os.system(f"{sys.executable} -m {module_name}")
    if result != 0:
        logger.error(f"Failed: {module_name}")
        return False
    return True


def run_pipeline(execute_trade=False):
    logger.info("=" * 50)
    logger.info("XAUUSD TRADING BOT PIPELINE STARTED")
    logger.info("=" * 50)

    for stage_name, modules in PIPELINE:
        logger.info(f"\n--- {stage_name} ---")
        for module in modules:
            success = run_module(module)
            if not success:
                logger.error(f"Pipeline aborted at {module}")
                return False

    if execute_trade:
        logger.info("\n--- Trade Execution ---")
        from trading_bot.signals.composite_signal import generate as get_signal
        from trading_bot.trading.executor import execute

        signal = get_signal()
        if signal:
            decision = signal.get("decision", "hold")
            logger.info(f"Signal decision: {decision}")
            result = execute(decision)
            logger.info(f"Execution result: {result}")

    logger.info("=" * 50)
    logger.info("PIPELINE COMPLETED")
    logger.info("=" * 50)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XAUUSD Trading Bot Pipeline")
    parser.add_argument("--trade", action="store_true", help="Enable live trade execution")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon (loop)")
    args = parser.parse_args()

    if args.daemon:
        import time
        settings = load_settings()
        interval = 3600
        logger.info(f"Daemon mode: running every {interval}s")
        while True:
            run_pipeline(execute_trade=args.trade)
            logger.info(f"Sleeping {interval}s...")
            time.sleep(interval)
    else:
        run_pipeline(execute_trade=args.trade)
