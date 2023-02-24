from rekono.commands.authentications import authentications
from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class AuthenticationsTest(RekonoCommandTest):
    
    command = authentications
    subcommands = {
        'get': [
            {
                'arguments': ['1'],
                'output': RekonoCommandTest._json_body(RekonoMock.data)
            },
            {
                'arguments': [],
                'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
            }
        ],
        'create': [
            {
                'arguments': ['--target-port', '1', '--name', 'Auth', '--credential', 'secret', '--type', 'Basic'],
                'output': RekonoCommandTest._json_body(RekonoMock.data)
            }
        ],
        'update': [
            {
                'arguments': ['1', '--target-port', '1', '--name', 'Auth', '--credential', 'secret', '--type', 'Basic'],
                'output': RekonoCommandTest._json_body(RekonoMock.data)
            }
        ],
        'delete': [
            {
                'arguments': ['1'],
                'output': RekonoCommandTest._json_body([])
            }
        ]
    }
