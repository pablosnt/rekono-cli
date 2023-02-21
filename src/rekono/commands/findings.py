import click

from rekono.framework.commands.entity import EntityCommand


class FindingsCommand(EntityCommand):
    '''Base Rekono CLI command for finding entities.'''

    commands = ['get', 'enable', 'disable']                                     # Supported CLI commands
    commands_mapping = {                                                        # Mapping between commands and methods
        'get': 'get_entity',
        'disable': 'delete_entity',
    }

@click.group('credentials', cls=FindingsCommand, help='Manage credentials')
def credentials():
    '''Manage credentials.'''


@click.group('exploits', cls=FindingsCommand, help='Manage exploits')
def exploits():
    '''Manage exploits.'''


@click.group('hosts', cls=FindingsCommand, help='Manage hosts')
def hosts():
    '''Manage hosts.'''


@click.group('paths', cls=FindingsCommand, help='Manage paths')
def paths():
    '''Manage paths.'''


@click.group('ports', cls=FindingsCommand, help='Manage ports')
def ports():
    '''Manage ports.'''


@click.group('technologies', cls=FindingsCommand, help='Manage technologies')
def technologies():
    '''Manage technologies.'''


@click.group('vulnerabilities', cls=FindingsCommand, help='Manage vulnerabilities')
def vulnerabilities():
    '''Manage vulnerabilities.'''


class OSINTCommand(FindingsCommand):
    '''Base Rekono CLI command for OSINT entities.'''

    commands = ['get', 'enable', 'disable', 'target']                           # Supported CLI commands


@click.group('osint', cls=OSINTCommand, help='Manage OSINT findings')
def osint():
    '''Manage OSINT findings.'''
