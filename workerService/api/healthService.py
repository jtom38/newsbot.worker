from workerInfra.enum.healthEnum import HealthStatusEnum
from workerInfra.models import HealthModel


class HealthService():
    """
    This class runs some checks to determin if dependancy services are alive.
    """
    def __init__(self) -> None:
        self.__health__ = HealthModel(
            status=HealthStatusEnum.UNHEALTHY.value
            ,outputs=list()
            ,sources=list()
        )
        pass

    def append(self, HealthCheckObject) -> None:
        pass

    def check(self) -> HealthModel:
        return self.__health__

    def getResults(self) -> HealthModel:
        return self.__health__

    def getDbStatus(self) -> None:
        pass