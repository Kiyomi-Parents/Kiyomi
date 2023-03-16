from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship

from kiyomi.database import Base
from kiyomi.database.types.string_list import StringList


class MessageView(Base):
    __tablename__ = "message_view"

    id = Column(Integer, primary_key=True)
    view_name = Column(String(128))
    view_parameters = Column(StringList)

    message_id = Column(BigInteger, ForeignKey("message.id"))
    message = relationship("Message", uselist=False, lazy="selectin")

    def __init__(self, message_id: int, view_name: str, view_parameters: List[str]):
        self.message_id = message_id
        self.view_name = view_name
        self.view_parameters = view_parameters

    def __str__(self):
        return f"Message View {self.view_name}({', '.join(self.view_parameters)}) ({self.id})"
