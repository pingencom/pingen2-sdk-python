import pingen2sdk
import json

from typing import Any, Dict, Mapping, Optional, List, Union
from typing_extensions import Literal


class Batches(object):
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
        batch_id: str,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/batches/%s" % (self.organisation_id, batch_id),
            params,
            supplied_headers,
        )

    def get_collection(
        self,
        params: Optional[Mapping[str, Any]] = None,
        supplied_headers: Optional[Mapping[str, str]] = None,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/batches" % self.organisation_id,
            params,
            supplied_headers,
        )

    def upload_and_create(
        self,
        path_to_file: str,
        name: str,
        icon: Literal[
            "campaign",
            "megaphone",
            "wave-hand",
            "flash",
            "rocket",
            "bell",
            "percent-tag",
            "percent-badge",
            "present",
            "receipt",
            "document",
            "information",
            "calendar",
            "newspaper",
            "crown",
            "virus",
        ],
        file_original_name: str,
        address_position: Literal["left", "right"],
        grouping_type: Literal["zip", "merge"],
        grouping_options_split_type: Literal["file", "page", "custom", "qr_invoice"],
        grouping_options_split_size: Optional[int] = None,
        grouping_options_split_separator: Optional[str] = None,
        grouping_options_split_position: Optional[
            Literal["first_page", "last_page"]
        ] = None,
        channel_type: Optional[Literal["post", "email", "ebill"]] = None,
    ) -> pingen2sdk.PingenResponse:
        file_upload = pingen2sdk.FileUpload(self.api_requestor)
        file_url, file_url_signature = file_upload.request_file_upload()
        file_upload.put_file(path_to_file, file_url)

        return self.create(
            file_url,
            file_url_signature,
            name,
            icon,
            file_original_name,
            address_position,
            grouping_type,
            grouping_options_split_type,
            grouping_options_split_size,
            grouping_options_split_separator,
            grouping_options_split_position,
            channel_type,
        )

    def create(
        self,
        file_url: str,
        file_url_signature: str,
        name: str,
        icon: Literal[
            "campaign",
            "megaphone",
            "wave-hand",
            "flash",
            "rocket",
            "bell",
            "percent-tag",
            "percent-badge",
            "present",
            "receipt",
            "document",
            "information",
            "calendar",
            "newspaper",
            "crown",
            "virus",
        ],
        file_original_name: str,
        address_position: Literal["left", "right"],
        grouping_type: Literal["zip", "merge"],
        grouping_options_split_type: Literal["file", "page", "custom", "qr_invoice"],
        grouping_options_split_size: Optional[int] = None,
        grouping_options_split_separator: Optional[str] = None,
        grouping_options_split_position: Optional[
            Literal["first_page", "last_page"]
        ] = None,
        channel_type: Optional[Literal["post", "email", "ebill"]] = None,
    ) -> pingen2sdk.PingenResponse:
        attributes: Dict[str, Any] = {
            "file_url": file_url,
            "file_url_signature": file_url_signature,
            "name": name,
            "icon": icon,
            "file_original_name": file_original_name,
            "address_position": address_position,
            "grouping_type": grouping_type,
            "grouping_options_split_type": grouping_options_split_type,
        }

        if channel_type is not None:
            attributes["channel_type"] = channel_type

        if grouping_options_split_size is not None:
            attributes["grouping_options_split_size"] = grouping_options_split_size

        if grouping_options_split_separator is not None:
            attributes["grouping_options_split_separator"] = (
                grouping_options_split_separator
            )

        if grouping_options_split_position is not None:
            attributes["grouping_options_split_position"] = (
                grouping_options_split_position
            )

        return self.api_requestor.perform_post_request(
            "/organisations/%s/batches" % self.organisation_id,
            json.dumps({"data": {"type": "batches", "attributes": attributes}}),
        )

    def send(
        self,
        batch_id: str,
        channel_type: Literal["post", "email", "ebill"] = "post",
        delivery_product: Optional[str] = None,
        print_mode: Optional[str] = None,
        print_spectrum: Optional[str] = None,
    ) -> pingen2sdk.PingenResponse:
        """Submit a batch for delivery.

        The request payload depends on the batch ``channel_type``:

        * ``post``  – requires ``delivery_product``
          (``fast`` / ``cheap`` / ``bulk`` / ``premium`` / ``registered``),
          ``print_mode`` (``simplex`` / ``duplex``) and
          ``print_spectrum`` (``color`` / ``grayscale``).
        * ``email`` – ``delivery_product`` defaults to ``electronic_email``.
        * ``ebill`` – ``delivery_product`` defaults to ``electronic_ebill``.
        """
        attributes: Dict[str, Any] = {}

        if channel_type == "email":
            attributes["delivery_product"] = delivery_product or "electronic_email"
        elif channel_type == "ebill":
            attributes["delivery_product"] = delivery_product or "electronic_ebill"
        else:
            attributes["delivery_product"] = delivery_product
            attributes["print_mode"] = print_mode
            attributes["print_spectrum"] = print_spectrum

        return self.api_requestor.perform_patch_request(
            "/organisations/%s/batches/%s/send" % (self.organisation_id, batch_id),
            json.dumps(
                {
                    "data": {
                        "id": batch_id,
                        "type": "batches_channel_%s_send" % channel_type,
                        "attributes": attributes,
                    }
                }
            ),
        )

    def update(
        self,
        batch_id: str,
        name: Optional[str] = None,
        icon: Optional[
            Literal[
                "campaign",
                "megaphone",
                "wave-hand",
                "flash",
                "rocket",
                "bell",
                "percent-tag",
                "percent-badge",
                "present",
                "receipt",
                "document",
                "information",
                "calendar",
                "newspaper",
                "crown",
                "virus",
            ]
        ] = None,
    ) -> pingen2sdk.PingenResponse:
        attributes: Dict[str, Any] = {}

        if name is not None:
            attributes["name"] = name

        if icon is not None:
            attributes["icon"] = icon

        return self.api_requestor.perform_patch_request(
            "/organisations/%s/batches/%s" % (self.organisation_id, batch_id),
            json.dumps(
                {
                    "data": {
                        "id": batch_id,
                        "type": "batches",
                        "attributes": attributes,
                    }
                }
            ),
        )

    def cancel(
        self,
        batch_id: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_cancel_request(
            "/organisations/%s/batches/%s/cancel" % (self.organisation_id, batch_id),
        )

    def delete(
        self,
        batch_id: str,
        with_deliverables: bool = True,
    ) -> pingen2sdk.PingenResponse:
        """Delete a batch.

        ``with_deliverables`` controls whether the deliverables contained in the
        batch are deleted as well (``True``) or kept as individual deliverables
        (``False``).
        """
        return self.api_requestor.perform_delete_request(
            "/organisations/%s/batches/%s" % (self.organisation_id, batch_id),
            json.dumps(
                {
                    "data": {
                        "type": "batches",
                        "id": batch_id,
                        "attributes": {
                            # TODO: `with_letters` is still required by the API but
                            # is deprecated in favour of `with_deliverables`. Remove
                            # it once the API no longer requires it.
                            "with_letters": with_deliverables,
                            "with_deliverables": with_deliverables,
                        },
                    }
                }
            ),
        )

    def edit(
        self,
        batch_id: str,
        paper_types: List[str],
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_patch_request(
            "/organisations/%s/batches/%s" % (self.organisation_id, batch_id),
            json.dumps(
                {
                    "data": {
                        "id": batch_id,
                        "type": "batches",
                        "attributes": {
                            "paper_types": paper_types,
                        },
                    }
                }
            ),
        )

    def get_statistics(
        self,
        batch_id: str,
    ) -> pingen2sdk.PingenResponse:
        return self.api_requestor.perform_get_request(
            "/organisations/%s/batches/%s/statistics" % (self.organisation_id, batch_id)
        )
