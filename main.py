from dat.server import Server

if __name__ == "__main__":
    vision = Server(3772, Server.ImageHandler)  # kill $(sudo lsof -t -i:3772)
    vision.start()
    hearing = Server(3773, Server.AudioHandler)
    hearing.start()
