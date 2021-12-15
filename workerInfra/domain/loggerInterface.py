from abc import abstractclassmethod, ABC


class LoggerInterface(ABC):
    @abstractclassmethod
    def debug(self, message: str) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def info(self, message: str) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def warning(self, message: str) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def error(self, message: str) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def critical(self, message: str) -> None:
        raise NotImplementedError()
