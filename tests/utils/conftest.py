# Python Standard Library Imports
import os

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
