import pingen2sdk
import requests
import pytest
import responses


class TestOAuth(object):
    def test_authorize_url_error(self):
        with pytest.raises(pingen2sdk.error.AuthenticationError):
            pingen2sdk.OAuth.authorize_url(
                scope="letter", state="RANDOMGENERATEDSTRING"
            )

    def test_authorize_url(self):
        url = pingen2sdk.OAuth.authorize_url(
            scope="letter",
            state="RANDOMGENERATEDSTRING",
            client_id="testClientId",
            response_type="code",
        )

        result = requests.utils.urlparse(url)
        query = result.query
        params = dict(x.split("=") for x in query.split("&"))

        assert result.scheme == "https"
        assert result.netloc == "identity.pingen.com"

        assert params["client_id"] == "testClientId"
        assert params["scope"] == "letter"
        assert params["state"] == "RANDOMGENERATEDSTRING"

    def test_authorize_url_staging(self):
        pingen2sdk.client_id = "testSetClientId"

        url = pingen2sdk.OAuth.authorize_url(
            use_staging=True, scope="letter", state="RANDOMGENERATEDSTRING"
        )

        result = requests.utils.urlparse(url)
        query = result.query
        params = dict(x.split("=") for x in query.split("&"))

        assert result.scheme == "https"
        assert result.netloc == "identity-staging.pingen.com"

        assert params["client_id"] == "testSetClientId"
        assert params["scope"] == "letter"
        assert params["state"] == "RANDOMGENERATEDSTRING"

    def test_token_error(self):
        with pytest.raises(pingen2sdk.error.AuthenticationError):
            pingen2sdk.client_id = "testSetClientId"

            pingen2sdk.OAuth.get_token(
                grant_type="client_credentials",
            )

    @responses.activate
    def test_token(self):
        pingen2sdk.client_id = "testSetClientId"

        responses.post(
            "https://api.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "YOUR_ACCESS_TOKEN",
            },
        )

        resp = pingen2sdk.OAuth.get_token(
            grant_type="client_credentials", client_secret="testClientSecret"
        )

        assert resp["access_token"] == "YOUR_ACCESS_TOKEN"

    @responses.activate
    def test_staging_token(self):
        pingen2sdk.client_id = "testSetClientId"
        pingen2sdk.client_secret = "testSetClientSecret"

        responses.post(
            "https://api-staging.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "YOUR_ACCESS_TOKEN",
            },
        )

        resp = pingen2sdk.OAuth.get_token(
            use_staging=True, grant_type="client_credentials"
        )

        assert resp["access_token"] == "YOUR_ACCESS_TOKEN"

    def test_get_token_from_implicit(self):
        resp = pingen2sdk.OAuth.get_token_from_implicit(
            "access_token=mock_access_token&token_type=Bearer&expires_in=43200&state=yourrandomstate"
        )

        assert resp["access_token"] == "mock_access_token"
        assert resp["expires_in"] == "43200"
