from mypaste import keymgr


def test_keymgr() -> None:
    key = "valid-key"
    keymgr.store_api_key(key)
    assert keymgr.get_api_key() == key
    keymgr.clear_api_key()
    assert keymgr.get_api_key() is None
