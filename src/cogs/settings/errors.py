from .storage.model.enums.setting_type import SettingType
from src.kiyomi.errors import CogException


class SettingsCogException(CogException):
    pass


class FailedToCreateSetting(SettingsCogException):
    def __init__(self, setting_name: str):
        self.setting_name = setting_name

    def __str__(self):
        return f"Failed to create setting with name {self.setting_name}"


class FailedToFindSetting(SettingsCogException):
    def __init__(self, setting_name: str):
        self.setting_name = setting_name

    def __str__(self):
        return f"Could not find setting with name {self.setting_name}"


class FailedToConvertSetting(SettingsCogException):
    def __init__(self, setting_type: SettingType):
        self.setting_type = setting_type

    def __str__(self):
        return f"Unable to convert setting of type {self.setting_type}"


class InvalidSettingType(SettingsCogException):
    def __init__(self, setting_type: SettingType, expected_setting_type: SettingType):
        self.setting_type = setting_type
        self.expected_setting_type = expected_setting_type

    def __str__(self):
        return f"Can't convert setting of type {self.setting_type} to {self.expected_setting_type}"


class PermissionDenied(SettingsCogException):
    def __init__(self, setting_name: str):
        self.setting_name = setting_name

    def __str__(self):
        return f"I can't let you edit that setting mister"


class InvalidSettingValue(SettingsCogException):
    def __init__(self, setting_name: str, setting_type: SettingType, setting_value: str):
        self.setting_name = setting_name
        self.setting_type = setting_type
        self.setting_value = setting_value

    def __str__(self):
        return f"{self.setting_value} is not a {self.setting_type.name}!"
