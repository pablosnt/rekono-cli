from enum import Enum


class AuthenticationType(Enum):
    '''Supported authentication types.'''

    BASIC = 'Basic'
    BEARER = 'Bearer'
    COOKIE = 'Cookie'
    DIGEST = 'Digest'
    JWT = 'JWT'
    NTLM = 'NTLM'
