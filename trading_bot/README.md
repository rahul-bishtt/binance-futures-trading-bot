# Binance Futures Trading Bot

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Binance Futures](https://img.shields.io/badge/Binance-Futures_Testnet-F3BA2F?logo=binance&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Typer-blueviolet)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-green)

A production-quality Python trading bot for the Binance Futures Testnet environment. Built with clean architecture, modular design, comprehensive validation, structured logging, and robust error handling.

---

## ✨ Highlights

- 🚀 Binance Futures Testnet Integration
- 📈 Market & Limit Order Support
- 🖥️ Interactive CLI using Typer
- ✅ Input Validation
- 📝 Structured Logging
- ⚠️ Robust Error Handling
- 🧩 Modular Clean Architecture

---

## Architecture & Application Flow

The bot processes operations according to the following top-down flow:

```
    CLI
     ↓
 Validators
     ↓
   Orders
     ↓
   Client
     ↓
Binance Futures Testnet API
```

* **CLI (`cli.py`)**: Entry point of the application, parsing terminal commands and handling output formatting.
* **Validators (`bot/validators.py`)**: Helper layer to validate incoming inputs (such as symbol names, side flags, quantity ranges, price boundaries, and environment configs) before hitting the execution layer.
* **Orders (`bot/orders.py`)**: Responsible for constructing order parameters and requesting order placements.
* **Client (`bot/client.py`)**: Manages the API key mapping, target endpoints (Testnet), and the underlying connection to the official Binance API client.
* **Binance Futures Testnet API**: The remote API endpoint simulating order execution.

---

## Folder Structure

```
trading_bot/
├── bot/
│   ├── __init__.py           # Package versioning and exports
│   ├── client.py             # Client wrapper class for API configuration
│   ├── orders.py             # Place market and limit orders
│   ├── validators.py         # Credentials and order parameter validators
│   ├── logging_config.py     # Central logging setup
│   └── exceptions.py         # Custom application exception classes
├── logs/
│   └── .gitkeep              # Log file placeholder
├── cli.py                    # Command-line interface shell
├── .env.example              # Sample environment file
├── .gitignore                # Git files/directories filter
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Installation Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/rahul-bishtt/binance-futures-trading-bot.git
   cd binance-futures-trading-bot/trading_bot
   ```

2. **Create and Activate a Virtual Environment:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variable Setup

1. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in a text editor and fill in your Binance Futures Testnet API credentials:
   ```ini
   BINANCE_API_KEY=your_testnet_api_key_here
   BINANCE_SECRET_KEY=your_testnet_secret_key_here
   ```
   *Note: Keys can be generated at the [Binance Futures Testnet Dashboard](https://testnet.binancefuture.com/).*

---

## Running the Application

To check if the CLI is set up correctly, run the help command:
```bash
python cli.py --help
```

To view bot system info and check if environment variables are loaded:
```bash
python cli.py info
```

To place a **MARKET** order (e.g. BUY 0.001 BTC):
```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
```

To place a **LIMIT** order (e.g. SELL 0.001 BTC at $120,000):
```bash
python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 120000
```

---

## Project Assumptions & Design Decisions

1. **Futures Testnet Only**: The bot is configured exclusively for the Binance Futures Testnet environment (`testnet.binance.vision`) to avoid accidental real money trades.
2. **Offline-friendly Info**: The `info` command checks if keys are defined in the environment variables without initiating a network handshake, preventing network delay.
3. **Strict Validation Layer**: Input parameter normalization (uppercasing, trimming whitespace) is executed locally before any network connection is established, saving API call bandwidth.
4. **Type-Aware Price Resolution**:
   - For `MARKET` orders, the price is resolved using `avgPrice` from the fill details.
   - For `LIMIT` orders, the price is resolved using the specified limit price.
5. **Console Encoding Security**: ASCII symbols `[OK]` and `[FAIL]` are used in print borders and labels to prevent `UnicodeEncodeError` on Windows consoles.
6. **Pinned Dependencies**: Dependency limits are strict (specifically Click 8.1.7) to prevent compatibility breaks with Typer.

---

## Future Scope

* **Leverage & Margin Controls**: Implement endpoints to configure leverage (`futures_change_leverage`) and switch between cross/isolated margin.
* **Pre-trade Risk Management**: Incorporate client-side max daily loss limits and position size boundaries.
* **Resilience & Retry Logic**: Add automatic order retries with exponential backoff for transient HTTP 5xx or connection issues.

