import json
import os
from typing import Any, Dict, List, Union
from unittest import TestCase

from click.testing import CliRunner

from tests.mock import RekonoMock


class RekonoCommandTest(TestCase):

    command = None

    def _test(
        self,
        arguments: List[str],
        output: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
        exit_code: int = 0,
        json_file: str = None,
        invalid_url: bool = False
    ) -> None:
        credential = 'test'
        runner = CliRunner()
        input_value = f'{credential}\n{credential}\n'
        prefix = f'Username: {credential}\nPassword: \n'
        if invalid_url:
            input_value += f'{RekonoMock.url}\n'
            prefix += f'URL is invalid\nURL: {RekonoMock.url}\n'
        result = runner.invoke(self.command, arguments, input=input_value)
        terminal_output = prefix + (f'{output}\n' if output else '')
        self.assertEqual(exit_code, result.exit_code)
        self.assertEqual(terminal_output, result.output)
        if json_file:
            self.assertTrue(os.path.isfile(json_file))
            with open(json_file, 'r', encoding='utf-8') as file:
                self.assertEqual(output, file.read())
            os.remove(json_file)
            

    def _json_body(self, content: Union[Dict[str, Any], List[Dict[str, Any]]]) -> str:
        return json.dumps(content, ensure_ascii=True, indent=4)

    def _expected_output_with_headers(
        self,
        method: str,
        status_code: int,
        response_headers: Dict[str, Any],
        expected_output = Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> str:
        expected_output_with_headers = f'\n{method.upper()} /api/entities/ {status_code}\n'
        for key, value in response_headers.items():
            expected_output_with_headers += f'{key}: {value}\n'
        expected_output_with_headers += '\n'
        expected_output_with_headers += self._json_body(expected_output)
        return expected_output_with_headers
