from sqlalchemy import Column, String
from uuid import uuid4
from ..services.base import Base


class SettingsSqlModel(Base):
    __tablename__ = "settings"
    id = Column("id", String, primary_key=True)
    key = Column("key", String)
    value = Column("value", String)
    options = Column("options", String)
    notes = Column("notes", String)

    def __init__(
        self, key: str = "", value: str = "", options: str = "", notes: str = ""
    ):
        self.id = str(uuid4())
        self.key = key
        self.value = value
        self.options = options
        self.notes = notes

    def convertFromData(self, item: object) -> object:
        res = Settings()
        res.key = item.key
        res.notes = item.notes
        res.options = item.options
        res.value = item.value
        return res
