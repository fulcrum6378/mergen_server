import os
from signal import SIGTERM
from socketserver import BaseRequestHandler
from time import sleep
from typing import Optional

import moviepy.editor as mpy
import soundfile as sf

from com.receiver import AudioHandler, ImageHandler, aTemp, dTemp, audio, sample_rate
from com.server import Server

defPort, conPort, visPort, earPort = 3772, 0, 1, 2
vision: Optional[Server] = None
hearing: Optional[Server] = None


def see(b=True) -> None:
    global vision, hearing
    if b:
        if vision is not None: return
        vision = Server(defPort + visPort, ImageHandler)
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
        hearing = Server(defPort + earPort, AudioHandler)
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
        elif note == "kill":
            print("RECEIVED KILL COMMAND!!")
            os.kill(os.getpid(), SIGTERM)


class Controller(Server):
    def __init__(self):
        Server.__init__(self, defPort + conPort, Control)

    def run(self) -> None:
        Server.run(self)
        if not os.path.isdir("mem"):
            os.mkdir("mem")
        if not os.path.isdir("mem/tmp"):
            os.mkdir("mem/tmp")
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()
