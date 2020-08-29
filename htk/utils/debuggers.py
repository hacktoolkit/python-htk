# Future Imports
from __future__ import absolute_import

# Python Standard Library Imports
import json

# Local Imports
from ..encoders import DecimalEncoder


def fdebug(file_path, text):
    with open(file_path, 'w+') as f:
        f.write(text)


def fdebug_json(file_path, obj, label='JSON'):
    fdebug(
        file_path,
        '%s: ```%s```' % (
            label,
            json.dumps(obj, indent=2, cls=DecimalEncoder),
        )
    )


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
    'fdebug',
    'fdebug_json',
    'slack_debug',
    'slack_debug_json',
]
