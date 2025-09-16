import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class DeviceType(str, enum.Enum):
    mqtt = "mqtt"
    api = "api"
