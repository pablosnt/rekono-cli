import subprocess

from rekono.config import REKONO_USER


def create_rekono_user() -> None:
    '''Create Rekono local user to execute the Rekono services.'''
    subprocess.run(['sudo', 'useradd', REKONO_USER], capture_output=True)


def remove_rekono_user() -> None:
    '''Remove Rekono local user.'''
    subprocess.run(['sudo', 'userdel', REKONO_USER], capture_output=True)
