from __future__ import annotations

import http
import socket
import typing as tp
from datetime import datetime

from httptools import HttpRequestParser
from httptools.parser.errors import HttpParserError, HttpParserInvalidMethodError

from .request import HTTPRequest
from .response import HTTPResponse

if tp.TYPE_CHECKING:
    from .server import TCPServer

Address = tp.Tuple[str, int]


class BaseRequestHandler:
    def __init__(self, socket: socket.socket, address: Address, server: TCPServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

    def handle(self) -> None:
        self.close()

    def close(self) -> None:
        self.socket.close()


class EchoRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        try:
            data = self.socket.recv(1024)
        except (socket.timeout, BlockingIOError) as e:
            print(e)
        else:
            self.socket.sendall(data)
        finally:
            self.close()


class BaseHTTPRequestHandler(BaseRequestHandler):
    request_class = HTTPRequest
    response_class = HTTPResponse

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body: bytes = b""
        self._parsed = False

    def handle(self) -> None:
        request = self.parse_request()
        if request:
            try:
                response = self.handle_request(request)
            except Exception as e:
                print("Exception:", e)
                response = self.response_class(status=500, headers={}, body=b"")
        else:
            response = self.response_class(status=400, headers={}, body=b"")
        self.handle_response(response)
        self.close()

    def parse_request(self) -> tp.Optional[HTTPRequest]:
        print("---")
        while not self._parsed:
            try:
                print("Getting")
                data = self.socket.recv(1024)
                if not data:
                    print("Break")
                    break
                print("Got")
                self.parser.feed_data(data)

            except (socket.timeout, BlockingIOError) as e:
                print("Socket error:", e)
                break
            except HttpParserInvalidMethodError as e:
                print("HTTPTools Invalid method detected:", e)
                break
            except HttpParserError as e:
                print("HTTPTools Invalid message (parsing error):", e)
                break
            except Exception as e:
                print("Unexpected error:", e)
                break

        response = None
        if self._parsed:
            response = self.request_class(
                method=self.parser.get_method(),
                url=self._url,
                headers=self._headers,
                body=self._body,
            )
        return response

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        content = b"No methods available"
        headers = BaseHTTPRequestHandler.create_headers(content)
        response = self.response_class(
            status=http.HTTPStatus.METHOD_NOT_ALLOWED.value, headers=headers, body=content
        )
        return response

    def handle_response(self, response: HTTPResponse) -> None:
        self.socket.sendall(response.to_http1())

    @staticmethod
    def create_headers(content: bytes) -> tp.Dict[str, str]:
        headers = {
            "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "Server": "Custom HTTP Server",
            "Content-Length": str(len(content)),
            "Content-Type": "text/plain",
            "Allow": "",
        }
        return headers

    def on_url(self, url: bytes) -> None:
        self._url = url
        print("on_url complete", url)

    def on_header(self, name: bytes, value: bytes) -> None:
        self._headers[name] = value
        print("on_header complete", name, value)

    def on_body(self, body: bytes) -> None:
        self._body = body
        print("on_body complete", body)

    def on_message_complete(self) -> None:
        self._parsed = True
        print("on_message_complete complete")
