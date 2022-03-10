from abc import ABC

from webob import Response, Request


class BaseView(ABC):
    def get(self, request: Request, response: Response, **kwargs):
        pass

    def post(self, request: Request, response: Response, **kwargs):
        pass

    def put(self, request: Request, response: Response, **kwargs):
        pass

    def patch(self, request: Request, response: Response, **kwargs):
        pass

    def delete(self, request: Request, response: Response, **kwargs):
        pass
