import socket

suck = socket.gethostname()
if suck == "fulcrum":
    root = "./"
elif suck == "WIN-KJ6QV3R1373":
    root = "/inetpub/wwwroot/"

default_folders = [
    '__pycache__'
]
