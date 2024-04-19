import pingen2sdk
import responses


class TestUsers(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"

        return pingen2sdk.Users(access_token, True)

    @responses.activate
    def test_get_details(self):
        user_id = "userxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx1"
        url = "%s/user" % pingen2sdk.api_staging

        users = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json={
                "data": {
                    "id": user_id,
                    "type": "users",
                    "attributes": {
                        "email": "email",
                        "first_name": "John",
                        "last_name": "Snow",
                        "status": "active",
                        "language": "en-GB",
                        "edition": "string",
                        "created_at": "2020-11-19T09:42:48+0100",
                        "updated_at": "2020-11-19T09:42:48+0100",
                    },
                    "relationships": {
                        "associations": {
                            "links": {
                                "related": {"href": "string", "meta": {"count": 0}}
                            }
                        },
                        "notifications": {
                            "links": {
                                "related": {"href": "string", "meta": {"count": 0}}
                            }
                        },
                    },
                    "links": {"self": "string"},
                    "meta": {
                        "abilities": {
                            "self": {
                                "reach": "ok",
                                "act": "ok",
                                "resend-activation": "ok",
                            }
                        }
                    },
                },
                "included": [{}],
            },
            status=200,
        )

        response = users.get_details()

        assert response.data["data"]["id"] == user_id
        assert response.data["data"]["type"] == "users"
        assert response.data["data"]["attributes"]["email"] == "email"
        assert response.status_code == 200
