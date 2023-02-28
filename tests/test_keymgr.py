from typing import Any, Optional

import keyring
import keyring.backend
import keyring.errors

from mypaste import keymgr


class MemoryKeyring(keyring.backend.KeyringBackend):
    """
    In-memory keyring, just for testing purposes.
    """
    priority = 1    # type: ignore

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()    # type: ignore
        self._storage: dict[str, str] = {}
    
    def set_password(self, servicename: str, username: str, password: str) -> None:
        self._storage["f{username}@{servicename}"] = password

    def get_password(self, servicename: str, username: str) -> Optional[str]:
        return self._storage.get("f{username}@{servicename}", None)

    def delete_password(self, servicename: str, username: str) -> None:
        try:
            del self._storage["f{username}@{servicename}"]
        except KeyError:
            raise keyring.errors.PasswordDeleteError("service or username not found")


def test_keymgr() -> None:
    keyring.set_keyring(MemoryKeyring())    # type: ignore
    key = "valid-key"
    keymgr.store_api_key(key)
    assert keymgr.get_api_key() == key
    keymgr.clear_api_key()
    assert keymgr.get_api_key() is None
