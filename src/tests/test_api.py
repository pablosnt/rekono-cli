'''Test "api" CLI command.'''

import json
from unittest import mock

import click

from rekono.commands.api import api
from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ApiTest(RekonoCommandTest):
    '''Test "api" CLI command.'''

    command = api                                                               # Set CLI command
    subcommands = {
        'get': [
            {
                'arguments': ['-u', RekonoMock.url, '-p', 'key1=value1', '-p', 'key2=value2', '--no-verify', 'entities/1'],
                'output': RekonoCommandTest._json_body(RekonoMock.data)
            },
            {
                'arguments': ['--all-pages', '--no-verify', 'entities'],
                'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
            },
            {
                'arguments': ['-u', 'invalidurl', 'entities/1'],
                'output': RekonoCommandTest._json_body(RekonoMock.data),
                'invalid_url': True
            },
            {
                'arguments': ['--show-headers', 'entities/1'],
                'output': RekonoCommandTest._expected_output_with_headers('GET', 200, RekonoMock.headers, RekonoMock.data)
            },
            {
                'arguments': ['--status-code', 'entities/1'],
                'output': '200'
            },
            {
                'arguments': ['--quiet', 'entities/1']
            },
            {
                'arguments': ['--json', RekonoCommandTest.testing_filepath, 'entities/1'],
                'output': RekonoCommandTest._json_body(RekonoMock.data)
                
            }
        ],
        'post': [
            {
                'arguments': ['-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities'],
                'output': RekonoCommandTest._json_body(RekonoMock.data)
            },
            {
                'arguments': ['-b', 'invalid JSON value', 'entities'],
                'output': click.style('Invalid JSON format for body value', fg='red'),
                'exit_code': 1
            }
        ],
        'put': [
            {
                'arguments': ['-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities/1'],
                'output': RekonoCommandTest._json_body(RekonoMock.data)
            }
        ],
        'delete': [
            {
                'arguments': ['-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'projects/1'],
                'output': RekonoCommandTest._json_body([])
            }
        ],
        'notfound': [
            {
                'arguments': [],
                'output': 'Usage: api [OPTIONS] COMMAND [ARGS]...\nTry \'api --help\' for help.\n\nError: No such command \'notfound\'.',
                'exit_code': 2,
                'input_values': False
            }
        ]
    }

    @mock.patch('rekono.framework.commands.command.Rekono.get', RekonoMock.get_multiple_entities)
    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_get_multiple_entities(self) -> None:
        self._cli_test(
            ['get', '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities'],
            self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        )
