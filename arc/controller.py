import json
from rtcbot import RTCConnection, getRTCBotJS, CVDisplay, Speaker
from simple_http_server import request_map, PathValue, Headers, StaticFile

display = CVDisplay()
speaker = Speaker()
conn = RTCConnection()
display.putSubscription(conn.video.subscribe())
speaker.putSubscription(conn.audio.subscribe())


@request_map("/connect", method="POST")
def connect():
    # clientOffer = None # json.dumps({"request": request})
    # serverResponse = await conn.getLocalDescription(clientOffer)
    return 200  # , Headers({"Content-Type": "application/json"}), serverResponse


@request_map("{path_val}.jpg")
def jpg(path_val=PathValue()):
    return StaticFile(path_val, "image/jpeg")


@request_map("{path_val}.wav")
def wav(path_val=PathValue()):
    return StaticFile(path_val, "audio/wav")
