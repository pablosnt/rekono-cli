import os

from tests.framework import RekonoCommandTest
from tests.mock import RekonoMock


class WordlistsTest(RekonoCommandTest):

    unit_tests = [
        {
            'arguments': ['wordlists', 'get', '1'],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['wordlists', 'get'],
            'output': RekonoCommandTest._json_body([RekonoMock.data, RekonoMock.data, RekonoMock.data])
        },
        {
            'arguments': ['wordlists', 'create', '-n', 'Wordlist', '-t', 'Endpoint', '-f', os.path.realpath(__file__)],
            'output': RekonoCommandTest._json_body(RekonoMock.data)
        },
        {
            'arguments': ['wordlists', 'delete', '1'],
            'output': RekonoCommandTest._json_body([])
        }
    ]