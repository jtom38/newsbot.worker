from sqlalchemy import Column, String, Boolean
from uuid import uuid4
from ..services.base import Base


class SourcesSqlModel(Base):
    __tablename__ = "sources"
    id: str = Column(String, primary_key=True)
    site: str = Column(String)
    name: str = Column(String)
    source: str = Column(String)
    type: str = Column(String)
    value: str = Column(String)
    enabled: bool = Column(Boolean)
    url: str = Column(String)
    tags: str = Column(String)
    fromEnv: bool = Column(Boolean)

    def __init__(
        self,
        id: str = "",
        site: str = "",
        name: str = "",
        source: str = "",
        type: str = "",
        value: str = "",
        enabled: bool = True,
        url: str = "",
        tags: str = "",
        fromEnv: bool = False
    ) -> None:
        self.id = str(uuid4())
        self.site: str = site
        self.name: str = name
        self.source: str = source
        self.type: str = type
        self.value: str = value
        self.enabled: bool = enabled
        self.url: str = url
        self.tags: str = tags
        self.fromEnv: bool = fromEnv

    def convertFromData(self, item: object) -> object:
        s = Sources()
        s.site = item.site
        s.name = item.name
        s.source = item.source
        s.type = item.type
        s.value = item.value
        s.enabled = item.enabled
        s.url = item.url
        s.tags = item.tags
        s.fromEnv = item.fromEnv
        return s
