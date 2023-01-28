import json
import sys
from typing import Any, Dict, List

import click

import requests


def get_url(url: str, endpoint: str) -> str:
    '''Get Rekono URL from base URL and endpoint after sanitization.

    Args:
        url (str): Rekono base URL
        endpoint (str): Rekono endpoint

    Returns:
        str: Rekono full URL
    '''
    if url.endswith('/'):
        url = url[:-1]                                                          # Remove latest slash from base URL
    prefix = '/api'
    if not endpoint.startswith(prefix):
        if not endpoint.startswith('/'):                                        # Add initial slash to the endpoint
            endpoint = f'/{endpoint}'
        endpoint = prefix + endpoint                                            # Add /api prefix to the endpoint
    if not endpoint.endswith('/'):
        endpoint = f'{endpoint}/'                                               # Add final slash to the endpoint
    return url + endpoint


def get_query_parameters(query_parameters: List[str]) -> Dict[str, Any]:
    '''Get query parameters to send in HTTP request.

    Args:
        query_parameters (List[str]): Query parameters to send

    Returns:
        Dict[str, Any]: Query parameters in dict format
    '''
    parameters = {}
    for query_parameter in query_parameters:
        if '=' not in query_parameter:                                          # Invalid parameter
            click.echo(f'Invalid query parameter: {query_parameter}')
            sys.exit(1)
        parsed = query_parameter.split('=')
        parameters[parsed[0]] = parsed[1]                                       # Add query parameter
    return parameters


def request(
    method: str,
    url: str,
    endpoint: str,
    api_token: str = None,
    params: List[str] = None,
    data: str = None
) -> requests.Response:
    '''Make a request to the Rekono API.

    Args:
        method (str): HTTP method to use
        url (str): Rekono base URL
        endpoint (str): Rekono endpoint to call
        api_token (str, optional): Rekono API token for authentication. Defaults to None.
        params (List[str], optional): Query parameters to send. Defaults to None.
        data (str, optional): Body data to send. Defaults to None.

    Returns:
        requests.Response: _description_
    '''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if api_token:
        headers['Authorization'] = f'Token {api_token}'                         # Add header for authentication
    response = requests.request(
        method=method.lower() if method.lower() in ['get', 'post', 'put', 'delete'] else 'get',
        url=get_url(url, endpoint),
        params=get_query_parameters(params) if params else None,
        data=data,
        headers=headers
    )
    return response
