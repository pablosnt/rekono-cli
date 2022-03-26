import os
import subprocess
import tempfile

from config import SYSTEMD_SERVICES

current_directory = os.path.dirname(os.path.realpath(__file__))
templates = os.path.join(current_directory, '..', 'templates')


def create_service(name: str, description: str, working_directory: str, command: str) -> None:
    '''Create systemd service.

    Args:
        name (str): Service name
        description (str): Service description
        working_directory (str): Working directory where the service will be executed
        command (str): Service command
    '''
    with open(os.path.join(templates, 'rekono.service'), 'r') as service:
        template = service.read()                                               # Read service template
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(template.format(                                             # Add service data
            description=description,
            working_directory=working_directory,
            command=command
        ).encode())
        subprocess.run(['sudo', 'cp', temp.name, os.path.join(SYSTEMD_SERVICES, f'rekono-{name}.service')])
