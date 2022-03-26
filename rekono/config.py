import os

from environment import REKONO_HOME

'''Rekono CLI configuration.'''

REKONO_HOME_DIRECTORY = os.getenv(REKONO_HOME, '/opt/rekono')                   # Rekono home directory
REKONO_GIT_REPOSITORY = 'https://github.com/pablosnt/rekono.git'                # Rekono git repository

# Default configuration
DB_DATABASE = 'rekono'
DB_USER = 'rekono'
RQ_USER = 'rekono'

# System configuration
SYSTEMD_SERVICES = '/etc/systemd/system'
