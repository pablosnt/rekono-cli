from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ExecutionsTest(RekonoCommandTest):

    unit_tests = [
        {
            'arguments': ['executions', 'get', '1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['executions', 'get'],
            'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        }
    ]
