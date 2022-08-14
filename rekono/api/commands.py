from getpass import getpass
from typing import List

import click
import requests
from rekono.api.parser import (parse_body_data, parse_http_response,
                               parse_query_parameters)
from rekono.config import API_TOKEN, API_URL


@click.group('api', help='Make requests to Rekono API REST')
@click.pass_context
def api(ctx: click.Context):
    ctx.ensure_object(dict)
    ctx.obj['API_URL'] = API_URL if API_URL else input('API URL: ')
    ctx.obj['API_TOKEN'] = API_TOKEN
    if not ctx.obj['API_TOKEN']:
        username = input('Username: ')
        password = getpass('Password: ')
        response = requests.post(ctx.obj['API_URL'] + '/api/api-token/', data={'username': username, 'password': password})
        if response.status_code == 200:
            ctx.obj['API_TOKEN'] = response.json().get('token')
    click.echo()
    ctx.obj['API_HEADERS'] = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Token {ctx.obj["API_TOKEN"]}'
    }


@api.command('get', help='Rekono API GET')
@click.argument('endpoint', type=str, nargs=1)
@click.option(
    '-p', '--parameter', 'query_parameters', type=str, multiple=True,
    required=False, help='HTTP query parameter. Format <parameter>=<value>'
)
@click.pass_context
def get(ctx: click.Context, endpoint: str, query_parameters: List[str]):
    response = requests.get(
        ctx.obj['API_URL'] + endpoint,
        params=parse_query_parameters(query_parameters),
        headers=ctx.obj['API_HEADERS']
    )
    click.echo(parse_http_response(response))


@api.command('post', help='Rekono API POST')
@click.argument('endpoint', type=str, nargs=1)
@click.option('-d', '--data', 'data', type=str, required=False, help='HTTP body data. JSON format')
@click.pass_context
def post(ctx: click.Context, endpoint: str, data: str):
    response = requests.post(ctx.obj['API_URL'] + endpoint, data=parse_body_data(data), headers=ctx.obj['API_HEADERS'])
    click.echo(parse_http_response(response))


@api.command('put', help='Rekono API PUT')
@click.argument('endpoint', type=str, nargs=1)
@click.option('-d', '--data', 'data', type=str, required=False, help='HTTP body data. JSON format')
@click.pass_context
def put(ctx: click.Context, endpoint: str, data: str):
    response = requests.put(ctx.obj['API_URL'] + endpoint, data=parse_body_data(data), headers=ctx.obj['API_HEADERS'])
    click.echo(parse_http_response(response))


@api.command('delete', help='Rekono API DELETE')
@click.argument('endpoint', type=str, nargs=1)
@click.pass_context
def delete(ctx: click.Context, endpoint: str):
    response = requests.delete(ctx.obj['API_URL'] + endpoint, headers=ctx.obj['API_HEADERS'])
    click.echo(parse_http_response(response))
