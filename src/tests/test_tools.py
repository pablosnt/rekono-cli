"""Test "tools" CLI command."""

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ToolsTest(RekonoCommandTest):
    """Test "tools" CLI command."""

    # List of unit tests to execute
    unit_tests = [
        {
            "arguments": ["tools", "get", "1"],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["tools", "get"],
            "output": RekonoCommandTest._json_body(
                [RekonoMock.data, RekonoMock.data, RekonoMock.data]
            ),
        },
    ]
