from dat.server import Server

vision = Server(3772, Server.ImageHandler)  # kill $(sudo lsof -t -i:3772)
vision.start()
hearing = Server(3773, Server.AudioHandler)  # kill $(sudo lsof -t -i:3773)
hearing.start()
