from com.controller import Controller

if __name__ == "__main__":
    Controller().start()  # kill $(sudo lsof -t -i:3772)
    # TO FINISH: os.kill(os.getpid(), signal.SIGTERM)
