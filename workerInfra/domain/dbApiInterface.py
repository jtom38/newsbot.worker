from abc import ABC, abstractclassmethod
from typing import List


class DbApiTableInterface(ABC):
    @abstractclassmethod
    def __generateBlank__(self) -> object:
        raise NotImplementedError()

    @abstractclassmethod
    def __toApi__(self, item:object) -> dict:
        raise NotImplementedError()

    @abstractclassmethod
    def __fromApi__(self, item: dict) -> object:
        raise NotImplementedError()

    @abstractclassmethod
    def __singleFromApi__(self, raw: str) -> object:
        raise NotImplementedError()

    @abstractclassmethod
    def __listFromApi__(self, raw: str) -> List[object]:
        raise NotImplementedError()
