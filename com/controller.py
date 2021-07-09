import os, os.path
from signal import SIGTERM
from socketserver import BaseRequestHandler
import subprocess as sp
from time import sleep
from typing import Optional

import moviepy.editor as mpy
from PIL import ImageFile
import numpy as np
import soundfile as sf

from com.receiver import AudioHandler, ImageHandler, aExt, dTemp, pExt, root, sample_rate
from com.server import Server


def see(b=True) -> None:
    global vision, hearing
    if b:
        if vision is not None: return
        vision = Server(defPort + visPort, ImageHandler)
        vision.start()
        vision.check()
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
        hearing.check()
    elif hearing is not None:
        if hearing.server is not None:
            hearing.server.shutdown()
        hearing.kill()
        hearing = None
        if vision is None: extract()


def extract():
    ear, vis = list(), list()
    for i in os.listdir(dTemp):
        if i.endswith(aExt):
            ear.append(os.path.join(dTemp, i))
        elif i.endswith(pExt):
            vis.append(os.path.join(dTemp, i))
    ear.sort()
    vis.sort()
    if len(ear) == 0 or len(vis) == 0: return
    data = np.array([])
    for w in ear:
        data = np.concatenate((data, sf.read(w)[0]))
        os.remove(w)
    sf.write(aTemp, data, sample_rate)

    # Store everything as a movie
    clip = mpy.ImageSequenceClip(vis, fps=20)
    clip.audio = (mpy.AudioFileClip(aTemp).set_duration(clip.duration))
    clip.write_videofile(os.path.join(mem, "0.mp4"))


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
            Controller.killAll(True)


class Controller(Server):
    def __init__(self):
        Server.__init__(self, defPort + conPort, Control)

    def run(self) -> None:
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        if not os.path.isdir(mem):
            os.mkdir(mem)
        if not os.path.isdir(dTemp):
            os.mkdir(dTemp)
        Server.run(self)

    @staticmethod
    def killAll(yourself: bool = False) -> sp.Popen:
        killer = sp.Popen(os.path.join(root(), "kill.bat"), shell=True)
        if yourself:
            killer.wait()
            os.kill(os.getpid(), SIGTERM)
        return killer


defPort, conPort, visPort, earPort = 3772, 0, 1, 2
mem = os.path.join(root(), "mem")
aTemp = os.path.join(dTemp, "audio" + aExt)
vision: Optional[Server] = None
hearing: Optional[Server] = None
