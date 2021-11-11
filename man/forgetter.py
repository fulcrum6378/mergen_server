from multiprocessing import Process


class Forgetter(Process):
    def __init__(self):
        Process.__init__(self)

    def run(self) -> None:
        pass

    def kill(self) -> None:
        Process.kill(self)
