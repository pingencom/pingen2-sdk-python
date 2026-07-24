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

    @responses.activate
    def test_stateful_oauth_reuses_token(self):
        responses.post(
            "https://api-staging.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "REUSED_TOKEN",
            },
        )

        oauth = pingen2sdk.OAuth(
            client_id="testClientId",
            client_secret="testClientSecret",
            use_staging=True,
            scope="letter",
        )

        assert oauth.get_current_token() is None

        first = oauth.get_access_token()
        second = oauth.get_access_token()

        assert first == "REUSED_TOKEN"
        assert second == "REUSED_TOKEN"
        # Only one token request – the cached token is reused.
        assert len(responses.calls) == 1

    @responses.activate
    def test_stateful_oauth_refreshes_expired_token(self):
        responses.post(
            "https://api-staging.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "FIRST_TOKEN",
            },
        )

        oauth = pingen2sdk.OAuth(
            client_id="testClientId",
            client_secret="testClientSecret",
            use_staging=True,
            scope="letter",
        )

        first = oauth.get_access_token()
        assert first == "FIRST_TOKEN"

        # Backdate the cached token so it is treated as expiring within the
        # refresh buffer, forcing the next call to fetch a new token.
        token = oauth.get_current_token()
        token.issued_at = token.issued_at - token.expires_in

        responses.replace(
            responses.POST,
            "https://api-staging.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "SECOND_TOKEN",
            },
        )

        second = oauth.get_access_token()

        assert second == "SECOND_TOKEN"
        assert len(responses.calls) == 2

    @responses.activate
    def test_stateful_oauth_falls_back_to_module_credentials(self):
        pingen2sdk.client_id = "moduleClientId"
        pingen2sdk.client_secret = "moduleClientSecret"

        responses.post(
            "https://api-staging.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "MODULE_TOKEN",
            },
        )

        # No client_id / client_secret / scope on the instance -> the _fetch_token
        # "None" branches are taken and the module-level credentials are used.
        oauth = pingen2sdk.OAuth(use_staging=True)

        assert oauth.get_access_token() == "MODULE_TOKEN"

    def test_access_token_is_expired(self):
        import time

        fresh = pingen2sdk.AccessToken("t", 43200)
        assert fresh.is_expired() is False

        expiring_soon = pingen2sdk.AccessToken(
            "t", 43200, issued_at=time.time() - (43200 - 100)
        )
        assert expiring_soon.is_expired(buffer_seconds=300) is True

        past = pingen2sdk.AccessToken("t", 60, issued_at=time.time() - 120)
        assert past.is_expired(buffer_seconds=0) is True
