import pingen2sdk
import responses


class TestBatches(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        return pingen2sdk.Batches(organisation_id, access_token)

    @staticmethod
    def _get_expected_payload(batch_id: str):
        return {
            "data": {
                "id": batch_id,
                "type": "batches",
                "attributes": {
                    "name": "Monthly Invoicing August 2022",
                    "icon": "campaign",
                    "status": "string",
                    "file_original_name": "lorem.pdf",
                    "letter_count": 2,
                    "address_position": "left",
                    "print_mode": "simplex",
                    "print_spectrum": "color",
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
                        "links": {"related": {"href": "string", "meta": {"count": 0}}}
                    },
                },
                "links": {"self": "string"},
                "meta": {
                    "abilities": {
                        "self": {
                            "cancel": "ok",
                            "delete": "ok",
                            "submit": "ok",
                            "edit": "ok",
                            "change-window-position": "ok",
                            "add-attachment": "ok",
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
    def test_get_batch(self):
        batch_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches/%s" % (
            pingen2sdk.api_production,
            batch_id,
        )

        batches = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"),
            status=200,
        )

        response = batches.get_details(
            batch_id, None, {"Content-Type": "application/vnd.api+json"}
        )

        assert response.data["data"]["id"] == batch_id
        assert response.data["data"]["type"] == "batches"
        assert response.status_code == 200

    @responses.activate
    def test_get_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches"
            % pingen2sdk.api_production
        )

        batches = self._construct_resource()

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
                        "type": "batches",
                        "attributes": {
                            "status": "string",
                            "file_original_name": "lorem.pdf",
                            "file_pages": 2,
                            "address": "Hans Meier\nExample street 4\n8000 Zürich\nSwitzerland",
                            "address_position": "left",
                            "country": "CH",
                            "delivery_product": "fast",
                            "print_mode": "simplex",
                            "print_spectrum": "color",
                            "price_currency": "CHF",
                            "price_value": 1.25,
                            "paper_types": ["normal", "qr"],
                            "fonts": [
                                {"name": "Helvetica", "is_embedded": True},
                                {"name": "Helvetica-Bold", "is_embedded": False},
                            ],
                            "source": "api",
                            "tracking_number": "98.1234.11",
                            "sender_address": "ACME GmbH | Strasse 3 | 8000 Zürich",
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
                            "batch": {
                                "links": {"related": "string"},
                                "data": {
                                    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                                    "type": "batches",
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

        response = batches.get_collection()

        assert response.data["data"][0]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert response.data["data"][0]["type"] == "batches"
        assert response.status_code == 200

    @responses.activate
    def test_create_batch(self):
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches" % (
            pingen2sdk.api_production,
        )

        batches = self._construct_resource()

        responses.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"),
            status=201,
        )

        response = batches.create(
            "https://s3.example/bucket/filename?signer=url",
            "$2y$10$BLOzVbYTXrh4LZbSYNVf7eEDrc58vvQ9PRVZABqV/9WS1eqIcm3M",
            "lorem.pdf",
            "flash",
            "lorem.pdf",
            "left",
            "merge",
            "page",
            1,
            ",",
            "last_page",
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
        }

    @responses.activate
    def test_upload_and_create_batch(self):
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches" % (
            pingen2sdk.api_production,
        )

        batches = self._construct_resource()
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

        response = batches.upload_and_create(
            "tests/api_resources/files/lorem.pdf",
            "testing",
            "flash",
            "lorem.pdf",
            "left",
            "merge",
            "file",
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx3",
        }

    @responses.activate
    def test_send_batch(self):
        batch_id = "testsend-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches/%s/send"
            % (pingen2sdk.api_production, batch_id)
        )

        batches = self._construct_resource()

        responses.patch(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx332",
            },
            json=self._get_expected_payload(batch_id),
            status=200,
        )

        response = batches.send(
            batch_id,
            [
                {"country": "CH", "delivery_product": "postag_a"},
                {"country": "DE", "delivery_product": "fast"},
            ],
            "simplex",
            "color",
        )

        assert response.data["data"]["id"] == batch_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx332",
        }
        assert response.request_id == "requestx-xxxx-xxxx-xxxx-xxxxxxxxx332"

    @responses.activate
    def test_cancel_batch(self):
        batch_id = "testsend-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches/%s/cancel"
            % (pingen2sdk.api_production, batch_id)
        )

        batches = self._construct_resource()

        responses.patch(
            url,
            status=202,
        )

        response = batches.cancel(
            batch_id,
        )

        assert response.status_code == 202

    @responses.activate
    def test_delete_batch(self):
        batch_id = "testdelx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches/%s" % (
            pingen2sdk.api_production,
            batch_id,
        )

        batches = self._construct_resource()

        responses.delete(
            url,
            status=204,
        )

        response = batches.delete(
            batch_id,
        )

        assert response.status_code == 204

    @responses.activate
    def test_edit_batch(self):
        batch_id = "testedit-xxxx-xxxx-xxxx-xxxxxxxxx551"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches/%s" % (
            pingen2sdk.api_production,
            batch_id,
        )

        batches = self._construct_resource()

        responses.patch(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx552",
            },
            json=self._get_expected_payload(batch_id),
            status=200,
        )

        response = batches.edit(
            batch_id,
            list({"normal", "qr"}),
        )

        assert response.data["data"]["id"] == batch_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx552",
        }

    @responses.activate
    def test_get_statistics(self):
        batch_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxx321111"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/batches/%s/statistics"
            % (pingen2sdk.api_production, batch_id)
        )

        batches = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxx1332",
            },
            json={
                "data": {
                    "id": batch_id,
                    "type": "batch_statistics",
                    "attributes": {
                        "letter_validating": 2,
                        "letter_groups": [
                            {"name": "valid", "count": 3},
                            {"name": "not_available", "count": 1},
                        ],
                        "letter_countries": [
                            {"country": "CH", "count": 3},
                            {"country": "DE", "count": 1},
                        ],
                    },
                    "links": {"self": "string"},
                }
            },
            status=202,
        )

        response = batches.get_statistics(batch_id)

        assert response.data["data"]["id"] == batch_id
        assert response.data["data"]["type"] == "batch_statistics"
