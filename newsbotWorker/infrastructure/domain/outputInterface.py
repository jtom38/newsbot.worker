from abc import ABC, abstractclassmethod


class OutputInterface(ABC):
    @abstractclassmethod
    def init(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def buildMessage(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def sendMessage(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def isSafeToRemove(self) -> bool:
        raise NotImplementedError

