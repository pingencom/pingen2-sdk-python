import pingen2sdk
import responses


class TestEmails(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        return pingen2sdk.Emails(organisation_id, access_token)

    @staticmethod
    def _get_expected_payload(email_id: str):
        return {
            "data": {
                "id": email_id,
                "type": "emails",
                "attributes": {
                    "status": "string",
                    "file_original_name": "lorem.pdf",
                    "file_pages": 2,
                    "recipient_identifier": "info@example.com",
                    "price_currency": "CHF",
                    "price_value": 1.25,
                    "source": "api",
                    "submitted_at": "2021-11-19T09:42:48+0100",
                    "created_at": "2020-11-19T09:42:48+0100",
                    "updated_at": "2020-11-19T09:42:48+0100",
                },
                "relationships": {
                    "organisation": {
                        "links": {"related": "string"},
                        "data": {
                            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "type": "organisations",
                        },
                    },
                    "events": {
                        "links": {
                            "related": {"href": "string", "meta": {"count": 0}}
                        }
                    },
                },
                "links": {"self": "string"},
                "meta": {
                    "abilities": {
                        "self": {
                            "delete": "ok",
                        }
                    }
                },
            },
            "included": [{}],
        }

    @staticmethod
    def mock_file_upload_request():
        responses.get(
            "%s/file-upload" % (pingen2sdk.api_production,),
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json={
                "data": {
                    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "type": "file_uploads",
                    "attributes": {
                        "url": "https://s3.example/bucket/filename?signer=url",
                        "url_signature": "$2y$10$BLOzVbYTXrh4LZbSYNVf7eEDrc58vvQ9PRVZABqV/9WS1eqIcm3M",
                        "expires_at": "2020-11-19T09:42:48+0100",
                    },
                    "links": {"self": "string"},
                }
            },
        )

        responses.put("https://s3.example/bucket/filename?signer=url", status=201)

    @responses.activate
    def test_get_email(self):
        email_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/emails/%s" % (
            pingen2sdk.api_production,
            email_id,
        )

        emails = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"),
            status=200,
        )

        response = emails.get_details(
            email_id, None, {"Content-Type": "application/vnd.api+json"}
        )

        assert response.data["data"]["id"] == email_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_get_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/emails"
            % pingen2sdk.api_production
        )

        emails = self._construct_resource()

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
                        "type": "emails",
                        "attributes": {
                            "status": "string",
                            "file_original_name": "lorem.pdf",
                            "file_pages": 2,
                            "recipient_identifier": "info@example.com",
                            "price_currency": "CHF",
                            "price_value": 1.25,
                            "source": "api",
                            "submitted_at": "2021-11-19T09:42:48+0100",
                            "created_at": "2020-11-19T09:42:48+0100",
                            "updated_at": "2020-11-19T09:42:48+0100",
                        },
                        "relationships": {
                            "organisation": {
                                "links": {"related": "string"},
                                "data": {
                                    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                                    "type": "organisations",
                                },
                            },
                            "events": {
                                "links": {
                                    "related": {"href": "string", "meta": {"count": 0}}
                                }
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

        response = emails.get_collection()

        assert response.data["data"][0]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_create_email(self):
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/emails" % (
            pingen2sdk.api_production,
        )

        emails = self._construct_resource()

        responses.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"),
            status=201,
        )

        response = emails.create(
            "https://s3.example/bucket/filename?signer=url",
            "$2y$10$BLOzVbYTXrh4LZbSYNVf7eEDrc58vvQ9PRVZABqV/9WS1eqIcm3M",
            "lorem.pdf",
            True,
            {
                "sender_name": "ACME GmbH",
                "recipient_email": "info@acme.com",
                "recipient_name": "ACME AG",
                "reply_email": "info@acme.com",
                "reply_name": "ACME AG",
                "subject": "Your new invoice Number xyz",
                "content": "Dear recipient\\n\\nAttached is your invoice",
            },
            {
                "preset": {
                    "data": {
                        "id": "xxxxxxxx-xxxx-xxxx-0000-xxxxxxxxx111",
                        "type": "presets",
                    }
                }
            },
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
        }

    @responses.activate
    def test_upload_and_create_email(self):
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/emails" % (
            pingen2sdk.api_production,
        )

        emails = self._construct_resource()
        self.mock_file_upload_request()

        responses.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx3",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111"),
            status=201,
        )

        response = emails.upload_and_create(
            "tests/api_resources/files/lorem.pdf",
            "lorem.pdf",
            False,
            None,
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx3",
        }
