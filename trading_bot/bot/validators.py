"""Validation helper functions for the Binance Futures Testnet Trading Bot.

This module provides individual functions to validate API credentials,
symbols, order sides (BUY/SELL), order types (LIMIT/MARKET), quantities, and prices.
Functions raise ValidationError when validations fail.
"""

from bot.exceptions import ValidationError


def validate_symbol(symbol: str) -> None:
    """Validate the trading pair symbol.

    Args:
        symbol: The symbol string (e.g., 'BTCUSDT').

    Raises:
        ValidationError: If the symbol is invalid or empty.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string.")


def validate_side(side: str) -> None:
    """Validate the order side.

    Args:
        side: The order side string ('BUY' or 'SELL').

    Raises:
        ValidationError: If the side is not 'BUY' or 'SELL'.
    """
    valid_sides = {"BUY", "SELL"}
    if not side or side.upper() not in valid_sides:
        raise ValidationError(f"Side must be one of {valid_sides}.")


def validate_order_type(order_type: str) -> None:
    """Validate the order type.

    Args:
        order_type: The order type string ('LIMIT' or 'MARKET').

    Raises:
        ValidationError: If the order type is not 'LIMIT' or 'MARKET'.
    """
    valid_types = {"LIMIT", "MARKET"}
    if not order_type or order_type.upper() not in valid_types:
        raise ValidationError(f"Order type must be one of {valid_types}.")


def validate_quantity(quantity: float) -> None:
    """Validate the order quantity.

    Args:
        quantity: The quantity of the order.

    Raises:
        ValidationError: If quantity is less than or equal to zero.
    """
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")


def validate_price(price: float) -> None:
    """Validate the order price.

    Args:
        price: The price of the order.

    Raises:
        ValidationError: If price is less than or equal to zero.
    """
    if price <= 0:
        raise ValidationError("Price must be greater than zero.")


def validate_api_credentials(api_key: str, secret_key: str) -> None:
    """Validate presence of Binance API credentials.

    Args:
        api_key: Binance API Key.
        secret_key: Binance Secret Key.

    Raises:
        ValidationError: If credentials are empty.
    """
    if not api_key or not secret_key:
        raise ValidationError("API key and secret key must not be empty.")
