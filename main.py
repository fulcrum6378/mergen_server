import socket
import socketserver
import traceback


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            print("{} wrote:".format(self.client_address[0]), self.request.recv(1024).strip())
            self.request.sendall(b"Fine")
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(traceback.format_tb(e.__traceback__)))


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    HOST, PORT = s.getsockname()[0], 3772
    s.close()
print("RUNNING SOCKET SERVER AT " + HOST + ":" + str(PORT))
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
server.serve_forever()
