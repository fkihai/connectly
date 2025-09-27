import enum


class DeviceType(str, enum.Enum):
    mqtt = "mqtt"
    api = "api"


class DataType(str, enum.Enum):
    string = "string"
    number = "number"
    objecj = "object"
