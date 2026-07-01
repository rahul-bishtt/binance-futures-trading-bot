"""Logging configuration module for the Binance Futures Testnet Trading Bot.

This module provides setup functions to configure logging formats, log levels,
and log handlers for both standard output (console) and log files.
"""

import logging


def setup_logging(log_level: int = logging.INFO) -> None:
    """Configure the built-in logging system for the trading bot.

    Args:
        log_level: The logging level to configure (e.g., logging.INFO).
    """
    # Minimal placeholder setup. Actual logging configuration will be implemented in a later loop.
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
