import os

from rekono.config import REKONO_HOME_DIRECTORY, SYSTEMD_SERVICES
from rekono.services.services import (BACKEND, EMAILS, EXECUTIONS, FINDINGS,
                                      FRONTEND, TASKS, TELEGRAM)


def check_rekono_installation() -> bool:
    '''Check if Rekono is already installed or not.

    Returns:
        bool: Indicate if Rekono is installed or not.
    '''
    is_installed = os.path.isdir(REKONO_HOME_DIRECTORY)
    for service in [BACKEND, FRONTEND, TELEGRAM, TASKS, EXECUTIONS, FINDINGS, EMAILS]:
        is_installed = is_installed and os.path.isfile(os.path.join(SYSTEMD_SERVICES, f'rekono-{service}.service'))
    return is_installed
