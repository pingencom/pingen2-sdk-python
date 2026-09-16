"""Pytest fixtures shared by the integration test suite.

All fixtures are session scoped: a single access token and organisation lookup
are acquired once and reused across every test.
"""

import pytest
import pingen2sdk

from tests.integration import support


@pytest.fixture(scope="session")
def credentials():
    creds = support.load_credentials()
    if support.missing_credentials(creds):
        pytest.skip(
            "Integration credentials not configured. Copy .env.example to .env "
            "and fill in PINGEN2_CLIENT_ID / PINGEN2_CLIENT_SECRET."
        )
    return creds


@pytest.fixture(scope="session")
def access_token(credentials):
    pingen2sdk.client_id = credentials["PINGEN2_CLIENT_ID"]
    pingen2sdk.client_secret = credentials["PINGEN2_CLIENT_SECRET"]

    resp = pingen2sdk.OAuth.get_token(
        use_staging=support.USE_STAGING,
        grant_type="client_credentials",
        scope=support.SCOPE,
    )

    if "access_token" not in resp:
        pytest.fail("Failed to obtain access token from Pingen: %s" % resp)

    return resp["access_token"]


@pytest.fixture(scope="session")
def organisations(access_token):
    return pingen2sdk.Organisations(access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def organisation_id(credentials, organisations):
    configured = credentials.get("PINGEN2_ORGANISATION_ID")
    if configured:
        print("Using organisation ID from .env: %s" % configured)
        return configured

    response = organisations.get_collection()
    items = response.data["data"]
    assert items, "No organisations returned – check the staging credentials."
    org_id = items[0]["id"]
    print("Using first organisation ID: %s" % org_id)
    return org_id


@pytest.fixture(scope="session")
def document_path():
    return support.document_path()


@pytest.fixture(scope="session")
def letters(organisation_id, access_token):
    return pingen2sdk.Letters(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def letter_events(organisation_id, access_token):
    return pingen2sdk.LetterEvents(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def batches(organisation_id, access_token):
    return pingen2sdk.Batches(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def batch_events(organisation_id, access_token):
    return pingen2sdk.BatchEvents(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def webhooks(organisation_id, access_token):
    return pingen2sdk.Webhooks(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def emails(organisation_id, access_token):
    return pingen2sdk.Emails(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def email_events(organisation_id, access_token):
    return pingen2sdk.EmailEvents(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def ebills(organisation_id, access_token):
    return pingen2sdk.Ebills(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def ebill_events(organisation_id, access_token):
    return pingen2sdk.EbillEvents(organisation_id, access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def users(access_token):
    return pingen2sdk.Users(access_token, support.USE_STAGING)


@pytest.fixture(scope="session")
def user_associations(access_token):
    return pingen2sdk.UserAssociations(access_token, support.USE_STAGING)
