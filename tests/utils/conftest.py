# Python Standard Library Imports
import os
import random

# Third Party (PyPI) Imports
import pytest
from dotenv import load_dotenv


# isort: off


load_dotenv()


@pytest.fixture
def test_username():
    return 'Hacktoolkit Bot'


@pytest.fixture
def test_channel():
    channel = os.environ.get('TEST_CHANNEL')
    return channel


EMOJIS = [
    ':comment:',
    ':heavy_check_mark:',
    ':heavy_plus_sign:',
    ':smile:',
    ':sunglasses:',
    ':upside_down_face:',
    ':white_check_mark:',
]


@pytest.fixture
def random_icon_emoji():
    emoji = random.choice(EMOJIS)
    return emoji


@pytest.fixture
def test_attachment():
    attachment = {
        'pretext': 'Attachment pretext',
        'text': 'Attachment text',
        'color': random.choice(['good', 'danger']),
    }
    return attachment
