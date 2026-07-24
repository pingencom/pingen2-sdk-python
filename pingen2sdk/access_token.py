import time

from typing import Optional


class AccessToken(object):
    access_token: str
    token_type: str
    expires_in: int
    issued_at: float

    def __init__(
        self,
        access_token: str,
        expires_in: int,
        token_type: str = "Bearer",
        issued_at: Optional[float] = None,
    ):
        self.access_token = access_token
        self.expires_in = int(expires_in)
        self.token_type = token_type
        self.issued_at = issued_at if issued_at is not None else time.time()

    @property
    def expires_at(self) -> float:
        return self.issued_at + self.expires_in

    def is_expired(self, buffer_seconds: int = 300) -> bool:
        return time.time() >= (self.expires_at - buffer_seconds)
