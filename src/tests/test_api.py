import json
from unittest.mock import patch

from rekono.commands.api import api
from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ApiTest(RekonoCommandTest):
    
    command = api

    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_get(self) -> None:
        self._test(
            ['get', '-p', 'key1=value1', '-p', 'key2=value2', '-n', 'entities/1'],
            output=self._json_body(RekonoMock.data)
        )

    @patch('rekono.framework.commands.Rekono.get', RekonoMock.get_multiple_entities)
    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_get_multiple(self) -> None:
        self._test(
            ['get', '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'entities'],
            output=self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        )

    @patch('rekono.framework.commands.Rekono.get', RekonoMock.get_paginated_entities)
    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_get_all_pages(self) -> None:
        self._test(
            ['get', '--all-pages', '--no-verify', 'entities'],
            output=self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        )

    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_post(self) -> None:
        self._test(
            ['post', '-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '-n', 'entities'],
            output=self._json_body(RekonoMock.data)
        )
        self._test(
            ['post', '-b', 'invalid JSON value', 'entities'],
            output='Invalid JSON format for body value',
            exit_code=1
        )

    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_put(self) -> None:
        self._test(
            ['put', '-b', json.dumps(RekonoMock.data), '-h', 'key1=value1', '-h', 'key2=value2', '-n', 'entities/1'],
            output=self._json_body(RekonoMock.data)
        )

    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_delete(self) -> None:
        self._test(
            ['delete', '-h', 'key1=value1', '-h', 'key2=value2', '--no-verify', 'projects/1'],
            output=self._json_body([])
        )

    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_url_option(self) -> None:
        self._test(['get', '-u', RekonoMock.url, 'entities/1'], output=self._json_body(RekonoMock.data))
        self._test(
            ['get', '-u', 'invalidurl', 'entities/1'],
            output=self._json_body(RekonoMock.data),
            invalid_url=True
        )

    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_display_options(self) -> None:
        self._test(
            ['get', '--show-headers', 'entities/1'],
            output=self._expected_output_with_headers('GET', 200, RekonoMock.response_headers, RekonoMock.data)
        )
        self._test(['get', '--status-code', 'entities/1'], output='200')
        self._test(['get', '--quiet', 'entities/1'])

    @patch('rekono.framework.commands.Rekono', RekonoMock)
    def test_json_output(self) -> None:
        test_filepath = 'test_json_export.json'
        self._test(
            ['get', '--json', test_filepath, 'entities/1'],
            output=self._json_body(RekonoMock.data),
            json_file=test_filepath
        )
