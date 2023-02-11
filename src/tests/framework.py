'''Framework for unit testing of Rekono CLI.'''

import json
import os
from typing import Any, Dict, List, Union
from unittest import TestCase

from click.testing import CliRunner

from tests.mock import RekonoMock


class RekonoCommandTest(TestCase):
    '''Framework for unit testing of Rekono CLI.'''

    command = None                                                              # CLI command to test

    def _test(
        self,
        arguments: List[str],
        output: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
        exit_code: int = 0,
        json_file: str = None,
        invalid_url: bool = False
    ) -> None:
        '''Test Rekono CLI command.

        Args:
            arguments (List[str]): Command arguments
            output (Union[Dict[str, Any], List[Dict[str, Any]]], optional): Expected command output. Defaults to None.
            exit_code (int, optional): Expected HTTP status code. Defaults to 0.
            json_file (str, optional): JSON file where the output is saved. Defaults to None.
            invalid_url (bool, optional): Test command with invalid URL option. Defaults to False.
        '''
        credential = 'test'
        runner = CliRunner()                                                    # Create CLI runner for testing
        input_value = f'{credential}\n{credential}\n'                           # Input value with basic credentials
        prefix = f'Username: {credential}\nPassword: \n'                        # Prefix for expected output
        if invalid_url:                                                         # Invalid URL is enabled
            input_value += f'{RekonoMock.url}\n'                                # Add URL as input value
            prefix += f'URL is invalid\nURL: {RekonoMock.url}\n'                # Add invalid URL message to output
        result = runner.invoke(self.command, arguments, input=input_value)      # Invoke CLI command
        terminal_output = prefix + (f'{output}\n' if output else '')            # Expected CLI command
        self.assertEqual(exit_code, result.exit_code)
        self.assertEqual(terminal_output, result.output)
        if json_file:                                                           # If JSOn file provided
            self.assertTrue(os.path.isfile(json_file))
            with open(json_file, 'r', encoding='utf-8') as file:                # Open file to check its content
                self.assertEqual(output, file.read())
            os.remove(json_file)                                                # Remove testing file

    def _json_body(self, content: Union[Dict[str, Any], List[Dict[str, Any]]]) -> str:
        '''Create JSON body from content.

        Args:
            content (Union[Dict[str, Any], List[Dict[str, Any]]]): Content to include in JSON body.

        Returns:
            str: JSON body.
        '''
        return json.dumps(content, ensure_ascii=True, indent=4)

    def _expected_output_with_headers(
        self,
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
        expected_output_with_headers += self._json_body(expected_output)        # Add expected body
        return expected_output_with_headers
