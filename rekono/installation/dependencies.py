import os
import random
import string
import subprocess
import sys

import click

from rekono.config import (DB_DATABASE, DB_USER, REKONO_HOME_DIRECTORY,
                           REKONO_USER)
from rekono.utils.linux.apt import apt_install
from rekono.utils.linux.systemctl import systemctl_command
from rekono.utils.linux.utils import check_installation


def install_postgresql() -> str:
    '''Install PostgreSQL in the system.

    Returns:
        str: PostgreSQL password for the default rekono user
    '''
    if not check_installation('psql'):                                          # Not installed yet
        apt_install(['postgresql'])                                             # Install PostgreSQL
    systemctl_command('start', 'postgresql')                                    # Start PostgreSQL
    password = ''.join(                                                         # Generate random password
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20)
    )
    postgresql_query(f'CREATE USER {DB_USER} WITH ENCRYPTED PASSWORD \'{password}\';')    # Create Rekono user
    postgresql_query(f'CREATE DATABASE {DB_DATABASE};')                         # Create Rekono database
    # Grant permissions for the Rekono user
    postgresql_query(f'GRANT ALL PRIVILEGES ON DATABASE {DB_DATABASE} TO {DB_USER};')
    return password


def drop_rekono_database() -> None:
    '''Drop Rekono database and user from PostgreSQL.'''
    systemctl_command('start', 'postgresql')                                    # Start PostgreSQL
    postgresql_query(f'DROP DATABASE {DB_DATABASE};')                           # Drop Rekono database
    postgresql_query(f'DROP USER {DB_USER};')                                   # Drop Rekono user


def postgresql_query(query: str) -> None:
    '''Run SQL query against PostgreSQL.

    Args:
        query (str): SQL query to execute
    '''
    subprocess.run(['sudo', '-u', 'postgres', 'psql', '-c', query], capture_output=True)


def install_rq() -> None:
    '''Install Redis Queue in the system.'''
    if not check_installation('redis-server'):                                  # Not installed yet
        apt_install(['redis-server'])                                           # Install Redis Queue


def install_vue() -> None:
    '''Install Vue in the system.'''
    if not check_installation('npm'):                                           # NPM not installed yet
        apt_install(['nodejs', 'npm'])                                          # Install Node
    if not check_installation('vue'):                                           # Vue not installed yet
        exec = subprocess.run(['npm', 'install', '-g', '@vue/cli'], capture_output=True)    # Install Vue
        if exec.returncode != 0:                                                # Error during installation
            click.echo(click.style('Error during Vue installation', fg='red'), err=True)
            sys.exit(10)


def install_backend() -> None:
    '''Install backend dependencies.'''
    exec = subprocess.run([
        sys.executable, '-m', 'pip', 'install', '-q', '-r',
        os.path.join(REKONO_HOME_DIRECTORY, 'requirements.txt')
    ])
    if exec.returncode != 0:                                                    # Error during installation
        click.echo(click.style('Error during backend installation', fg='red'), err=True)
        sys.exit(10)


def install_frontend() -> None:
    '''Install frontend dependencies.'''
    exec = subprocess.run(
        ['sudo', '-u', REKONO_USER, 'npm', 'install', '.'],
        capture_output=True,
        cwd=os.path.join(REKONO_HOME_DIRECTORY, 'rekono', 'frontend')
    )
    if exec.returncode != 0:                                                    # Error during installation
        click.echo(click.style('Error during frontend installation', fg='red'), err=True)
        sys.exit(10)
