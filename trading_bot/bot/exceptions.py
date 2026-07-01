"""Custom exception classes for the Binance Futures Testnet Trading Bot.

This module defines the hierarchy of exceptions raised by the trading bot's
components to handle API client issues, configuration/parameter validation failures,
and order execution errors.
"""


class TradingBotError(Exception):
    """Base exception class for all errors arising from the trading bot."""

    pass


class ClientError(TradingBotError):
    """Raised when there is an issue with the Binance client or API connectivity."""

    pass


class ValidationError(TradingBotError):
    """Raised when configuration values or order parameters fail validation checks."""

    pass


class InvalidSymbolError(ValidationError):
    """Raised when a symbol fails format or existence validation."""

    pass


class InvalidSideError(ValidationError):
    """Raised when an order side is invalid."""

    pass


class InvalidOrderTypeError(ValidationError):
    """Raised when an order type is invalid."""

    pass


class InvalidQuantityError(ValidationError):
    """Raised when an order quantity is invalid."""

    pass


class InvalidPriceError(ValidationError):
    """Raised when an order price is invalid."""

    pass


class OrderError(TradingBotError):
    """Raised when an order placement or order-related action fails."""

    pass
