'''Test "settings" CLI command.'''

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class SettingsTest(RekonoCommandTest):
    '''Test "settings" CLI command.'''

    unit_tests = [                                                              # List of unit tests to execute
        {
            'arguments': ['settings', 'get'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        }
    ]
