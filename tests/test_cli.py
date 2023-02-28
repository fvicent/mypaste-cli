from pathlib import Path

from typer.testing import CliRunner
import keyring

from memorykeyring import MemoryKeyring
from mypaste.cli import app
from mypaste import __version__, keymgr
from requestsmocks import *


runner = CliRunner()
keyring.set_keyring(MemoryKeyring())    # type: ignore


def invoke_and_find(filename: str, api_key: str, string: str) -> None:
    """
    Shortcut for invoking the CLI and finding something in `stdout`.
    The specified `api_key` is both passed via `--api-key` and `stdin`.
    """
    result = runner.invoke(app, [filename, f"--api-key={api_key}"])
    assert string in result.stdout
    result = runner.invoke(app, [filename], input=api_key)
    assert string in result.stdout


def test_version()  -> None:
    result = runner.invoke(app, "--version")
    assert __version__ in result.stdout


def test_upload(tmp_path: Path) -> None:
    tmp_file = tmp_path / "hello.py"
    tmp_file.write_text("print('Hello world!')", "utf8")
    invalid_key = "invalid-key"
    valid_key = "valid-key"
    invalid_file = "notfound.py"
    valid_file = str(tmp_file.resolve())
    # Make sure the test service name is being used.
    assert keymgr.KEYRING_SERVICE_NAME == "mypaste-cli-test"
    # Non-existent file.
    invoke_and_find(invalid_file, valid_key, "not found")
    # Existent file.
    with SuccessfulUploadRequestsMock() as rsps:
        invoke_and_find(valid_file, valid_key, rsps.paste_url)
    # Invalid key.
    with InvalidKeyUploadRequestsMock():
        invoke_and_find(valid_file, invalid_key, "Invalid API key")
    # Unkown server error.
    with ServerErrorUploadRequestsMock():
        invoke_and_find(valid_file, valid_key, "Server error. Try again later")
    # Make sure `--no-store-key` does not store the API key.
    keymgr.clear_api_key()
    with SuccessfulUploadRequestsMock() as rsps:
        runner.invoke(app, [valid_file, "--no-store-key", f"--api-key={valid_key}"])
    assert keymgr.get_api_key() is None
