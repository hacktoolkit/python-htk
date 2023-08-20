# Third Party (PyPI) Imports
import pytest

# HTK Imports
# from htk.utils.debuggers import (
#     fdb,
#     fdb_json,
# )
from htk.utils.slack import (
    SlackMessage,
    send_message,
    send_messages_as_thread,
    send_webhook_message,
    slack_message,
)


class TestSlack:
    def _build_message(self, text, username, channel):
        m = SlackMessage(
            username=username,
            channel=channel,
            text=f'[TEST] {text}',
        )
        return m

    def test_send_message(self, test_username, test_channel):
        m = self._build_message(
            'This is sending a single message via the *Slack API*.',
            test_username,
            test_channel,
        )
        response_json = send_message(m)
        # fdb_json(response_json)
        assert (response_json.get('ts')) is not None

    def test_send_messages_as_thread(self, test_username, test_channel):
        text = 'Threaded messages via API, a smashing success.'
        messages = [
            self._build_message(t, test_username, test_channel)
            for t in text.split()
        ]
        thread_ts = send_messages_as_thread(messages)
        assert thread_ts is not None

    def test_send_webhook_message(self, test_username, test_channel):
        m = self._build_message(
            'This is sending a single message via the *Slack Incoming Webhook*.',
            test_username,
            test_channel,
        )
        response = send_webhook_message(m)
        assert response.status_code == 200

    def test_slack_message(self, test_username, test_channel):
        text = 'This is sending a single message via the `slack_message` wrapper.'
        response = slack_message(
            channel=test_channel,
            username=test_username,
            text=text,
        )
        assert response.status_code == 200
