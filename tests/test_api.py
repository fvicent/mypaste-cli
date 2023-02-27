from pathlib import Path

import pytest

from requestsmocks import *
from mypaste import api


def test_upload(tmp_path: Path) -> None:
    tmp_file = tmp_path / "hello.py"
    tmp_file.write_text("print('Hello world!')", "utf8")
    # Non-existent file.
    with pytest.raises(FileNotFoundError):
        api.upload(Path("notfound.py"), "valid-key")
    # Existent file.
    with SuccessfulUploadRequestsMock() as rsps:
        assert api.upload(tmp_file, "valid-key") == (api.Status.OK, rsps.paste_url)
    # Invalid key.
    with InvalidKeyUploadRequestsMock():
        assert api.upload(tmp_file, "invalid-key") == (api.Status.FAILED, "Invalid API key.")
    # Unkown server error.
    with ServerErrorUploadRequestsMock():
        assert api.upload(tmp_file, "valid-key") == (api.Status.FAILED, None)
