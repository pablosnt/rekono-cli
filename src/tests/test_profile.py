"""Test "profile" CLI command."""

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ProfileTest(RekonoCommandTest):
    """Test "profile" CLI command."""

    # List of unit tests to execute
    unit_tests = [
        {
            "arguments": ["profile", "get"],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["profile", "telegram", "--token", "telegramotp"],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
    ]
