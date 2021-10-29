from newsbotWorkerApiService.logger import Logger

class DemoJobService():
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        pass

    def start(self) -> None:
        self.logger.info("Hello from DemoJobService!")