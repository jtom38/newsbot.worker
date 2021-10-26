from typing import List
from abc import ABC, abstractclassmethod
from newsbotWorker.infra.enum import SourcesEnum

class OutputFormatterInterface(ABC):
    @abstractclassmethod
    def replaceImages(self, msg: str, replaceWith:str) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def findAllImages(self, text: str) -> List[str]:
        raise NotImplementedError()

    @abstractclassmethod
    def convertFromHtml(self, msg: str) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def replaceLinks(self, msg: str) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def getAuthorIcon(self, icon: str, name: str, type: SourcesEnum, source:str) -> str:
        """
        Query the Icons table to find the correct icon
        """
