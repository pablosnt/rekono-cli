'''Rekono API.'''

import json
import os
from typing import Any, Callable, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RetryError, Timeout
from requests.models import Response

from rekono.client.exceptions import AuthenticationError, AuthorizationError


class Rekono:
    '''Rekono API.'''

    def __init__(
        self,
        url: str,
        token: str,
        headers: Optional[Dict[str, str]] = None,
        verify: bool = True
    ) -> None:
        '''Rekono API client constructor.

        Args:
            url (str): Base Rekono URL.
            token (str): API token for Rekono authentication. Defaults to None.
            headers (Optional[Dict[str, str]], optional): Extra HTTP request headers. Defaults to None.
            verify (bool, optional): Indicates if TLS verification should be performed or not. Defaults to True.

        Raises:
            AuthenticationError: Authentication error during basic authentication attempt.
        '''
        self.url = url
        self.token = token
        self.headers = headers or {}
        self.headers.update({'Authorization': f'Token {self.token}'})           # Configure HTTP request headers
        self.verify = verify
        self.session = requests.Session()                                       # Configure retries of HTTP requests
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount(self.url, HTTPAdapter(max_retries=retries))

    def _get_endpoint(self, endpoint: str) -> str:
        '''Get valid Rekono endpoint from the provided value.

        Args:
            endpoint (str): Endpoint provided.

        Returns:
            str: Valid Rekono endpoint.
        '''
        if not endpoint.startswith('/api/'):                                    # If endpoint doesn't start by /api/
            if endpoint.startswith('/'):
                endpoint = endpoint[1:]
            endpoint = '/api/' + endpoint                                       # Add /api/ prefix to the endpoint
        if not endpoint.endswith('/'):                                          # If endpoint doesn't end by slash
            endpoint += '/'                                                     # Add slash suffix to the endpoint
        return endpoint

    def _request(
        self,
        method: Callable,
        endpoint: str,
        parameters: Optional[Dict[str, Any]] = None,
        body: Optional[str] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Response:
        '''Perform HTTP request to Rekono API.

        Args:
            method (Callable): HTTP method to use.
            endpoint (str): Endpoint to call.
            parameters (Optional[Dict[str, Any]], optional): Query parameters to send. Defaults to None.
            body (Optional[str], optional): Body to send. Defaults to None.
            files (Optional[Dict[str, Any]], optional): Files to send. Defaults to None.

        Raises:
            AuthenticationError: Unauthenticated, API token is invalid
            AuthorizationError: Unauthorized, user hasn't required permissions.

        Returns:
            Response: HTTP response.
        '''
        if files:
            self.headers.pop('Content-Type', None)                              # If files provided, remove Content-Type
        else:
            self.headers['Content-Type'] = 'application/json'                   # If not, set application/json
        url = self.url + self._get_endpoint(endpoint)                           # Prepare URL to call
        try:
            # First attempt
            response = method(url, params=parameters, data=body, files=files, headers=self.headers, verify=self.verify)
        except (ConnectionError, RetryError, Timeout):                          # Unexpected error during HTTP request
            # Second attempt
            response = method(url, params=parameters, data=body, files=files, headers=self.headers, verify=self.verify)
        if response.status_code == 401:                                         # Unauthenticated
            raise AuthenticationError(response)
        elif response.status_code == 403:                                       # Access Denied
            raise AuthorizationError(response)
        return response

    def get(
        self,
        endpoint: str,
        parameters: Optional[Dict[str, Any]] = None,
        pagination: bool = False
    ) -> Union[List[Response], Response]:
        '''GET request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            parameters (Optional[Dict[str, Any]], optional): Query parameters to send. Defaults to {}.
            pagination (bool, optional): Enables iteration over all API pages. Defaults to False.

        Raises:
            AuthenticationError: Unauthenticated, API token is invalid
            AuthorizationError: Unauthorizated, user doesn't have required permissions.

        Returns:
            Union[List[Response], Response]: HTTP responses if pagination is enabled or one HTTP response if not.
        '''
        parameters = parameters or {}
        if not pagination:                                                      # Pagination is disabled
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

    def post(self, endpoint: str, body: Optional[str] = None, filepath: Optional[str] = None) -> Response:
        '''POST request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            body (Optional[str], optional): Body to send. Defaults to None.
            filepath (Optional[str], optional): File to send. Defaults to None.

        Raises:
            AuthenticationError: Unauthenticated, API token is invalid
            AuthorizationError: Unauthorizated, user doesn't have required permissions.

        Returns:
            Response: HTTP response.
        '''
        if filepath and os.path.isfile(filepath):                               # If filepath is provided
            with open(filepath, 'rb') as file:                                  # Read file
                return self._request(                                           # Perform POST request
                    self.session.post, endpoint, body=json.loads(body) if body else None, files={'file': file}
                )
        return self._request(self.session.post, endpoint, body=body)            # Perform POST request without files

    def put(self, endpoint: str, body: Optional[str] = None) -> Response:
        '''PUT request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.
            body (Optional[str], optional): Body to send. Defaults to None.

        Raises:
            AuthenticationError: Unauthenticated, API token is invalid
            AuthorizationError: Unauthorizated, user doesn't have required permissions.

        Returns:
            Response: HTTP response.
        '''
        return self._request(self.session.put, endpoint, body=body)             # Perform PUT request

    def delete(self, endpoint: str) -> Response:
        '''DELETE request to Rekono API.

        Args:
            endpoint (str): Endpoint to call.

        Raises:
            AuthenticationError: Unauthenticated, API token is invalid
            AuthorizationError: Unauthorizated, user doesn't have required permissions.

        Returns:
            Response: HTTP response.
        '''
        return self._request(self.session.delete, endpoint)                     # Perform DELETE request
