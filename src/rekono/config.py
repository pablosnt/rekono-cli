import os

from rekono.environment import REKONO_TOKEN, REKONO_URL

'''Rekono CLI configuration.'''

API_URL = os.getenv(REKONO_URL, 'http://127.0.0.1:8000')
API_TOKEN = os.getenv(REKONO_TOKEN)                                             # Rekono API token
