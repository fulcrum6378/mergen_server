import simple_http_server.server as server
import socket

print("EXPECT THE FUTURE...")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server.scan("", "server.py")
    server.start(host=s.getsockname()[0], port=3772)
except Exception as e:
    print("COULD NOT START THE SERVER:", e)
