from unittest import mock

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class FindingsTest(RekonoCommandTest):

    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_get_one_finding(self) -> None:
        self._cli([self.__class__.__name__.lower().replace('test', ''), 'get', '1'], self._json_body(RekonoMock.data))

    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_get_multiple_findings(self) -> None:
        self._cli([self.__class__.__name__.lower().replace('test', ''), 'get'], self._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data]))

    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_disable_finding(self) -> None:
        self._cli([self.__class__.__name__.lower().replace('test', ''), 'disable', '1'], self._json_body([]))

    @mock.patch('rekono.framework.commands.command.Rekono.post', RekonoMock.post_empty_response)
    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_enable_finding(self) -> None:
        self._cli([self.__class__.__name__.lower().replace('test', ''), 'enable', '1'], self._json_body([]))


class CredentialsTest(FindingsTest):
    pass


class ExploitsTest(FindingsTest):
    pass


class HostsTest(FindingsTest):
    pass

class PathsTest(FindingsTest):
    pass


class PortsTest(FindingsTest):
    pass


class TechnologiesTest(FindingsTest):
    pass


class VulnerabilitiesTest(FindingsTest):
    pass


class OSINTTest(FindingsTest):

    @mock.patch('rekono.framework.commands.command.Rekono', RekonoMock)
    def test_disable_finding(self) -> None:
        self._cli(['osint', 'target', '1'], self._json_body(RekonoMock.data))
