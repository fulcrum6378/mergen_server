from socketserver import BaseRequestHandler, TCPServer
from threading import Thread
from traceback import format_tb


class Server(Thread):
    def __init__(self, host: str, port: int, handler):
        super().__init__()
        self.host = host
        self.port = port
        self.server = None
        self.handler = handler

    def run(self) -> None:
        self.notify("RUNNING SOCKET SERVER AT " + self.host + ":" + str(self.port))
        self.server = TCPServer((self.host, self.port), self.handler)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()

    @staticmethod
    def notify(msg):
        print(msg)  # "WATCHER: ",

    @staticmethod
    def handle(data, ext):
        try:
            with open("0." + ext, "wb") as f:
                f.write(data)
                f.close()
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))

    class ImageHandler(BaseRequestHandler):  # initiated in every request
        def handle(self):  # self.client_address[0]
            Server.handle(self.request.recv(1024), "jpg")

    class AudioHandler(BaseRequestHandler):  # initiated in every request
        def handle(self):  # self.client_address[0]
            Server.handle(self.request.recv(1024), "wav")
