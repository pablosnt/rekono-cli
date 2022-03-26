import os
import subprocess
import sys
from getpass import getpass

import yaml
from config import DB_DATABASE, DB_USER, REKONO_HOME_DIRECTORY


def create_config_file(db_password: str) -> None:
    '''Create Rekono configuration file.

    Args:
        db_password (str): Database password for Rekono user
    '''
    config = {                                                                  # Prepare configuration file
        'frontend': {
            'url': 'http://127.0.0.1:8080'
        },
        'security': {
            'allowed-hosts': [
                '127.0.0.1',
                'localhost',
                '::1'
            ],
            'otp-expiration-hours': 24,
            'upload-files-max-mb': 500
        },
        'database': {
            'name': DB_DATABASE,
            'user': DB_USER,
            'password': db_password,
            'host': '127.0.0.1',
            'port': 5432
        },
        'rq': {
            'host': '127.0.0.1',
            'port': 6379
        },
        'telegram': {
            'bot': 'Rekono',
            'token': getpass("Telegram token (Don't worry if you haven't one): "),
        },
        'defect-dojo': {
            'url': input('Defect-Dojo URL [http://127.0.0.1:8080]: ') or 'http://127.0.0.1:8080',
            'api-key': getpass("Defect-Dojo API key (don't worry if you haven't one): "),
            'verify': True,
            'tags': ['rekono'],
            'product': {
                'auto-creation': True
            },
            'product-type': 'Rekono Project',
            'test-type': 'Rekono Findings Import',
            'test': 'Rekono Test'
        },
        'tools': {
            'cmseek': {
                'directory': '/usr/share/cmseek'
            },
            'log4j-scanner': {
                'directory': '/opt/log4j-scanner'
            },
            'gittools': {
                'directory': '/opt/GitTools'
            }
        }
    }
    with open(os.path.join(REKONO_HOME_DIRECTORY, 'config.yaml'), 'w') as config_file:
        yaml.dump(config, config_file)


def manage_command(command: str) -> None:
    '''Execute Django command.

    Args:
        command (str): Command to run
    '''
    subprocess.run(
        [sys.executable, 'manage.py', command],
        cwd=os.path.join(REKONO_HOME_DIRECTORY, 'rekono')
    )
