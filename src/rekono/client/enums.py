'''Rekono enums.'''

from enum import Enum


class AuthenticationType(Enum):
    '''Supported authentication types.'''

    BASIC = 'Basic'
    BEARER = 'Bearer'
    COOKIE = 'Cookie'
    DIGEST = 'Digest'
    JWT = 'JWT'
    NTLM = 'NTLM'


class UserRole(Enum):
    '''User role names.'''

    ADMIN = 'Admin'
    AUDITOR = 'Auditor'
    READER = 'Reader'


class IntensityRank(Enum):
    '''Intensity ranks.'''

    SNEAKY = 'Sneaky'
    LOW = 'Low'
    NORMAL = 'Normal'
    HARD = 'Hard'
    INSANE = 'Insane'


class TimeUnit(Enum):
    '''Time units supported for Task scheduling and repeating configuration.'''

    MINUTES = 'Minutes'
    HOURS = 'Hours'
    DAYS = 'Days'
    WEEKS = 'Weeks'


class WordlistType(Enum):
    '''Wordlist type names.'''

    ENDPOINT = 'Endpoint'
    SUBDOMAIN = 'Subdomain'
