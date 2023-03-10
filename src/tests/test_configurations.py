'''Test "configurations" CLI command.'''

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ConfigurationsTest(RekonoCommandTest):
    '''Test "configurations" CLI command.'''

    unit_tests = [                                                              # List of unit tests to execute
        {
            'arguments': ['configurations', 'get', '1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['configurations', 'get'],
            'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        }
    ]
