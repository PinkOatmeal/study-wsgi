from parse import parse, Result, Match
from typing import Callable, Optional, Any, Union, Tuple

from webob import Request, Response


class API:
    def __init__(self) -> None:
        self.routes: dict[str, Callable] = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        return self._handle_request(request)(environ, start_response)

    def _find_handler(self, request_path) \
            -> Union[tuple[Callable[[Request, Response], None], dict[str, Any]], tuple[None, None]]:
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result:
                return handler, parse_result.named
        return None, None

    def _handle_request(self, request: Request) -> Response:
        response = Response()
        handler, kwargs = self._find_handler(request.path)
        if handler:
            handler(request, response, **kwargs)
        else:
            response.status_code = 404
            response.text = "Not found"
        return response

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper
