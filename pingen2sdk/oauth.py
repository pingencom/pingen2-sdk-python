import json
import requests
import pingen2sdk

from pingen2sdk import error
from pingen2sdk.access_token import AccessToken
from requests.models import PreparedRequest
from typing import Dict, Optional


class OAuth(object):
    TOKEN_REFRESH_BUFFER_SECONDS = 300

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        use_staging: bool = False,
        scope: Optional[str] = None,
        grant_type: str = "client_credentials",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_staging = use_staging
        self.scope = scope
        self.grant_type = grant_type
        self._current_token: Optional[AccessToken] = None

    def get_current_token(self) -> Optional[AccessToken]:
        return self._current_token

    def get_access_token(self) -> str:
        if self._current_token is None or self._current_token.is_expired(
            self.TOKEN_REFRESH_BUFFER_SECONDS
        ):
            self._fetch_token()

        return self._current_token.access_token

    def _fetch_token(self) -> AccessToken:
        params: Dict[str, str] = {"grant_type": self.grant_type}

        if self.scope is not None:
            params["scope"] = self.scope
        if self.client_id is not None:
            params["client_id"] = self.client_id
        if self.client_secret is not None:
            params["client_secret"] = self.client_secret

        response = OAuth.get_token(self.use_staging, **params)

        self._current_token = AccessToken(
            access_token=response["access_token"],
            expires_in=response["expires_in"],
            token_type=response.get("token_type", "Bearer"),
        )

        return self._current_token

    @staticmethod
    def _set_client_id(params):
        if "client_id" in params:
            return

        from pingen2sdk import client_id

        if client_id:
            params["client_id"] = client_id
            return

        raise error.AuthenticationError(
            'No client_id provided. (HINT: set your client_id using "pingen2sdk.client_id = <CLIENT-ID>").'
        )

    @staticmethod
    def _set_client_secret(params):
        if "client_secret" in params:
            return

        from pingen2sdk import client_secret

        if client_secret:
            params["client_secret"] = client_secret
            return

        raise error.AuthenticationError(
            'No client_secret provided. (HINT: set your client_secret using "pingen2sdk.client_secret = <CLIENT-SECRET>").'
        )

    @staticmethod
    def authorize_url(use_staging=False, **params) -> str:
        if use_staging is False:
            path = pingen2sdk.auth_production
        else:
            path = pingen2sdk.auth_staging

        OAuth._set_client_id(params)
        if "response_type" not in params:
            params["response_type"] = "code"

        request = PreparedRequest()
        request.prepare_url(path, params)

        return request.url

    @staticmethod
    def get_token(use_staging=False, **params) -> Dict:
        if use_staging is False:
            url = pingen2sdk.api_production
        else:
            url = pingen2sdk.api_staging

        OAuth._set_client_id(params)
        OAuth._set_client_secret(params)

        response = requests.post(
            url + "/auth/access-tokens",
            params,
            {"Content-Type: application/x-www-form-urlencoded"},
        )

        return json.loads(response.text)

    @staticmethod
    def get_token_from_implicit(fragment: str) -> Dict:
        params = dict(x.split("=") for x in fragment.split("&"))

        return {
            "access_token": params["access_token"],
            "expires_in": params["expires_in"],
        }
