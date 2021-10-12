import dataclasses
import http
import http.client
import typing as tp


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        response = b""
        response += (
            b"HTTP/1.1 "
            + bytes(str(self.status), "utf-8")
            + b" "
            + bytes(http.client.responses[self.status], "utf-8")
            + b"\r\n"
        )
        for name, weight in self.headers.items():
            response += bytes(str(name), "utf-8") + b": " + bytes(str(weight), "utf-8") + b"\r\n"
        response += b"\r\n"
        response += self.body
        return response
