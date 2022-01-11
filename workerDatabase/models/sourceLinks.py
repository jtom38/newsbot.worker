from sqlalchemy import Column, String
from uuid import uuid4

from workerInfra.enum.sourcesEnum import SourcesEnum
from ..services.base import Base


class SourceLinksSqlModel(Base):
    __tablename__ = "sourcelinks"
    id = Column("id", String, primary_key=True)
    sourceID: str = Column("sourceID", String)
    sourceType: str = Column('sourceType', String)
    sourceName: str = Column("sourceName", String)
    discordName: str = Column("discordName", String)
    discordID: str = Column("discordID", String)

    def __init__(self, sourceName: SourcesEnum = "", sourceID: str = "", sourceType: str = '', discordName: str = '', discordID: str = ""):
        self.id = str(uuid4())
        self.sourceID = sourceID
        self.sourceType = sourceType
        self.sourceName = sourceName
        # self.sourceData = Source
        self.discordID = discordID
        self.discordName = discordName

    def convertFromData(self, item: object) -> object:
        s = SourceLinks()
        s.sourceID = item.sourceID
        s.sourceType = item.sourceType
        s.sourceName = item.sourceName
        s.discordID = item.discordID
        s.discordName = item.discordName
        return s
