'''Rekono API.'''

from typing import Any, Callable, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ConnectionError, RetryError, Timeout
from requests.models import Response

from rekono.client.exceptions import AuthenticationError


class Rekono:
    '''Rekono API.'''

    def __init__(
        self,
        url: str,
        token: str = None,
        username: str = None,
        password: str = None,
        headers: Dict[str, str] = {},
        verify: bool = False
    ) -> None:
        self.url = url
        self.verify = verify
        self.headers = headers
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount(self.url, HTTPAdapter(max_retries=retries))
        if token:
            self.token = token
        elif username and password:
            response = self.post('/api/api-token/', {'username': username, 'password': password})
            if response.status_code == 200:
                self.token = response.json().get('token')
            else:
                raise AuthenticationError('Unauthorized: Invalid username or password', response)
        self.headers.update({
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        })

    def _get_endpoint(self, endpoint: str) -> str:
        if not endpoint.startswith('/api/'):
            if endpoint.startswith('/'):
                endpoint = endpoint[1:]
            endpoint = '/api/' + endpoint
        if not endpoint.endswith('/'):
            endpoint += '/'
        return endpoint

    def _request(
        self,
        method: Callable,
        endpoint: str,
        parameters: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> Response:
        try:
            return method(
                self.url + self._get_endpoint(endpoint),
                params=parameters,
                data=body,
                headers=self.headers,
                verify=self.verify
            )
        except (ConnectionError, RetryError, Timeout):
            return method(
                self.url + self._get_endpoint(endpoint),
                params=parameters,
                data=body,
                headers=self.headers,
                verify=self.verify
            )

    def get(self, endpoint: str, parameters: Optional[Dict[str, Any]] = {}, all_pages: bool = True) -> List[Response]:
        page = 1
        size = 100
        count = 101
        responses = []
        while page * size < count:
            if all_pages:
                parameters.update({'page': page, 'size': size})
            response = self._request(self.session.get, endpoint, parameters=parameters)
            responses.append(response)
            body = response.json()
            if body and 'count' in body:
                count = body.get('count', 0)
                page += 1
            else:
                break
        return responses

    def post(self, endpoint: str, body: Optional[Dict[str, Any]] = None) -> Response:
        return self._request(self.session.post, endpoint, body=body)

    def put(self, endpoint: str, body: Optional[Dict[str, Any]] = None) -> Response:
        return self._request(self.session.put, endpoint, body=body)

    def delete(self, endpoint: str) -> Response:
        return self._request(self.session.delete, endpoint)
