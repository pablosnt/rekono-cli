import subprocess

from rekono.config import REKONO_HOME_DIRECTORY, REKONO_USER


def create_rekono_user() -> None:
    '''Create Rekono local user to execute the Rekono services.'''
    subprocess.run(
        ['sudo', 'useradd', '-r', REKONO_USER, '--shell=/usr/sbin/nologin', f'--home={REKONO_HOME_DIRECTORY}'],
        capture_output=True
    )
    subprocess.run(
        ['sudo', 'chown', '-R', f'{REKONO_USER}:{REKONO_USER}', REKONO_HOME_DIRECTORY],
        capture_output=True
    )


def remove_rekono_user() -> None:
    '''Remove Rekono local user.'''
    subprocess.run(['sudo', 'userdel', REKONO_USER], capture_output=True)
