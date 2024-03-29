import json
import os
import subprocess as sp
from signal import SIGTERM
from socketserver import BaseRequestHandler
from time import sleep
from typing import Dict

from PIL import ImageFile

from man.receiver import AudHandler, ManException, HptHandler, VisHandler, dTemp, vExt, root
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
    def killAll(yourself: bool = False):
        if os.name == 'posix':
            os.system("killall python")
        elif os.name == 'nt':
            killer = sp.Popen(os.path.join(root(), "man", "kill.bat"), shell=True)
            if yourself:
                killer.wait()
                os.kill(os.getpid(), SIGTERM)
        else:
            print("Could not kill all the processes. Unsupported operating system!")

    @staticmethod
    def updateDev():
        with open(devPath, "w") as f:
            f.write(json.dumps(dev))


class ControlHandler(BaseRequestHandler):
    def handle(self):  # self.client_address[0]
        note = str(self.request.recv(102400))[2:-1]  # 100KB
        if note.startswith("ackn"):
            if len(dev.keys()) > 0:
                maxKey = 0
                for k in dev.keys():
                    if int(k) > maxKey:
                        maxKey = int(k)
                newId = str(maxKey + 1)
            else:
                newId = "1"
            dev[newId] = json.loads(note[4:])
            Controller.updateDev()
            self.request.sendall(newId.encode())
        elif note.startswith("init"):
            global nextServer
            deviceId = note[4:]
            if deviceId in dev:
                respond = "true"
                deviceReceivers = list()
                for sense in dev[deviceId]["sensors"]:
                    st = sense["type"]
                    if st == "aud":
                        h = AudHandler
                    elif st == "hpt":
                        h = HptHandler
                    elif st == "vis":
                        h = VisHandler
                    else:
                        raise ManException("Unsupported sense: " + str(sense))
                    rec = Server(nextServer, h, sense["type"])
                    nextServer += 1
                    rec.start()
                    rec.check()
                    respond += str(rec.port) + ","
                    deviceReceivers.append(rec)
                receivers[deviceId] = deviceReceivers
                respond = respond[:-1].encode()
            else:
                respond = b"false"
            sleep(1)
            self.request.sendall(respond)
        elif note.startswith("halt"):
            deviceId = note[4:]
            if deviceId in dev.keys():
                for rec in receivers[deviceId]:
                    rec.kill()
                receivers.pop(deviceId)
            if len(receivers.keys()) == 0:
                extract()
        elif note == "kill":
            Controller.killAll(True)


def extract():
    vis = list()
    for i in os.listdir(dTemp):
        if i.endswith(vExt):
            vis.append(os.path.join(dTemp, i))
    vis.sort()


mem = os.path.join(root(), "mem")
dev, devPath = {}, os.path.join(root(), "man", "dev.json")
receivers: Dict = dict()
nextServer = 3773
