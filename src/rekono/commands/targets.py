import click

from rekono.framework.commands.entity import EntityCommand


class TargetsCommand(EntityCommand):

    commands = ['get', 'create', 'delete']                                      # Supported CLI commands
    entity_options = [
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
