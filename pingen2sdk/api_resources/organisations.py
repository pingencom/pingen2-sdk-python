import pingen2sdk

from typing import Any, Mapping, Optional


class Organisations(object):
    api_requestor: pingen2sdk.APIRequestor

    def __init__(
        self,
        access_token: str,
        use_staging: bool = False,
    ):
        self.api_requestor = pingen2sdk.APIRequestor(access_token, use_staging)

    def get_details(
        self,
        organisation_id: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s" % organisation_id,
            params,
            supplied_headers,
        )

    def get_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations",
            params,
            supplied_headers,
        )
