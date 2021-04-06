import socket
import socketserver
import traceback

last_client = None


class MyTCPHandler(socketserver.BaseRequestHandler):  # initiated in every request
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        global last_client
        try:
            if self.client_address[0] != last_client:
                if last_client is not None: print("")
                print(str(self.client_address[0]) + ":")
            last_client = self.client_address[0]
            print(str(self.request.recv(1024))[2:-1])
            # self.request.sendall(b"OK")
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(traceback.format_tb(e.__traceback__)))


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    HOST, PORT = s.getsockname()[0], 3772
    s.close()
print("RUNNING SOCKET SERVER AT " + HOST + ":" + str(PORT))
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass  # THE END
# FORCE KILL SERVER: kill $(sudo lsof -t -i:3772)
