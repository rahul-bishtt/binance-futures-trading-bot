# Binance Futures Testnet Trading Bot

A production-quality Python trading bot for the Binance Futures Testnet environment. The application is built using standard, clean architecture patterns ensuring single-responsibility and separation of concerns.

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

To check if the CLI wrapper is set up correctly, run the help command:

```bash
python cli.py --help
```

To view bot system info:
```bash
python cli.py info
```

To execute a test/mock order (placeholder):
```bash
python cli.py order --symbol BTCUSDT --side BUY --type LIMIT --qty 0.01 --price 90000
```

---

## Future Implementation Roadmap

* **Loop 2:**
  - Complete integration of python-binance client connected specifically to Binance Futures Testnet API.
  - Implement full validation logic inside `validators.py` and catch custom exceptions.
  - Finalize local logs setup using `logging_config.py` targeting the `logs/` directory.
  - Hook CLI arguments to actual execution endpoints.
* **Loop 3:**
  - Add leverage adjustment and risk check features.
  - Write comprehensive unit tests and automated mock tests.
  - Establish error retry strategies.
