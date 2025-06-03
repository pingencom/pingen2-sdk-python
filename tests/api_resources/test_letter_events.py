import pingen2sdk
import responses


def _mock_empty_response():
    return {
        "data": [{}],
        "links": {
            "first": "string",
            "last": "string",
            "prev": "string",
            "next": "string",
            "self": "string",
        },
        "meta": {
            "current_page": 2,
            "last_page": 3,
            "per_page": 10,
            "from": 10,
            "to": 19,
            "total": 30,
        },
    }


class TestLetterEvents(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        return pingen2sdk.LetterEvents(organisation_id, access_token)

    @responses.activate
    def test_get_collection(self):
        letter_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/%s/events"
            % (
                pingen2sdk.api_production,
                letter_id,
            )
        )

        letters_events = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=_mock_empty_response(),
            status=200,
        )

        response = letters_events.get_collection(
            letter_id, None, {"Content-Type": "application/vnd.api+json"}
        )

        assert len(response.data["data"][0]) == 0
        assert response.status_code == 200

    @responses.activate
    def test_get_issue_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/events/issues"
            % pingen2sdk.api_production
        )

        letters_events = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=_mock_empty_response(),
            status=200,
        )

        response = letters_events.get_issue_collection()

        assert len(response.data["data"][0]) == 0
        assert response.status_code == 200

    @responses.activate
    def test_get_undeliverable_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/events/undeliverable"
            % pingen2sdk.api_production
        )

        letters_events = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=_mock_empty_response(),
            status=200,
        )

        response = letters_events.get_undeliverable_collection()

        assert len(response.data["data"][0]) == 0
        assert response.status_code == 200

    @responses.activate
    def test_get_sent_collection(self):
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/events/sent"
            % pingen2sdk.api_production
        )

        letters_events = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=_mock_empty_response(),
            status=200,
        )

        response = letters_events.get_sent_collection()

        assert len(response.data["data"][0]) == 0
        assert response.status_code == 200

    @responses.activate
    def test_get_delivered_collection(self):
        url = (
                "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/letters/events/delivered"
                % pingen2sdk.api_production
        )

        letters_events = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=_mock_empty_response(),
            status=200,
        )

        response = letters_events.get_delivered_collection()

        assert len(response.data["data"][0]) == 0
        assert response.status_code == 200
