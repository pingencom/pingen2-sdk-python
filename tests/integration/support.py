"""Shared helpers, constants and credential loading for the integration tests.

The integration tests hit the real Pingen **staging** API and therefore need
valid staging credentials. Credentials are read from a ``.env`` file at the
repository root (copy ``.env.example`` to ``.env`` and fill it in).
"""

import os
import uuid
from datetime import date, timedelta
from typing import Dict

# OAuth scope requested for the staging access token. Mirrors the scopes used
# by the manual test script and covers every resource exercised below.
SCOPE = "letter batch webhook organisation_read email ebill"

# Document names sent to the API. The staging environment recognises the magic
# ``simulate_cancellable`` suffix and keeps such deliveries in a state that can
# be cancelled, which lets us exercise the cancel flow deterministically.
FILE_NAME = "test.pdf"
FILE_NAME_CANCELLABLE = "test_simulate_cancellable.pdf"

# Keys the credential loader looks for.
_KEYS = (
    "PINGEN2_CLIENT_ID",
    "PINGEN2_CLIENT_SECRET",
    "PINGEN2_ORGANISATION_ID",
)

# The suite must never run against production.
USE_STAGING = True


def _repo_root() -> str:
    # tests/integration/support.py -> repository root is two levels up.
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _parse_dotenv(path: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not os.path.isfile(path):
        return values

    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            values[key] = value

    return values


def load_credentials() -> Dict[str, str]:
    """Return the integration credentials."""
    dotenv_values = _parse_dotenv(os.path.join(_repo_root(), ".env"))

    credentials: Dict[str, str] = {}
    for key in _KEYS:
        env_value = os.environ.get(key)
        credentials[key] = env_value if env_value else dotenv_values.get(key, "")

    return credentials


def missing_credentials(credentials: Dict[str, str]) -> bool:
    client_id = credentials.get("PINGEN2_CLIENT_ID")
    client_secret = credentials.get("PINGEN2_CLIENT_SECRET")
    return not (client_id and client_secret)


def document_path(file_name: str = FILE_NAME) -> str:
    return os.path.join(_repo_root(), "tests", "api_resources", "files", file_name)


def document_name(path: str) -> str:
    """``file_original_name`` derived from the uploaded file itself."""
    return os.path.basename(path)


def build_email_meta_data() -> Dict[str, str]:
    return {
        "sender_name": "Pingen Test",
        "recipient_email": "grzegorz.morgas@pingen.com",
        "recipient_name": "Test Recipient",
        "reply_email": "noreply@example.com",
        "reply_name": "Reply Test",
        "subject": "Integration Test Email",
        "content": "Dear Recipient\\n\\nThis is an integration test.\\n\\nBest regards",
    }


def build_ebill_meta_data() -> Dict[str, str]:
    # Unique per call so repeated runs never clash on a duplicate invoice number.
    return {
        "invoice_number": "INV-%s" % uuid.uuid4().hex[:12],
        "invoice_date": date.today().isoformat(),
        "invoice_due_date": (date.today() + timedelta(days=30)).isoformat(),
        "recipient_identifier": "41100000014283293",
    }
