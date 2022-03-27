import os
import shutil
import subprocess
import sys

from config import REKONO_HOME_DIRECTORY, SYSTEMD_SERVICES
from services.services import (BACKEND, EMAILS, EXECUTIONS, FINDINGS, FRONTEND,
                               TASKS, TELEGRAM)
from utils.linux.systemctl import systemctl_command

current_directory = os.path.dirname(os.path.realpath(__file__))
templates = os.path.join(current_directory, '..', 'utils', 'templates')


def create_rekono_services() -> None:
    '''Create systemd service.'''
    with open(os.path.join(templates, 'rekono.service'), 'r') as service:
        template = service.read()                                               # Read service template
    django = os.path.join(REKONO_HOME_DIRECTORY, 'rekono')
    vue = os.path.join(django, 'frontend')
    manage_py = f'{sys.executable} {os.path.join(django, "manage.py")}'
    for name, description, working_directory, command in [
        (BACKEND, 'Rekono backend', django, f'{manage_py} runserver'),
        (FRONTEND, 'Rekono frontend', vue, f'{shutil.which("npm")} run serve'),
        (TELEGRAM, 'Rekono Telegram bot', django, f'{manage_py} telegram_bot'),
        (TASKS, 'Rekono tasks worker', django, f'{manage_py} rqworker tasks-queue'),
        (
            EXECUTIONS,
            'Rekono executions worker number %i',
            django,
            f'{manage_py} rqworker --with-scheduler executions-queue'
        ),
        (FINDINGS, 'Rekono findings worker', django, f'{manage_py} rqworker findings-queue'),
        (EMAILS, 'Rekono emails worker', django, f'{manage_py} rqworker emails-queue')
    ]:
        temppath = os.path.join(templates, f'rekono-{name}.service')
        with open(temppath, 'w') as temp:
            temp.write(template.format(                                         # Add service data
                description=description,
                working_directory=working_directory,
                command=command
            ))
        subprocess.run(['sudo', 'mv', temppath, SYSTEMD_SERVICES])


def rekono_services_command(command: str, executors: int) -> None:
    for service in [BACKEND, FRONTEND, TELEGRAM, TASKS, FINDINGS, EMAILS]:
        systemctl_command(command, f'rekono-{service}')
    for number in range(executors):
        systemctl_command(command, f'rekono-{EXECUTIONS}{number + 1}')
