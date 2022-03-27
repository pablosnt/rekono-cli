import os

from rekono.environment import REKONO_HOME

'''Rekono CLI configuration.'''

REKONO_HOME_DIRECTORY = os.getenv(REKONO_HOME, '/opt/rekono')                   # Rekono home directory
REKONO_GIT_REPOSITORY = 'https://github.com/pablosnt/rekono.git'                # Rekono git repository

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
