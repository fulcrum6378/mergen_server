import os, os.path
from socketserver import StreamRequestHandler
from traceback import format_tb
import wave


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
            with open(os.path.join(dTemp, str(iTime) + pExt), "wb") as f:
                f.write(data)
            iTime += 1
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))


class AudioHandler(StreamRequestHandler):
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
            global sample_rate, aTime, dTemp
            last_time = str(aTime)
            fTemp = os.path.join(dTemp, last_time + aExt)
            with wave.open(fTemp, 'wb') as f:
                f.setparams((1, 2, sample_rate, 0, 'NONE', 'NONE'))
                f.writeframes(data)
            aTime += 1
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))


def root():
    r = os.path.dirname(__file__)
    for _ in range(5):
        if os.path.basename(r) != "mergen":
            r = os.path.dirname(r)
    if os.path.basename(r) != "mergen":
        raise Exception("Can't find the root folder!")
    return r


iTime = aTime = 0
dTemp = os.path.join(root(), "mem", "tmp")
sample_rate, aExt, pExt = 44100, ".wav", ".jpg"
