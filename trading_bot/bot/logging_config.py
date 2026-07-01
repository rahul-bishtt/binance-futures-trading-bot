"""Logging configuration module for the Binance Futures Testnet Trading Bot.

This module provides setup functions to configure logging formats, log levels,
and log handlers for both standard output (console) and log files.
"""

import logging
from pathlib import Path


def setup_logging(log_level: int = logging.INFO, log_file: str = "logs/bot.log") -> None:
    """Configure the built-in logging system for the trading bot.

    Sets up a console handler and a file handler targeting the log_file path.

    Args:
        log_level: The logging level to configure (e.g., logging.INFO).
        log_file: The path to the log file to write to.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Check if handlers are already configured to prevent duplication
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        log_path = Path(log_file)
        # Ensure parent directories exist
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

