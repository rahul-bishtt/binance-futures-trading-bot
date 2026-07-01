"""Command Line Interface for the Binance Futures Testnet Trading Bot.

This module is the sole entry point for the application. It accepts user
arguments via Typer, delegates validation to the validation layer, initializes
the Binance Futures client, and dispatches order placement to the order layer.

No business logic lives here. The CLI is responsible only for:
- Accepting and forwarding user input.
- Displaying a formatted order request summary.
- Displaying a formatted order response.
- Catching and presenting application-specific errors cleanly.
"""

from __future__ import annotations

import sys
from typing import Optional

import typer
from colorama import Fore, Style, init

from bot.client import BinanceFuturesClient, load_and_validate_env
from bot.exceptions import ClientError, OrderError, ValidationError
from bot.logging_config import setup_logging
from bot.orders import OrderResult, place_limit_order, place_market_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

# Initialize colorama (resets colour after every echo automatically)
init(autoreset=True)

# Configure logging once at startup so all layers write to logs/bot.log
setup_logging()

app = typer.Typer(
    help="Binance Futures Testnet Trading Bot — place MARKET and LIMIT orders from the terminal.",
    add_completion=False,
)

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

_PANEL_WIDTH = 44


def _panel(title: str, rows: list[tuple[str, str]], colour: str) -> None:
    """Print a simple bordered panel to stdout.

    Args:
        title: Panel heading displayed at the top.
        rows: List of (label, value) pairs to display.
        colour: A colorama Fore colour constant for the border and title.
    """
    border = colour + "-" * _PANEL_WIDTH
    typer.echo(colour + "+" + "-" * _PANEL_WIDTH + "+")
    typer.echo(colour + "|" + Style.BRIGHT + f"  {title}".ljust(_PANEL_WIDTH) + colour + "|")
    typer.echo(border)
    for label, value in rows:
        line = f"  {label:<18}{value}"
        typer.echo(colour + "|" + Style.RESET_ALL + line.ljust(_PANEL_WIDTH) + colour + "|")
    typer.echo(colour + "+" + "-" * _PANEL_WIDTH + "+")


def _error(exc: Exception) -> None:
    """Print a clean, single-line error message without a stack trace.

    Args:
        exc: The caught exception instance.
    """
    typer.echo(Fore.RED + f"[ERROR] {type(exc).__name__}: {exc}", err=True)


# ──────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────

@app.command()
def info() -> None:
    """Display bot version and confirm that environment credentials are loaded."""
    from bot import __version__

    try:
        load_and_validate_env()
        cred_status = Fore.GREEN + "Loaded [OK]"
    except ValidationError:
        cred_status = Fore.RED + "Missing [FAIL]"

    typer.echo(Fore.CYAN + Style.BRIGHT + "Binance Futures Testnet Trading Bot")
    typer.echo(f"  Version     : {__version__}")
    typer.echo(f"  Credentials : {cred_status}")
    typer.echo(Style.DIM + "  Run `python cli.py order --help` to place an order.")


@app.command()
def order(
    symbol: str = typer.Option(
        ..., "--symbol", "-s",
        help="Trading pair symbol, e.g. BTCUSDT.",
    ),
    side: str = typer.Option(
        ..., "--side", "-d",
        help="Order side: BUY or SELL.",
    ),
    order_type: str = typer.Option(
        ..., "--type", "-t",
        help="Order type: MARKET or LIMIT.",
    ),
    quantity: float = typer.Option(
        ..., "--qty", "-q",
        help="Order quantity (must be greater than zero).",
    ),
    price: Optional[float] = typer.Option(
        None, "--price", "-p",
        help="Limit price (required for LIMIT orders, ignored for MARKET orders).",
    ),
) -> None:
    """Validate inputs and place a MARKET or LIMIT order on Binance Futures Testnet."""

    # ── 1. Validate and normalize all inputs ──────────────────────────────
    try:
        clean_symbol = validate_symbol(symbol)
        clean_side = validate_side(side)
        clean_type = validate_order_type(order_type)
        clean_qty = validate_quantity(quantity)
        clean_price = validate_price(price, required=(clean_type == "LIMIT"))
    except ValidationError as exc:
        _error(exc)
        raise typer.Exit(code=1)

    # ── 2. Display order request summary ──────────────────────────────────
    request_rows: list[tuple[str, str]] = [
        ("Symbol", clean_symbol),
        ("Side", clean_side),
        ("Type", clean_type),
        ("Quantity", str(clean_qty)),
        ("Price", str(clean_price) if clean_price is not None else "N/A (MARKET)"),
    ]
    _panel("ORDER REQUEST", request_rows, Fore.CYAN)

    # ── 3. Initialize client ───────────────────────────────────────────────
    try:
        api_key, api_secret = load_and_validate_env()
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret, testnet=True)
    except (ValidationError, ClientError) as exc:
        _error(exc)
        raise typer.Exit(code=1)

    # ── 4. Dispatch to order layer ─────────────────────────────────────────
    try:
        if clean_type == "MARKET":
            result: OrderResult = place_market_order(
                client=client,
                symbol=clean_symbol,
                side=clean_side,
                quantity=clean_qty,
            )
        else:
            result = place_limit_order(
                client=client,
                symbol=clean_symbol,
                side=clean_side,
                quantity=clean_qty,
                price=clean_price,  # type: ignore[arg-type]  # validated above
            )
    except OrderError as exc:
        _error(exc)
        raise typer.Exit(code=1)

    # ── 5. Display order response ──────────────────────────────────────────
    response_rows: list[tuple[str, str]] = [
        ("Order ID", str(result.order_id)),
        ("Status", result.status),
        ("Executed Qty", str(result.executed_qty)),
        ("Price", str(result.price) if result.price is not None else "N/A"),
    ]
    _panel("ORDER PLACED SUCCESSFULLY [OK]", response_rows, Fore.GREEN)


if __name__ == "__main__":
    app()

