import json
from getpass import getpass
from typing import List, Tuple

import click
from rekono.api.requests import request
from rekono.config import API_TOKEN, API_URL

import requests


def get_url_and_token() -> Tuple[str, str]:
    api_url = API_URL if API_URL else input('API URL: ')
    api_token = API_TOKEN
    if not api_token:
        username = input('Username: ')
        password = getpass('Password: ')
        response = request(
            'post', api_url, '/api/api-token/',
            data='{' + f'"username": "{username}", "password": "{password}"' + '}'
        )
        if response.status_code == 200:
            api_token = response.json().get('token')
    return api_url, api_token


def display_api_response(response: requests.Response) -> str:
    try:
        text = json.dumps(response.json(), indent=4)
    except:
        text = response.text if response.text else 'No response content'
    click.echo(f'\n{text}\n')


@click.group('api', help='Make requests to Rekono API REST')
def api():
    pass


@api.command('get', help='HTTP GET request to Rekono API')
@click.argument('endpoint', type=str, nargs=1)
@click.option(
    '-p', '--parameter', 'query_parameters', type=str, multiple=True,
    required=False, help='HTTP query parameter. Format <parameter>=<value>'
)
def get(endpoint: str, query_parameters: List[str]):
    api_url, api_token = get_url_and_token()
    response = request('get', api_url, endpoint, api_token=api_token, params=query_parameters)
    display_api_response(response)


@api.command('post', help='HTTP POST request to Rekono API')
@click.argument('endpoint', type=str, nargs=1)
@click.option('-d', '--data', 'data', type=str, required=False, help='HTTP body data. JSON format')
def post(endpoint: str, data: str):
    api_url, api_token = get_url_and_token()
    response = request('post', api_url, endpoint, api_token=api_token, data=data)
    display_api_response(response)


@api.command('put', help='HTTP PUT request to Rekono API')
@click.argument('endpoint', type=str, nargs=1)
@click.option('-d', '--data', 'data', type=str, required=False, help='HTTP body data. JSON format')
def put(endpoint: str, data: str):
    api_url, api_token = get_url_and_token()
    response = request('put', api_url, endpoint, api_token=api_token, data=data)
    display_api_response(response)


@api.command('delete', help='HTTP DELETE request to Rekono API')
@click.argument('endpoint', type=str, nargs=1)
def delete(endpoint: str):
    api_url, api_token = get_url_and_token()
    response = request('delete', api_url, endpoint, api_token=api_token)
    display_api_response(response)
