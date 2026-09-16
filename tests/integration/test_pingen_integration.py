"""Integration tests for the Pingen Python SDK against the staging environment.

These tests make real HTTP calls and require valid staging credentials (see
``.env.example``). They are excluded from the normal unit-test run via the
``integration`` marker and must be triggered explicitly::

    pytest -m integration tests/integration

The suite walks every resource end to end: organisations, letters (happy /
cancel / delete), batches, webhooks, emails, e-bills and the user endpoints.
Cancel / delete / update steps rely on the ``simulate_cancellable`` document and
the ``time.sleep`` waits to reach the required state and assert strictly.

Tests within a class run top-to-bottom (pytest preserves definition order) and
share created resource IDs through class attributes.
"""

import time

import pytest
import pingen2sdk

from tests.integration import support

pytestmark = pytest.mark.integration


def _create_ebill(ebills, path, auto_send=False):
    """Create an e-bill, skipping the test if the channel is not configured."""
    try:
        return ebills.upload_and_create(
            path,
            support.document_name(path),
            auto_send,
            support.build_ebill_meta_data(),
        )
    except pingen2sdk.PingenError as error:
        if "conflict_missing_configuration" in str(error.json_body):
            pytest.skip("E-Bill channel not configured – skipping.")
        raise


# =============================================================================
# Organisations
# =============================================================================


class TestOrganisations:
    def test_1_list_organisations(self, organisations):
        response = organisations.get_collection()

        assert response.status_code == 200
        items = response.data["data"]
        assert len(items) >= 1
        assert all(item["id"] for item in items)

    def test_2_list_organisations_paginated(self, organisations):
        response = organisations.get_collection({"page[number]": 1, "page[limit]": 5})

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_3_get_organisation_by_id(self, organisations, organisation_id):
        response = organisations.get_details(organisation_id)

        assert response.status_code == 200
        assert response.data["data"]["id"] == organisation_id


# =============================================================================
# Letters
# =============================================================================


class TestLettersHappyCase:
    letter_id = None

    def test_1_list_letters(self, letters):
        response = letters.get_collection()

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_2_list_letters_paginated(self, letters):
        response = letters.get_collection({"page[number]": 1, "page[limit]": 3})

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_3_create_letter(self, letters, document_path):
        response = letters.upload_and_create(
            document_path,
            support.document_name(document_path),
            "left",
            True,
            "cheap",
            "simplex",
            "grayscale",
        )

        assert response.data["data"]["id"]
        assert response.data["data"]["attributes"]["status"] == "validating"

        TestLettersHappyCase.letter_id = response.data["data"]["id"]

        detail = letters.get_details(TestLettersHappyCase.letter_id)
        assert detail.data["data"]["id"] == TestLettersHappyCase.letter_id

        print("sleep 30 seconds so the collection contains the newly created letter")
        time.sleep(30)

        # Newest first, so the letter we just created must be on the first page.
        collection = letters.get_collection(
            {"sort": "-created_at", "page[number]": 1, "page[limit]": 20}
        )
        ids = [item["id"] for item in collection.data["data"]]
        assert TestLettersHappyCase.letter_id in ids

    def test_4_get_letter_by_id(self, letters):
        assert self.letter_id, "Requires test_3_create_letter to have run"

        response = letters.get_details(self.letter_id)

        assert response.data["data"]["id"] == self.letter_id
        print("Letter status: %s" % response.data["data"]["attributes"]["status"])

    def test_5_get_letter_events(self, letter_events):
        assert self.letter_id, "Requires test_3_create_letter to have run"

        response = letter_events.get_collection(self.letter_id)

        assert response.status_code == 200
        print("Letter events: %d" % len(response.data["data"]))

    def test_6_get_letter_file(self, letters):
        assert self.letter_id, "Requires test_3_create_letter to have run"

        file_content = letters.get_file(self.letter_id)

        assert file_content is not None

    def test_7_calculate_letter_price(self, letters):
        response = letters.calculate_price(
            "CH",
            ["normal", "normal"],
            "simplex",
            "grayscale",
            "cheap",
        )

        assert response.data["data"]["id"]
        attributes = response.data["data"].get("attributes", {})
        print(
            "Price calculator: currency=%s, price=%s"
            % (attributes.get("currency"), attributes.get("price"))
        )

    def test_8_get_letter_sent_events(self, letter_events):
        response = letter_events.get_sent_collection()
        assert response.status_code == 200

    def test_9_get_letter_delivered_events(self, letter_events):
        response = letter_events.get_delivered_collection()
        assert response.status_code == 200

    def test_10_get_letter_issue_events(self, letter_events):
        response = letter_events.get_issue_collection()
        assert response.status_code == 200

    def test_11_get_letter_undeliverable_events(self, letter_events):
        response = letter_events.get_undeliverable_collection()
        assert response.status_code == 200


class TestLettersCancelCase:
    letter_id = None

    def test_1_create_letter(self, letters):
        path = support.document_path(support.FILE_NAME_CANCELLABLE)
        response = letters.upload_and_create(
            path,
            support.document_name(path),
            "left",
            True,
            "cheap",
            "simplex",
            "grayscale",
        )

        assert response.data["data"]["id"]
        assert response.data["data"]["attributes"]["status"] == "validating"

        TestLettersCancelCase.letter_id = response.data["data"]["id"]

    def test_2_cancel_letter(self, letters):
        assert self.letter_id, "Requires test_1_create_letter to have run"

        print("sleep 10 seconds so the letter reaches a cancellable state")
        time.sleep(10)

        response = letters.cancel(self.letter_id)
        assert response.status_code == 202


class TestLettersDeleteCase:
    letter_id = None

    def test_1_create_letter(self, letters, document_path):
        response = letters.upload_and_create(
            document_path,
            support.document_name(document_path),
            "right",
            False,
            "cheap",
            "simplex",
            "grayscale",
        )

        assert response.data["data"]["id"]
        assert response.data["data"]["attributes"]["status"] == "validating"
        time.sleep(5)

        TestLettersDeleteCase.letter_id = response.data["data"]["id"]

    def test_2_delete_letter(self, letters):
        assert self.letter_id, "Requires test_1_create_letter to have run"

        response = letters.delete(self.letter_id)
        assert response.status_code == 204
        print("Deleted letter: %s" % self.letter_id)


# =============================================================================
# Batches
# =============================================================================


class TestBatchesHappyCase:
    batch_id = None

    def test_1_list_batches(self, batches):
        response = batches.get_collection()

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_2_list_batches_paginated(self, batches):
        response = batches.get_collection({"page[number]": 1, "page[limit]": 3})

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_3_create_batch(self, batches, document_path):
        response = batches.upload_and_create(
            document_path,
            "Integration Test Batch",
            "document",
            support.document_name(document_path),
            "left",
            "merge",
            "qr_invoice",
            2,
        )

        assert response.data["data"]["id"]

        TestBatchesHappyCase.batch_id = response.data["data"]["id"]
        print(
            "Created batch: %s (status: %s)"
            % (
                TestBatchesHappyCase.batch_id,
                response.data["data"]["attributes"]["status"],
            )
        )

    def test_4_get_batch_by_id(self, batches):
        assert self.batch_id, "Requires test_3_create_batch to have run"

        response = batches.get_details(self.batch_id)

        assert response.data["data"]["id"] == self.batch_id
        print("Batch status: %s" % response.data["data"]["attributes"]["status"])

    def test_5_update_batch(self, batches):
        assert self.batch_id, "Requires test_3_create_batch to have run"

        print("sleep 10 seconds so the batch reaches an updatable state")
        time.sleep(10)

        response = batches.update(self.batch_id, "Updated Integration Batch", "rocket")
        assert response.status_code in (200, 202)

    def test_6_get_batch_events(self, batch_events):
        assert self.batch_id, "Requires test_3_create_batch to have run"

        response = batch_events.get_collection(self.batch_id)

        assert response.status_code == 200
        print("Batch events: %d" % len(response.data["data"]))

    def test_7_get_batch_statistics(self, batches):
        assert self.batch_id, "Requires test_3_create_batch to have run"

        response = batches.get_statistics(self.batch_id)
        assert response.status_code == 200


class TestBatchesDeleteCase:
    batch_id = None

    def test_1_create_batch(self, batches):
        path = support.document_path(support.FILE_NAME_CANCELLABLE)
        response = batches.upload_and_create(
            path,
            "Integration Test Batch",
            "document",
            support.document_name(path),
            "left",
            "merge",
            "qr_invoice",
            2,
        )

        assert response.data["data"]["id"]

        TestBatchesDeleteCase.batch_id = response.data["data"]["id"]
        print("Created batch: %s" % TestBatchesDeleteCase.batch_id)

    def test_2_delete_batch(self, batches):
        assert self.batch_id, "Requires test_1_create_batch to have run"

        print("sleep 10 seconds so the batch reaches a deletable state")
        time.sleep(10)

        response = batches.delete(self.batch_id)
        assert response.status_code == 204
        print("Deleted batch: %s" % self.batch_id)


# =============================================================================
# Webhooks
# =============================================================================


class TestWebhooks:
    webhook_id = None

    def test_1_list_webhooks(self, webhooks):
        response = webhooks.get_collection()

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_2_create_webhook(self, webhooks):
        response = webhooks.create(
            "issues",
            "https://httpbin.org/post",
            "integration-test-signing-key-32c",
        )

        assert response.data["data"]["id"]

        TestWebhooks.webhook_id = response.data["data"]["id"]
        print(
            "Created webhook: %s (url: %s)"
            % (
                TestWebhooks.webhook_id,
                response.data["data"]["attributes"]["url"],
            )
        )

    def test_3_get_webhook_by_id(self, webhooks):
        assert self.webhook_id, "Requires test_2_create_webhook to have run"

        response = webhooks.get_details(self.webhook_id)

        assert response.data["data"]["id"] == self.webhook_id
        print("Webhook url: %s" % response.data["data"]["attributes"]["url"])

    def test_4_delete_webhook(self, webhooks):
        assert self.webhook_id, "Requires test_2_create_webhook to have run"

        response = webhooks.delete(self.webhook_id)
        assert response.status_code == 204
        print("Deleted webhook: %s" % self.webhook_id)


# =============================================================================
# Emails
# =============================================================================


class TestEmailsHappyCase:
    email_id = None

    def test_1_list_emails(self, emails):
        response = emails.get_collection()

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_2_create_email(self, emails, document_path):
        response = emails.upload_and_create(
            document_path,
            support.document_name(document_path),
            True,
            support.build_email_meta_data(),
        )

        assert response.data["data"]["id"]

        TestEmailsHappyCase.email_id = response.data["data"]["id"]
        print(
            "Created email: %s (status: %s)"
            % (
                TestEmailsHappyCase.email_id,
                response.data["data"]["attributes"]["status"],
            )
        )

    def test_3_get_email_by_id(self, emails):
        assert self.email_id, "Requires test_2_create_email to have run"

        response = emails.get_details(self.email_id)

        assert response.data["data"]["id"] == self.email_id
        print("Email status: %s" % response.data["data"]["attributes"]["status"])

    def test_4_get_email_events(self, email_events):
        assert self.email_id, "Requires test_2_create_email to have run"

        response = email_events.get_collection(self.email_id)

        assert response.status_code == 200
        print("Email events: %d" % len(response.data["data"]))

    def test_5_get_email_file(self, emails):
        assert self.email_id, "Requires test_2_create_email to have run"

        print("sleep 5 seconds so the email reaches a retrievable state")
        time.sleep(5)

        file_content = emails.get_file(self.email_id)
        assert file_content is not None


class TestEmailsCancelCase:
    email_id = None

    def test_1_create_email(self, emails):
        path = support.document_path(support.FILE_NAME_CANCELLABLE)
        response = emails.upload_and_create(
            path,
            support.document_name(path),
            True,
            support.build_email_meta_data(),
        )

        assert response.data["data"]["id"]
        TestEmailsCancelCase.email_id = response.data["data"]["id"]

    def test_2_cancel_email(self, emails):
        assert self.email_id, "Requires test_1_create_email to have run"

        print("sleep 10 seconds so the email reaches a cancellable state")
        time.sleep(10)

        response = emails.cancel(self.email_id)
        assert response.status_code == 202


class TestEmailsDeleteCase:
    email_id = None

    def test_1_create_email(self, emails, document_path):
        response = emails.upload_and_create(
            document_path,
            support.document_name(document_path),
            False,
            support.build_email_meta_data(),
        )

        assert response.data["data"]["id"]
        TestEmailsDeleteCase.email_id = response.data["data"]["id"]

    def test_2_delete_email(self, emails):
        assert self.email_id, "Requires test_1_create_email to have run"

        print("sleep 10 seconds so the email reaches a deletable state")
        time.sleep(10)

        response = emails.delete(self.email_id)
        assert response.status_code == 204
        print("Deleted email: %s" % self.email_id)


# =============================================================================
# E-Bills
# =============================================================================


class TestEbillsHappyCase:
    ebill_id = None

    def test_1_list_ebills(self, ebills):
        response = ebills.get_collection()

        assert response.status_code == 200
        assert isinstance(response.data["data"], list)

    def test_2_create_ebill(self, ebills, document_path):
        response = _create_ebill(ebills, document_path)

        assert response.data["data"]["id"]

        TestEbillsHappyCase.ebill_id = response.data["data"]["id"]
        print(
            "Created e-bill: %s (status: %s)"
            % (
                TestEbillsHappyCase.ebill_id,
                response.data["data"]["attributes"]["status"],
            )
        )

    def test_3_get_ebill_by_id(self, ebills):
        if not self.ebill_id:
            pytest.skip("Requires test_2_create_ebill to have created an e-bill.")

        response = ebills.get_details(self.ebill_id)

        assert response.data["data"]["id"] == self.ebill_id
        print("E-Bill status: %s" % response.data["data"]["attributes"]["status"])

    def test_4_get_ebill_events(self, ebill_events):
        if not self.ebill_id:
            pytest.skip("Requires test_2_create_ebill to have created an e-bill.")

        response = ebill_events.get_collection(self.ebill_id)

        assert response.status_code == 200
        print("E-Bill events: %d" % len(response.data["data"]))

    def test_5_get_ebill_file(self, ebills):
        if not self.ebill_id:
            pytest.skip("Requires test_2_create_ebill to have created an e-bill.")

        print("sleep 10 seconds so the e-bill reaches a retrievable state")
        time.sleep(10)

        file_content = ebills.get_file(self.ebill_id)
        assert file_content is not None


class TestEbillsCancelCase:
    ebill_id = None

    def test_1_create_ebill(self, ebills):
        response = _create_ebill(
            ebills,
            support.document_path(support.FILE_NAME_CANCELLABLE),
            auto_send=True,
        )

        assert response.data["data"]["id"]
        TestEbillsCancelCase.ebill_id = response.data["data"]["id"]

    def test_2_cancel_ebill(self, ebills):
        assert self.ebill_id, "Requires test_1_create_ebill to have run"

        print("sleep 10 seconds so the e-bill reaches a cancellable state")
        time.sleep(10)

        response = ebills.cancel(self.ebill_id)
        assert response.status_code == 202


class TestEbillsDeleteCase:
    ebill_id = None

    def test_1_create_ebill(self, ebills, document_path):
        response = _create_ebill(ebills, document_path)

        assert response.data["data"]["id"]
        TestEbillsDeleteCase.ebill_id = response.data["data"]["id"]

    def test_2_delete_ebill(self, ebills):
        assert self.ebill_id, "Requires test_1_create_ebill to have run"

        print("sleep 10 seconds so the e-bill reaches a deletable state")
        time.sleep(10)

        response = ebills.delete(self.ebill_id)
        assert response.status_code == 204
        print("Deleted e-bill: %s" % self.ebill_id)


# =============================================================================
# User
# =============================================================================


class TestUser:
    def test_1_get_user(self, users):
        response = users.get_details()

        assert response.data["data"]["id"]
        assert response.data["data"]["attributes"]["email"]
        attributes = response.data["data"]["attributes"]
        print(
            "User: %s %s (%s)"
            % (
                attributes.get("first_name"),
                attributes.get("last_name"),
                attributes.get("email"),
            )
        )

    def test_2_get_user_associations(self, user_associations):
        response = user_associations.get_collection()

        assert response.status_code == 200
        print("User associations: %d" % len(response.data["data"]))
