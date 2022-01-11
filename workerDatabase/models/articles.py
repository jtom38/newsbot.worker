from sqlalchemy import Column, String, Integer
from uuid import uuid4
from ..services.base import Base


class ArticlesSqlModel(Base):
    __tablename__ = "articles"
    id = Column(String, primary_key=True)
    sourceId: str = Column(String)
    tags = Column(String)
    title = Column(String)
    url = Column(String)
    pubDate = Column(String)
    video = Column(String)
    videoHeight = Column(Integer)
    videoWidth = Column(Integer)
    thumbnail = Column(String)
    description = Column(String)
    authorName = Column(String)
    authorImage = Column(String)

    def __init__(
        self,
        sourceId: str = '',
        tags: str = "",
        title: str = "",
        url: str = "",
        pubDate: str = "",
        video: str = "",
        videoHeight: int = 0,
        videoWidth: int = 0,
        thumbnail: str = "",
        description: str = "",
        authorName: str = "",
        authorImage: str = "",
    ) -> None:
        self.id = str(uuid4())
        self.sourceId = sourceId
        self.tags = tags
        self.title = title
        self.url = url
        self.pubDate = pubDate
        self.video = video
        self.videoHeight = videoHeight
        self.videoWidth = videoWidth
        self.thumbnail = thumbnail
        self.description = description
        self.authorName = authorName
        self.authorImage = authorImage
