from abc import ABC, abstractclassmethod


class DriverInterface(ABC):
    @abstractclassmethod
    def start(self) -> object:
        raise NotImplementedError()

    @abstractclassmethod
    def getContent(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def goTo(self) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def saveScreenshot(self, path: str) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def getUrl(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def close(self, displayMsg: bool = True) -> None:
        raise NotImplementedError()
