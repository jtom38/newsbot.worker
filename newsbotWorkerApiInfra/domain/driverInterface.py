from abc import ABC, abstractclassmethod


class DriverInterface(ABC):
    @abstractclassmethod
    def driverStart(self) -> object:
        raise NotImplementedError()

    @abstractclassmethod
    def driverGetContent(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def driverGoTo(self) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def driverSaveScreenshot(self, path: str) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def driverGetUrl(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def driverClose(self, displayMsg: bool = True) -> None:
        raise NotImplementedError()
        