import os
import shutil
import sys
import tempfile

import click
from config import REKONO_GIT_REPOSITORY, REKONO_SOURCE_DIRECTORY
from git import Repo


def download_rekono_source() -> None:
    '''Download Rekono source code from GitHub.'''
    if os.path.isdir(REKONO_SOURCE_DIRECTORY):                                  # Rekono source directory already exists
        click.echo(click.style(
            f'{REKONO_SOURCE_DIRECTORY} already exists. Please, set the directory where Rekono '
            'should be downloaded, using the environment variable "REKONO_SOURCE"'
        ), err=True)
        click.echo('If Rekono is already installed in your system, use the "update" command')
        sys.exit(1)
    else:
        temp = tempfile.mkdtemp()                                               # Create temporal directory
        Repo.clone_from(REKONO_GIT_REPOSITORY, temp)                            # Clone Rekono in the temporal directory
        os.mkdir(REKONO_SOURCE_DIRECTORY)                                       # Create Rekono source code directory
        shutil.move(os.path.join(temp, 'rekono'), REKONO_SOURCE_DIRECTORY)      # Save rekono subdirectory
        shutil.move(os.path.join(temp, 'requirements.txt'), REKONO_SOURCE_DIRECTORY)    # Save requirements.txt
        shutil.rmtree(temp)                                                     # Remove temporal directory
