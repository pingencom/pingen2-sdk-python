import json
import requests
import pingen2sdk

from pingen2sdk import error
from requests.models import PreparedRequest
from typing import Dict


class OAuth(object):
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
