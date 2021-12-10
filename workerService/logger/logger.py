import logging
from string import Formatter

from workerInfra.domain.loggerInterface import LoggerInterface
#from workerInfra.enum.envEnum import EnvEnum
from workerService.envReaderService import EnvReaderService

def getFileHandler(level: int, formatter: Formatter) -> logging.Handler:
    f = logging.FileHandler('invmon.log')
    f.setLevel(level)
    f.setFormatter(logging.Formatter(formatter))
    return f


def getConsoleHandler(level: int, formatter: Formatter) -> logging.Handler:
    c = logging.StreamHandler()
    c.setLevel(level)
    c.setFormatter(logging.Formatter(formatter))
    return c


def getLogger() -> logging.Logger:
    messageFormat = '%(levelname)s: %(message)s'
    log = logging.getLogger(__name__)
    log.addHandler(getFileHandler(logging.ERROR, messageFormat))
    log.addHandler(getConsoleHandler(logging.DEBUG, messageFormat))
    return log


class BasicLoggerService(LoggerInterface):
    _env: EnvReaderService

    def __init__(self) -> None:
        # Not used yet
        self._env = EnvReaderService()

    def debug(self, message: str) -> None:
        print(f"DEBUG:    {message}")

    def info(self, message: str) -> None:
        print(f"INFO:     {message}")

    def warning(self, message: str) -> None:
        print(f"WARNING   {message}")

    def error(self, message: str) -> None:
        print(f"ERROR:    {message}")

    def critical(self, message: str) -> None:
        print(f"CRITICAL: {message}")


