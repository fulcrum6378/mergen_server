from socket import AF_INET, SOCK_DGRAM, socket
from socketserver import BaseRequestHandler, TCPServer
from multiprocessing import Process
from typing import Optional, Type


class Server(Process):
    def __init__(self, port: int, handler: Type[BaseRequestHandler]):
        Process.__init__(self)
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            self.host: str = s.getsockname()[0]
            s.close()
        self.port: int = port
        self.server: Optional[TCPServer] = None
        self.handler: Type[BaseRequestHandler] = handler

    def run(self) -> None:
        print("RUNNING SOCKET SERVER AT", self.host + ":" + str(self.port))
        self.server = TCPServer((self.host, self.port), self.handler)
