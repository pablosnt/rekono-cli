"""Rekono API client mock."""

import json
from typing import Any, Dict, List, Optional, Union

from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict


class RekonoMock:
    """Rekono API client mock."""

    data = {"id": 1, "name": "rekono", "description": "test"}  # Default body data
    url = "https://rekono.test"  # Rekono base URL for testing
    headers = {"Header": "Value"}  # HTTP headers for testing

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Mock constructor for Rekono API client."""

    def _response_factory(
        self,
        method: str,
        status_code: int,
        content: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    ) -> Response:
        """Create moked responses for Rekono API.

        Args:
            method (str): HTTP method used in the HTTP request.
            status_code (int): Response status code.
            content (Optional[Union[Dict[str, Any], List[Dict[str, Any]]]], optional): Response content. Defaults to None.  # noqa: E501

        Returns:
            Response: HTTP response.
        """
        response = Response()  # Build HTTP response
        # Set related request
        response.request = Request(
            method=method, url=self.url + "/api/entities/"
        ).prepare()
        response.status_code = status_code  # Set response status code
        response.headers = CaseInsensitiveDict(self.headers)  # Set response headers
        # Set body
        response._content = (
            json.dumps(content, ensure_ascii=True, indent=4).encode()
            if content
            else None
        )
        return response

    def get(self, *args: Any, **kwargs: Any) -> Union[Response, List[Response]]:
        """Mock GET request to Rekono API.

        Returns:
            Response: HTTP response.
        """
        if kwargs.get("pagination", False):
            # Return paginated mock value
            return self.get_paginated_entities(*args, **kwargs)
        return self._response_factory("GET", 200, self.data)  # Return standard response

    def get_multiple_entities(self, *args: Any, **kwargs: Any) -> Response:
        """Mock GET request to Rekono API with multiple items.

        Returns:
            Response: HTTP response.
        """
        return self._response_factory("GET", 200, [self.data, self.data, self.data])

    def get_paginated_entities(self, *args: Any, **kwargs: Any) -> List[Response]:
        """Mock GET request to Rekono API with pagination.

        Returns:
            List[Response]: List of HTTP responses.
        """
        return [
            self._response_factory("GET", 200, self.data),
            self._response_factory("GET", 200, self.data),
            self._response_factory("GET", 200, self.data),
        ]

    def post(self, *args: Any, **kwargs: Any) -> Response:
        """Mock POST request to Rekono API.

        Returns:
            Response: HTTP response.
        """
        return self._response_factory("POST", 201, self.data)

    def post_empty_response(self, *args: Any, **kwargs: Any) -> Response:
        """Mock POST request to Rekono API with empty response body.

        Returns:
            Response: HTTP response.
        """
        return self._response_factory("POST", 201)

    def put(self, *args: Any, **kwargs: Any) -> Response:
        """Mock PUT request to Rekono API.

        Returns:
            Response: HTTP response.
        """
        return self._response_factory("PUT", 200, self.data)

    def delete(self, *args: Any, **kwargs: Any) -> Response:
        """Mock DELETE request to Rekono API.

        Returns:
            Response: HTTP response.
        """
        return self._response_factory("DELETE", 204)
