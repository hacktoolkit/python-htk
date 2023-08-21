# Third Party (PyPI) Imports
import pytest
import requests

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
    def _build_message(
        self,
        text,
        username='HTK',
        channel=None,
        icon_emoji=None,
        attachments=None,
    ):
        m = SlackMessage(
            username=username,
            channel=channel,
            text=f'[TEST] {text}',
            icon_emoji=icon_emoji,
            attachments=attachments,
        )
        return m

    def test_send_message(
        self, test_username, test_channel, random_icon_emoji, test_attachment
    ):
        m = self._build_message(
            'This is sending a single message via the *Slack API*.',
            test_username,
            channel=test_channel,
            icon_emoji=random_icon_emoji,
            attachments=[test_attachment],
        )
        response_json = send_message(m)
        # fdb_json(response_json)
        assert (response_json.get('ts')) is not None

    def test_send_message__override_channel(self, test_username, test_channel):
        m = self._build_message(
            'This is sending a single message via the *Slack API*, but manually overriding the channel.',
            test_username,
            channel=None,
        )
        response_json = send_message(m, channel=test_channel)
        assert (response_json.get('ts')) is not None

    def test_send_messages_as_thread(self, test_username, test_channel):
        text = 'Threaded messages via API, a smashing success.'
        messages = [
            self._build_message(t, username=test_username, channel=test_channel)
            for t in text.split()
        ]
        assert len(messages) > 1
        thread_ts = send_messages_as_thread(messages)
        assert thread_ts is not None

    def test_send_messages_as_thread__override_channel(
        self, test_username, test_channel
    ):
        text = 'Threaded messages with overriden channel.'
        messages = [
            self._build_message(t, username=test_username, channel=None)
            for t in text.split()
        ]
        thread_ts = send_messages_as_thread(messages, channel=test_channel)
        assert thread_ts is not None

    def test_send_webhook_message(self, test_username, test_channel):
        m = self._build_message(
            'This is sending a single message via the *Slack Incoming Webhook*.',
            test_username,
            test_channel,
        )
        response = send_webhook_message(m)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        ['url', 'exception'],
        [
            (
                'invalid://api.slack.com/blah',
                requests.exceptions.InvalidSchema,
            ),
            ('api.slack.com/blah', requests.exceptions.MissingSchema),
        ],
    )
    def test_send_webhook_message__bad_url(self, url, exception):
        m = self._build_message('Blah')
        with pytest.raises(Exception) as excinfo:
            _ = send_webhook_message(m, webhook_url=url)
            assert exception.__class__.__name__ in str(excinfo.value)

    def test_slack_message(self, test_username, test_channel):
        text = (
            'This is sending a single message via the `slack_message` wrapper.'
        )
        response = slack_message(
            channel=test_channel,
            username=test_username,
            text=text,
        )
        assert response.status_code == 200
