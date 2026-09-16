import pingen2sdk
import responses


class TestEbills(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        return pingen2sdk.Ebills(organisation_id, access_token)

    @staticmethod
    def _get_expected_payload(ebill_id: str):
        return {
            "data": {
                "id": ebill_id,
                "type": "ebills",
                "attributes": {
                    "status": "string",
                    "file_original_name": "test.pdf",
                    "file_pages": 2,
                    "recipient_identifier": "41100010014282213",
                    "recipient_address": "ACME GmbH\\nExamplestreet 432\\n3000 Bern",
                    "invoice_number": "Invoice 8051",
                    "invoice_date": "2025-10-01",
                    "invoice_due_date": "2025-10-30",
                    "invoice_value": 1250.3,
                    "invoice_currency": "CHF",
                    "invoice_iban": "CH8009000000854254426",
                    "invoice_address": "ACME GmbH\\nExamplestreet 432\\n3000 Bern",
                    "invoice_reference": "111119346200000000000127257",
                    "price_value": 1.25,
                    "price_currency": "CHF",
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
                    "batch": {
                        "links": {"related": "string"},
                        "data": {
                            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "type": "batches",
                        },
                    },
                },
                "links": {"self": "string"},
                "meta": {
                    "abilities": {
                        "self": {
                            "get-pdf-raw": "ok",
                            "get-pdf-validation": "ok",
                            "restore-original": "ok",
                            "delete": "ok",
                            "cancel": "ok",
                            "submit": "ok",
                            "apply-preset": "ok",
                            "create-preset": "ok",
                            "revalidate": "ok",
                            "fix-format": "ok",
                            "define-qr": "ok",
                            "define-invoice-date": "ok",
                            "define-invoice-due-date": "ok",
                            "define-recipient-identifier": "ok",
                            "define-invoice-number": "ok",
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
    def test_get_ebill(self):
        ebill_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills/%s"
            % (
                pingen2sdk.api_production,
                ebill_id,
            )
        )

        ebills = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"),
            status=200,
        )

        response = ebills.get_details(
            ebill_id, None, {"Content-Type": "application/vnd.api+json"}
        )

        assert response.data["data"]["id"] == ebill_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_get_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills"
            % pingen2sdk.api_production
        )

        ebills = self._construct_resource()

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
                        "type": "ebills",
                        "attributes": {
                            "status": "string",
                            "file_original_name": "test.pdf",
                            "file_pages": 2,
                            "recipient_identifier": "41100010014282213",
                            "invoice_number": "Invoice 8051",
                            "invoice_date": "2025-10-01",
                            "invoice_due_date": "2025-10-30",
                            "invoice_value": 1.25,
                            "invoice_currency": "CHF",
                            "price_value": 1.25,
                            "price_currency": "CHF",
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

        response = ebills.get_collection()

        assert response.data["data"][0]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_create_ebill(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills"
            % (pingen2sdk.api_production,)
        )

        ebills = self._construct_resource()

        responses.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"),
            status=201,
        )

        response = ebills.create(
            "https://s3.example/bucket/filename?signer=url",
            "$2y$10$BLOzVbYTXrh4LZbSYNVf7eEDrc58vvQ9PRVZABqV/9WS1eqIcm3M",
            "test.pdf",
            True,
            None,
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
    def test_upload_and_create_ebill(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills"
            % (pingen2sdk.api_production,)
        )

        ebills = self._construct_resource()
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

        response = ebills.upload_and_create(
            "tests/api_resources/files/test.pdf",
            "test.pdf",
            False,
            {
                "invoice_number": "Invoice 8051",
                "invoice_date": "2025-10-16",
                "invoice_due_date": "2025-10-30",
                "recipient_identifier": "41100010014282213",
            },
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx3",
        }

    @responses.activate
    def test_send_ebill(self):
        ebill_id = "testsend-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills/%s/send"
            % (pingen2sdk.api_production, ebill_id)
        )

        ebills = self._construct_resource()

        responses.patch(
            url,
            json=self._get_expected_payload(ebill_id),
            status=200,
        )

        response = ebills.send(ebill_id)

        assert response.data["data"]["id"] == ebill_id
        assert response.status_code == 200
        sent = responses.calls[0].request.body
        assert '"type": "ebills"' in sent
        assert '"id": "%s"' % ebill_id in sent

    @responses.activate
    def test_cancel_ebill(self):
        ebill_id = "testcanc-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills/%s/cancel"
            % (pingen2sdk.api_production, ebill_id)
        )

        ebills = self._construct_resource()

        responses.patch(url, status=202)

        response = ebills.cancel(ebill_id)

        assert response.status_code == 202

    @responses.activate
    def test_delete_ebill(self):
        ebill_id = "testdelx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills/%s"
            % (
                pingen2sdk.api_production,
                ebill_id,
            )
        )

        ebills = self._construct_resource()

        responses.delete(url, status=204)

        response = ebills.delete(ebill_id)

        assert response.status_code == 204

    @responses.activate
    def test_get_ebill_file(self):
        ebill_id = "testfile-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/ebills/%s/file"
            % (pingen2sdk.api_staging, ebill_id)
        )

        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        ebills = pingen2sdk.Ebills(organisation_id, access_token, True)

        responses.get(
            url,
            match=[responses.matchers.request_kwargs_matcher({"stream": True})],
        )

        ebills.get_file(ebill_id)
