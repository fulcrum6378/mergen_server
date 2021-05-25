import os
import signal
from socketserver import BaseRequestHandler
from typing import Optional

import moviepy.editor as mpy
import soundfile as sf

from com.receiver import AudioHandler, ImageHandler, aTemp, dTemp, audio, sample_rate
from com.server import Server


class Control(BaseRequestHandler):
    def handle(self):  # self.client_address[0]
        print(str(self.request.recv(1024))[2:-1])


class Controller(Server):
    def __init__(self):
        Server.__init__(self, 3772, Control)
        self.vision: Optional[Server] = None
        self.hearing: Optional[Server] = None

    def run(self) -> None:
        Server.run(self)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()

    def see(self, b=True) -> None:
        if b:
            self.vision = Server(3773, ImageHandler)
            self.vision.start()
        elif self.vision is not None:
            self.vision.server.shutdown()
            self.vision.kill()
            self.vision = None
            if self.hearing is None:
                self.exit()

    def hear(self, b=True) -> None:
        if b:
            self.hearing = Server(3774, AudioHandler)
            self.hearing.start()
        elif self.hearing is not None:
            self.hearing.server.shutdown()
            self.hearing.kill()
            self.hearing = None
            if self.vision is None:
                self.exit()

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
