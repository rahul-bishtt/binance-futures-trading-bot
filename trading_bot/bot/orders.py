"""Order execution module for Binance Futures Testnet.

This module exposes two public functions for placing Market and Limit orders
on the Binance Futures Testnet. It assumes all inputs have already been
validated and normalized by the validation layer.

Responsibilities:
- Send order requests to the Binance Futures Testnet API.
- Parse and normalize the raw API response into an OrderResult.
- Log all outgoing requests and incoming responses.
- Map all external exceptions to application-specific OrderError.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import requests
from binance.exceptions import BinanceAPIException

from bot.client import BinanceFuturesClient
from bot.exceptions import OrderError

logger = logging.getLogger(__name__)


@dataclass
class OrderResult:
    """Normalized representation of a Binance Futures order response.

    Attributes:
        order_id: Unique order identifier assigned by Binance.
        symbol: Trading pair symbol (e.g. 'BTCUSDT').
        side: Order direction ('BUY' or 'SELL').
        order_type: Order type ('MARKET' or 'LIMIT').
        quantity: Originally requested quantity (origQty from Binance response).
        executed_qty: Quantity actually filled (executedQty from Binance response).
        price: Average fill price for MARKET orders (avgPrice); stated limit
               price for LIMIT orders. None if the order has not yet filled.
        status: Order status string as returned by Binance (e.g. 'NEW', 'FILLED').
        timestamp: Order update timestamp in milliseconds (updateTime).
    """

    order_id: int
    symbol: str
    side: str
    order_type: str
    quantity: float
    executed_qty: float
    price: float | None
    status: str
    timestamp: int


def _build_order_result(response: dict) -> OrderResult:
    """Convert a raw Binance Futures API order response into an OrderResult.

    For MARKET orders the price is sourced from avgPrice and set to None when
    the order has not yet filled (avgPrice == "0" or absent). For LIMIT orders
    the stated limit price is used as a fallback when avgPrice is zero.

    Args:
        response: The raw dict returned by the Binance Futures API.

    Returns:
        OrderResult: The normalized order result.
    """
    avg_price_raw = response.get("avgPrice", "0")

    # Parse avgPrice; treat "0" and missing values as None (unfilled)
    try:
        avg_price = float(avg_price_raw)
        price: float | None = avg_price if avg_price > 0 else None
    except (ValueError, TypeError):
        price = None

    # For LIMIT orders, fall back to the stated price when not yet filled
    if response.get("type") == "LIMIT" and price is None:
        try:
            limit_price = float(response.get("price", 0))
            price = limit_price if limit_price > 0 else None
        except (ValueError, TypeError):
            price = None

    return OrderResult(
        order_id=int(response["orderId"]),
        symbol=response["symbol"],
        side=response["side"],
        order_type=response["type"],
        quantity=float(response["origQty"]),
        executed_qty=float(response["executedQty"]),
        price=price,
        status=response["status"],
        timestamp=int(response["updateTime"]),
    )


def place_market_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
) -> OrderResult:
    """Place a MARKET order on Binance Futures Testnet.

    Inputs are assumed to be already validated and normalized.

    Args:
        client: An initialized BinanceFuturesClient instance.
        symbol: Normalized trading pair symbol (e.g. 'BTCUSDT').
        side: Normalized order side ('BUY' or 'SELL').
        quantity: Validated positive quantity to trade.

    Returns:
        OrderResult: Normalized result of the executed order.

    Raises:
        OrderError: On any Binance API error, network failure, or unexpected error.
    """
    logger.info(
        "Placing MARKET order — symbol=%s side=%s quantity=%s",
        symbol, side, quantity,
    )

    try:
        response = client.get_client().futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
    except BinanceAPIException as e:
        logger.error("Binance API error placing MARKET order: %s", e)
        raise OrderError(f"Binance API error placing MARKET order: {e}") from e
    except requests.exceptions.RequestException as e:
        logger.error("Network error placing MARKET order: %s", e)
        raise OrderError(f"Network error placing MARKET order: {e}") from e
    except Exception as e:
        logger.exception("Unexpected error placing MARKET order: %s", e)
        raise OrderError(f"Unexpected error placing MARKET order: {e}") from e

    logger.info("MARKET order response — %s", response)
    return _build_order_result(response)


def place_limit_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
) -> OrderResult:
    """Place a LIMIT order on Binance Futures Testnet.

    Inputs are assumed to be already validated and normalized.
    Time-in-force is always GTC (Good Till Cancelled).

    Args:
        client: An initialized BinanceFuturesClient instance.
        symbol: Normalized trading pair symbol (e.g. 'BTCUSDT').
        side: Normalized order side ('BUY' or 'SELL').
        quantity: Validated positive quantity to trade.
        price: Validated positive limit price.

    Returns:
        OrderResult: Normalized result of the submitted order.

    Raises:
        OrderError: On any Binance API error, network failure, or unexpected error.
    """
    logger.info(
        "Placing LIMIT order — symbol=%s side=%s quantity=%s price=%s",
        symbol, side, quantity, price,
    )

    try:
        response = client.get_client().futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
    except BinanceAPIException as e:
        logger.error("Binance API error placing LIMIT order: %s", e)
        raise OrderError(f"Binance API error placing LIMIT order: {e}") from e
    except requests.exceptions.RequestException as e:
        logger.error("Network error placing LIMIT order: %s", e)
        raise OrderError(f"Network error placing LIMIT order: {e}") from e
    except Exception as e:
        logger.exception("Unexpected error placing LIMIT order: %s", e)
        raise OrderError(f"Unexpected error placing LIMIT order: {e}") from e

    logger.info("LIMIT order response — %s", response)
    return _build_order_result(response)

