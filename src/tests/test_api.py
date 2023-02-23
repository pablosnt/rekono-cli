'''Test "api" CLI command.'''

import json
from unittest.mock import patch

import click

from rekono.commands.api import api
from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ApiTest(RekonoCommandTest):
    '''Test "api" CLI command.'''

    command = api                                                               # Set CLI command

    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_get(self) -> None:
        '''Test "api get" command.'''
        self._test(
            ['get', '-u', RekonoMock.url, '-p', 'key1=value1', '-p', 'key2=value2', '--no-verify', 'entities/1'],
            output=self._json_body(RekonoMock.data)
        )
        # Test command with invalid URL option
        self._test(['get', '-u', 'invalidurl', 'entities/1'], output=self._json_body(RekonoMock.data), invalid_url=True)

    @patch('rekono.framework.commands.command.Rekono.get', RekonoMock.get_multiple_entities)
    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_get_multiple(self) -> None:
        '''Test "api get" command with multiple entities as response.'''
        self._test(
            ['get', '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities'],
            output=self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        )

    @patch('rekono.framework.commands.command.Rekono.get', RekonoMock.get_paginated_entities)
    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_get_all_pages(self) -> None:
        '''Test "api get" command with paginated responses.'''
        self._test(
            ['get', '--all-pages', '--no-verify', 'entities'],
            output=self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        )

    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_post(self) -> None:
        '''Test "api post" command.'''
        self._test(
            ['post', '-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities'],
            output=self._json_body(RekonoMock.data)
        )
        self._test(                                                             # Test command with invalid body option
            ['post', '-b', 'invalid JSON value', 'entities'],
            output=click.style('Invalid JSON format for body value', fg='red'),
            exit_code=1
        )

    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_put(self) -> None:
        '''Test "api put" command.'''
        self._test(
            ['put', '-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities/1'],
            output=self._json_body(RekonoMock.data)
        )

    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_delete(self) -> None:
        '''Test "api delete" command.'''
        self._test(
            ['delete', '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'projects/1'],
            output=self._json_body([])
        )

    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_display_options(self) -> None:
        '''Test display options with "api get" command.'''
        self._test(                                                             # Test show headers option
            ['get', '--show-headers', 'entities/1'],
            output=self._expected_output_with_headers('GET', 200, RekonoMock.headers, RekonoMock.data)
        )
        self._test(['get', '--status-code', 'entities/1'], output='200')        # Test status code option
        self._test(['get', '--quiet', 'entities/1'])                            # Test quiet option

    @patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_json_output(self) -> None:
        '''Test JSON option with "api get" command.'''
        test_filepath = 'test_json_export.json'
        self._test(
            ['get', '--json', test_filepath, 'entities/1'],
            output=self._json_body(RekonoMock.data),
            json_file=test_filepath
        )
