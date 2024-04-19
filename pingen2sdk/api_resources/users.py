import pingen2sdk

from typing import Any, Mapping, Optional


class Users(object):
    api_requestor: pingen2sdk.APIRequestor

    def __init__(
        self,
        access_token: str,
        use_staging: bool = False,
    ):
        self.api_requestor = pingen2sdk.APIRequestor(access_token, use_staging)

    def get_details(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/user",
            params,
            supplied_headers,
        )
