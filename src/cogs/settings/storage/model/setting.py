from typing import Optional

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, BigInteger

from src.kiyomi.database.database import Base
from .enums.setting_type import SettingType


class Setting(Base):
    """Settings"""
    __tablename__ = "setting"

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey("guild.id", ondelete="CASCADE"))

    setting_type = Column(Enum(SettingType))
    name = Column(String(128))
    value = Column(String(1024))

    def __init__(self, guild_id: Optional[int], setting_type: SettingType, name: str, value: Optional[str]):
        self.guild_id = guild_id
        self.setting_type = setting_type
        self.name = name
        self.value = value

    def __str__(self):
        return f"Setting {self.name} [{self.setting_type}]"
