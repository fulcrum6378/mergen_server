import os
import signal
from socketserver import BaseRequestHandler
from time import sleep
from typing import Optional

import moviepy.editor as mpy
import soundfile as sf

from com.receiver import AudioHandler, ImageHandler, aTemp, dTemp, audio, sample_rate
from com.server import Server


class Control(BaseRequestHandler):
    def handle(self):  # self.client_address[0]
        note = str(self.request.recv(1024))[2:-1]
        if note == "start":
            Controller.see()
            Controller.hear()
            sleep(1)
            self.request.sendall(b"true")
        elif note == "stop":
            Controller.see(False)
            Controller.hear(False)


class Controller(Server):
    vision: Optional[Server] = None
    hearing: Optional[Server] = None

    def __init__(self):
        Server.__init__(self, 3772, Control)

    def run(self) -> None:
        Server.run(self)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()

    @staticmethod
    def see(b=True) -> None:
        if b:
            if Controller.vision is not None: return
            Controller.vision = Server(3773, ImageHandler)
            Controller.vision.start()
        elif Controller.vision is not None:
            Controller.vision.server.shutdown()
            Controller.vision.kill()
            Controller.vision = None
            if Controller.hearing is None:
                Controller.exit()

    @staticmethod
    def hear(b=True) -> None:
        if b:
            if Controller.hearing is not None: return
            Controller.hearing = Server(3774, AudioHandler)
            Controller.hearing.start()
        elif Controller.hearing is not None:
            Controller.hearing.server.shutdown()
            Controller.hearing.kill()
            Controller.hearing = None
            if Controller.vision is None:
                Controller.exit()

    @staticmethod
    def exit():
        if audio is not None:
            sf.write(dTemp + aTemp, audio, sample_rate)

        seq = list()
        for i in os.listdir(dTemp):
            if i.endswith(".wav"): continue
            seq.append(dTemp + i)
        seq.sort()
        clip = mpy.ImageSequenceClip(seq, fps=5)  # 20
        clip.audio = (mpy.AudioFileClip(dTemp + aTemp).set_duration(clip.duration))
        clip.write_videofile("mem/0.mp4")

        os.kill(os.getpid(), signal.SIGTERM)
