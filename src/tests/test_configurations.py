from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ConfigurationsTest(RekonoCommandTest):

    unit_tests = [
        {
            'arguments': ['configurations', 'get', '1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['configurations', 'get'],
            'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        }
    ]
