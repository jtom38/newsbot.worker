from abc import ABC, abstractclassmethod
from workerInfra.domain.loggerInterface import LoggerInterface


class OutputInterface(ABC):
    _logger: LoggerInterface

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
