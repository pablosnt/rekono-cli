import os
import shutil
import sys
import tempfile

import click
from config import REKONO_GIT_REPOSITORY, REKONO_HOME_DIRECTORY
from git import Repo


def download_rekono_source() -> None:
    '''Download Rekono source code from GitHub.'''
    if os.path.isdir(REKONO_HOME_DIRECTORY):                                    # Rekono directory already exists
        click.echo(click.style(
            f'{REKONO_HOME_DIRECTORY} already exists. Please, set the directory where Rekono '
            'should be downloaded, using the environment variable "REKONO_SOURCE"'
        ), err=True)
        click.echo('If Rekono is already installed in your system, use the "update" command')
        sys.exit(1)
    else:
        temp = tempfile.mkdtemp()                                               # Create temporal directory
        Repo.clone_from(REKONO_GIT_REPOSITORY, temp)                            # Clone Rekono in the temporal directory
        os.mkdir(REKONO_HOME_DIRECTORY)                                         # Create Rekono directory
        # Save rekono subdirectory
        shutil.move(os.path.join(temp, 'rekono'), os.path.join(REKONO_HOME_DIRECTORY, 'rekono'))
        shutil.move(os.path.join(temp, 'requirements.txt'), REKONO_HOME_DIRECTORY)      # Save requirements.txt
        shutil.rmtree(temp)                                                     # Remove temporal directory
