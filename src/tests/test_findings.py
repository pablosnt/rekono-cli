"""Test findings CLI command."""

from unittest import mock

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class FindingsTest(RekonoCommandTest):
    """Test findings CLI command."""

    @mock.patch("rekono.framework.commands.command.Rekono", RekonoMock)
    def test_get_one_finding(self) -> None:
        """Test to get one finding by ID."""
        self._cli(
            [self.__class__.__name__.lower().replace("test", ""), "get", "1"],
            self._json_body(RekonoMock.data),
        )

    @mock.patch("rekono.framework.commands.command.Rekono", RekonoMock)
    def test_get_multiple_findings(self) -> None:
        """Test to get multiple findings."""
        self._cli(
            [self.__class__.__name__.lower().replace("test", ""), "get"],
            self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data]),
        )

    @mock.patch("rekono.framework.commands.command.Rekono", RekonoMock)
    def test_disable_finding(self) -> None:
        """Test to disable one finding."""
        self._cli(
            [self.__class__.__name__.lower().replace("test", ""), "disable", "1"],
            self._json_body([]),
        )

    @mock.patch(
        "rekono.framework.commands.command.Rekono.post", RekonoMock.post_empty_response
    )
    @mock.patch("rekono.framework.commands.command.Rekono", RekonoMock)
    def test_enable_finding(self) -> None:
        """Test to enable one finding."""
        self._cli(
            [self.__class__.__name__.lower().replace("test", ""), "enable", "1"],
            self._json_body([]),
        )


class CredentialsTest(FindingsTest):
    """Test "credentials" CLI command."""


class ExploitsTest(FindingsTest):
    """Test "exploits" CLI command."""


class HostsTest(FindingsTest):
    """Test "hosts" CLI command."""


class PortsTest(FindingsTest):
    """Test "ports" CLI command."""


class PathsTest(FindingsTest):
    """Test "paths" CLI command."""


class TechnologiesTest(FindingsTest):
    """Test "technologoies" CLI command."""


class VulnerabilitiesTest(FindingsTest):
    """Test "vulnerabilities" CLI command."""


class OSINTTest(FindingsTest):
    """Test "osint" CLI command."""

    @mock.patch("rekono.framework.commands.command.Rekono", RekonoMock)
    def test_target_creation(self) -> None:
        """Test to create one target from OSINT data."""
        self._cli(["osint", "target", "1"], self._json_body(RekonoMock.data))
