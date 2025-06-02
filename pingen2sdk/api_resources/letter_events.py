import pingen2sdk

from typing import Any, Mapping, Optional


class LetterEvents(object):
    organisation_id: str
    api_requestor: pingen2sdk.APIRequestor

    def __init__(
        self,
        organisation_id: str,
        access_token: str,
        use_staging: bool = False,
    ):
        self.organisation_id = organisation_id
        self.api_requestor = pingen2sdk.APIRequestor(access_token, use_staging)

    def get_collection(
        self,
        letter_id: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/letters/%s/events" % (self.organisation_id, letter_id),
            params,
            supplied_headers,
        )

    def get_issue_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/letters/events/issues" % self.organisation_id,
            params,
            supplied_headers,
        )

    def get_undeliverable_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/letters/events/undeliverable" % self.organisation_id,
            params,
            supplied_headers,
        )

    def get_delivered_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/letters/events/delivered" % self.organisation_id,
            params,
            supplied_headers,
        )

    def get_sent_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/letters/events/sent" % self.organisation_id,
            params,
            supplied_headers,
        )
