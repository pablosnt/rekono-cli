'''Test "api" CLI command.'''

import json
from unittest import mock

import click

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ApiTest(RekonoCommandTest):
    '''Test "api" CLI command.'''

    unit_tests = [
        {
            'arguments': ['api', 'get', '-u', RekonoMock.url, '-p', 'key1=value1', '-p', 'key2=value2', '--no-verify', 'entities/1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['api', 'get', '--all-pages', '--no-verify', 'entities'],
            'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        },
        {
            'arguments': ['api', 'get', '-u', 'invalidurl', 'entities/1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data),
            'invalid_url': True
        },
        {
            'arguments': ['api', 'get', '--show-headers', 'entities/1'],
            'output': RekonoCommandTest._expected_output_with_headers('GET', 200, RekonoMock.headers, RekonoMock.data)
        },
        {
            'arguments': ['api', 'get', '--status-code', 'entities/1'],
            'output': '200'
        },
        {
            'arguments': ['api', 'get', '--quiet', 'entities/1']
        },
        {
            'arguments': ['api', 'get', '--json', RekonoCommandTest.testing_filepath, 'entities/1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
            
        },
        {
            'arguments': ['api', 'post', '-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['api', 'post', '-b', 'invalid JSON value', 'entities'],
            'output': click.style('Invalid JSON format for body value', fg='red'),
            'exit_code': 1
        },
        {
            'arguments': ['api', 'put', '-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities/1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['api', 'delete', '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'projects/1'],
            'output': RekonoCommandTest._json_body([])
        },
        {
            'arguments': ['api', 'notfound'],
            'output': 'Usage: rekono api [OPTIONS] COMMAND [ARGS]...\nTry \'rekono api --help\' for help.\n\nError: No such command \'notfound\'.',
            'exit_code': 2,
            'input_values': False
        }
    ]

    @mock.patch('rekono.framework.commands.command.Rekono.get', RekonoMock.get_multiple_entities)
    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_get_multiple_entities(self) -> None:
        self._cli(
            ['api', 'get', '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities'],
            self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        )
