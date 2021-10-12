import typing as tp

from httpserver import BaseHTTPRequestHandler, HTTPServer

from .request import WSGIRequest
from .response import WSGIResponse

ApplicationType = tp.Any


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[ApplicationType] = None

    def set_app(self, app: ApplicationType) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[ApplicationType]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_class = WSGIRequest
    response_class = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        environ = {
            **request.to_environ(),
            "SERVER_NAME": self.address[0],
            "SERVER_PORT": str(self.address[1]),
            "SERVER_PROTOCOL": "HTTP/1.1",
        }

        r = self.response_class()
        data_response = self.server.app(environ, r.start_response)
        r.body = b"".join(data_response)

        return r
