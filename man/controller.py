import json
import os
import os.path
import subprocess as sp
from signal import SIGTERM
from socketserver import BaseRequestHandler
from time import sleep
from typing import Dict

import numpy as np
import soundfile as sf
from PIL import ImageFile

from man.receiver import aExt, dTemp, handlers, pExt, root, sample_rate
from man.server import Server


class Controller(Server):
    def __init__(self):
        Server.__init__(self, 3772, ControlHandler)

    def run(self) -> None:
        # Truncate the TMP folder
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        if not os.path.isdir(mem):
            os.mkdir(mem)
        if not os.path.isdir(dTemp):
            os.mkdir(dTemp)
        else:
            for d in os.listdir(dTemp):
                os.remove(os.path.join(dTemp, d))

        # Create DEV file
        global dev, devPath
        if not os.path.isfile(devPath):
            with open(devPath, "w") as f:
                f.write(json.dumps(dev))
        else:
            with open(devPath, "r") as f:
                dev = json.loads(f.read())

        Server.run(self)

    @staticmethod
    def killAll(yourself: bool = False) -> sp.Popen:
        killer = sp.Popen(os.path.join(root(), "man", "kill.bat"), shell=True)
        if yourself:
            killer.wait()
            os.kill(os.getpid(), SIGTERM)
        return killer

    @staticmethod
    def updateDev():
        with open(devPath, "w") as f:
            f.write(json.dumps(dev))


class ControlHandler(BaseRequestHandler):
    def handle(self):  # self.client_address[0]
        note = str(self.request.recv(1024))[2:-1]
        if note.startswith("ackn"):
            if len(dev.keys()) > 0:
                maxKey = 0
                for k in dev.keys():
                    if int(k) > maxKey:
                        maxKey = k
                newId = str(maxKey + 1)
            else:
                newId = "1"
            dev[newId] = json.loads(note[4:])
            Controller.updateDev()
            self.request.sendall(newId.encode())
        elif note.startswith("init"):
            deviceId = note[4:]
            if deviceId in dev:
                respond = "true"
                deviceReceivers = list()
                for sense in dev[deviceId]["sensors"]:
                    rec = Server(0, handlers[sense])
                    rec.start()
                    rec.check(True)
                    respond += str(rec.port) + ","
                    deviceReceivers.append(rec)
                receivers[deviceId] = deviceReceivers
                respond = respond[:-1].encode()
            else:
                respond = b"false"
            sleep(1)
            self.request.sendall(respond)
        elif note == "halt":
            deviceId = note[4:]
            if deviceId in dev:
                for rec in receivers[deviceId]:
                    if rec.server is not None:
                        rec.server.shutdown()
                    rec.kill()
                receivers.pop(deviceId)
            if len(receivers.keys()) == 0:
                extract()
        elif note == "kill":
            Controller.killAll(True)


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


mem = os.path.join(root(), "mem")
aTemp = os.path.join(dTemp, "audio" + aExt)
dev, devPath = {}, os.path.join(root(), "man", "dev.json")
receivers: Dict = dict()
