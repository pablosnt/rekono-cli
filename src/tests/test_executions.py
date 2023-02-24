from rekono.commands.executions import executions
from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class ExecutionsTest(RekonoCommandTest):
    
    command = executions
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
        ]
    }
