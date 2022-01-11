from sqlalchemy import Column, String
from uuid import uuid4
from ..services.base import Base


class IconsSqlModel(Base):
    __tablename__ = "icons"
    id = Column(String, primary_key=True)
    filename = Column(String)
    site = Column(String)

    def __init__(self, fileName: str = "", site: str = "") -> None:
        self.id = str(uuid4())
        self.filename = fileName
        self.site = site

    def convertFromData(self, data: object) -> object:
        res = Icons(
            fileName=data.filename,
            site=data.site
        )
        return res
