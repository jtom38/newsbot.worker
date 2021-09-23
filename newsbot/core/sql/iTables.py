from abc import ABC, abstractclassmethod


class ITables():
    """
    This interface defines common access to the API.
    """

    baseUrl: str = ''
    uri: str = ""

    @abstractclassmethod
    def getAll(self) -> list[object]:
        raise NotImplementedError

    @abstractclassmethod
    def getById(self, id: str) -> object:
        raise NotImplementedError

    @abstractclassmethod
    def add(self, item: object) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def find(self, item: object) -> object:
        raise NotImplementedError()

    @abstractclassmethod
    def update(self, item: object) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def deleteById(self, id: str) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def __toApi__(self, item: object) -> dict:
        raise NotImplementedError()

    @abstractclassmethod
    def __fromApi__(self, item: dict) -> object:
        raise NotImplementedError

    @abstractclassmethod
    def __generateBlank__(self) -> object:
        raise NotImplementedError()
