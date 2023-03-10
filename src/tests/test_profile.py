'''Test "profile" CLI command.'''

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ProfileTest(RekonoCommandTest):
    '''Test "profile" CLI command.'''

    unit_tests = [                                                              # List of unit tests to execute
        {
            'arguments': ['profile', 'get'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['profile', 'telegram', '--token', 'telegramotp'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        }
    ]
