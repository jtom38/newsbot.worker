from abc import abstractclassmethod, ABC


class CacheInterface(ABC):
    @abstractclassmethod
    def find(self, key: str) -> str:
        raise NotImplementedError

    @abstractclassmethod
    def findBool(self, key: str) -> bool:
        raise NotImplementedError

    @abstractclassmethod
    def add(self, key: str, value: str) -> str:
        raise NotImplementedError

    @abstractclassmethod
    def remove(self, key: str) -> None:
        raise NotImplementedError