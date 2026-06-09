import time

from trading_bot.utils.config_loader import load_settings
from trading_bot.utils.logger import setup_logger

logger = setup_logger("mt5_connector")

_connected = False


def connect():
    global _connected
    settings = load_settings()
    mt5_config = settings.get("mt5", {})

    try:
        import MetaTrader5 as mt5
    except ImportError:
        logger.error("MetaTrader5 package not installed. Run: pip install MetaTrader5")
        return False

    path = mt5_config.get("path", "")
    login = mt5_config.get("login", 0)
    password = mt5_config.get("password", "")
    server = mt5_config.get("server", "")
    timeout = mt5_config.get("timeout", 60000)

    if _connected:
        return True

    if not mt5.initialize(path=path, timeout=timeout):
        logger.error(f"MT5 initialize failed: {mt5.last_error()}")
        _connected = False
        return False

    if login and password:
        authorized = mt5.login(login, password=password, server=server)
        if not authorized:
            logger.error(f"MT5 login failed: {mt5.last_error()}")
            mt5.shutdown()
            _connected = False
            return False
        logger.info(f"MT5 logged in: {login} @ {server}")
    else:
        logger.info("MT5 initialized (no login credentials)")

    _connected = True
    return True


def disconnect():
    global _connected
    try:
        import MetaTrader5 as mt5
        mt5.shutdown()
    except ImportError:
        pass
    _connected = False
    logger.info("MT5 disconnected")


def get_account_info():
    try:
        import MetaTrader5 as mt5
        if not _connected:
            return None
        info = mt5.account_info()
        if info is None:
            logger.error(f"Failed to get account info: {mt5.last_error()}")
            return None
        account = info._asdict()
        logger.info(f"Account: {account.get('login')} | Balance: {account.get('balance')} | Equity: {account.get('equity')}")
        return account
    except ImportError:
        logger.warning("MetaTrader5 not installed")
        return None


def get_positions(symbol=None):
    try:
        import MetaTrader5 as mt5
        if not _connected:
            return []
        positions = mt5.positions_get(symbol=symbol)
        if positions is None:
            return []
        return [p._asdict() for p in positions]
    except ImportError:
        return []


def get_symbol_info(symbol="XAUUSD"):
    try:
        import MetaTrader5 as mt5
        if not _connected:
            return None
        info = mt5.symbol_info(symbol)
        if info is None:
            logger.error(f"Symbol {symbol} not found in MT5")
            return None
        return info._asdict()
    except ImportError:
        return None


def get_tick(symbol="XAUUSD"):
    try:
        import MetaTrader5 as mt5
        if not _connected:
            return None
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None
        return tick._asdict()
    except ImportError:
        return None
