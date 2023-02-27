"""
    API key managament module.
"""

from typing import Optional
import os

import keyring


KEYRING_SERVICE_NAME = os.getenv(
    "MYPASTE_CLI_KEYRING_SERVICE_NAME",
    "mypaste-cli"
)
KEYRING_USERNAME = "mypaste-api-key"


def clear_api_key() -> None:
    """
    Remove the stored API key from the current system.
    """
    keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME)


def get_api_key() -> Optional[str]:
    """
    Retrieve the stored API key or `None` if not found.
    """
    return keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME)


def store_api_key(key: str) -> None:
    """
    Securely store the specified `key` within the current system.
    """
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME, key)
