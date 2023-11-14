"""Test "wordlists" CLI command."""

import os
from pathlib import Path

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class WordlistsTest(RekonoCommandTest):
    """Test "wordlists" CLI command."""

    unit_tests = [  # List of unit tests to execute
        {
            "arguments": ["wordlists", "get", "1"],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["wordlists", "get"],
            "output": RekonoCommandTest._json_body(
                [RekonoMock.data, RekonoMock.data, RekonoMock.data]
            ),
        },
        {
            "arguments": [
                "wordlists",
                "create",
                "-n",
                "Wordlist",
                "-t",
                "Endpoint",
                "-f",
                Path(__file__).absolute(),
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["wordlists", "delete", "1"],
            "output": RekonoCommandTest._json_body([]),
        },
    ]
