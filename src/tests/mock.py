import json
from typing import Any, Dict, List, Union

from requests.models import Request, Response


class RekonoMock:

    data = {
        'id': 1,
        'name': 'rekono',
        'description': 'test'
    }
    url = 'https://rekono.test'
    response_headers = {
        'Header': 'Value'
    }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def _response_factory(
        self,
        method: str,
        status_code: int,
        content: Union[Dict[str, Any], List[Dict[str, Any]]] = None
    ) -> Response:
        response = Response()
        response.request = Request(method=method, url=self.url + '/api/entities/').prepare()
        response.status_code = status_code
        response.headers = self.response_headers
        response._content = json.dumps(content, ensure_ascii=True, indent=4).encode() if content else None
        return response

    def get(self, *args: Any, **kwargs: Any) -> List[Response]:
        return [self._response_factory('GET', 200, self.data)]

    def get_multiple_entities(self, *args: Any, **kwargs: Any) -> List[Response]:
        return [self._response_factory('GET', 200, [self.data, self.data, self.data])]

    def get_paginated_entities(self, *args: Any, **kwargs: Any) -> List[Response]:
        return [
            self._response_factory('GET', 200, self.data),
            self._response_factory('GET', 200, self.data),
            self._response_factory('GET', 200, self.data)
        ]

    def post(self, *args: Any, **kwargs: Any) -> Response:
        return self._response_factory('POST', 201, self.data)

    def put(self, *args: Any, **kwargs: Any) -> Response:
        return self._response_factory('PUT', 200, self.data)

    def delete(self, *args: Any, **kwargs: Any) -> Response:
        return self._response_factory('DELETE', 204)
