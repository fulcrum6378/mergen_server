from socketserver import BaseRequestHandler, StreamRequestHandler, TCPServer
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
        print("RUNNING SOCKET SERVER AT", self.host + ":" + str(self.port))
        self.server = TCPServer((self.host, self.port), self.handler)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()

    class VideoHandler(StreamRequestHandler):
        def handle(self):
            try:
                package = self.request.recv(1073741824)  # 1GB (maximum bytes downloadable)
                data_size = int(package[:10].strip(b'0'))
                data = package[10:]
                while len(data) < data_size:
                    package = self.request.recv(1073741824)
                    if not package: break
                    data += package
                global time
                with open("mem/" + str(time) + ".mp4", "wb") as f:
                    f.write(data)
                    f.close()
                time += 1
            except Exception as e:
                print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))

    class TextHandler(BaseRequestHandler):  # initiated in every request
        def handle(self):  # self.client_address[0]
            print(str(self.request.recv(1024))[2:-1])


time = 0
