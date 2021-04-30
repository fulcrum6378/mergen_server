import os.path
from socket import AF_INET, SOCK_DGRAM, socket
from socketserver import BaseRequestHandler, StreamRequestHandler, TCPServer
from threading import Thread
from traceback import format_tb
import wave

import numpy as np
import soundfile as sf


class Server(Thread):
    def __init__(self, port: int, handler):
        super().__init__()
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            self.host = s.getsockname()[0]
            s.close()
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

    class ImageHandler(StreamRequestHandler):
        def handle(self):
            try:
                package = self.request.recv(1073741824)  # 1GB (maximum bytes downloadable)
                if str(package) == "b''" or str(package) == "b'0000000000'": return
                data_size = int(package[:10].strip(b'0'))
                data = package[10:]
                while len(data) < data_size:
                    package = self.request.recv(1073741824)
                    if not package: break
                    data += package
                global dTemp, iTime
                with open(dTemp + str(iTime) + ".jpg", "wb") as f:
                    f.write(data)
                iTime += 1
            except Exception as e:
                print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))

    class AudioHandler(StreamRequestHandler):
        def handle(self):
            try:
                package = self.request.recv(1073741824)  # 1GB (maximum bytes downloadable)
                if str(package) == "b''" or str(package) == "b'0000000000'": return
                data_size = int(package[:10].strip(b'0'))
                data = package[10:]
                while len(data) < data_size:
                    package = self.request.recv(1073741824)
                    if not package: break
                    data += package
                global audio, sample_rate, aTime, dTemp
                last_time = str(aTime)
                wTemp = dTemp + "temp" + last_time + ".wav"
                with wave.open(wTemp, 'wb') as f:
                    f.setparams((1, 2, 44100, 0, 'NONE', 'NONE'))
                    f.writeframesraw(data)
                arr, sample_rate = sf.read(wTemp)
                audio = np.concatenate((audio, arr)) if audio is not None else arr
                del arr
                os.remove(wTemp)
            except Exception as e:
                print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))

    class DebugHandler(BaseRequestHandler):  # initiated in every request
        def handle(self):  # self.client_address[0]
            print(str(self.request.recv(1024))[2:-1])


iTime = aTime = 0
dTemp = "mem/tmp/"
audio = None
sample_rate = 0


def extractAudio():
    global dTemp, audio, sample_rate
    if audio is not None:
        sf.write(dTemp + "audio.wav", audio, sample_rate)
