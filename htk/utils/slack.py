# Future Imports
from __future__ import absolute_import

# Python Standard Library Imports
import json
import typing as T
from dataclasses import dataclass

# Third Party (PyPI) Imports
import requests
from requests.exceptions import JSONDecodeError

# Local Imports
from ..settings import (
    SLACK_BOT_TOKEN,
    SLACK_WEBHOOK_URL,
)
from .http import HTTPBearerAuth


@dataclass
class SlackMessage:
    channel: T.Optional[str] = None
    username: T.Optional[str] = None
    text: str = ""
    attachments: T.Optional[list] = None
    icon_emoji: T.Optional[str] = None
    unfurl_links: bool = True
    unfurl_media: bool = True
    thread_ts: T.Optional[str] = None
    reply_broadcast: bool = False

    @property
    def as_payload(self):
        payload = {
            "text": self.text,
            "unfurl_links": self.unfurl_links,
            "unfurl_media": self.unfurl_media,
        }

        if self.channel:
            payload["channel"] = self.channel
        if self.username:
            payload["username"] = self.username
        if self.icon_emoji:
            payload["icon_emoji"] = self.icon_emoji
        if self.attachments:
            payload["attachments"] = self.attachments

        if self.thread_ts is not None:
            payload["thread_ts"] = self.thread_ts
            payload["reply_broadcast"] = self.reply_broadcast

        return payload


def slack_message(
    webhook_url: T.Optional[str] = SLACK_WEBHOOK_URL,
    channel: T.Optional[str] = None,
    username: T.Optional[str] = None,
    text: str = "",
    attachments: T.Optional[list] = None,
    icon_emoji: T.Optional[str] = None,
    unfurl_links: bool = True,
    unfurl_media: bool = True,
    thread_ts: T.Optional[str] = None,
    reply_broadcast: bool = False,
    error_response_handlers=None,
) -> requests.Response:
    """Wrapper around `send_webhook_message` + `SlackMessage` for legacy/backwards-compatibility.

    New implementations should directly use `send_webhook_message` or `send_message`
    """
    return send_webhook_message(
        message=SlackMessage(
            channel=channel,
            username=username,
            text=text,
            attachments=attachments,
            icon_emoji=icon_emoji,
            unfurl_links=unfurl_links,
            unfurl_media=unfurl_media,
            thread_ts=thread_ts,
            reply_broadcast=reply_broadcast,
        ),
        webhook_url=webhook_url,
        error_response_handlers=error_response_handlers,
    )


def send_webhook_message(
    message: SlackMessage,
    webhook_url: str = None,
    error_response_handlers=None,
) -> requests.Response:
    """Performs a webhook call to Slack to send a single message

    https://api.slack.com/incoming-webhooks
    https://api.slack.com/docs/message-formatting

    `channel` override must be a public channel

    NOTE: Incoming webhooks is deprecated, and when possible, `send_message` should be used instead
    """
    if webhook_url is None:
        webhook_url = SLACK_WEBHOOK_URL
        if webhook_url is None:
            raise Exception("HTK_SLACK_WEBHOOK_URL or SLACK_WEBHOOK_URL not set in ENV")

    try:
        response = requests.post(webhook_url, json=message.as_payload)
        if response.status_code == 200:
            # success case, do nothing
            pass
        elif response.status_code <= 399:
            # 200-300, do nothing
            pass
        else:
            print(
                "Slack webhook call error: [{}] {}".format(
                    response.status_code, response.content
                )
            )
    except (requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema) as e:
        raise Exception(
            "Bad Slack webhook URL: [{}] ({})".format(
                webhook_url,
                e.__class__.__name__,
            )
        )
    except:
        raise

    return response


def send_message(
    message: SlackMessage,
    thread_ts=None,
    error_response_handlers=None,
    token=None,
) -> requests.Response:
    """Posts a Slack message via HTTP API

    POST https://slack.com/api/chat.postMessage
    Content-type: application/json
    Authorization: Bearer xoxb-your-token
    {
      "channel": "YOUR_CHANNEL_ID",
      "text": "Hello world :tada:"
    }
    """
    if token is None:
        token = SLACK_BOT_TOKEN
        if token is None:
            raise Exception("HTK_SLACK_BOT_TOKEN or SLACK_BOT_TOKEN not set in ENV")

    if thread_ts is not None:
        message.thread_ts = thread_ts

    url = "https://slack.com/api/chat.postMessage"
    auth = HTTPBearerAuth(token)

    try:
        response = requests.post(url, auth=auth, json=message.as_payload)
        response_json = response.json()
    except JSONDecodeError as e:
        response_json = {
            "response": {
                "status": response.status_code,
                "content": response.content,
            },
        }
    except Exception as e:
        response = None
        print(e)

    return response_json


def send_messages_as_thread(
    messages: T.List[SlackMessage], error_response_handlers=None
):
    """Sends a series of `SlackMessage` objects in a thread

    The first message is posted, then each message is posted subsequently in the thread of the first message.
    """
    is_first = True
    thread_ts = None

    print(len(messages))

    for message in messages:
        response = send_message(
            message,
            thread_ts=thread_ts,
            error_response_handlers=error_response_handlers,
        )
        if is_first:
            is_first = False
            thread_ts = response.get("ts")
        else:
            pass


__all__ = [
    "SlackMessage",
    "send_message",
    "send_messages_as_thread",
    "send_webhook_message",
    "slack_message",
]
