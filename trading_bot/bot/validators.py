"""Validation helper functions for the Binance Futures Testnet Trading Bot.

This module provides individual functions to validate API credentials,
symbols, order sides, order types, quantities, and prices.
Functions raise specific sub-exceptions of ValidationError when validation fails.
"""

import re
from typing import Any
from bot.exceptions import (
    ValidationError,
    InvalidSymbolError,
    InvalidSideError,
    InvalidOrderTypeError,
    InvalidQuantityError,
    InvalidPriceError,
)

# Module-level constants for validation rules
VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"LIMIT", "MARKET"}

# Regex for lightweight symbol validation: uppercase alphanumeric, 3 to 15 characters
SYMBOL_REGEX = re.compile(r"^[A-Z0-9]{3,15}$")


def validate_symbol(symbol: Any) -> str:
    """Validate the trading pair symbol format.

    Args:
        symbol: The symbol to validate.

    Returns:
        str: The cleaned, normalized uppercase symbol string.

    Raises:
        InvalidSymbolError: If the symbol is invalid, empty, or not format compliant.
    """
    if symbol is None:
        raise InvalidSymbolError("Symbol is required and cannot be None.")

    # basic normalization
    cleaned_symbol = str(symbol).strip().upper()

    if not cleaned_symbol:
        raise InvalidSymbolError("Symbol cannot be empty or whitespace only.")

    if not SYMBOL_REGEX.match(cleaned_symbol):
        raise InvalidSymbolError(
            f"Symbol '{cleaned_symbol}' is invalid. Must be alphanumeric and 3-15 characters."
        )

    return cleaned_symbol


def validate_side(side: Any) -> str:
    """Validate the order side.

    Args:
        side: The order side (e.g. 'BUY', 'SELL').

    Returns:
        str: The normalized uppercase side.

    Raises:
        InvalidSideError: If the side is not valid.
    """
    if side is None:
        raise InvalidSideError("Order side is required and cannot be None.")

    cleaned_side = str(side).strip().upper()

    if cleaned_side not in VALID_SIDES:
        raise InvalidSideError(
            f"Invalid order side '{cleaned_side}'. Allowed values are: {VALID_SIDES}"
        )

    return cleaned_side


def validate_order_type(order_type: Any) -> str:
    """Validate the order type.

    Args:
        order_type: The order type (e.g. 'LIMIT', 'MARKET').

    Returns:
        str: The normalized uppercase order type.

    Raises:
        InvalidOrderTypeError: If the order type is not valid.
    """
    if order_type is None:
        raise InvalidOrderTypeError("Order type is required and cannot be None.")

    cleaned_type = str(order_type).strip().upper()

    if cleaned_type not in VALID_ORDER_TYPES:
        raise InvalidOrderTypeError(
            f"Invalid order type '{cleaned_type}'. Allowed values are: {VALID_ORDER_TYPES}"
        )

    return cleaned_type


def validate_quantity(quantity: Any) -> float:
    """Validate the order quantity.

    Args:
        quantity: The quantity of the order.

    Returns:
        float: The validated float quantity.

    Raises:
        InvalidQuantityError: If quantity is missing, non-numeric, or <= 0.
    """
    if quantity is None:
        raise InvalidQuantityError("Quantity is required and cannot be None.")

    try:
        val = float(quantity)
    except (ValueError, TypeError) as e:
        raise InvalidQuantityError(f"Quantity '{quantity}' must be numeric.") from e

    if val <= 0:
        raise InvalidQuantityError(f"Quantity must be greater than zero. Got {val}.")

    return val


def validate_price(price: Any, required: bool = False) -> float | None:
    """Validate the order price.

    Args:
        price: The price of the order.
        required: Whether the price is strictly required (e.g., for LIMIT orders).

    Returns:
        float | None: The validated float price or None if not required and not provided.

    Raises:
        InvalidPriceError: If price is invalid, or missing when required.
    """
    if price is None or str(price).strip() == "":
        if required:
            raise InvalidPriceError("Price is required for LIMIT orders.")
        return None

    try:
        val = float(price)
    except (ValueError, TypeError) as e:
        raise InvalidPriceError(f"Price '{price}' must be numeric.") from e

    if val <= 0:
        raise InvalidPriceError(f"Price must be greater than zero. Got {val}.")

    return val


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

