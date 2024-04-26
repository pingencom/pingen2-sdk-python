# flake8: noqa
from typing import Optional

import os

api_key: Optional[str] = None
client_id: Optional[str] = None
client_secret: Optional[str] = None
api_production: str = "https://api.pingen.com"
auth_production: str = "https://identity.pingen.com"
api_staging: str = "https://api-staging.pingen.com"
auth_staging: str = "https://identity-staging.pingen.com"
request_timeout: int = 20

# OAuth
from pingen2sdk.oauth import OAuth

# PingenResponse
from pingen2sdk.response import PingenResponse

# PingenError
from pingen2sdk.error import PingenError

# APIRequestor
from pingen2sdk.api import APIRequestor

# API Resources
from pingen2sdk.api_resources import *

# PingenWebhook
from pingen2sdk.webhook_event import WebhookEvent

# PingenWebhook
from pingen2sdk.incoming_webhook import IncomingWebhook
