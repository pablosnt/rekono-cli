import os
from getpass import getpass
from typing import List

import yaml

from rekono.config import (CMSEEK_DIR, DB_DATABASE, DB_USER, GITTOOLS_DIR,
                           LOG4J_SCANNER_DIR, REKONO_HOME_DIRECTORY)


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
        'email': {
            'host': input('SMTP host: '),
            'port': input('SMTP port: '),
            'user': input('SMTP user: '),
            'password': getpass('SMTP password: '),
            'tls': True
        },
        'telegram': {
            'bot': 'Rekono',
            'token': getpass('Telegram token: '),
        },
        'defect-dojo': {
            'url': input('Defect-Dojo URL [Format <protocol>://<host>]: '),
            'api-key': getpass('Defect-Dojo API key: '),
            'verify': True,
            'tags': ['rekono'],
            'product-type': 'Rekono Project',
            'test-type': 'Rekono Findings Import',
            'test': 'Rekono Test'
        },
        'tools': {
            'cmseek': {
                'directory': CMSEEK_DIR
            },
            'log4j-scanner': {
                'directory': LOG4J_SCANNER_DIR
            },
            'gittools': {
                'directory': GITTOOLS_DIR
            }
        }
    }
    with open(os.path.join(REKONO_HOME_DIRECTORY, 'config.yaml'), 'w') as config_file:
        yaml.safe_dump(config, config_file)


def check_configuration(env: str, config_path: List[str]) -> bool:
    '''Check if a Rekono configuration items is configured or not.

    Args:
        env (str): Environment variable to check
        config_path (List[str]): Path to the item in the configuration file

    Returns:
        bool: Indicate if the item is configured or not
    '''
    with open(os.path.join(REKONO_HOME_DIRECTORY, 'config.yaml'), 'r') as config_file:
        config = yaml.safe_load(config_file)                                    # Get configuration from file
    for key in config_path:                                                     # Browse the configuration path
        config = config.get(key)
        if not config:
            break
    return bool(os.getenv(env, config))                                         # Check if item is configured or not
