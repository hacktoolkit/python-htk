# Python Standard Library Imports
import os


##
# Various Settings and Configuration Variables

SLACK_WEBHOOK_URL = 'Overwrite this value in local_settings.py'


##
# Import Local Settings if `./local_settings.py` exists

LOCAL_SETTINGS_FILENAME = os.path.realpath(os.path.join(os.path.dirname(__file__), 'local_settings.py'))

if os.path.isfile(LOCAL_SETTINGS_FILENAME):
    from .local_settings import *
