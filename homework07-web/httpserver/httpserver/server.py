import socket
import threading
import typing as tp

from .handlers import BaseRequestHandler


class TCPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = None,
        request_handler_cls: tp.Type[BaseRequestHandler] = BaseRequestHandler,
    ) -> None:
        self.host = host
        self.port = port
        self.server_address = (host, port)
        self.backlog_size = backlog_size
        self.request_handler_cls = request_handler_cls
        self.max_workers = max_workers
        self.timeout = timeout
        self._threads: tp.List[threading.Thread] = []

    def serve_forever(self) -> None:
        server_socket = TCPServer.server_socket_initiate(self.server_address, self.backlog_size)

        for i in range(self.max_workers):
            self._threads.append(self.handle_accept_thread_initiate((server_socket,)))

        while True:
            try:
                input()
            except KeyboardInterrupt:
                print("Stopping server...")
                break

    def handle_accept(self, server_socket: socket.socket) -> None:
        while True:
            client_socket = TCPServer.server_socket_accept(server_socket, self.timeout)
            handler = self.request_handler_cls(client_socket, self.server_address, self)
            handler.handle()

    def handle_accept_thread_initiate(self, args: tp.Tuple[tp.Any]) -> threading.Thread:
        t = threading.Thread(target=self.handle_accept, args=args)
        t.daemon = True
        t.start()
        return t

    @staticmethod
    def server_socket_accept(server_socket: socket.socket, timeout: tp.Optional[float]) -> socket.socket:
        client_socket, _ = server_socket.accept()
        client_socket.settimeout(timeout)
        return client_socket

    @staticmethod
    def server_socket_initiate(server_address: tp.Tuple[str, int], backlog: int) -> socket.socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        server_socket.bind(server_address)
        server_socket.listen(backlog)
        return server_socket


class HTTPServer(TCPServer):
    pass
