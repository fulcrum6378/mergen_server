from man.controller import Controller
from man.forgetter import Forgetter
from rew.main import Stimulator
from tnk.main import Awareness

if __name__ == "__main__":
    controller = Controller()
    controller.start()
    controller.check()
    forgetter = Forgetter()
    forgetter.start()
    stimulator = Stimulator()
    stimulator.start()
    Awareness()
