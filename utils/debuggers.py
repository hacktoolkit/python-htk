# Future Imports
from __future__ import absolute_import

# Python Standard Library Imports
import json

# Local Imports
from ..encoders import DecimalEncoder


def slack_debug(text):
    from .slack import slack_message

    response = slack_message(text=text)

    return response


def slack_debug_json(obj, label='JSON'):
    slack_debug(
        '%s: ```%s```' % (
            label,
            json.dumps(obj, indent=2, cls=DecimalEncoder),
        )
    )


__all__ = [
    'slack_debug',
    'slack_debug_json',
]
