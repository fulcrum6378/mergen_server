from rtcbot import RTCConnection, CVDisplay, Speaker
from typing import Dict

display = CVDisplay()
speaker = Speaker()

# For this example, we use just one global connection
conn = RTCConnection()
display.putSubscription(conn.video.subscribe())
speaker.putSubscription(conn.audio.subscribe())


async def main(params: Dict):
    return await conn.getLocalDescription(params)
