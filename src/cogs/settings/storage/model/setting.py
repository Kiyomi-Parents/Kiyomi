from sqlalchemy import Column, String, Integer, ForeignKey, Enum

from .enums.setting_type import SettingType
from src.database.database import Base


class Setting(Base):
    """Settings"""
    __tablename__ = "setting"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey("guild.id", ondelete="CASCADE"))

    setting_type = Column(Enum(SettingType))
    name = Column(String)
    value = Column(String)

    def __init__(self, guild_id: int, setting_type: SettingType, name: str, value: str):
        self.guild_id = guild_id
        self.setting_type = setting_type
        self.name = name
        self.value = value

    def __str__(self):
        return f"Setting {self.name} [{self.setting_type}]"
