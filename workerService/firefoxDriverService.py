from workerInfra.base.driverBase import DriverBase
from workerInfra.domain import DriverInterface, LoggerInterface
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class FirefoxDriverService(DriverBase, DriverInterface):
    """
    This class helps to interact with Chrome/Selenium.
    It was made to be used as a Base class for the sources who need Chrome.
    """
    _logger: LoggerInterface

    def __init__(self, logger: LoggerInterface) -> None:
        self._logger = logger

    def driverStart(self, displayMsg: bool = True) -> Firefox:
        try:
            self._logger.debug("Driver is starting up Firefox")
            o = FirefoxOptions()
            o.headless = True
            driver = Firefox(options=o)
            self.__driver__ = driver
            return driver
        except Exception as e:
            self._logger.critical(f"Firefox driver failed to start: Error: {e}")

