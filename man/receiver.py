import os
import os.path
from socketserver import StreamRequestHandler
from traceback import format_tb


class AudHandler(StreamRequestHandler):
    def handle(self):
        try:
            package = self.request.recv(1073741824)  # 1GB (maximum bytes downloadable)
            if package in [b'', b'0000000000']: return
            data_size = int(package[:10].strip(b'0'))
            data = package[10:]
            while len(data) < data_size:
                package = self.request.recv(1073741824)
                if not package: break
                data += package
            global aTemp
            with open(aTemp, "ab") as f:
                f.write(data)
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))


class HptHandler(StreamRequestHandler):
    def handle(self):
        try:
            package = self.request.recv(10485760)  # 10MB: maximum bytes downloadable
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))


class VisHandler(StreamRequestHandler):
    def handle(self):
        try:
            package = self.request.recv(10485760)  # 10MB: maximum bytes downloadable
            if str(package) == "b''" or str(package) == "b'0000000000'": return
            data_size = int(package[:10].strip(b'0'))
            data = package[10:]
            while len(data) < data_size:
                package = self.request.recv(10485760)
                if not package: break
                data += package
            global dTemp, vTime
            with open(os.path.join(dTemp, str(vTime) + vExt), "wb") as f:
                f.write(data)
            vTime += 1
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))


def root():
    r = os.path.dirname(__file__)
    for _ in range(5):
        if os.path.basename(r) != "MergenServer":
            r = os.path.dirname(r)
    if os.path.basename(r) != "MergenServer":
        raise ManException("Can't find the root folder!")
    return r


class ManException(Exception):
    pass


vTime = 0
dTemp = os.path.join(root(), "mem", "tmp")
aTemp = os.path.join(dTemp, "audio.pcm")
sample_rate, vExt = 44100, ".jpg"
