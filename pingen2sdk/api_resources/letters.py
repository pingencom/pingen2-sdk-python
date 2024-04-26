import pingen2sdk
import json

from io import IOBase
from typing import Any, Mapping, Optional, Dict, List
from typing_extensions import Literal


class Letters(object):
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
        letter_id: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/letters/%s" % (self.organisation_id, letter_id),
            params,
            supplied_headers,
        )

    def get_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/letters" % self.organisation_id,
            params,
            supplied_headers,
        )

    def upload_and_create(
        self,
        path_to_file: str,
        file_original_name: str,
        address_position: Literal["left", "right"],
        auto_send: False,
        delivery_product: Optional[str] = None,
        print_mode: Optional[str] = None,
        print_spectrum: Optional[str] = None,
        sender_address: Optional[str] = None,
        meta_data: Optional[Dict] = None,
    ) -> pingen2sdk.PingenResponse:
        file_upload = pingen2sdk.FileUpload(self.api_requestor)
        file_url, file_signature = file_upload.request_file_upload()
        file_upload.put_file(path_to_file, file_url)

        return self.create(
            file_url,
            file_signature,
            file_original_name,
            address_position,
            auto_send,
            delivery_product,
            print_mode,
            print_spectrum,
            sender_address,
            meta_data,
        )

    def create(
        self,
        file_url: str,
        file_signature: str,
        file_original_name: str,
        address_position: Literal["left", "right"],
        auto_send: False,
        delivery_product: Optional[str] = None,
        print_mode: Optional[str] = None,
        print_spectrum: Optional[str] = None,
        sender_address: Optional[str] = None,
        meta_data: Optional[Dict] = None,
    ) -> pingen2sdk.PingenResponse:
        attributes = {
            "file_original_name": file_original_name,
            "file_url": file_url,
            "file_url_signature": file_signature,
            "address_position": address_position,
            "auto_send": auto_send,
        }

        if delivery_product is not None:
            attributes["delivery_product"] = delivery_product

        if print_mode is not None:
            attributes["print_mode"] = print_mode

        if print_spectrum is not None:
            attributes["print_spectrum"] = print_spectrum

        if sender_address is not None:
            attributes["sender_address"] = sender_address

        if meta_data is not None:
            attributes["meta_data"] = meta_data

        return self.api_requestor.perform_post_request(
            "/organisations/%s/letters" % self.organisation_id,
            json.dumps({"data": {"type": "letters", "attributes": attributes}}),
        )

    def send(
        self,
        letter_id: str,
        delivery_product: str,
        print_mode: str,
        print_spectrum: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_patch_request(
            "/organisations/%s/letters/%s/send" % (self.organisation_id, letter_id),
            json.dumps(
                {
                    "data": {
                        "id": letter_id,
                        "type": "letters",
                        "attributes": {
                            "delivery_product": delivery_product,
                            "print_mode": print_mode,
                            "print_spectrum": print_spectrum,
                        },
                    }
                }
            ),
        )

    def cancel(
        self,
        letter_id: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_cancel_request(
            "/organisations/%s/letters/%s/cancel" % (self.organisation_id, letter_id),
        )

    def delete(
        self,
        letter_id: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_delete_request(
            "/organisations/%s/letters/%s" % (self.organisation_id, letter_id),
        )

    def edit(
        self,
        letter_id: str,
        paper_types: List[str],
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_patch_request(
            "/organisations/%s/letters/%s" % (self.organisation_id, letter_id),
            json.dumps(
                {
                    "data": {
                        "id": letter_id,
                        "type": "letters",
                        "attributes": {
                            "paper_types": paper_types,
                        },
                    }
                }
            ),
        )

    def get_file(
        self,
        letter_id: str,
    ) -> IOBase:
        return self.api_requestor.perform_stream_request(
            "/organisations/%s/letters/%s/file" % (self.organisation_id, letter_id),
        )

    def calculate_price(
        self,
        country: str,
        paper_types: List[str],
        print_mode: str,
        print_spectrum: str,
        delivery_product: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_post_request(
            "/organisations/%s/letters/price-calculator" % self.organisation_id,
            json.dumps(
                {
                    "data": {
                        "type": "letter_price_calculator",
                        "attributes": {
                            "country": country,
                            "paper_types": paper_types,
                            "print_mode": print_mode,
                            "print_spectrum": print_spectrum,
                            "delivery_product": delivery_product,
                        },
                    }
                }
            ),
        )
