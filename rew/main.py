from multiprocessing import Process


class Stimulator(Process):
    # Duties: Emotions, Managing expressions (not creating them)

    def __init__(self):
        Process.__init__(self)

    def run(self) -> None:
        pass

    def kill(self) -> None:
        Process.kill(self)
