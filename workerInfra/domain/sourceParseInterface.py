from abc import abstractclassmethod, ABC
from workerInfra.models import Articles


class SourceParseInterface(ABC):
    """
    This interface helps to define how to convert source data into an Article.
    """

    @abstractclassmethod
    def __newArticle__(self) -> Articles:
        raise NotImplementedError()

    @abstractclassmethod
    def start(self) -> Articles:
        raise NotImplementedError()

    @abstractclassmethod
    def getAuthorName(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def getAuthorImage(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def getDescription(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def getUrl(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def getThumbnail(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def getPublishDate(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def getTags(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def articleExists(self) -> bool:
        """
        Checks to see if the article exists in the db.
        """
        raise NotImplementedError()
