from workerInfra.domain import DriverInterface
from workerInfra.base import DriverBase
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.webdriver import FirefoxWebElement

class FirefoxDriverService(DriverBase, DriverInterface):
    """
    This class helps to interact with Chrome/Selenium.
    It was made to be used as a Base class for the sources who need Chrome.
    """

    def driverStart(self, displayMsg: bool = True) -> Firefox:
        try:
            self.logger.debug("Driver is starting up Firefox")
            o = FirefoxOptions()
            o.headless = True
            driver = Firefox(options=o)
            self.__driver__ = driver
            return driver
        except Exception as e:
            self.logger.critical(f"Firefox driver failed to start: Error: {e}")

    def driverFindByXPath(self, xpath: str) -> FirefoxWebElement:
        try:
            ele = self.driver.find_element_by_xpath(xpath)
            return ele
        except Exception as e:
            self.logger.error(f"Firefox failed to select the item via xpath.  Something changed on the page. Error: {e}")
