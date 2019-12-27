class EntityType:
    _IOT=0
    _CLIENT=1
    _GATEWAY=2
    _Server=3


class CameraOperation:
    _STREAM_DIRECT=0
    _STREAM_TO_SERVER=1


class CameraCommand:
    _START_RECORD=0
    _STOP_RECORD=1
    __START_SAVE=2
    _STOP_SAVE=3
