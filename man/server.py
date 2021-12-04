import errno
from multiprocessing import Process
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, error, socket
from socketserver import BaseRequestHandler, TCPServer
from typing import Optional, Type


class Server(Process):
    def __init__(self, port: int, handler: Type[BaseRequestHandler], sense_type: str = None):
        Process.__init__(self)
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            self.host: str = s.getsockname()[0]
            s.close()
        self.port: int = port
        self.server: Optional[TCPServer] = None
        self.handler: Type[BaseRequestHandler] = handler
        self.sense_type = sense_type
        self.active = False

    def run(self) -> None:
        Process.run(self)
        self.server = TCPServer((self.host, self.port), self.handler)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()

    def kill(self) -> None:
        Process.kill(self)
        self.check()

    def check(self, echo: bool = True) -> None:
        senseIndicator = (" for " + self.sense_type).upper() if self.sense_type is not None else ""
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
            if echo:
                if not self.active:
                    print("BEGAN LISTENING AT", self.host + ":" + str(self.port) + senseIndicator)
                else:
                    print("PORT", self.port, "ALREADY IN USE! (ACTIVE)" + senseIndicator)
            self.active = True
        except error as e:
            if echo:
                if self.active:
                    print("ENDED LISTENING AT", self.host + ":" + str(self.port) + senseIndicator)
                else:
                    if e.errno == errno.EADDRINUSE:
                        print("PORT", self.port, "ALREADY IN USE! (INACTIVE)" + senseIndicator)
                    else:
                        print(e)
            self.active = False
        s.close()
