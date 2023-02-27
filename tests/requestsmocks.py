import responses

from mypaste import api


class UploadRequestsMock(responses.RequestsMock):

    def add_post_upload(self,
                        success: bool,
                        status: int,
                        extra_json: dict[str, str]) -> None:
        """
        Shortcut function to include a fake response to `POST /api/upload`
        into the current object.
        """
        self.add(
            responses.POST,
            f"{api.HOST}/api/upload",
            json={"success": success, **extra_json},
            status=status,
            content_type="application/json",
        )


class SuccessfulUploadRequestsMock(UploadRequestsMock):

    paste_url: str

    def __enter__(self) -> "SuccessfulUploadRequestsMock":
        super().__enter__()
        self.paste_url = "https://mypaste.dev/dDjg721X"
        self.add_post_upload(True, 201, {"url": self.paste_url})
        return self


class InvalidKeyUploadRequestsMock(UploadRequestsMock):

    def __enter__(self) -> "InvalidKeyUploadRequestsMock":
        super().__enter__()
        self.add_post_upload(False, 403, {"message": "Invalid API key."})
        return self


class ServerErrorUploadRequestsMock(responses.RequestsMock):

    def __enter__(self) -> "ServerErrorUploadRequestsMock":
        super().__enter__()
        self.add(
            responses.POST,
            f"{api.HOST}/api/upload",
            body="Internal server error",
            status=500,
        )
        return self
