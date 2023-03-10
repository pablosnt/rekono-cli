'''Test "users" CLI command.'''

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class UsersTest(RekonoCommandTest):
    '''Test "users" CLI command.'''

    unit_tests = [                                                              # List of unit tests to execute
        {
            'arguments': ['users', 'get', '1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['users', 'get'],
            'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        },
        {
            'arguments': ['users', 'delete', '1'],
            'output': RekonoCommandTest._json_body([])
        },
        {
            'arguments': ['users', 'role', '1', '--role', 'Reader'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['users', 'invite', '--email', 'newuser@rekono.com', '--role', 'Reader'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        }
    ]
