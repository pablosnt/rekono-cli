from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ToolsTest(RekonoCommandTest):

   unit_tests = [
        {
            'arguments': ['tools', 'get', '1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['tools', 'get'],
            'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        }
    ]
