import os

from environment import REKONO_HOME, REKONO_SOURCE

'''Rekono CLI configuration.'''

REKONO_SOURCE_DIRECTORY = os.getenv(REKONO_SOURCE, '/opt/rekono')               # Rekono code
REKONO_HOME_DIRECTORY = os.getenv(REKONO_HOME, '/usr/share/rekono')             # Rekono config and outputs
REKONO_GIT_REPOSITORY = 'https://github.com/pablosnt/rekono.git'                # Rekono git repository

# Default configuration
DB_DATABASE = 'rekono'
DB_USER = 'rekono'
RQ_USER = 'rekono'
