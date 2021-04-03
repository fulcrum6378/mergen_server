import asyncio
import json
import socket
import websockets

import connect_aio
import connect_bot

mode = "bot"


async def connect(websocket, path):
    data = await websocket.recv()
    params = json.loads(data)
    print(params)
    if mode == "aio":
        ret = connect_aio.main(params)
    elif mode == "bot":
        ret = connect_bot.main(params)
    else:
        ret = "Hiyo Mahdi!"
    await websocket.send(ret)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host, port = s.getsockname()[0], 3772
print("RUNNING SOCKET SERVER AT " + host + ":" + str(port))
start_server = websockets.serve(connect, host, port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
