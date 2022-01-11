from sqlalchemy import Column, String
from uuid import uuid4
from ..services.base import Base


class DiscordQueueSqlModel(Base):
    __tablename__ = "discordQueue"
    id = Column(String, primary_key=True)
    articleId: str = Column(String)

    def __init__(self) -> None:
        self.id = str(uuid4())

    def convertFromData(self, data: object) -> None:
        res = DiscordQueue()
        res.articleId = data.articleId
        return res
