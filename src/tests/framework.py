'''Framework for unit testing of Rekono CLI.'''

import json
import os
from typing import Any, Dict, List, Optional, Union
from unittest import TestCase, mock

import click
from click.testing import CliRunner

from rekono.main import rekono
from tests.mock import RekonoMock


class RekonoCommandTest(TestCase):
    '''Framework for unit testing of Rekono CLI.'''

    testing_filepath = 'test_json_export.json'
    unit_tests: List[Dict[str, Any]] = []

    def _cli(
        self,
        arguments: List[str],
        output: Optional[str] = None,
        exit_code: int = 0,
        invalid_url: bool = False,
        input_values: bool = True
    ) -> None:
        '''Test Rekono CLI command.

        Args:
            arguments (List[str]): Command arguments
            output (Optional[str], optional): Expected output. Defaults to None.
            exit_code (int, optional): Expected HTTP status code. Defaults to 0.
            json_file (Optional[str], optional): JSON file where the output is saved. Defaults to None.
            invalid_url (bool, optional): Test command with invalid URL option. Defaults to False.
        '''
        if not self.unit_tests:
            return
        runner = CliRunner()                                                    # Create CLI runner for testing
        input_value = None
        prefix = ''
        if input_values:
            input_value = 'test\n'                                              # Input value with API token
            prefix = 'API token: \n'                                            # Prefix for expected output
            if invalid_url:                                                     # Invalid URL is enabled
                input_value += f'{RekonoMock.url}\n'                            # Add URL as input value
                # Add invalid URL message to output
                prefix += f'{click.style("URL is invalid", fg="red")}\nURL: {RekonoMock.url}\n'
        result = runner.invoke(rekono, arguments, input=input_value)      # Invoke CLI command
        terminal_output = prefix + (f'{output}\n' if output else '')            # Expected CLI command
        self.assertEqual(exit_code, result.exit_code)
        self.assertEqual(terminal_output, result.output)
        if os.path.isfile(self.testing_filepath):                               # If JSOn file provided
            with open(self.testing_filepath, 'r', encoding='utf-8') as file:    # Open file to check its content
                self.assertEqual(output, file.read())
            os.remove(self.testing_filepath)                                    # Remove testing file

    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_rekono_cli(self) -> None:
        for test in self.unit_tests or []:
            self._cli(
                test.get('arguments', []),
                test.get('output'),
                test.get('exit_code', 0),
                test.get('invalid_url', False),
                test.get('input_values', True)
            )

    @classmethod
    def _json_body(cls, content: Union[Dict[str, Any], List[Dict[str, Any]]]) -> str:
        '''Create JSON body from content.

        Args:
            content (Union[Dict[str, Any], List[Dict[str, Any]]]): Content to include in JSON body.

        Returns:
            str: JSON body.
        '''
        return json.dumps(content, ensure_ascii=True, indent=4)

    @classmethod
    def _expected_output_with_headers(
        cls,
        method: str,
        status_code: int,
        response_headers: Dict[str, Any],
        expected_output: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> str:
        '''Get expected output with HTTP response headers.

        Args:
            method (str): HTTP method used in request.
            status_code (int): Expected status code.
            response_headers (Dict[str, Any]): Expected HTTP response headers.
            expected_output (_type_, optional): Expected HTTP response body.

        Returns:
            str: Expected output with HTTP response headers.
        '''
        # Add request and response summary
        expected_output_with_headers = f'\n{method.upper()} /api/entities/ {status_code}\n'
        for key, value in response_headers.items():
            expected_output_with_headers += f'{key}: {value}\n'                 # Add header values
        expected_output_with_headers += '\n'
        expected_output_with_headers += cls._json_body(expected_output)         # Add expected body
        return expected_output_with_headers
