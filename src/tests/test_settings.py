from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class SettingsTest(RekonoCommandTest):

    unit_tests = [
        {
            'arguments': ['settings', 'get'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        }
    ]
