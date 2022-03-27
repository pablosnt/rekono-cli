import os
import shutil
import subprocess
import tempfile

from config import REKONO_GIT_REPOSITORY, REKONO_HOME_DIRECTORY
from git import Repo


def download_source_code() -> None:
    '''Download Rekono source code from GitHub.'''
    temp = tempfile.mkdtemp()                                                   # Create temporal directory
    Repo.clone_from(REKONO_GIT_REPOSITORY, temp)                                # Clone Rekono in the temporal directory
    if not os.path.isdir(REKONO_HOME_DIRECTORY):
        subprocess.run(['sudo', 'mkdir', REKONO_HOME_DIRECTORY])                # Create Rekono directory
        subprocess.run(['sudo', 'chmod', '-R', '777', REKONO_HOME_DIRECTORY])   # Change Rekono directory permissions
    # Save rekono subdirectory
    shutil.move(os.path.join(temp, 'rekono'), os.path.join(REKONO_HOME_DIRECTORY, 'rekono'))
    shutil.move(os.path.join(temp, 'requirements.txt'), REKONO_HOME_DIRECTORY)      # Save requirements.txt
    shutil.rmtree(temp)                                                         # Remove temporal directory
