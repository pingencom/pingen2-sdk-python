import requests
import pingen2sdk

from io import IOBase, BytesIO
from typing import Any, Dict, Mapping, Optional, cast
from requests.models import PreparedRequest


def _response_interpreter(
    body: Dict,
    status_code: int,
    headers: Mapping[str, str],
) -> pingen2sdk.PingenResponse:
    if 200 <= status_code < 310:
        return pingen2sdk.PingenResponse(body, status_code, headers)
    else:
        raise pingen2sdk.PingenError(None, body, status_code, headers)


class APIRequestor(object):
    access_token: str
    api_base: str
    user_agent: str = "PINGEN.SDK.PYTHON"

    def __init__(self, access_token: str, use_staging: Optional[bool] = False):
        if use_staging is False:
            self.api_base = pingen2sdk.api_production
        else:
            self.api_base = pingen2sdk.api_staging

        self.access_token = access_token

    def perform_get_request(
        self,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        r = requests.get(
            self.prepare_path(url, params),
            headers=self.request_headers(supplied_headers),
            timeout=pingen2sdk.request_timeout,
        )

        return _response_interpreter(r.text, r.status_code, r.headers)

    @staticmethod
    def perform_put_request(
        url: str,
        file: BytesIO,
    ):
        requests.put(url, data=file)

    def perform_post_request(
        self,
        url: str,
        payload: str,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        r = requests.post(
            self.prepare_path(url),
            payload,
            headers=self.request_headers(supplied_headers),
            timeout=pingen2sdk.request_timeout,
        )

        return _response_interpreter(r.text, r.status_code, r.headers)

    def perform_patch_request(
        self,
        url: str,
        payload: str,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        r = requests.patch(
            self.prepare_path(url),
            payload,
            headers=self.request_headers(supplied_headers),
            timeout=pingen2sdk.request_timeout,
        )

        return _response_interpreter(r.text, r.status_code, r.headers)

    def perform_cancel_request(self, url: str) -> pingen2sdk.PingenResponse:
        r = requests.patch(
            self.prepare_path(url),
            headers=self.request_headers(),
            timeout=pingen2sdk.request_timeout,
        )

        return _response_interpreter(r.text, r.status_code, r.headers)

    def perform_delete_request(self, url: str) -> pingen2sdk.PingenResponse:
        r = requests.delete(
            self.prepare_path(url),
            headers=self.request_headers(),
            timeout=pingen2sdk.request_timeout,
        )

        return _response_interpreter(r.text, r.status_code, r.headers)

    def perform_stream_request(
        self,
        url: str,
    ) -> IOBase:
        response = requests.get(
            self.prepare_path(url),
            headers=self.request_headers(),
            timeout=pingen2sdk.request_timeout,
            stream=True,
        )

        return cast(IOBase, response.text)

    def prepare_path(
        self,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
    ) -> str:
        path = "%s%s" % (self.api_base, url)

        request = PreparedRequest()
        request.prepare_url(path, params)

        return request.url

    def request_headers(
        self,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> Mapping[str, str]:
        supplied_headers_dict: Optional[Dict[str, str]] = (
            dict(supplied_headers) if supplied_headers is not None else None
        )

        headers = {
            "User-Agent": self.user_agent,
            "Authorization": "Bearer {}".format(self.access_token),
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }

        if supplied_headers_dict is not None:
            for key, value in supplied_headers_dict.items():
                headers[key] = value

        return headers
