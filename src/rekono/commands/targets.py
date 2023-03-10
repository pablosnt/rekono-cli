'''CLI command to manage Target entities.'''

import click

from rekono.framework.commands.entity import EntityCommand


class TargetsCommand(EntityCommand):
    '''CLI command to manage Target entities.'''

    commands = ['get', 'create', 'delete']                                      # CLI commands
    help_messages = {                                                           # Help messages for each command
        'get': 'Get all targets or one if ID is provided',
        'create': 'Create target',
        'delete': 'Delete target',
    }
    entity_options = [                                                          # Specific options for post and put
        click.option('-p', '--project', 'project', required=True, type=int, help='Project ID'),
        click.option('-t', '--target', 'target', required=True, type=str, help='Target address'),
        click.option(
            '-d', '--dd-engagement', 'defectdojo_engagement_id',
            required=False, default=None, type=int,
            help='Engagement ID in Defect-Dojo'
        )
    ]


@click.group('targets', cls=TargetsCommand, help='Manage targets')
def targets():
    '''Manage targets.'''
