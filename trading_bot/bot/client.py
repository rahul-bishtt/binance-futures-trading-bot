"""Client initialization and management module for Binance Futures.

This module contains the BinanceFuturesClient class, which is responsible for
holding API credentials and configuration to communicate with the Binance Futures API.
"""


class BinanceFuturesClient:
    """Manager for the Binance API client instance.

    Responsible for housing client-level configuration such as API keys,
    secret keys, and connection targets (e.g. Testnet vs Production).
    """

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True) -> None:
        """Initialize the Binance Futures Client.

        Args:
            api_key: The API key for Binance Futures Testnet.
            api_secret: The API secret for Binance Futures Testnet.
            testnet: Boolean indicating whether to connect to the Testnet environment.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self._client = None  # Placeholder for the actual python-binance client instance
