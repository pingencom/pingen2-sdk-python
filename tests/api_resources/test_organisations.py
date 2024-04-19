import pingen2sdk
import responses


class TestOrganisations(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"

        return pingen2sdk.Organisations(access_token, True)

    @responses.activate
    def test_get_details(self):
        organisation_id = "orgxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/%s" % (pingen2sdk.api_staging, organisation_id)

        organisations = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json={
                "data": {
                    "id": organisation_id,
                    "type": "organisations",
                    "attributes": {
                        "name": "ACME GmbH",
                        "status": "active",
                        "plan": "free",
                        "billing_mode": "prepaid",
                        "billing_currency": "CHF",
                        "billing_balance": 11.23,
                        "missing_credits": 0,
                        "default_country": "CH",
                        "edition": "string",
                        "default_address_position": "left",
                        "default_sender_address": "ACME GmbH | Strasse 3 | 8000 Zürich",
                        "data_retention_addresses": 18,
                        "data_retention_pdf": 12,
                        "color": "#0758FF",
                        "created_at": "2020-11-19T09:42:48+0100",
                        "updated_at": "2020-11-19T09:42:48+0100",
                    },
                    "relationships": {
                        "associations": {
                            "links": {
                                "related": {"href": "string", "meta": {"count": 0}}
                            }
                        }
                    },
                    "links": {"self": "string"},
                    "meta": {"abilities": {"self": {"manage": "ok"}}},
                },
                "included": [{}],
            },
            status=200,
        )

        response = organisations.get_details(organisation_id)

        assert response.data["data"]["id"] == organisation_id
        assert response.data["data"]["type"] == "organisations"
        assert response.status_code == 200

    @responses.activate
    def test_get_collection(self):
        organisation_id = "orgxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"
        url = "%s/organisations" % pingen2sdk.api_staging

        organisations = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json={
                "data": [
                    {
                        "id": organisation_id,
                        "type": "organisations",
                        "attributes": {
                            "name": "ACME GmbH",
                            "status": "active",
                            "plan": "free",
                            "billing_mode": "prepaid",
                            "billing_currency": "CHF",
                            "billing_balance": 11.23,
                            "missing_credits": 0,
                            "default_country": "CH",
                            "edition": "string",
                            "default_address_position": "left",
                            "default_sender_address": "ACME GmbH | Strasse 3 | 8000 Zürich",
                            "data_retention_addresses": 18,
                            "data_retention_pdf": 12,
                            "color": "#0758FF",
                            "created_at": "2020-11-19T09:42:48+0100",
                            "updated_at": "2020-11-19T09:42:48+0100",
                        },
                        "relationships": {
                            "associations": {
                                "links": {
                                    "related": {"href": "string", "meta": {"count": 0}}
                                }
                            }
                        },
                        "links": {"self": "string"},
                    }
                ],
                "included": [{}],
                "links": {
                    "first": "string",
                    "last": "string",
                    "prev": "string",
                    "next": "string",
                    "self": "string",
                },
                "meta": {
                    "current_page": 0,
                    "last_page": 0,
                    "per_page": 0,
                    "from": 0,
                    "to": 0,
                    "total": 0,
                },
            },
            status=200,
        )

        response = organisations.get_collection()

        assert response.data["data"][0]["id"] == organisation_id
        assert response.data["data"][0]["type"] == "organisations"
        assert response.data["data"][0]["attributes"]["name"] == "ACME GmbH"
        assert response.status_code == 200
