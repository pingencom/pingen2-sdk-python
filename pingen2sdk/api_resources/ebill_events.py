import pingen2sdk

from typing import Any, Mapping, Optional, Union


class EbillEvents(object):
    organisation_id: str
    api_requestor: pingen2sdk.APIRequestor

    def __init__(
        self,
        organisation_id: str,
        access_token: Union[str, "pingen2sdk.OAuth"],
        use_staging: bool = False,
    ):
        self.organisation_id = organisation_id
        self.api_requestor = pingen2sdk.APIRequestor(access_token, use_staging)

    def get_collection(
        self,
        ebill_id: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/deliveries/ebills/%s/events"
            % (self.organisation_id, ebill_id),
            params,
            supplied_headers,
        )
