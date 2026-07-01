import os
import logging
import requests
from dotenv import load_dotenv
from binance import Client
from binance.exceptions import BinanceAPIException
from bot.exceptions import ValidationError, ClientError

logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()


def load_and_validate_env() -> tuple[str, str]:
    """Load and validate the Binance API credentials from environment variables.

    Returns:
        tuple[str, str]: The API key and Secret key.

    Raises:
        ValidationError: If any of the required keys are missing or empty.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    secret_key = os.getenv("BINANCE_SECRET_KEY")

    if not api_key:
        logger.error("Missing environment variable: BINANCE_API_KEY")
        raise ValidationError("BINANCE_API_KEY environment variable is missing or empty.")

    if not secret_key:
        logger.error("Missing environment variable: BINANCE_SECRET_KEY")
        raise ValidationError("BINANCE_SECRET_KEY environment variable is missing or empty.")

    return api_key, secret_key


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
        logger.info("Client initialization started.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

        # Initialize the underlying python-binance client configured for testnet
        try:
            self._client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=self.testnet
            )
        except Exception as e:
            logger.error(f"Client initialization failed: {e}")
            raise ClientError(f"Failed to initialize Binance Client: {e}") from e
        logger.info("Client initialized successfully.")

    def get_client(self) -> Client:
        """Expose the initialized Binance client.

        Returns:
            Client: The underlying python-binance Client instance.
        """
        return self._client

    def check_connectivity(self) -> bool:
        """Verify that the Binance Futures Testnet server is reachable.

        Returns:
            bool: True if the server is reachable and responds to a ping.

        Raises:
            ClientError: If network connection or server ping fails.
        """
        try:
            self._client.futures_ping()
            logger.info("Server connectivity verified.")
            return True
        except (BinanceAPIException, requests.exceptions.RequestException) as e:
            logger.error(f"Network / Server connectivity check failed: {e}")
            raise ClientError(f"Failed to connect to Binance Futures Testnet server: {e}") from e

    def validate_credentials(self) -> bool:
        """Verify that the provided API credentials are valid using an authenticated Futures endpoint.

        Returns:
            bool: True if credentials are authenticated successfully.

        Raises:
            ClientError: If authentication fails or an API error occurs.
        """
        try:
            self._client.futures_account_balance()
            logger.info("API credentials verified successfully.")
            return True
        except BinanceAPIException as e:
            logger.error(f"Authentication check failed: {e}")
            raise ClientError(f"Invalid API credentials or authentication failure: {e}") from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during authentication verification: {e}")
            raise ClientError(f"Network error during credential validation: {e}") from e


