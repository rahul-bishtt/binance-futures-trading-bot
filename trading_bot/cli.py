"""Command Line Interface for the Binance Futures Testnet Trading Bot.

This module provides the terminal interface using Typer, allowing users to
run commands to configure, test, and execute market/limit orders.
"""

import typer
from colorama import Fore, Style, init

# Initialize colorama for colored terminal outputs
init(autoreset=True)

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")


@app.command()
def info() -> None:
    """Display information about the trading bot and environment configuration."""
    typer.echo(Fore.GREEN + "Binance Futures Testnet Trading Bot CLI is active.")
    typer.echo(Style.DIM + "Ready for Loop 2 integration.")


@app.command()
def order(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading symbol (e.g. BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Order side (BUY or SELL)"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type (LIMIT or MARKET)"),
    quantity: float = typer.Option(..., "--qty", "-q", help="Order quantity"),
    price: float = typer.Option(None, "--price", "-p", help="Limit price (required for LIMIT orders)"),
) -> None:
    """Place a simulated market or limit order."""
    typer.echo(Fore.BLUE + f"Received order command: {side} {quantity} {symbol} ({order_type})")
    if order_type.upper() == "LIMIT" and price is None:
        typer.echo(Fore.RED + "Error: Price must be specified for LIMIT orders.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
