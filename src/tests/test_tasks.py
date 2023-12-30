"""Test "tasks" CLI command."""

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class TasksTest(RekonoCommandTest):
    """Test "tasks" CLI command."""

    # List of unit tests to execute
    unit_tests = [
        {
            "arguments": ["tasks", "get", "1"],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["tasks", "get"],
            "output": RekonoCommandTest._json_body(
                [RekonoMock.data, RekonoMock.data, RekonoMock.data]
            ),
        },
        {
            "arguments": [
                "tasks",
                "create",
                "--target",
                "1",
                "--process",
                "1",
                "--intensity",
                "Normal",
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": [
                "tasks",
                "create",
                "--target",
                "1",
                "--tool",
                "1",
                "--configuration",
                "1",
                "--intensity",
                "Hard",
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": [
                "tasks",
                "create",
                "--target",
                "1",
                "--process",
                "1",
                "--intensity",
                "Normal",
                "--scheduled-at",
                "2000-01-01 01:00:00",
                "--wordlist",
                "1",
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": [
                "tasks",
                "create",
                "--target",
                "1",
                "--process",
                "1",
                "--intensity",
                "Normal",
                "--scheduled-in",
                "5",
                "--scheduled-time-unit",
                "Hours",
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": [
                "tasks",
                "create",
                "--target",
                "1",
                "--process",
                "1",
                "--intensity",
                "Normal",
                "--repeat-in",
                "5",
                "--repeat-time-unit",
                "Days",
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["tasks", "cancel", "1"],
            "output": RekonoCommandTest._json_body([]),
        },
        {
            "arguments": ["tasks", "repeat", "1"],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
    ]
