# Python Standard Library Imports
import os

# Third Party (PyPI) Imports
import requests
from dotenv import load_dotenv


load_dotenv()


##
# Various Settings and Configuration Variables

SLACK_WEBHOOK_URL = os.environ.get('HTK_SLACK_WEBHOOK_URL', os.environ.get('SLACK_WEBHOOK_URL'))


##
# Import Local Settings if `./local_settings.py` exists

LOCAL_SETTINGS_FILENAME = os.path.realpath(os.path.join(os.path.dirname(__file__), 'local_settings.py'))

if os.path.isfile(LOCAL_SETTINGS_FILENAME):
    from .local_settings import *
