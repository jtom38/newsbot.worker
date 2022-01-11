from sqlalchemy import Column, String, Boolean
from uuid import uuid4
from ..services.base import Base


class DiscordWebHooksSqlModel(Base):
    __tablename__ = "discordwebhooks"
    id = Column(String, primary_key=True)
    name = Column(String)
    key = Column(String)
    url = Column(String)
    server = Column(String)
    channel = Column(String)
    enabled = Column(Boolean)
    fromEnv = Column(Boolean)

    def __init__(
        self,
        name: str = "",
        key: str = "",
        server: str = "",
        channel: str = "",
        url: str = "",
        fromEnv: bool = False
    ) -> None:
        self.name = name
        self.id = str(uuid4())
        self.server = server
        self.channel = channel
        if name == "":
            self.name = self.__generateName__()
        else:
            self.name = name
        self.key = key
        self.url = url
        self.enabled = True
        self.fromEnv: bool = fromEnv

    def convertFromData(self, data: object) -> None:
        res = DiscordWebHooks()
        if data.id != '':
            res.id = data.id
        res.name = data.name
        res.key = data.key
        res.url = data.url
        res.server = data.server
        res.channel = data.channel
        res.enabled = data.enabled
        res.fromEnv = data.fromEnv
        return res

    def __generateName__(self) -> str:
        return f"{self.server} - {self.channel}"
