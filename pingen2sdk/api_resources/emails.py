import pingen2sdk
import json

from typing import Any, Mapping, Optional, Dict


class Emails(object):
    def __init__(
        self,
        organisation_id: str,
        access_token: str,
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
        )

    def create(
        self,
        file_url: str,
        file_signature: str,
        file_original_name: str,
        auto_send: False,
        meta_data: Optional[Dict],
    ) -> pingen2sdk.PingenResponse:
        attributes = {
            "file_original_name": file_original_name,
            "file_url": file_url,
            "file_url_signature": file_signature,
            "auto_send": auto_send,
            "meta_data": meta_data,
        }

        return self.api_requestor.perform_post_request(
            "/organisations/%s/deliveries/emails" % self.organisation_id,
            json.dumps({"data": {"type": "emails", "attributes": attributes}}),
        )
