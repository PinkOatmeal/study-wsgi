import inspect
from typing import Callable, Any, Union

from parse import parse
from webob import Request, Response

from study_wsgi.exceptions.routing import DuplicateRouteFound, MethodIsNotAllowed


class API:
    def __init__(self) -> None:
        self.routes: dict[str, Callable[[Request, Response, ...], None]] = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        return self._handle_request(request)(environ, start_response)

    def _find_handler(self, request_path) \
            -> Union[tuple[Callable[[Request, Response, ...], None], dict[str, Any]], tuple[None, None]]:
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result:
                return handler, parse_result.named
        return None, None

    def _handle_request(self, request: Request) -> Response:
        response = Response()
        handler, kwargs = self._find_handler(request.path)
        if handler:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower())
                if not handler:
                    raise MethodIsNotAllowed(f"{request.method} is not allowed for this route")

            handler(request, response)
        else:
            response.status_code = 404
            response.text = "Not found"
        return response

    def route(self, path):
        def wrapper(handler):
            if _handler := self.routes.get(path):
                raise DuplicateRouteFound(f"Route {path} is already handled by {_handler.__name__}")
            self.routes[path] = handler
            return handler

        return wrapper
