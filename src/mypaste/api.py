"""
    Python interface to the Web API.
"""

from enum import IntEnum
from pathlib import Path
from typing import Optional
import json
import os

import requests

from . import __version__
from .logger import get_logger


HOST = os.getenv("MYPASTE_CLI_HOST", "https://www.mypaste.dev")


class Status(IntEnum):
    OK = 1
    FAILED = 2


def upload(file: Path, api_key: str) -> tuple[Status, Optional[str]]:
    """
    Upload the specified `file` content to the server. The return value
    is a 2-tuple, where the second item might be:

        - The resulting URL if status is `Status.OK`.
        - An human-readable error message from the server if status is
          `Status.FAILED`.
        - `None` if status is `Status.FAILED` and the server returned
          no message.
    """
    endpoint = f"{HOST}/api/upload"
    body = {"paste_content": file.read_text("utf8")}
    headers = {
        "Authentication": f"Bearer {api_key}",
        "User-Agent": f"mypaste-cli/{__version__}"
    }
    get_logger().debug(f"Uploading {file.resolve()}")
    r = requests.post(endpoint, json=body, headers=headers)
    get_logger().debug(f"{r.status_code=} {r.content=}")
    if r.status_code != 201:
        try:
            return Status.FAILED, r.json()["message"]
        except json.JSONDecodeError:
            get_logger().debug("Could not decode JSON in response.")
            return Status.FAILED, None
    return Status.OK, r.json()["url"]
