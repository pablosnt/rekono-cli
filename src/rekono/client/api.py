'''Rekono API.'''

import json
from typing import Any, Callable, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RetryError, Timeout
from requests.models import Response

from rekono.client.exceptions import AuthenticationError


class Rekono:
    '''Rekono API.'''

    def __init__(
        self,
        url: str,
        token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        headers: Dict[str, str] = {},
        verify: bool = False
    ) -> None:
        '''Rekono API client constructor.

        Args:
            url (str): Base Rekono URL.
            token (Optional[str], optional): API token (required if no credentials provided). Defaults to None.
            username (Optional[str], optional): Username (required if no token provided). Defaults to None.
            password (Optional[str], optional): Password (required if no token provided). Defaults to None.
            headers (Dict[str, str], optional): Extra HTTP request headers. Defaults to {}.
            verify (bool, optional): Indicates if TLS verification should be performed or not. Defaults to False.

        Raises:
            AuthenticationError: Authentication error during basic authentication attempt.
        '''
        self.url = url
        self.verify = verify
        self.headers = headers
        self.session = requests.Session()
        # Configure retries of HTTP requests
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount(self.url, HTTPAdapter(max_retries=retries))
        if token:
            self.token = token
        elif username and password:
            # Make basic authentication to get the API token
            response = self.post('/api/api-token/', json.dumps({'username': username, 'password': password}))
            if response.status_code == 200:
                self.token = response.json().get('token')
            else:                                                               # Invalid credentials
                raise AuthenticationError('Unauthorized: Invalid username or password', response)
        self.headers.update({                                                   # Configure HTTP request headers
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        })

    def _get_endpoint(self, endpoint: str) -> str:
        '''Get valid Rekono endpoint from the provided value.

        Args:
            endpoint (str): Endpoint provided.

        Returns:
            str: Valid Rekono endpoint.
        '''
        if not endpoint.startswith('/api/'):                                    # Endpoint doesn't start by /api/
            if endpoint.startswith('/'):
                endpoint = endpoint[1:]
            endpoint = '/api/' + endpoint                                       # Add /api/ prefix to the endpoint
        if not endpoint.endswith('/'):                                          # Endpoint doesn't end by slash
            endpoint += '/'                                                     # Add slash suffix to the endpoint
        return endpoint

    def _request(
        self,
        method: Callable,
        endpoint: str,
        parameters: Optional[Dict[str, Any]] = None,
        body: Optional[str] = None
    ) -> Response:
        '''Perform HTTP request to Rekono API.

        Args:
            method (Callable): HTTP method to use.
            endpoint (str): Endpoint to call.
            parameters (Optional[Dict[str, Any]], optional): Query parameters to send. Defaults to None.
            body (Optional[str], optional): Body to send. Defaults to None.

        Returns:
            Response: HTTP response.
        '''
        url = self.url + self._get_endpoint(endpoint)                           # Prepare URL to call
        try:
            return method(url, params=parameters, data=body, headers=self.headers, verify=self.verify)  # Attempt one
        except (ConnectionError, RetryError, Timeout):                          # Unexpected error during HTTP request
            return method(url, params=parameters, data=body, headers=self.headers, verify=self.verify)  # Attempt two

    def get(
        self,
        endpoint: str,
        parameters: Dict[str, Any] = {},
        all_pages: bool = False
    ) -> Union[List[Response], Response]:
        '''GET request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            parameters (Optional[Dict[str, Any]], optional): Query parameters to send. Defaults to {}.
            all_pages (bool, optional): Iteration over all API pages is required. Defaults to False.

        Returns:
            Union[List[Response], Response]: HTTP responses if all pages is enabled or one HTTP response if not.
        '''
        if not all_pages:                                                       # All pages is disabled
            return self._request(self.session.get, endpoint, parameters=parameters)     # Perform only one GET request
        page = 1                                                                # Start page number
        size = 100                                                              # Default page size (max is 1000)
        count = 101                                                             # Initial fake count value
        responses = []
        while page * size < count:
            parameters.update({'page': page, 'size': size})                     # Set pagination parameters
            response = self._request(self.session.get, endpoint, parameters=parameters)     # Paginated GET request
            responses.append(response)                                          # Save HTTP response
            body = response.json()
            if body and 'count' in body:
                count = body.get('count', 0)                                    # Update count value
                page += 1                                                       # Increase page number
            else:
                break
        return responses

    def post(self, endpoint: str, body: Optional[str] = None) -> Response:
        '''POST request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            body (Optional[str], optional): Body to send. Defaults to None.

        Returns:
            Response: HTTP response.
        '''
        return self._request(self.session.post, endpoint, body=body)            # Perform POST request

    def put(self, endpoint: str, body: Optional[str] = None) -> Response:
        '''PUT request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            body (Optional[str], optional): Body to send. Defaults to None.

        Returns:
            Response: HTTP response.
        '''
        return self._request(self.session.put, endpoint, body=body)             # Perform PUT request

    def delete(self, endpoint: str) -> Response:
        '''DELETE request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.

        Returns:
            Response: HTTP response.
        '''
        return self._request(self.session.delete, endpoint)                     # Perform DELETE request