"""OAuth integration test against the Pingen staging environment.

Verifies the stateful :class:`pingen2sdk.OAuth` token source end to end: a
client-credentials token can be obtained and used, it is reused while still
valid, and once it is close to expiry the next call transparently fetches a
fresh, working token.
"""

import pytest
import pingen2sdk

from tests.integration import support

pytestmark = pytest.mark.integration


class TestOAuthIntegration:
    def _build_oauth(self, credentials, staging):
        return pingen2sdk.OAuth(
            client_id=credentials["PINGEN2_CLIENT_ID"],
            client_secret=credentials["PINGEN2_CLIENT_SECRET"],
            use_staging=staging,
            scope=support.SCOPE,
        )

    def test_token_can_be_obtained_and_used(self, credentials, staging):
        oauth = self._build_oauth(credentials, staging)

        token = oauth.get_access_token()
        assert token, "Token request must succeed"
        assert oauth.get_current_token().expires_in > 0

        organisations = pingen2sdk.Organisations(oauth, staging)
        response = organisations.get_collection()
        assert response.status_code == 200
        assert response.data["data"], "Expected at least one organisation"

    def test_token_is_reused_while_valid(self, credentials, staging):
        oauth = self._build_oauth(credentials, staging)

        first = oauth.get_access_token()
        second = oauth.get_access_token()

        assert first == second

    def test_expired_token_is_refreshed(self, credentials, staging):
        oauth = self._build_oauth(credentials, staging)

        organisations = pingen2sdk.Organisations(oauth, staging)

        # Initial call acquires the first token and proves it works.
        assert organisations.get_collection().status_code == 200
        first_token = oauth.get_current_token()
        first_value = first_token.access_token

        # Backdate the token so it is treated as expiring within the refresh
        # buffer, guaranteeing a refresh on the next request.
        first_token.issued_at = first_token.issued_at - first_token.expires_in
        assert first_token.is_expired(oauth.TOKEN_REFRESH_BUFFER_SECONDS)

        # The next call must transparently fetch a brand-new, working token.
        assert organisations.get_collection().status_code == 200

        second_token = oauth.get_current_token()
        assert (
            second_token.access_token != first_value
        ), "A new access token must have been fetched"
        assert not second_token.is_expired()
