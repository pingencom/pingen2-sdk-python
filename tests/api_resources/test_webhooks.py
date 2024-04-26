import pingen2sdk
import responses
import pytest


class TestWebhooks(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        return pingen2sdk.Webhooks(organisation_id, access_token)

    @staticmethod
    def _get_expected_payload(webhook_id: str):
        return {
            "data": {
                "id": webhook_id,
                "type": "webhooks",
                "attributes": {
                    "event_category": "issues",
                    "url": "https://valid-url",
                    "signing_key": "d09a095a0d1d2ae896f985c0fff1ad51",
                },
                "relationships": {
                    "organisation": {
                        "links": {"related": "string"},
                        "data": {
                            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "type": "organisations",
                        },
                    },
                },
                "links": {"self": "string"},
            },
            "included": [{}],
        }

    @responses.activate
    def test_get_details(self):
        webhook_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/webhooks/%s" % (
            pingen2sdk.api_production,
            webhook_id,
        )

        webhooks = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"),
            status=200,
        )

        response = webhooks.get_details(
            webhook_id, None, {"Content-Type": "application/vnd.api+json"}
        )

        assert response.data["data"]["id"] == webhook_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_get_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/webhooks"
            % pingen2sdk.api_production
        )

        webhooks = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json={
                "data": [
                    {
                        "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                        "type": "webhooks",
                        "attributes": {
                            "event_category": "issues",
                            "url": "https://valid-url",
                            "signing_key": "d09a095a0d1d2ae896f985c0fff1ad51",
                        },
                        "relationships": {
                            "organisation": {
                                "links": {"related": "string"},
                                "data": {
                                    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                                    "type": "organisations",
                                },
                            },
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

        response = webhooks.get_collection()

        assert response.data["data"][0]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_create(self):
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/webhooks" % (
            pingen2sdk.api_production,
        )

        webhooks = self._construct_resource()

        responses.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"),
            status=201,
        )

        response = webhooks.create(
            "issues",
            "https://valid-url",
            "d09a095a0d1d2ae896f985c0fff1ad51",
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
        }

    @responses.activate
    def test_delete(self):
        webhook_id = "testdelx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/webhooks/%s" % (
            pingen2sdk.api_production,
            webhook_id,
        )

        webhooks = self._construct_resource()

        responses.delete(
            url,
            status=204,
        )

        response = webhooks.delete(
            webhook_id,
        )

        assert response.status_code == 204

    @responses.activate
    def test_delete_unauthorize(self):
        with pytest.raises(pingen2sdk.PingenError):
            webhook_id = "testdelx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
            url = (
                "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/webhooks/%s"
                % (
                    pingen2sdk.api_production,
                    webhook_id,
                )
            )

            webhooks = self._construct_resource()

            responses.delete(
                url,
                json={
                    "errors": {
                        "code": "access_denied",
                        "title": "The resource owner or authorization server denied the request.",
                        "detail": "The JWT string must have two dots",
                        "source": {"pointer": None, "parameter": None},
                    }
                },
                status=401,
            )

            webhooks.delete(
                webhook_id,
            )
