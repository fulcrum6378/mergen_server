import asyncio
import websockets


async def hello(websocket, path):
    await websocket.send("Hiyo Mahdi!")


start_server = websockets.serve(hello, "192.168.1.9", 3772)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
