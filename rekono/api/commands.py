import json
from getpass import getpass
from typing import List

import click
from rekono.api.requests import request
from rekono.config import API_TOKEN, API_URL

import requests


def display_api_response(response: requests.Response) -> str:
    try:
        text = json.dumps(response.json(), indent=4)
    except:
        text = response.text if response.text else 'No response content'
    click.echo(f'\n{text}\n')


@click.group('api', help='Make requests to Rekono API REST')
@click.pass_context
def api(ctx: click.Context):
    ctx.ensure_object(dict)
    ctx.obj['API_URL'] = API_URL if API_URL else input('API URL: ')
    ctx.obj['API_TOKEN'] = API_TOKEN
    if not ctx.obj['API_TOKEN']:
        username = input('Username: ')
        password = getpass('Password: ')
        response = request(
            'post', ctx.obj['API_URL'], '/api/api-token/',
            data='{' + f'"username": "{username}", "password": "{password}"' + '}'
        )
        if response.status_code == 200:
            ctx.obj['API_TOKEN'] = response.json().get('token')


@api.command('get', help='Rekono API GET')
@click.argument('endpoint', type=str, nargs=1)
@click.option(
    '-p', '--parameter', 'query_parameters', type=str, multiple=True,
    required=False, help='HTTP query parameter. Format <parameter>=<value>'
)
@click.pass_context
def get(ctx: click.Context, endpoint: str, query_parameters: List[str]):
    response = request('get', ctx.obj['API_URL'], endpoint, api_token=ctx.obj['API_TOKEN'], params=query_parameters)
    display_api_response(response)


@api.command('post', help='Rekono API POST')
@click.argument('endpoint', type=str, nargs=1)
@click.option('-d', '--data', 'data', type=str, required=False, help='HTTP body data. JSON format')
@click.pass_context
def post(ctx: click.Context, endpoint: str, data: str):
    response = request('post', ctx.obj['API_URL'], endpoint, api_token=ctx.obj['API_TOKEN'], data=data)
    display_api_response(response)


@api.command('put', help='Rekono API PUT')
@click.argument('endpoint', type=str, nargs=1)
@click.option('-d', '--data', 'data', type=str, required=False, help='HTTP body data. JSON format')
@click.pass_context
def put(ctx: click.Context, endpoint: str, data: str):
    response = request('put', ctx.obj['API_URL'], endpoint, api_token=ctx.obj['API_TOKEN'], data=data)
    display_api_response(response)


@api.command('delete', help='Rekono API DELETE')
@click.argument('endpoint', type=str, nargs=1)
@click.pass_context
def delete(ctx: click.Context, endpoint: str):
    response = request('delete', ctx.obj['API_URL'], endpoint, api_token=ctx.obj['API_TOKEN'])
    display_api_response(response)
