from simple_http_server import request_map, PathValue, Headers, StaticFile


@request_map("/", method="GET")
def index():  # return 200, Headers({"Content-Type": mime}), read
    return "Hi there"


@request_map("{path_val}.jpg")
def jpg(path_val=PathValue()):
    return StaticFile(path_val, "image/jpeg")


@request_map("{path_val}.wav")
def wav(path_val=PathValue()):
    return StaticFile(path_val, "audio/wav")
