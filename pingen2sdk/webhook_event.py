import json


class WebhookEvent(object):
    body: str

    def __init__(self, body: str):
        self.body = body

        if bool(body):  # pragma: no cover
            self.data = json.loads(body.decode("utf-8"))
