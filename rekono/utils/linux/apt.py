import subprocess
import sys
from typing import List

import click


def apt_update() -> None:
    '''Update APT sources.'''
    subprocess.run(['sudo', 'apt', 'update'], capture_output=True)


def apt_install(packages: List[str], required: bool = True) -> None:
    '''Install APT packages.

    Args:
        packages (List[str]): Packages to install
        required (bool, optional): Indicate if packages are required or not. Defaults to True.
    '''
    command = ['sudo', 'apt', 'install']
    command.extend(packages)
    command.append('-y')
    exec = subprocess.run(command, capture_output=True)
    if exec.returncode != 0 and required:                                       # Required packages
        click.echo(click.style(f'Error during {" ".join(packages)} installation', fg='red'), err=True)
        sys.exit(10)
