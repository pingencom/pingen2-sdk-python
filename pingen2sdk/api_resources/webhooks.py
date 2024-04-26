import pingen2sdk
import json

from typing import Any, Mapping, Optional


class Webhooks(object):
    api_requestor: pingen2sdk.APIRequestor

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
        webhook_id: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/webhooks/%s" % (self.organisation_id, webhook_id),
            params,
            supplied_headers,
        )

    def get_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/webhooks" % self.organisation_id,
            params,
            supplied_headers,
        )

    def create(
        self, event_category: str, url: str, signing_key: str
    ) -> pingen2sdk.PingenResponse:
        attributes = {
            "event_category": event_category,
            "url": url,
            "signing_key": signing_key,
        }

        return self.api_requestor.perform_post_request(
            "/organisations/%s/webhooks" % self.organisation_id,
            json.dumps({"data": {"type": "webhooks", "attributes": attributes}}),
        )

    def delete(
        self,
        webhook_id: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_delete_request(
            "/organisations/%s/webhooks/%s" % (self.organisation_id, webhook_id),
        )
