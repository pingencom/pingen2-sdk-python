import pingen2sdk
from typing import Tuple


class FileUpload(object):
    def __init__(
        self,
        api_requestor: pingen2sdk.APIRequestor,
    ):
        self.api_requestor = api_requestor

    def request_file_upload(self) -> Tuple[str, str]:
        response = self.api_requestor.perform_get_request(
            "/file-upload",
        )

        return (
            response.data["data"]["attributes"]["url"],
            response.data["data"]["attributes"]["url_signature"],
        )

    def put_file(
        self,
        path_to_file: str,
        file_url: str,
    ):
        file = open(path_to_file, "rb")

        self.api_requestor.perform_put_request(file_url, file)

        file.close()
