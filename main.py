from socket import AF_INET, SOCK_DGRAM, socket

from server import Server

with socket(AF_INET, SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    HOST = s.getsockname()[0]
    s.close()

recorder = Server(HOST, 3772, Server.VideoHandler)
recorder.start()
