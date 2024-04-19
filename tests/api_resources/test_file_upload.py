import pingen2sdk
import responses


class TestFileUpload(object):
    @staticmethod
    def _construct_resource():
        access_token = "test_access_token"

        return pingen2sdk.FileUpload(pingen2sdk.APIRequestor(access_token))

    @responses.activate
    def test_request_file_upload(self):
        url = "%s/file-upload" % (pingen2sdk.api_production,)

        file_upload = self._construct_resource()

        expected_url = "https://s3.example/bucket/filename?signer=url"
        expected_signature = (
            "$2y$10$BLOzVbYTXrh4LZbSYNVf7eEDrc58vvQ9PRVZABqV/9WS1eqIcm3M"
        )

        responses.get(
            url,
            headers={
                "Content-Type": "application/vnd.api+json",
                "X-Request-Id": "requestx-xxxx-xxxx-xxxx-xxxxxxxxxxx1",
            },
            json={
                "data": {
                    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "type": "file_uploads",
                    "attributes": {
                        "url": expected_url,
                        "url_signature": expected_signature,
                        "expires_at": "2020-11-19T09:42:48+0100",
                    },
                    "links": {"self": "string"},
                }
            },
        )

        url, url_signature = file_upload.request_file_upload()

        assert url == expected_url
        assert url_signature == expected_signature
