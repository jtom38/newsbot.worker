from typing import List
from workerInfra.domain import CacheInterface
from workerInfra.models import Settings
from workerService.db import SettingsTable


class CacheFactory():
    __item__: CacheInterface

    def __init__(self, item: CacheInterface) -> None:
        self.__item__ = item

    def find(self, key: str) -> str:
        res = self.__item__.find(key)
        return res

    def findBool(self, key: str) -> bool:
        res = self.__item__.findBool(key)
        return res

    def add(self, key: str, value: str) -> str:
        self.__item__.add(key, value)
        return value

    def remove(self, key: str) -> None:
        self.__item__.remove(key)


class Cache():
    def __init__(self) -> None:
        self.sql: CacheInterface = SqlCache()

    def find(self, key: str) -> str:
        return self.sql.find(key)

    def findBool(self, key: str) -> bool:
        return self.sql.findBool(key)

    def add(self, key: str, value: str) -> str:
        self.sql.add(key, value)
        return value

    def remove(self, key: str) -> None:
        self.sql.remove(key)


class CacheValidation():
    """
    CacheValidation is here to validate the values that come back as strings, to other types.
    """

    def validateBool(self, value: str):
        v = value.lower()
        if v == "true":
            return True
        if v == "false":
            return False


class SqlCache(CacheInterface):
    """
    This is an implementation of basic cashing with sql.
    Do not use this class directly.
    Always use Cache class and it will find the data as needed.
    """

    def __init__(self):
        pass

    def find(self, key: str) -> str:
        res = SettingsTable().getByKey(key=key)
        return res.value

    def findBool(self, key: str) -> bool:
        res = SettingsTable().getByKey(key=key)
        r = CacheValidation().validateBool(res.value)
        return r

    def add(self, key: str, value: str) -> str:
        SettingsTable().update(Settings(key=key, value=value))
        return value

    def remove(self, key: str) -> None:
        SettingsTable().remove(key=key)
