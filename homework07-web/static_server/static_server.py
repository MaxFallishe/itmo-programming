import mimetypes
import os
import pathlib
import time
import typing as tp
from datetime import datetime
from urllib.parse import quote, unquote, urlparse, urlunparse

from httpserver import (
    BaseHTTPRequestHandler,
    BaseRequestHandler,
    HTTPRequest,
    HTTPResponse,
    HTTPServer,
)


def url_normalize(path: str) -> str:
    pieces = urlparse(path)
    return urlunparse(pieces._replace(path=quote(pieces.path)))


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:

        content: bytes = b""
        status: int = 200
        headers: tp.Dict[str, str] = dict()
        content_type: tp.Optional[str] = "text/html"

        if request.method not in [b"GET", b"HEAD"]:
            content = b"No methods available"
            status = 405
            headers = {
                "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "Server": "Custom HTTP Server",
                "Content-Length": str(len(content)),
                "Content-Type": "text/plain",
                "Allow": "GET, HEAD",
            }

        else:
            url = request.url.decode(encoding="utf-8")
            parsed_url = urlparse(unquote(url))
            path = (
                parsed_url.path + "index.html" if parsed_url.path.endswith("/") else parsed_url.path
            )
            path = self.server.document_root + path  # type: ignore

            if os.path.isfile(path) and os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        content = f.read()
                    content_type = mimetypes.guess_type(url)[0]
                except OSError:
                    status = 404
                    print("Invalid file requested", parsed_url.path)
                except Exception as e:
                    status = 404
                    print("Unexpected error:", e)
            else:
                status = 404
                print("Invalid path requested", path)

            headers = {
                "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "Server": "Custom HTTP Server",
                "Content-Length": str(len(content)),
                "Content-Type": "text/html" if content_type is None else content_type,
            }

            if request.method == b"HEAD":
                content = b""

        response = self.response_class(status=status, headers=headers, body=content)

        return response


class StaticServer(HTTPServer):
    def __init__(self, document_root: str = "/", **kwargs):
        super(StaticServer, self).__init__(**kwargs)
        self.document_root = document_root


if __name__ == "__main__":
    server = StaticServer(
        timeout=60,
        document_root=str(pathlib.Path("static") / "root"),
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
