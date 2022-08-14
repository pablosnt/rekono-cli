import os
import shutil
import subprocess
import tempfile

from git import Repo

from rekono.config import (REKONO_GIT_REPOSITORY, REKONO_HOME_DIRECTORY,
                           REKONO_USER)


def download_source_code() -> None:
    '''Download Rekono source code from GitHub.'''
    temp = tempfile.mkdtemp()                                                   # Create temporal directory
    Repo.clone_from(REKONO_GIT_REPOSITORY, temp)                                # Clone Rekono in the temporal directory
    if not os.path.isdir(REKONO_HOME_DIRECTORY):
        subprocess.run(['sudo', 'mkdir', REKONO_HOME_DIRECTORY])                # Create Rekono directory
        subprocess.run(['sudo', 'chmod', '-R', '777', REKONO_HOME_DIRECTORY])   # Change Rekono directory permissions
    rekono = os.path.join(REKONO_HOME_DIRECTORY, 'rekono')
    if os.path.isdir(rekono):                                                   # Check if Rekono subdirectory exists
        subprocess.run(['sudo', 'rm', '-R', rekono, '-f'], capture_output=True)     # Remove Rekono subdirectory
    shutil.move(os.path.join(temp, 'rekono'), rekono)                           # Save Rekono subdirectory
    requirements = os.path.join(REKONO_HOME_DIRECTORY, 'requirements.txt')
    if os.path.isfile(requirements):                                            # Check if requirements.txt exists
        os.remove(requirements)                                                 # Remove requirements.txt
    shutil.move(os.path.join(temp, 'requirements.txt'), REKONO_HOME_DIRECTORY)  # Save requirements.txt
    shutil.rmtree(temp, ignore_errors=True)                                     # Remove temporal directory
    # Change owner of the Rekono home directory
    subprocess.run(['sudo', 'chown', '-R', f'{REKONO_USER}:{REKONO_USER}', REKONO_HOME_DIRECTORY])
