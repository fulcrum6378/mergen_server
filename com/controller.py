import os
from socketserver import BaseRequestHandler
from time import sleep
from typing import Optional

import moviepy.editor as mpy
import soundfile as sf

from com.receiver import AudioHandler, ImageHandler, aTemp, dTemp, audio, sample_rate
from com.server import Server

vision: Optional[Server] = None
hearing: Optional[Server] = None


def see(b=True) -> None:
    global vision, hearing
    if b:
        if vision is not None: return
        vision = Server(3773, ImageHandler)
        vision.start()
    elif vision is not None:
        if vision.server is not None:
            vision.server.shutdown()
        vision.kill()
        vision = None
        if hearing is None: extract()


def hear(b=True) -> None:
    global vision, hearing
    if b:
        if hearing is not None: return
        hearing = Server(3774, AudioHandler)
        hearing.start()
    elif hearing is not None:
        if hearing.server is not None:
            hearing.server.shutdown()
        hearing.kill()
        hearing = None
        if vision is None: extract()


def extract():
    if audio is not None:
        sf.write(dTemp + aTemp, audio, sample_rate)

    seq = list()
    for i in os.listdir(dTemp):
        if i.endswith(".wav"): continue
        seq.append(dTemp + i)
    seq.sort()
    if len(seq) > 0:
        clip = mpy.ImageSequenceClip(seq, fps=5)  # 20
        clip.audio = (mpy.AudioFileClip(dTemp + aTemp).set_duration(clip.duration))
        clip.write_videofile("mem/0.mp4")


class Control(BaseRequestHandler):
    def handle(self):  # self.client_address[0]
        note = str(self.request.recv(1024))[2:-1]
        if note == "start":
            see()
            hear()
            sleep(1)
            self.request.sendall(b"true")
        elif note == "stop":
            see(False)
            hear(False)


class Controller(Server):
    def __init__(self):
        Server.__init__(self, 3772, Control)

    def run(self) -> None:
        Server.run(self)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()
