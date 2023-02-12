'''Rekono API client mock.'''

import json
from typing import Any, Dict, List, Optional, Union

from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict


class RekonoMock:
    '''Rekono API client mock.'''

    data = {                                                                    # Default body data
        'id': 1,
        'name': 'rekono',
        'description': 'test'
    }
    url = 'https://rekono.test'                                                 # Rekono base URL for testing
    headers = {                                                                 # HTTP headers for testing
        'Header': 'Value'
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''Mock constructor for Rekono API client.'''

    def _response_factory(
        self,
        method: str,
        status_code: int,
        content: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None
    ) -> Response:
        '''Create moked responses for Rekono API.

        Args:
            method (str): HTTP method used in the HTTP request.
            status_code (int): Response status code.
            content (Optional[Union[Dict[str, Any], List[Dict[str, Any]]]], optional): Response content. Defaults to None.  # noqa: E501

        Returns:
            Response: HTTP response.
        '''
        response = Response()
        response.request = Request(method=method, url=self.url + '/api/entities/').prepare()    # Set related request
        response.status_code = status_code
        response.headers = CaseInsensitiveDict(self.headers)
        response._content = json.dumps(content, ensure_ascii=True, indent=4).encode() if content else None  # Set body
        return response

    def get(self, *args: Any, **kwargs: Any) -> Response:
        '''Mock GET request to Rekono API.

        Returns:
            Response: HTTP response.
        '''
        return self._response_factory('GET', 200, self.data)

    def get_multiple_entities(self, *args: Any, **kwargs: Any) -> Response:
        '''Mock GET request to Rekono API with multiple items.

        Returns:
            Response: HTTP response.
        '''
        return self._response_factory('GET', 200, [self.data, self.data, self.data])

    def get_paginated_entities(self, *args: Any, **kwargs: Any) -> List[Response]:
        '''Mock GET request to Rekono API with pagination.

        Returns:
            List[Response]: List of HTTP responses.
        '''
        return [
            self._response_factory('GET', 200, self.data),
            self._response_factory('GET', 200, self.data),
            self._response_factory('GET', 200, self.data)
        ]

    def post(self, *args: Any, **kwargs: Any) -> Response:
        '''Mock POST request to Rekono API.

        Returns:
            Response: HTTP response.
        '''
        return self._response_factory('POST', 201, self.data)

    def put(self, *args: Any, **kwargs: Any) -> Response:
        '''Mock PUT request to Rekono API.

        Returns:
            Response: HTTP response.
        '''
        return self._response_factory('PUT', 200, self.data)

    def delete(self, *args: Any, **kwargs: Any) -> Response:
        '''Mock DELETE request to Rekono API.

        Returns:
            Response: HTTP response.
        '''
        return self._response_factory('DELETE', 204)
