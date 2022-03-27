import os
import subprocess
import sys

from rekono.config import REKONO_HOME_DIRECTORY


def manage_command(command: str) -> None:
    '''Execute Django command.

    Args:
        command (str): Command to run
    '''
    subprocess.run([sys.executable, 'manage.py', command], cwd=os.path.join(REKONO_HOME_DIRECTORY, 'rekono'))
