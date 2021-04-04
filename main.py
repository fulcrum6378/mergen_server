import asyncio
import json
import socket
import traceback
import websockets


async def connect(websocket, path):
    data = await websocket.recv()
    params = json.loads(data)
    print(params)
    try:
        ret = "Hiyo Mahdi!"
    except Exception as e:
        ret = str(e.__class__)[8:-2] + ": " + str(e) + "\n" + ''.join(traceback.format_tb(e.__traceback__))
    print("RESPONSE:", ret)
    await websocket.send(ret)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host, port = s.getsockname()[0], 3772
print("RUNNING WEB-SOCKET SERVER AT " + host + ":" + str(port))
start_server = websockets.serve(connect, host, port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
