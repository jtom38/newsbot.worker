from selenium.webdriver.firefox.webdriver import WebDriver
from workerInfra.base.driverBase import DriverBase
from workerInfra.domain import DriverInterface, LoggerInterface
from selenium.webdriver import Firefox, FirefoxOptions


class FirefoxDriverService(DriverBase, DriverInterface):
    """
    This class helps to interact with Chrome/Selenium.
    It was made to be used as a Base class for the sources who need Chrome.
    """
    _logger: LoggerInterface
    __driver__: WebDriver

    def __init__(self, logger: LoggerInterface) -> None:
        self._logger = logger

    def driverStart(self) -> Firefox:
        try:
            self._logger.debug("Driver is starting up Firefox")
            o = FirefoxOptions()
            o.headless = True
            driver = Firefox(options=o)
            self.__driver__ = driver
            return driver
        except Exception as e:
            self._logger.critical(f"Firefox driver failed to start: Error: {e}")

