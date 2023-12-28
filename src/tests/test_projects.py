"""Test "projects" CLI command."""

from unittest import mock

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ProjectsTest(RekonoCommandTest):
    """Test "projects" CLI command."""

    # List of unit tests to execute
    unit_tests = [
        {
            "arguments": ["projects", "get", "1"],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["projects", "get"],
            "output": RekonoCommandTest._json_body(
                [RekonoMock.data, RekonoMock.data, RekonoMock.data]
            ),
        },
        {
            "arguments": [
                "projects",
                "create",
                "--name",
                "Process",
                "--description",
                "Test",
                "--tag",
                "test",
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": [
                "projects",
                "update",
                "1",
                "--name",
                "Process",
                "--description",
                "Test",
                "--tag",
                "test",
            ],
            "output": RekonoCommandTest._json_body(RekonoMock.data),
        },
        {
            "arguments": ["projects", "delete", "1"],
            "output": RekonoCommandTest._json_body([]),
        },
        {
            "arguments": ["projects", "remove-member", "1", "--user", "1"],
            "output": RekonoCommandTest._json_body([]),
        },
    ]

    @mock.patch(
        "rekono.framework.commands.command.Rekono.post", RekonoMock.post_empty_response
    )
    @mock.patch("rekono.framework.commands.command.Rekono", RekonoMock)
    def test_add_member(self) -> None:
        """Test to add a new project member."""
        self._cli(["projects", "add-member", "1", "--user", "1"], self._json_body([]))
