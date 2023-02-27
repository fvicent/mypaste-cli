"""
    MyPaste CLI.
"""

from pathlib import Path
from typing import Optional
import logging

from rich.console import Console
import typer

from . import __version__, api
from .keymgr import get_api_key, store_api_key
from .logger import config_logger


app = typer.Typer(pretty_exceptions_show_locals=False)
stdout = Console()
# These are user errors, not stderr.
errors = Console(style="red")

HELP_API_KEY = "Your API key."
HELP_STORE_KEY = (
    "When passed along with --api-key, the key will be stored locally for "
    "later usage."
)
HELP_DEBUG = "Enables debug messages."


def version_callback(value: bool) -> None:
    if value:
        stdout.print(f"MyPaste CLI {__version__}")
        raise typer.Exit()


@app.command()
def upload(file: Path,
           api_key: str = typer.Option("", help=HELP_API_KEY),
           store_key: bool = typer.Option(True, help=HELP_STORE_KEY),
           debug: bool = typer.Option(False, help=HELP_DEBUG),
           version: Optional[bool] = typer.Option(
               None, "--version", callback=version_callback
               )
           ) -> None:
    """
    Uploads FILE to mypaste.dev and prints the resulting URL.
    """
    if debug:
        config_logger(logging.DEBUG)
    
    stored_api_key = get_api_key()
    if stored_api_key is None:
        if not api_key:
            api_key = typer.prompt(
                "Enter your API key",
                hide_input=True
            )
        if store_key:
            store_api_key(api_key)
    else:
        if api_key:
            # If a new API key is passed, drop the old one.
            store_api_key(api_key)
        else:
            # Work with the stored key.
            api_key = stored_api_key
    
    try:
        result = api.upload(file, api_key)
    except FileNotFoundError:
        errors.print(f"File {file.resolve()} not found.")
        return
    match result:
        case api.Status.OK, url:
            stdout.print(url)
        case api.Status.FAILED, None:
            errors.print("Server error. Try again later.")
        case api.Status.FAILED, message:
            errors.print(message)
