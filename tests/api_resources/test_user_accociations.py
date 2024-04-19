import pingen2sdk
import responses


class TestUsers(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"

        return pingen2sdk.UserAssociations(access_token, True)

    @responses.activate
    def test_get_details(self):
        user_id = "userxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx2"
        url = "%s/user/associations" % pingen2sdk.api_staging

        user_associations = self._construct_resource()

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json={
                "data": [
                    {
                        "id": user_id,
                        "type": "associations",
                        "attributes": {
                            "role": "owner",
                            "status": "pending",
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
                            }
                        },
                        "links": {"self": "string"},
                        "meta": {
                            "abilities": {
                                "self": {"join": "ok", "leave": "ok", "block": "ok"},
                                "organisation": {"manage": "ok"},
                            }
                        },
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

        response = user_associations.get_collection()

        assert response.data["data"][0]["id"] == user_id
        assert response.data["data"][0]["type"] == "associations"
        assert response.status_code == 200
