# Future Imports
from __future__ import absolute_import

# Python Standard Library Imports
import datetime
import json

# Local Imports
from ..encoders import DecimalEncoder


DEFAULT_FILE_PATH = '/tmp/fdebug.log'


# isort: off


class FDebugCounter:
    _instance = None

    # singleton
    class __FDebugCounter:
        def __init__(self):
            self.count = 0

        def increment(self):
            self.count += 1

    def __init__(self):
        if FDebugCounter._instance is None:
            FDebugCounter._instance = FDebugCounter.__FDebugCounter()

    def __getattr__(self, name):
        return getattr(self._instance, name)


def fdebug(text, file_path=DEFAULT_FILE_PATH):
    counter = FDebugCounter()
    counter.increment()
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%I:%S')

    with open(file_path, 'a+') as f:
        f.write(
            '>>>>>>>>>> FDEBUG {} {} <<<<<<<<<<\n'.format(
                counter.count,
                now_str
            )
        )
        f.write('{}\n'.format(text))
        f.write(
            '<<<<<<<<<< FDEBUG {} {} >>>>>>>>>>\n'.format(
                counter.count,
                now_str
            )
        )


def fdebug_json(obj, file_path=DEFAULT_FILE_PATH, label='JSON'):
    fdebug(
        '%s: ```%s```' % (
            label,
            json.dumps(obj, indent=2, cls=DecimalEncoder),
        ),
        file_path=file_path
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


# Aliases


fdb = fdebug
fdb_json = fdebug_json


__all__ = [
    'fdb',
    'fdb_json',
    'fdebug',
    'fdebug_json',
    'slack_debug',
    'slack_debug_json',
]
