import json
import sys
from typing import Any, Dict, List

import click

import requests


def get_url(url: str, endpoint: str) -> str:
    if url.endswith('/'):
        url = url[:-1]
    prefix = '/api'
    if not endpoint.startswith(prefix):
        if not endpoint.startswith('/'):
            endpoint = f'/{endpoint}'
        endpoint = prefix + endpoint
    if not endpoint.endswith('/'):
        endpoint = f'{endpoint}/'
    return url + endpoint


def get_query_parameters(query_parameters: List[str]) -> Dict[str, Any]:
    parameters = {}
    for query_parameter in query_parameters:
        if '=' not in query_parameter:
            click.echo(f'Invalid query parameter: {query_parameter}')
            sys.exit(1)
        parsed = query_parameter.split('=')
        parameters[parsed[0]] = parsed[1]
    return parameters


def request(
    method: str,
    url: str,
    endpoint: str,
    api_token: str = None,
    params: List[str] = None,
    data: str = None
) -> requests.Response:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if api_token:
        headers['Authorization'] = f'Token {api_token}'
    response = requests.request(
        method=method.lower() if method.lower() in ['get', 'post', 'put', 'delete'] else 'get',
        url=get_url(url, endpoint),
        params=get_query_parameters(params) if params else None,
        data=data,
        headers=headers
    )
    return response
