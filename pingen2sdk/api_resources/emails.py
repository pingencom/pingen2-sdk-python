import pingen2sdk
import json

from io import IOBase
from typing import Any, Mapping, Optional, Dict, Union


class Emails(object):
    def __init__(
        self,
        organisation_id: str,
        access_token: Union[str, "pingen2sdk.OAuth"],
        use_staging: bool = False,
    ):
        self.organisation_id = organisation_id
        self.api_requestor = pingen2sdk.APIRequestor(access_token, use_staging)

    def get_details(
        self,
        email_id: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/deliveries/emails/%s" % (self.organisation_id, email_id),
            params,
            supplied_headers,
        )

    def get_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/deliveries/emails" % self.organisation_id,
            params,
            supplied_headers,
        )

    def upload_and_create(
        self,
        path_to_file: str,
        file_original_name: str,
        auto_send: False,
        meta_data: Optional[Dict],
        relationships: Optional[Dict] = None,
    ) -> pingen2sdk.PingenResponse:
        file_upload = pingen2sdk.FileUpload(self.api_requestor)
        file_url, file_signature = file_upload.request_file_upload()
        file_upload.put_file(path_to_file, file_url)

        return self.create(
            file_url,
            file_signature,
            file_original_name,
            auto_send,
            meta_data,
            relationships,
        )

    def create(
        self,
        file_url: str,
        file_signature: str,
        file_original_name: str,
        auto_send: False,
        meta_data: Optional[Dict],
        relationships: Optional[Dict] = None,
    ) -> pingen2sdk.PingenResponse:
        attributes = {
            "file_original_name": file_original_name,
            "file_url": file_url,
            "file_url_signature": file_signature,
            "auto_send": auto_send,
            "meta_data": meta_data,
        }

        payload: Dict[str, Any] = {
            "data": {
                "type": "emails",
                "attributes": attributes,
            }
        }

        if relationships is not None:
            payload["data"]["relationships"] = relationships

        return self.api_requestor.perform_post_request(
            "/organisations/%s/deliveries/emails" % self.organisation_id,
            json.dumps(payload),
        )

    def cancel(
        self,
        email_id: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_cancel_request(
            "/organisations/%s/deliveries/emails/%s/cancel"
            % (self.organisation_id, email_id),
        )

    def delete(
        self,
        email_id: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_delete_request(
            "/organisations/%s/deliveries/emails/%s" % (self.organisation_id, email_id),
        )

    def get_file(
        self,
        email_id: str,
    ) -> IOBase:
        return self.api_requestor.perform_stream_request(
            "/organisations/%s/deliveries/emails/%s/file"
            % (self.organisation_id, email_id),
        )
