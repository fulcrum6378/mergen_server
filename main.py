import os
import signal
from threading import Thread
from time import sleep

from dat.server import extractAudio, Server


class Exit(Thread):
    def __init__(self, out: int = 10):
        super().__init__()
        self.out = out

    def run(self) -> None:
        sleep(self.out)
        extractAudio()
        os.kill(os.getpid(), signal.SIGTERM)


if __name__ == "__main__":
    Exit().start()
    vision = Server(3772, Server.ImageHandler)  # kill $(sudo lsof -t -i:3772)
    vision.start()
    hearing = Server(3773, Server.AudioHandler)  # kill $(sudo lsof -t -i:3773)
    hearing.start()
