from com.controller import Controller

if __name__ == "__main__":
    # First pause the anti-virus!
    killer = Controller.killAll()
    killer.wait()
    print("\n" * 2, "*" * 20, "\n" * 2)
    controller = Controller()
    controller.start()
    controller.check()
