import hmac
import hashlib

from typing import Mapping

import pingen2sdk.response
from pingen2sdk import error


class IncomingWebhook(object):
    @staticmethod
    def construct_event(
        payload: str, header: Mapping[str, str], secret: str
    ) -> pingen2sdk.WebhookEvent:
        WebhookSignature.verify_header(payload, header, secret)

        return pingen2sdk.WebhookEvent(payload)


class WebhookSignature(object):
    @staticmethod
    def verify_header(payload: str, header: Mapping[str, str], secret: str) -> bool:
        signature = header.get("Signature")

        if not signature:
            raise error.WebhookSignatureException("Signature missing.")

        expected_sig = hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        if signature != expected_sig:
            raise error.WebhookSignatureException("Webhook signature matching failed.")

        return True
