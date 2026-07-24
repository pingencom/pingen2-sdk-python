import pingen2sdk

from typing import Optional


class Pingen(object):
    """High-level entry point that wires a shared token source into every resource.

    Create it once with your OAuth client credentials and then obtain ready-to-use
    resource objects from it. Credentials, environment (staging vs production) and
    automatic token reuse/refresh are configured in a single place, so you never
    have to pass an access token or the staging flag around::

        pingen = pingen2sdk.Pingen(
            client_id, client_secret, use_staging=True,
            scope="letter batch webhook organisation_read email ebill",
        )

        orgs = pingen.organisations().get_collection()
        org_id = orgs.data["data"][0]["id"]
        pingen.letters(org_id).get_collection()

    Under the hood every resource is constructed with a shared
    :class:`pingen2sdk.OAuth` token source, so the bearer token is fetched once,
    reused across all resources and refreshed transparently before it expires.

    Pass an already configured ``oauth`` instance to reuse an existing token
    source instead of building one from ``client_id`` / ``client_secret``.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        use_staging: bool = False,
        scope: Optional[str] = None,
        oauth: Optional["pingen2sdk.OAuth"] = None,
    ):
        self.use_staging = use_staging
        self.oauth = oauth or pingen2sdk.OAuth(
            client_id=client_id,
            client_secret=client_secret,
            use_staging=use_staging,
            scope=scope,
        )

    def get_oauth(self) -> "pingen2sdk.OAuth":
        return self.oauth

    def get_access_token(self) -> str:
        return self.oauth.get_access_token()

    def organisations(self) -> "pingen2sdk.Organisations":
        return pingen2sdk.Organisations(self.oauth, self.use_staging)

    def users(self) -> "pingen2sdk.Users":
        return pingen2sdk.Users(self.oauth, self.use_staging)

    def user_associations(self) -> "pingen2sdk.UserAssociations":
        return pingen2sdk.UserAssociations(self.oauth, self.use_staging)

    def letters(self, organisation_id: str) -> "pingen2sdk.Letters":
        return pingen2sdk.Letters(organisation_id, self.oauth, self.use_staging)

    def letter_events(self, organisation_id: str) -> "pingen2sdk.LetterEvents":
        return pingen2sdk.LetterEvents(organisation_id, self.oauth, self.use_staging)

    def batches(self, organisation_id: str) -> "pingen2sdk.Batches":
        return pingen2sdk.Batches(organisation_id, self.oauth, self.use_staging)

    def batch_events(self, organisation_id: str) -> "pingen2sdk.BatchEvents":
        return pingen2sdk.BatchEvents(organisation_id, self.oauth, self.use_staging)

    def webhooks(self, organisation_id: str) -> "pingen2sdk.Webhooks":
        return pingen2sdk.Webhooks(organisation_id, self.oauth, self.use_staging)

    def emails(self, organisation_id: str) -> "pingen2sdk.Emails":
        return pingen2sdk.Emails(organisation_id, self.oauth, self.use_staging)

    def email_events(self, organisation_id: str) -> "pingen2sdk.EmailEvents":
        return pingen2sdk.EmailEvents(organisation_id, self.oauth, self.use_staging)

    def ebills(self, organisation_id: str) -> "pingen2sdk.Ebills":
        return pingen2sdk.Ebills(organisation_id, self.oauth, self.use_staging)

    def ebill_events(self, organisation_id: str) -> "pingen2sdk.EbillEvents":
        return pingen2sdk.EbillEvents(organisation_id, self.oauth, self.use_staging)
