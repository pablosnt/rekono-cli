import json
import sys
from typing import Any, Dict, List

import click
import requests


def parse_body_data(data: str) -> Dict[str, Any]:
    try:
        return json.loads(data)
    except:
        click.echo(f'Invalid body data')
        sys.exit(1)


def parse_query_parameters(query_parameters: List[str]) -> Dict[str, Any]:
    parameters = {}
    for query_parameter in query_parameters:
        if '=' not in query_parameter:
            click.echo(f'Invalid query parameter: {query_parameter}')
            sys.exit(1)
        parsed = query_parameter.split('=')
        parameters[parsed[0]] = parsed[1]
    return parameters


def parse_http_response(response: requests.Response) -> str:
    try:
        text = json.dumps(response.json(), indent=4)
    except:
        text = response.text if response.text else 'No response content'
    return f'{text}\n'
