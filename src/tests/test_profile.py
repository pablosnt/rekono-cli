from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ProfileTest(RekonoCommandTest):

    unit_tests = [
        {
            'arguments': ['profile', 'get'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['profile', 'telegram', '--token', 'telegramotp'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        }
    ]
