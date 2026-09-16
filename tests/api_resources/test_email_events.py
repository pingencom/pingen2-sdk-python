import pingen2sdk
import responses


def _mock_events_response():
    return {
        "data": [
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "type": "deliverables_events",
                "attributes": {
                    "code": "undeliverable",
                    "name": "Content failed inspection",
                    "producer": "Pingen",
                    "location": "8051 Zürich, CH",
                    "has_image": False,
                    "data": ["string"],
                    "emitted_at": "2020-11-19T09:42:48+0100",
                    "created_at": "2020-11-19T09:42:48+0100",
                    "updated_at": "2020-11-19T09:42:48+0100",
                },
                "relationships": {
                    "email": {
                        "links": {"related": "string"},
                        "data": {
                            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                            "type": "emails",
                        },
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
            "current_page": 1,
            "last_page": 1,
            "per_page": 10,
            "from": 1,
            "to": 1,
            "total": 1,
        },
    }


class TestEmailEvents(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"
        organisation_id = "testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"

        return pingen2sdk.EmailEvents(organisation_id, access_token)

    @responses.activate
    def test_get_collection(self):
        email_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = (
            "%s/organisations/testxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1/deliveries/emails/%s/events"
            % (pingen2sdk.api_production, email_id)
        )

        email_events = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json=_mock_events_response(),
            status=200,
        )

        response = email_events.get_collection(
            email_id, None, {"Content-Type": "application/vnd.api+json"}
        )

        assert response.data["data"][0]["type"] == "deliverables_events"
        assert response.status_code == 200
