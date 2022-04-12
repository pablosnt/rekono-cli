import os
import shutil
import subprocess
import sys

from rekono.config import REKONO_HOME_DIRECTORY, REKONO_USER, SYSTEMD_SERVICES
from rekono.services.services import (BACKEND, EMAILS, EXECUTIONS, FINDINGS,
                                      FRONTEND, TASKS, TELEGRAM)
from rekono.utils.linux.systemctl import systemctl_command

current_directory = os.path.dirname(os.path.realpath(__file__))
templates = os.path.join(current_directory, 'templates')


def create_rekono_services() -> None:
    '''Create all Rekono systemctl services.'''
    with open(os.path.join(templates, 'rekono.service'), 'r') as service:
        template = service.read()                                               # Read service template
    django = os.path.join(REKONO_HOME_DIRECTORY, 'rekono')
    vue = os.path.join(django, 'frontend')
    manage_py = f'{sys.executable} {os.path.join(django, "manage.py")}'
    for name, description, working_directory, command in [
        (BACKEND, 'Rekono backend', django, f'{manage_py} runserver'),
        (FRONTEND, 'Rekono frontend', vue, f'{shutil.which("npm")} run serve'),
        (TELEGRAM, 'Rekono Telegram bot', django, f'{manage_py} telegram_bot'),
        (TASKS, 'Rekono tasks worker', django, f'{manage_py} rqworker --with-scheduler tasks-queue'),
        (EXECUTIONS, 'Rekono executions worker number %i', django, f'{manage_py} rqworker executions-queue'),
        (FINDINGS, 'Rekono findings worker', django, f'{manage_py} rqworker findings-queue'),
        (EMAILS, 'Rekono emails worker', django, f'{manage_py} rqworker emails-queue')
    ]:
        temppath = os.path.join(templates, f'rekono-{name}.service')
        with open(temppath, 'w') as temp:
            temp.write(template.format(                                         # Add service data
                description=description,
                user=REKONO_USER,
                working_directory=working_directory,
                command=command
            ))
        subprocess.run(['sudo', 'mv', temppath, SYSTEMD_SERVICES])


def remove_rekono_services() -> None:
    '''Remove all Rekono systemctl services.'''
    for service in [BACKEND, FRONTEND, TELEGRAM, TASKS, EXECUTIONS, FINDINGS, EMAILS]:
        if os.path.isfile(os.path.join(SYSTEMD_SERVICES, f'rekono-{service}.service')):
            subprocess.run(
                ['sudo', 'rm', os.path.join(SYSTEMD_SERVICES, f'rekono-{service}.service')], capture_output=True
            )


def rekono_services_command(command: str, executors: int) -> None:
    '''Execute systemctl command to all Rekono services.

    Args:
        command (str): Systemctl command
        executors (int): Number of instances afected for executions worker service
    '''
    services = [BACKEND, FRONTEND, TELEGRAM, TASKS, FINDINGS, EMAILS]
    for number in range(executors):
        services.append(f'{EXECUTIONS}{number + 1}')                            # Add executions worker instances
    for service in services:
        systemctl_command(command, f'rekono-{service}')
