import os, os.path
from signal import SIGTERM
from socketserver import BaseRequestHandler
import subprocess as sp
from time import sleep
from typing import Optional

from PIL import ImageFile
import numpy as np
import soundfile as sf

from man.receiver import AudioHandler, ImageHandler, aExt, dTemp, pExt, root, sample_rate
from man.server import Server


class Controller(Server):
    def __init__(self):
        Server.__init__(self, defPort + conPort, ControlHandler)

    def run(self) -> None:
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        if not os.path.isdir(mem):
            os.mkdir(mem)
        if not os.path.isdir(dTemp):
            os.mkdir(dTemp)
        else:
            for d in os.listdir(dTemp):
                os.remove(os.path.join(dTemp, d))
        Server.run(self)

    @staticmethod
    def killAll(yourself: bool = False) -> sp.Popen:
        killer = sp.Popen(os.path.join(root(), "man", "kill.bat"), shell=True)
        if yourself:
            killer.wait()
            os.kill(os.getpid(), SIGTERM)
        return killer


class ControlHandler(BaseRequestHandler):
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
            Controller.killAll(True)


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
        hearing = Server(defPort + audPort, AudioHandler)
        hearing.start()
        hearing.check()
    elif hearing is not None:
        if hearing.server is not None:
            hearing.server.shutdown()
        hearing.kill()
        hearing = None
        if vision is None: extract()


def extract():
    aud, vis = list(), list()
    for i in os.listdir(dTemp):
        if i.endswith(aExt):
            aud.append(os.path.join(dTemp, i))
        elif i.endswith(pExt):
            vis.append(os.path.join(dTemp, i))
    aud.sort()
    vis.sort()
    if len(aud) == 0 or len(vis) == 0: return
    data = np.array([])
    for w in aud:
        data = np.concatenate((data, sf.read(w)[0]))
        # os.remove(w)
    sf.write(aTemp, data, sample_rate)


defPort, conPort, visPort, audPort = 3772, 0, 1, 2
mem = os.path.join(root(), "mem")
aTemp = os.path.join(dTemp, "audio" + aExt)
vision: Optional[Server] = None
hearing: Optional[Server] = None
