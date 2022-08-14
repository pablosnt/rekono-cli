import os

from rekono.environment import REKONO_HOME, REKONO_TOKEN, REKONO_URL

'''Rekono CLI configuration.'''

REKONO_HOME_DIRECTORY = os.getenv(REKONO_HOME, '/opt/rekono')                   # Rekono home directory
REKONO_GIT_REPOSITORY = 'https://github.com/pablosnt/rekono.git'                # Rekono git repository

API_URL = os.getenv(REKONO_URL, 'http://127.0.0.1:8000')
API_TOKEN = os.getenv(REKONO_TOKEN)                                             # Rekono API token

# Default configuration
DB_DATABASE = 'rekono'
DB_USER = 'rekono'
RQ_USER = 'rekono'
CMSEEK_DIR = '/usr/share/cmseek'
LOG4J_SCANNER_DIR = '/opt/log4j-scanner'
GITTOOLS_DIR = '/opt/GitTools'

# System configuration
REKONO_USER = 'rekono'
SYSTEMD_SERVICES = '/etc/systemd/system'
