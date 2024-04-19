import json

from typing import Mapping, Optional


class PingenResponse(object):
    body: str
    status_code: int
    headers: Mapping[str, str]
    data: Optional[object] = None

    def __init__(self, body: str, status_code: int, headers: Mapping[str, str]):
        self.body = body

        if bool(body):
            self.data = json.loads(body)

        self.status_code = status_code
        self.headers = headers

    @property
    def request_id(self) -> Optional[str]:
        return self.headers.get("x-request-id", None)
