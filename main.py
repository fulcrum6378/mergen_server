import base64
import cgi
import socket
from soundfile import SoundFile

import dat.config as cfg
import pro.main as pro
import rew.main as rew

if rew.do_communicate():
    if socket.gethostname() == "WIN-KJ6QV3R1373":
        print("Content-Type: text/plain\n")
        got = {"t": ""}
        try:
            for g in cgi.FieldStorage().list: got[g.name] = g.value
        except:
            pass
        if got["t"] == "":
            print("hello there")
        else:
            fName = pro.main(got["t"])
            with open(cfg.root + 'pro/' + fName + '.wav', 'rb') as f:
                print(str(base64.b64encode(f.read()))[2:-1])
                f.close()
