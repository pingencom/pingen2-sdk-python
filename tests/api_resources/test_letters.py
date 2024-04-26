import pingen2sdk
import responses
import pytest


class TestLetters(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        return pingen2sdk.Letters(organisation_id, access_token)

    @staticmethod
    def _get_expected_payload(letter_id: str):
        return {
            "data": {
                "id": letter_id,
                "type": "letters",
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
                            "related": {
                                "href": "string",
                                "meta": {"count": 0},
                            }
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
                "meta": {
                    "abilities": {
                        "self": {
                            "cancel": "ok",
                            "delete": "ok",
                            "submit": "ok",
                            "send-simplex": "ok",
                            "edit": "ok",
                            "get-pdf-raw": "ok",
                            "get-pdf-validation": "ok",
                            "change-paper-type": "ok",
                            "change-window-position": "ok",
                            "create-coverpage": "ok",
                            "add-attachment": "ok",
                            "fix-overwrite-restricted-areas": "ok",
                            "fix-coverpage": "ok",
                            "fix-country": "ok",
                            "fix-regular-paper": "ok",
                            "fix-address": "ok",
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
    def test_get_letter(self):
        letter_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s" % (
            pingen2sdk.api_production,
            letter_id,
        )

        letters = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"),
            status=200,
        )

        response = letters.get_details(
            letter_id, None, {"Content-Type": "application/vnd.api+json"}
        )

        assert response.data["data"]["id"] == letter_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_get_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters"
            % pingen2sdk.api_production
        )

        letters = self._construct_resource()

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
                        "type": "letters",
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

        response = letters.get_collection()

        assert response.data["data"][0]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
        }

    @responses.activate
    def test_create_letter(self):
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters" % (
            pingen2sdk.api_production,
        )

        letters = self._construct_resource()

        responses.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
            },
            json=self._get_expected_payload("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"),
            status=201,
        )

        response = letters.create(
            "https://s3.example/bucket/filename?signer=url",
            "$2y$10$BLOzVbYTXrh4LZbSYNVf7eEDrc58vvQ9PRVZABqV/9WS1eqIcm3M",
            "lorem.pdf",
            "left",
            True,
            "fast",
            "simplex",
            "color",
            "ACME GmbH | Strasse 3 | 8000 Zürich",
            {
                "recipient": {
                    "name": "R_Example",
                    "street": "R_Street",
                    "number": "R_12 ",
                    "zip": "R_12",
                    "city": "R_Warsaw",
                    "country": "PL",
                },
                "sender": {
                    "name": "S_Example",
                    "street": "S_Street",
                    "number": "S_12 ",
                    "zip": "S_12",
                    "city": "S_Warsaw",
                    "country": "PL",
                },
            },
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx11"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx2",
        }

    @responses.activate
    def test_upload_and_create_letter(self):
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters" % (
            pingen2sdk.api_production,
        )

        letters = self._construct_resource()
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

        response = letters.upload_and_create(
            "tests/api_resources/files/lorem.pdf",
            "lorem.pdf",
            "left",
            False,
        )

        assert response.data["data"]["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx111"
        assert response.status_code == 201
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx3",
        }

    @responses.activate
    def test_send_letter(self):
        letter_id = "testsend-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s/send"
            % (pingen2sdk.api_production, letter_id)
        )

        letters = self._construct_resource()

        responses.patch(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx332",
            },
            json=self._get_expected_payload(letter_id),
            status=200,
        )

        response = letters.send(
            letter_id,
            "fast",
            "simplex",
            "color",
        )

        assert response.data["data"]["id"] == letter_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx332",
        }
        assert response.request_id == "requestx-xxxx-xxxx-xxxx-xxxxxxxxx332"

    @responses.activate
    def test_cancel_letter(self):
        letter_id = "testsend-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s/cancel"
            % (pingen2sdk.api_production, letter_id)
        )

        letters = self._construct_resource()

        responses.patch(
            url,
            status=202,
        )

        response = letters.cancel(
            letter_id,
        )

        assert response.status_code == 202

    @responses.activate
    def test_delete_letter(self):
        letter_id = "testdelx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s" % (
            pingen2sdk.api_production,
            letter_id,
        )

        letters = self._construct_resource()

        responses.delete(
            url,
            status=204,
        )

        response = letters.delete(
            letter_id,
        )

        assert response.status_code == 204

    @responses.activate
    def test_delete_letter_unauthorize(self):
        with pytest.raises(pingen2sdk.PingenError):
            letter_id = "testdelx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
            url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s" % (
                pingen2sdk.api_production,
                letter_id,
            )

            letters = self._construct_resource()

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

            letters.delete(
                letter_id,
            )

    @responses.activate
    def test_edit_letter(self):
        letter_id = "testedit-xxxx-xxxx-xxxx-xxxxxxxxx551"
        url = "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s" % (
            pingen2sdk.api_production,
            letter_id,
        )

        letters = self._construct_resource()

        responses.patch(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx552",
            },
            json=self._get_expected_payload(letter_id),
            status=200,
        )

        response = letters.edit(
            letter_id,
            list({"normal", "qr"}),
        )

        assert response.data["data"]["id"] == letter_id
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxx552",
        }

    @responses.activate
    def test_get_letter_file(self):
        letter_id = "testsend-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s/file"
            % (pingen2sdk.api_staging, letter_id)
        )

        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        letters = pingen2sdk.Letters(organisation_id, access_token, True)

        responses.get(
            url,
            match=[responses.matchers.request_kwargs_matcher({"stream": True})],
        )

        letters.get_file(
            letter_id,
        )

    @responses.activate
    def test_calculate_price(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/price-calculator"
            % pingen2sdk.api_production
        )

        letters = self._construct_resource()

        responses.post(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxx1332",
            },
            json={
                "data": {
                    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "type": "letter_price_calculator",
                    "attributes": {"currency": "CHF", "price": 12.12},
                    "links": {"self": "string"},
                }
            },
            status=200,
        )

        response = letters.calculate_price(
            "CH",
            list({"normal", "qr"}),
            "simplex",
            "color",
            "fast",
        )

        assert response.data["data"]["attributes"] == {
            "currency": "CHF",
            "price": 12.12,
        }
        assert response.status_code == 200
        assert response.headers == {
            "Content-Type": "application/vnd.api+json",
            "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxx1332",
        }
