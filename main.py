from socket import AF_INET, SOCK_DGRAM, socket

from server import Server

with socket(AF_INET, SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    HOST = s.getsockname()[0]
    s.close()

watcher = Server(HOST, 3772, Server.ImageHandler)
watcher.start()
# hearer = Server(HOST, 3773, Server.AudioHandler)
# hearer.start()
