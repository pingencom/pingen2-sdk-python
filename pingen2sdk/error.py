import json

from typing import Dict, Optional


class PingenError(Exception):
    _message: Optional[str]
    json_body: Optional[object]
    status_code: Optional[int]
    headers: Optional[Dict[str, str]]
    request_id: Optional[str]

    def __init__(
        self,
        message: Optional[str] = None,
        body: Optional[str] = None,
        status_code: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        super(PingenError, self).__init__(message)

        self._message = message

        if bool(body):
            self.json_body = json.loads(body)

        self.headers = headers or {}
        self.status_code = status_code
        self.request_id = self.headers.get("x-request-id", None)


class AuthenticationError(PingenError):
    pass


class WebhookSignatureException(Exception):
    _message: Optional[str]

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
