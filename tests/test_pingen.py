import pingen2sdk
import responses


class TestPingen(object):
    @responses.activate
    def test_facade_wires_resources_and_reuses_token(self):
        responses.post(
            "https://api-staging.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "FACADE_TOKEN",
            },
        )
        responses.get(
            "https://api-staging.pingen.com/organisations",
            json={
                "data": [
                    {
                        "id": "org-1",
                        "type": "organisations",
                        "attributes": {"name": "Acme"},
                    }
                ]
            },
            status=200,
        )
        responses.get(
            "https://api-staging.pingen.com/organisations/org-1/deliveries/letters",
            json={"data": []},
            status=200,
        )

        pingen = pingen2sdk.Pingen(
            client_id="cid",
            client_secret="secret",
            use_staging=True,
            scope="letter",
        )

        orgs = pingen.organisations().get_collection()
        assert orgs.status_code == 200
        assert orgs.data["data"][0]["id"] == "org-1"

        letters = pingen.letters("org-1").get_collection()
        assert letters.status_code == 200

        # The token is fetched once and reused across every resource.
        token_calls = [
            call
            for call in responses.calls
            if call.request.url.endswith("/auth/access-tokens")
        ]
        assert len(token_calls) == 1

        # Both API calls carried the shared bearer token.
        api_calls = [
            call for call in responses.calls if "/organisations" in call.request.url
        ]
        assert api_calls
        assert all(
            call.request.headers["Authorization"] == "Bearer FACADE_TOKEN"
            for call in api_calls
        )

    def test_all_resource_factories(self):
        pingen = pingen2sdk.Pingen(
            client_id="cid", client_secret="secret", use_staging=True
        )
        org_id = "org-1"

        assert isinstance(pingen.get_oauth(), pingen2sdk.OAuth)
        assert isinstance(pingen.organisations(), pingen2sdk.Organisations)
        assert isinstance(pingen.users(), pingen2sdk.Users)
        assert isinstance(pingen.user_associations(), pingen2sdk.UserAssociations)
        assert isinstance(pingen.letters(org_id), pingen2sdk.Letters)
        assert isinstance(pingen.letter_events(org_id), pingen2sdk.LetterEvents)
        assert isinstance(pingen.batches(org_id), pingen2sdk.Batches)
        assert isinstance(pingen.batch_events(org_id), pingen2sdk.BatchEvents)
        assert isinstance(pingen.webhooks(org_id), pingen2sdk.Webhooks)
        assert isinstance(pingen.emails(org_id), pingen2sdk.Emails)
        assert isinstance(pingen.email_events(org_id), pingen2sdk.EmailEvents)
        assert isinstance(pingen.ebills(org_id), pingen2sdk.Ebills)
        assert isinstance(pingen.ebill_events(org_id), pingen2sdk.EbillEvents)

    @responses.activate
    def test_get_access_token_delegates(self):
        responses.post(
            "https://api-staging.pingen.com/auth/access-tokens",
            json={
                "token_type": "Bearer",
                "expires_in": 43200,
                "access_token": "FACADE_TOK",
            },
        )

        pingen = pingen2sdk.Pingen(
            client_id="cid",
            client_secret="secret",
            use_staging=True,
            scope="letter",
        )

        assert pingen.get_access_token() == "FACADE_TOK"

    def test_accepts_existing_oauth(self):
        oauth = pingen2sdk.OAuth(
            client_id="cid", client_secret="secret", use_staging=True
        )
        pingen = pingen2sdk.Pingen(oauth=oauth, use_staging=True)

        assert pingen.get_oauth() is oauth
        assert pingen.letters("org-1").api_requestor._token_source is oauth

    def test_staging_flag_propagates_to_resources(self):
        staging = pingen2sdk.Pingen(
            client_id="cid", client_secret="secret", use_staging=True
        )
        assert staging.letters("org-1").api_requestor.api_base == pingen2sdk.api_staging

        production = pingen2sdk.Pingen(client_id="cid", client_secret="secret")
        prod_base = production.organisations().api_requestor.api_base
        assert prod_base == pingen2sdk.api_production
